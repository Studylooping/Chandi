"""Build a metre-annotated study guide (out/guide.html) from data/prosody.json.

Each metrical pada is shown syllable by syllable with its weight: laghu (◡, 1 mAtrA) or
guru (—, 2 mAtrAs); the pada-final syllable is marked as held guru. Prose lines are plain.
"""
import html
import json
import pathlib

from chandi.prosody import norm, syllables

ROOT = pathlib.Path(__file__).resolve().parent.parent
TITLES = {'pre': 'Chaṇḍikā-dhyāna', 'kavacha': 'Devī-kavaca', 'argala': 'Argalā-stotra',
          'kilaka': 'Kīlaka', 'aparadha': 'Aparādha-kṣamāpaṇa', 'devisukta': 'Devī-sūkta (Ṛgveda)'}
ORDER = ['pre', 'kavacha', 'argala', 'kilaka'] + [f'ch{i}' for i in range(1, 14)] + ['aparadha', 'devisukta']


def chunks(text):
    """Orthographic syllable chunks of a pada, aligned with syllables()."""
    t = norm(text)
    sy = syllables(t)
    bounds = [s['start'] for s in sy] + [len(t)]
    return [t[a:b] for a, b in zip(bounds, bounds[1:])]


def pada_html(text, weights, yati=()):
    cells = []
    ch = chunks(text)
    for k, (c, w) in enumerate(zip(ch, weights)):
        final = k == len(ch) - 1
        mark = '—' if w == 'G' else '◡'
        cls = 'g' if w == 'G' else 'l'
        if final and w == 'L':
            mark, cls = '◡→—', 'f'
        cells.append(f'<span class="s {cls}"><b>{html.escape(c.strip())}</b><i>{mark}</i></span>')
        if k + 1 in yati and not final:
            cells.append('<span class="yati" title="yati">|</span>')
    return '<div class="pada">' + ''.join(cells) + f'<span class="pat">{weights}</span></div>'


def unit_html(u):
    label = u['id'] or u['kind']
    meta = html.escape(u.get('metre') or '')
    note = ''
    if u.get('issues'):
        note = f'<div class="note">⚠ {html.escape("; ".join(u["issues"]))}' + (
            f' — {html.escape(u["review"])}' if u.get('review') else '') + '</div>'
    if u.get('padas'):
        body = ''.join(pada_html(p, w, u.get('yati') or ()) for p, w, _ in u['padas'])
        labels = ', '.join(dict.fromkeys(lab for _, _, lab in u['padas'] if lab and lab != u.get('metre')))
        if labels:
            meta += f' · {html.escape(labels)}'
        if u.get('yati'):
            meta += f' · yati after {", ".join(map(str, u["yati"]))}'
    else:
        body = ''.join(f'<div class="prose">{html.escape(x)}</div>' for x in u['lines'])
    extra = ''.join(f'<span class="bija">{html.escape(x)}</span>' for x in (u.get('bija_head'), u.get('extra')) if x)
    return (f'<section class="u {u["kind"]}"><header><span class="id">{html.escape(label)}</span>'
            f'<span class="m">{meta}</span>{extra}</header>{body}{note}</section>')


CSS = '''
:root{--bg:#fbf8f2;--fg:#2a2118;--mut:#7a6a58;--l:#2f6f8f;--g:#a2462a;--line:#e6dccb;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--fg:#efe6d8;--mut:#a8977f;--l:#7cc0e0;--g:#f08a65;--line:#3a3128;--card:#231e18}}
body{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;margin:0 auto;max-width:960px;padding:16px}
h1{font-size:1.5rem}h2{margin-top:2.5rem;border-bottom:1px solid var(--line)}
nav a{margin-right:.6em;color:var(--g)}
.u{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.6em .8em;margin:.6em 0}
.u header{font-size:.8rem;color:var(--mut);display:flex;gap:.8em;flex-wrap:wrap}
.id{font-weight:700;color:var(--fg)}.bija{font-style:italic}
.pada{display:flex;flex-wrap:wrap;align-items:flex-end;gap:2px;margin:.35em 0}
.s{display:inline-flex;flex-direction:column;align-items:center;min-width:1.6em}
.s b{font:500 1.35rem/1.3 "Noto Serif Devanagari","Sanskrit Text",serif}
.s i{font-style:normal;font-size:.8rem}.l i{color:var(--l)}.g i,.f i{color:var(--g)}
.pat{margin-left:auto;font:12px ui-monospace,monospace;color:var(--mut);align-self:center}
.prose{font:1.15rem "Noto Serif Devanagari",serif;color:var(--mut)}
.note{font-size:.8rem;color:var(--g);margin-top:.3em}
.yati{color:var(--mut);align-self:center;padding:0 .2em}
'''


def build():
    corpus = json.loads((ROOT / 'data' / 'prosody.json').read_text(encoding='utf-8'))
    secs = {}
    for u in corpus:
        secs.setdefault(u['section'], []).append(u)
    order = [s for s in ORDER if s in secs]
    title = lambda s: TITLES.get(s) or f'Adhyāya {s[2:]}'
    nav = ''.join(f'<a href="#{s}">{title(s)}</a>' for s in order)
    body = ''.join(f'<h2 id="{s}">{title(s)}</h2>' + ''.join(unit_html(u) for u in secs[s]) for s in order)
    page = (f'<!doctype html><html lang="sa"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>Saptaśatī Chandas Guide</title>'
            f'<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari:wght@500&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><h1>Durgā Saptaśatī — chandas study guide</h1>'
            f'<p>◡ laghu = 1 mātrā · — guru = 2 mātrās · ◡→— pada-final syllable held as guru. '
            f'Text: sanskritdocuments.org durga700 (Gita Press arrangement), for personal study.</p>'
            f'<nav>{nav}</nav>{body}</body></html>')
    out = ROOT / 'out' / 'guide.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding='utf-8')
    return out


if __name__ == '__main__':
    print(build())
