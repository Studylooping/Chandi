"""Run metre identification over the corpus; write data/prosody.json and print a summary."""
import collections
import json
import pathlib

from chandi.prosody import identify

ROOT = pathlib.Path(__file__).resolve().parent.parent
METRICAL = {'shloka', 'half', 'tripada', 'gayatri', 'verse', 'dhyana', 'refrain'}


# Irregular verses reviewed by hand. "GP" = the reading is identical in the Gita Press scan,
# so the irregularity belongs to the text and is recited as written (syllable by syllable).
REVIEWED = {
    ('ch1', '1.92'): 'hypermetric pada (9 syllables); same in GP',
    ('ch2', '2.2'): 'hypermetric pada (9 syllables); same in GP',
    ('ch5', '5.12'): 'even pada 5-7 LGG (sArAyai sarvakAriNyai); same in GP',
    ('ch5', '5.99'): 'syllables 2-3 laghu (vahnirapi); same in GP',
    ('ch8', '8.4'): 'odd pada 5-7 LLG (kambUnAM chaturashItiH); not found in GP OCR, needs manual check',
    ('argala', '26'): 'sanskritdocuments recension differs from GP here (GP: tAriNIM durgasaMsArasAgarasya kulodbhavAm)',
    ('argala', '27'): 'syllables 2-3 laghu (saptashatIM); not in GP argalA recension',
    ('kavacha', '8'): 'syllables 2-3 laghu (rakShasi); not cross-checked',
    ('pre', None): 'optional "athavA" dhyAna, line 1 has 21 syllables; not cross-checked',
}


def analyze(corpus):
    for u in corpus:
        if u['kind'] in METRICAL and u['section'] != 'devisukta':
            r = identify(u['lines'])
            u['metre'], u['padas'], u['issues'], u['yati'] = r['metre'], r['padas'], r['issues'], list(r['yati'])
            u['extra'] = r['extra']
            u['review'] = REVIEWED.get((u['section'], u['id'])) if u['issues'] else None
        elif u['section'] == 'devisukta':
            u['metre'], u['padas'], u['issues'], u['yati'] = 'vaidika (svara not in source)', [], [], []
        else:
            u['metre'], u['padas'], u['issues'], u['yati'] = 'gadya (prose)', [], [], []
    return corpus


def summary(corpus):
    runs = collections.defaultdict(list)  # section -> [(metre, first id, last id, n)]
    for u in corpus:
        lab = u['id'] or u['kind']
        r = runs[u['section']]
        if r and r[-1][0] == u['metre']:
            r[-1][2] = lab; r[-1][3] += 1
        else:
            r.append([u['metre'], lab, lab, 1])
    return runs


if __name__ == '__main__':
    corpus = analyze(json.loads((ROOT / 'data' / 'corpus.json').read_text(encoding='utf-8')))
    (ROOT / 'data' / 'prosody.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1), encoding='utf-8')
    for sec, r in summary(corpus).items():
        print(sec + ': ' + '; '.join(f'{m} [{a}..{b}]x{n}' if n > 1 else f'{m} [{a}]' for m, a, b, n in r))
    flagged = [u for u in corpus if u['issues']]
    print(f'\n{len(flagged)} units with issues:')
    for u in flagged:
        print(f"  {u['section']} {u['id'] or u['kind']}: {u['metre']} :: {'; '.join(u['issues'])}"
              f"  [{u.get('review') or 'UNREVIEWED'}]")
