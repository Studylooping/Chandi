"""Render metre-faithful recitation: TTS -> syllable alignment -> time-map stretch -> verify.

Every metrical pada is rendered so that each syllable lasts exactly its mAtrA count times the
unit u (laghu 1, guru 2; the pada-final syllable is held as guru, pAdAnta-guru). The result is
re-aligned and checked; a pada that fails the check is re-synthesised with another seed, and
reported if it still fails.
"""
import dataclasses

import numpy as np
import pylibrb
import torch

from chandi.audio.align import align, check_rhythm, iois
from chandi.prosody import norm, syllables

# Pauses in mAtrA units
PAUSE = {'yati': 1, 'pada': 2, 'half': 3, 'verse': 5}


def matras_for(weights, pada_final=True):
    m = [1 if w == 'L' else 2 for w in weights]
    if pada_final:
        m[-1] = 2  # pAdAnta: the last syllable of a pada is held as guru
    return m


class MMSEngine:
    """facebook/mms-tts-hin (VITS). Stand-in voice for testing the timing pipeline only:
    it is a Hindi model and may drop word-final inherent 'a' (Hindi schwa deletion)."""
    name = 'mms-hin'

    def __init__(self):
        from transformers import AutoTokenizer, VitsModel
        self.tok = AutoTokenizer.from_pretrained('facebook/mms-tts-hin')
        self.model = VitsModel.from_pretrained('facebook/mms-tts-hin').eval()
        self.sr = self.model.config.sampling_rate

    def synth(self, text, seed=0):
        torch.manual_seed(seed)
        with torch.inference_mode():
            out = self.model(**self.tok(text, return_tensors='pt')).waveform[0]
        return out.numpy().astype(np.float32)


class ParlerEngine:
    """ai4bharat/indic-parler-tts, speaker "Aryan" (recommended male Sanskrit voice).
    Gated on Hugging Face: needs HF_TOKEN with the model's terms accepted."""
    name = 'parler-aryan'
    DESC = ('Aryan speaks in a slow, deep, calm and measured voice, with very clear audio, '
            'no background noise and a close-sounding recording.')

    def __init__(self):
        from parler_tts import ParlerTTSForConditionalGeneration
        from transformers import AutoTokenizer
        mid = 'ai4bharat/indic-parler-tts'
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(mid).eval()
        self.tok = AutoTokenizer.from_pretrained(mid)
        self.dtok = AutoTokenizer.from_pretrained(self.model.config.text_encoder._name_or_path)
        self.sr = self.model.config.sampling_rate

    def synth(self, text, seed=0):
        torch.manual_seed(seed)
        d = self.dtok(self.DESC, return_tensors='pt')
        p = self.tok(text, return_tensors='pt')
        with torch.inference_mode():
            a = self.model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                                    prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
        return a[0].numpy().astype(np.float32)


def _rb(wave, sr, ratio):
    """Constant-ratio Rubber Band stretch (offline, R3 engine, formants preserved)."""
    opts = (pylibrb.Option.PROCESS_OFFLINE | pylibrb.Option.ENGINE_FINER
            | pylibrb.Option.FORMANT_PRESERVED)
    rb = pylibrb.RubberBandStretcher(sample_rate=sr, channels=1, options=opts, initial_time_ratio=ratio)
    audio = np.ascontiguousarray(wave[np.newaxis, :], dtype=np.float32)
    rb.set_expected_input_duration(audio.shape[1])
    rb.study(audio, final=True)
    rb.process(audio, final=True)
    return rb.retrieve(rb.available())[0]


def stretch(wave, sr, anchors_in, anchors_out, ctx=0.06, fade=0.008):
    """Piecewise time map: input times anchors_in[k] land at output times anchors_out[k].

    Each segment is stretched at its own constant ratio together with `ctx` seconds of context
    on both sides (so the stretcher has no edge artefacts), then cut to its exact output span
    and joined to its neighbours with short equal-power crossfades. Audio before the first and
    after the last anchor is copied unchanged.
    """
    n_out = int(round((anchors_out[-1] + (len(wave) / sr - anchors_in[-1])) * sr))
    out = np.zeros(n_out + int(fade * sr) * 2, dtype=np.float32)
    weight = np.zeros_like(out)
    f = int(fade * sr)

    def add(seg, at):
        """Overlap-add seg at output sample `at`, with half-sine fades of f samples at its edges."""
        env = np.ones(len(seg), dtype=np.float32)
        if f and len(seg) > 2 * f:
            ramp = np.sin(np.linspace(0, np.pi / 2, f, dtype=np.float32)) ** 2
            env[:f], env[-f:] = ramp, ramp[::-1]
        lo, hi = max(at, 0), min(at + len(seg), len(out))
        out[lo:hi] += (seg * env)[lo - at:hi - at]
        weight[lo:hi] += env[lo - at:hi - at]

    a0 = int(anchors_in[0] * sr)
    add(wave[: a0 + f // 2], 0 - 0)  # lead-in, unchanged
    for k in range(len(anchors_in) - 1):
        ti0, ti1, to0, to1 = anchors_in[k], anchors_in[k + 1], anchors_out[k], anchors_out[k + 1]
        ratio = (to1 - to0) / max(ti1 - ti0, 1e-3)
        c0, c1 = max(ti0 - ctx, 0), min(ti1 + ctx, len(wave) / sr)
        y = _rb(wave[int(c0 * sr): int(c1 * sr)], sr, ratio)
        s0 = int(round((ti0 - c0) * ratio * sr)) - f // 2
        s1 = int(round((ti1 - c0) * ratio * sr)) + f // 2
        seg = y[max(s0, 0): s1]
        add(seg, int(round(to0 * sr)) - f // 2)
    tail = wave[int(anchors_in[-1] * sr) - f // 2:]
    add(tail, int(round(anchors_out[-1] * sr)) - f // 2)
    weight[weight == 0] = 1
    return (out / weight)[:n_out]


@dataclasses.dataclass
class PhraseResult:
    text: str
    weights: str
    audio: np.ndarray
    ok: bool
    u: float
    recovered: str
    errors: list
    seed: int


def render_phrase(engine, text, weights, u, pada_final=True, seeds=(0, 1, 2), tol=0.2, refine=2):
    """Render one phrase (pada or yati-segment) to exact mAtrA timing; verify by re-alignment."""
    sr = engine.sr
    matras = matras_for(weights, pada_final)
    best = None
    for seed in seeds:
        raw = engine.synth(text, seed)
        onsets, start, end, _ = align(torch.from_numpy(raw), sr, text)
        if len(onsets) != len(matras):
            raise ValueError(f'{text}: {len(onsets)} aligned syllables vs {len(matras)} in metre')
        # keyframes: vowel onset i -> lead + sum(matras[:i]) * u ; speech end -> lead + total
        # anchors: vowel onset i -> lead + sum(matras[:i]) * u ; speech end -> lead + total
        a_in, a_out, t = [], [], onsets[0]
        for o, m in zip(onsets, matras):
            a_in.append(o); a_out.append(t)
            t += m * u
        a_in.append(end); a_out.append(t)
        out = stretch(raw, sr, a_in, a_out)
        for _ in range(refine + 1):
            o2, _, e2, _ = align(torch.from_numpy(out), sr, text)
            ok, u_fit, rec, errs = check_rhythm(iois(o2, e2), matras, tol)
            if ok:
                break
            # correction pass: move the measured onsets onto the targets again
            out = stretch(out, sr, o2 + [e2], [a + (o2[0] - a_out[0]) for a in a_out])
        res = PhraseResult(text, weights, out[: int(e2 * sr) + int(0.05 * sr)], ok, u_fit, rec, errs, seed)
        if ok:
            return res
        if best is None or max(map(abs, errs)) < max(map(abs, best.errors)):
            best = res
    return best


def split_yati(pada, weights, yati):
    """Split a vRtta pada at its yati positions -> [(text, weights)].

    A yati that falls inside a word (yati-bhaGga, common in compounds) is not split: the
    reciter does not pause mid-word, so that segment stays joined."""
    text = norm(pada)
    sy = syllables(text)
    cuts = [0] + [y for y in yati if y < len(sy) and text[sy[y]['start'] - 1] == ' '] + [len(sy)]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        lo = sy[a]['start'] if a else 0
        hi = sy[b]['start'] if b < len(sy) else len(text)
        out.append((text[lo:hi].strip(), weights[a:b]))
    return out


def silence(sr, matras, u):
    return np.zeros(int(sr * matras * u), dtype=np.float32)
