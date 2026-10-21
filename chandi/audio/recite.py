"""Recite units of the corpus to a WAV file with a per-pada chandas compliance report.

  python -m chandi.audio.recite --engine parler --section ch1 [--ids 1.1-1.10] [--u 0.2]

Metrical units: every pada is rendered by render_phrase (exact mAtrA timing, verified).
vRtta padas with a yati are split there with a 1-mAtrA pause. Pauses: pada end 2 mAtrAs,
half-verse end 3, verse end 5. Prose units (uvAca, viniyoga, invocations, bIja prefixes,
an extra-metrical OM) have no metre: they are read naturally, scaled to the same tempo.
"""
import argparse
import json
import pathlib

import numpy as np
import soundfile as sf

from chandi.audio.align import active_region
from chandi.audio.render import PAUSE, render_phrase, silence, split_yati, _rb
from chandi.prosody import syllables

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIJA = {'OM': 'ॐ', 'OM aiM': 'ॐ ऐं', 'OM hrIM': 'ॐ ह्रीं', 'OM klIM': 'ॐ क्लीं', 'klIM OM': 'क्लीं ॐ'}
METRICAL = {'shloka', 'half', 'tripada', 'verse', 'dhyana', 'refrain'}


def prose(engine, text, u):
    """Natural reading of an unmetred line, scaled so the mean syllable lasts 1.5 u."""
    raw = engine.synth(text, 0)
    a, b = active_region(raw, engine.sr)
    raw = raw[int(a * engine.sr): int(b * engine.sr) + int(0.05 * engine.sr)]
    n = max(len(syllables(text)), 1)
    ratio = (1.5 * u * n) / max(b - a, 1e-3)
    return _rb(raw, engine.sr, ratio)


def recite_unit(engine, unit, u):
    sr, parts, report = engine.sr, [], []
    clean = lambda t: t.replace('॥', '').replace('।', '').replace('|', '').strip()
    if unit.get('bija_head'):
        parts += [prose(engine, BIJA.get(unit['bija_head'], unit['bija_head']), u), silence(sr, 2, u)]
    if unit['kind'] not in METRICAL or not unit.get('padas'):
        for ln in unit['lines']:
            if clean(ln):
                parts += [prose(engine, clean(ln), u), silence(sr, PAUSE['half'], u)]
        parts[-1] = silence(sr, PAUSE['verse'], u)
        return np.concatenate(parts), report
    if unit.get('extra'):
        parts += [prose(engine, unit['extra'], u), silence(sr, 2, u)]
    padas = unit['padas']
    for i, (text, weights, label) in enumerate(padas):
        segs = split_yati(text, weights, unit.get('yati') or ())
        for j, (seg, w) in enumerate(segs):
            last_seg = j == len(segs) - 1
            r = render_phrase(engine, seg, w, u, pada_final=last_seg)
            parts.append(r.audio)
            report.append({'id': unit['id'], 'pada': i + 1, 'text': seg, 'pattern': w,
                           'measured': r.recovered, 'ok': bool(r.ok), 'u': round(r.u, 4),
                           'max_err': round(max(map(abs, r.errors)), 3), 'seed': r.seed})
            if not last_seg:
                parts.append(silence(sr, PAUSE['yati'], u))
        if i == len(padas) - 1:
            parts.append(silence(sr, PAUSE['verse'], u))
        else:
            parts.append(silence(sr, PAUSE['half'] if i % 2 else PAUSE['pada'], u))
    if unit.get('bija_tail'):
        parts += [prose(engine, BIJA.get(unit['bija_tail'], unit['bija_tail']), u), silence(sr, PAUSE['verse'], u)]
    return np.concatenate(parts), report


def select(corpus, section, ids):
    units = [x for x in corpus if x['section'] == section]
    if ids:
        lo, _, hi = ids.partition('-')
        idx = [k for k, x in enumerate(units) if x['id'] in (lo, hi or lo)]
        units = units[idx[0]: idx[-1] + 1]
    return units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', choices=['parler', 'mms'], default='parler')
    ap.add_argument('--section', required=True)
    ap.add_argument('--ids', default='')
    ap.add_argument('--u', type=float, default=0.2, help='seconds per mAtrA')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    from chandi.audio.render import MMSEngine, ParlerEngine
    engine = ParlerEngine() if a.engine == 'parler' else MMSEngine()
    corpus = json.loads((ROOT / 'data' / 'prosody.json').read_text(encoding='utf-8'))
    units = select(corpus, a.section, a.ids)
    out = pathlib.Path(a.out or ROOT / 'out' / f'{a.section}{"_" + a.ids if a.ids else ""}_{engine.name}.wav')
    out.parent.mkdir(parents=True, exist_ok=True)
    cache = ROOT / 'out' / 'units' / f'{engine.name}_u{a.u}' / a.section
    cache.mkdir(parents=True, exist_ok=True)
    audio, report, failed = [], [], []
    section_units = [x for x in corpus if x['section'] == a.section]
    for unit in units:
        # per-unit cache (keyed by position in the full section) so an interrupted run resumes
        k = next(i for i, x in enumerate(section_units) if x is unit)
        stem = cache / f"{k:04d}_{(unit['id'] or unit['kind']).replace('.', '-')}"
        if stem.with_suffix('.wav').exists() and stem.with_suffix('.json').exists():
            w, _ = sf.read(stem.with_suffix('.wav'), dtype='float32')
            r = json.loads(stem.with_suffix('.json').read_text(encoding='utf-8'))
        else:
            try:
                w, r = recite_unit(engine, unit, a.u)
            except Exception as e:  # noqa: BLE001 - keep going; the unit is retried on the next run
                failed.append(f"{unit['id'] or unit['kind']}: {e}")
                print(f"FAILED {unit['section']} {unit['id'] or unit['kind']}: {e}", flush=True)
                continue
            sf.write(stem.with_suffix('.wav'), w, engine.sr)
            stem.with_suffix('.json').write_text(json.dumps(r, ensure_ascii=False), encoding='utf-8')
        audio.append(w); report += r
        bad = [x for x in r if not x['ok']]
        print(f"{unit['section']} {unit['id'] or unit['kind']}: {len(r) - len(bad)}/{len(r)} padas compliant", flush=True)
    if failed:  # an incomplete section is not written, so it is not published
        print(f'{a.section}: {len(failed)} unit(s) failed, section not written; rerun to retry them')
        raise SystemExit(1)
    sf.write(out, np.concatenate(audio), engine.sr)
    out.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    n_ok = sum(x['ok'] for x in report)
    print(f'{out}: {n_ok}/{len(report)} metrical phrases verified compliant')


if __name__ == '__main__':
    main()
