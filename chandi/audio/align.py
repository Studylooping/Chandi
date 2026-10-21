"""Syllable-level forced alignment (torchaudio MMS_FA) and rhythm measurement.

Timing model: a syllable's duration is the interval from its vowel onset to the next
syllable's vowel onset (inter-onset interval, IOI); the last syllable of a pada runs from its
vowel onset to the end of speech. This is the interval a listener hears as the beat.
"""
import numpy as np
import torch
import torchaudio

from chandi.prosody import syllables

CONS = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'n', 'च': 'c', 'छ': 'ch', 'ज': 'j',
        'झ': 'jh', 'ञ': 'n', 'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n', 'त': 't',
        'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n', 'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh',
        'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's',
        'ह': 'h', 'ळ': 'l'}
VOW = {'a': 'a', 'A': 'aa', 'i': 'i', 'I': 'ii', 'u': 'u', 'U': 'uu', 'f': 'ri', 'F': 'rii',
       'x': 'li', 'e': 'e', 'E': 'ai', 'o': 'o', 'O': 'au'}
CODA = {'ं': 'm', 'ः': 'h', 'ँ': 'n'}

_bundle = torchaudio.pipelines.MMS_FA
_model = None


def romanize(text):
    """Per-syllable romanised tokens for MMS_FA: [(consonant chars, vowel chars, coda chars)]."""
    out = []
    for s in syllables(text):
        onset = ''.join(CONS[c.rstrip('्')[0]] for c in s['onset'] if c.rstrip('्')[0] in CONS)
        out.append((onset, VOW[s['vowel']], ''.join(CODA.get(c, '') for c in s['coda'])))
    return out


def _get_model():
    global _model
    if _model is None:
        _model = _bundle.get_model(with_star=False).eval()
    return _model


def align(wave, sr, text):
    """Return per-syllable vowel onset times (s), end of speech (s), and token spans."""
    model, dic = _get_model(), _bundle.get_dict(star=None)
    if sr != _bundle.sample_rate:
        wave = torchaudio.functional.resample(wave, sr, _bundle.sample_rate)
    parts = romanize(text)
    chars, vowel_first = [], []
    for onset, vow, coda in parts:
        chars.extend(onset)
        vowel_first.append(len(chars))
        chars.extend(vow + coda)
    tokens = torch.tensor([[dic[c] for c in chars]], dtype=torch.int32)
    with torch.inference_mode():
        emission, _ = model(wave.unsqueeze(0) if wave.dim() == 1 else wave)
        ali, scores = torchaudio.functional.forced_align(emission, tokens, blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], scores[0].exp())
    ratio = (wave.shape[-1] / _bundle.sample_rate) / emission.shape[1]
    onsets = [spans[k].start * ratio for k in vowel_first]
    # CTC spans are "peaky" (one or two 20 ms frames), so the last token's span does not mark
    # where the final vowel dies away; take the end of speech from the energy envelope instead.
    speech_start, speech_end = active_region(wave[0] if wave.dim() > 1 else wave, _bundle.sample_rate)
    speech_end = max(speech_end, spans[-1].end * ratio)
    return onsets, speech_start, speech_end, [(chars[i], sp.start * ratio, sp.end * ratio, sp.score)
                                               for i, sp in enumerate(spans)]


def active_region(wave, sr, floor_db=-35.0, hop=0.01):
    """First/last time where 10 ms RMS energy is within floor_db of the peak."""
    w = wave.numpy() if hasattr(wave, 'numpy') else wave
    h = int(hop * sr)
    n = max(len(w) // h, 1)
    rms = (w[: n * h].reshape(n, h) ** 2).mean(axis=1) ** 0.5
    db = 20 * np.log10(rms / (rms.max() + 1e-12) + 1e-12)
    act = np.where(db > floor_db)[0]
    return act[0] * hop, (act[-1] + 1) * hop


def iois(onsets, speech_end):
    return [b - a for a, b in zip(onsets, onsets[1:] + [speech_end])]


def check_rhythm(durations, matras, tol=0.2):
    """Compare measured syllable durations to the mAtrA targets.

    The unit u is fitted (least squares) so tempo drift does not count as an error; each
    syllable must be within tol of m*u, and the recovered pattern (L if d < 1.5u else G)
    must equal the metre pattern. Returns (ok, u, recovered, errors).
    """
    num = sum(d * m for d, m in zip(durations, matras))
    den = sum(m * m for m in matras)
    u = num / den
    errors = [d / (m * u) - 1 for d, m in zip(durations, matras)]
    recovered = ''.join('L' if d < 1.5 * u else 'G' for d in durations)
    target = ''.join('L' if m == 1 else 'G' for m in matras)
    ok = recovered == target and all(abs(e) <= tol for e in errors)
    return ok, u, recovered, errors
