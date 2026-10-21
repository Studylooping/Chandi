"""Syllabification, laghu/guru weights and metre identification for Devanagari verse.

Weight rules (classical): a syllable is guru (G) if its vowel is long (A I U F e E o O), or if
the vowel is followed by anusvara/visarga, or by two or more consonants (conjunct) before the
next vowel, also across word boundaries inside a pada. Otherwise laghu (L). The last syllable
of every pada is anceps (pAdAnta guru/laghu); patterns below write it as written in the
canonical definition and matching ignores it.
"""
import re
import unicodedata

V_INDEP = {'अ': 'a', 'आ': 'A', 'इ': 'i', 'ई': 'I', 'उ': 'u', 'ऊ': 'U', 'ऋ': 'f', 'ॠ': 'F',
           'ऌ': 'x', 'ए': 'e', 'ऐ': 'E', 'ओ': 'o', 'औ': 'O'}
V_SIGN = {'ा': 'A', 'ि': 'i', 'ी': 'I', 'ु': 'u', 'ू': 'U', 'ृ': 'f', 'ॄ': 'F', 'ॢ': 'x',
          'े': 'e', 'ै': 'E', 'ो': 'o', 'ौ': 'O'}
LONG = set('AIUFeEoO')
VIRAMA, NUKTA = '्', '़'
NASAL_VISARGA = {'ं', 'ः', 'ँ', 'ᳲ', 'ᳳ'}


def is_consonant(c):
    return 'क' <= c <= 'ह' or 'क़' <= c <= 'य़' or c == 'ळ'


def syllables(text):
    """Split Devanagari text into syllables.

    Returns a list of dicts with keys: vowel (code), weight ("L"/"G"), start (index in the
    normalised text where the syllable's orthographic akshara begins), onset (consonants
    written before the vowel), coda (anusvara/visarga after it).
    Spaces do not block weight: a conjunct after a word boundary still makes the preceding
    syllable heavy, as in recitation with sandhi.
    """
    text = norm(text)
    toks = []  # (kind, value, index)  kind: C consonant, V vowel, M nasal/visarga
    i = 0
    while i < len(text):
        c = text[i]
        if c in V_INDEP:
            toks.append(('V', V_INDEP[c], i))
        elif is_consonant(c):
            j = i + 1
            if j < len(text) and text[j] == NUKTA:
                j += 1
            toks.append(('C', text[i:j], i))
            nxt = text[j] if j < len(text) else ''
            if nxt == VIRAMA:
                j += 1
            elif nxt in V_SIGN:
                toks.append(('V', V_SIGN[nxt], j)); j += 1
            else:
                toks.append(('V', 'a', j - 1))
            i = j
            continue
        elif c in NASAL_VISARGA:
            toks.append(('M', c, i))
        i += 1

    vidx = [k for k, t in enumerate(toks) if t[0] == 'V']
    out = []
    for n, k in enumerate(vidx):
        nxt = vidx[n + 1] if n + 1 < len(vidx) else len(toks)
        gap = toks[k + 1:nxt]
        cons = [t for t in gap if t[0] == 'C']
        heavy = toks[k][1] in LONG or any(t[0] == 'M' for t in gap) or len(cons) >= 2
        # onset: consonants directly preceding this vowel back to the previous M/V
        b = k
        while b > 0 and toks[b - 1][0] == 'C':
            b -= 1
        onset = [t[1] for t in toks[b:k]]
        start = toks[b][2] if b < k else toks[k][2]
        out.append({'vowel': toks[k][1], 'weight': 'G' if heavy else 'L', 'start': start,
                    'onset': onset, 'coda': [t[1] for t in gap if t[0] == 'M']})
    return out


def norm(text):
    return unicodedata.normalize('NFC', text.replace('ॐ', 'ओम्').replace('ऽ', ''))


def weights(text):
    return ''.join(s['weight'] for s in syllables(text))


# ---------------------------------------------------------------------------------- metres
VRTTA = {
    # name: (pattern per pada, yati positions after syllable n)
    'indravajrA': ('GGLGGLLGLGG', ()),
    'upendravajrA': ('LGLGGLLGLGG', ()),
    'vaMshastha': ('LGLGGLLGLGLG', ()),
    'indravaMshA': ('GGLGGLLGLGLG', ()),
    'dodhaka': ('GLLGLLGLLGG', ()),
    'vasantatilakA': ('GGLGLLLGLLGLGG', ()),  # no fixed yati in the standard definition
    'shArdUlavikrIDita': ('GGGLLGLGLLLGGGLGGLG', (12,)),
    'sragdharA': ('GGGGLGGLLLLLLGGLGGLGG', (7, 14)),
    # ardhasama: odd / even padas
    'aupachChandasika:odd': ('LLGLLGLGLGG', ()),
    'aupachChandasika:even': ('LLGGLLGLGLGG', ()),
}
FAMILIES = {
    'indravajrA': 'upajAti', 'upendravajrA': 'upajAti',
    'vaMshastha': 'upajAti (vaMshastha/indravaMshA)', 'indravaMshA': 'upajAti (vaMshastha/indravaMshA)',
}


def match(pat, w):
    """True if weights w match pattern pat, ignoring the anceps final syllable."""
    return len(pat) == len(w) and pat[:-1] == w[:-1]


def mismatches(pat, w):
    if len(pat) != len(w):
        return None
    return [i + 1 for i in range(len(w) - 1) if pat[i] != w[i]]


def anushtubh_pada(w, odd):
    """Classify an 8-syllable anuShTubh pada. Returns (ok, label)."""
    if len(w) != 8:
        return False, f'{len(w)} syllables'
    if w[1] == 'L' and w[2] == 'L':
        return False, 'syllables 2-3 both laghu'
    if not odd:
        if w[4:7] == 'LGL':
            return True, 'pathyA'
        return False, f'even pada 5-7 = {w[4:7]} (needs LGL)'
    t = w[4:7]
    if t == 'LGG':
        return True, 'pathyA'
    vipula = {'LLL': 'na-vipulA', 'GLL': 'bha-vipulA', 'GGG': 'ma-vipulA', 'GLG': 'ra-vipulA'}
    if t in vipula:
        return True, vipula[t]
    return False, f'odd pada 5-7 = {t}'


PADA_LENGTHS = {len(p) for p, _ in VRTTA.values()}


def split_padas(lines):
    """Physical lines -> padas. A line of 16-17 syllables is an anuShTubh half-verse (8+8);
    a line twice as long as a known vRtta pada holds two padas (e.g. the dodhaka dhyAna)."""
    padas = []
    for ln in lines:
        ln = re.sub(r'[।॥|]', ' ', ln).strip()
        if not ln:
            continue
        w = weights(ln)
        if any(match(p, w) for p, _ in VRTTA.values()):
            padas.append(ln)
        elif len(w) == 16:
            padas.extend(split_at_syllable(ln, 8))
        elif len(w) == 17:  # hypermetric half-verse: put the extra syllable where a word ends
            padas.extend(split_hypermetric(ln))
        elif len(w) % 2 == 0 and len(w) // 2 in PADA_LENGTHS:
            padas.extend(split_at_syllable(ln, len(w) // 2))
        else:
            padas.append(ln)
    return padas


def split_hypermetric(text):
    """17-syllable half-verse: choose a 9+8 or 8+9 split that falls on a word boundary."""
    words = norm(text).split()
    for k in range(1, len(words)):
        n = len(syllables(' '.join(words[:k])))
        if n in (8, 9):
            left, right = ' '.join(words[:k]), ' '.join(words[k:])
            if len(syllables(right)) == 17 - n:
                return [left, right]
    # no word boundary (sandhi across the pada break, e.g. 1.92 durAtmAnAvativIrya-):
    # the first pada carries the extra syllable, as in 2.2 where a boundary exists
    return split_at_syllable(text, 9)


def split_at_syllable(text, n):
    """Split text before syllable n+1, preferring a word boundary; else cut inside the word."""
    text = norm(text)
    sy = syllables(text)
    if len(sy) <= n:
        return [text]
    cut = sy[n]['start']
    return [text[:cut].strip(), text[cut:].strip()]


def _fits(lines):
    ws = [weights(p) for p in split_padas(lines)]
    return bool(ws) and (all(len(w) == 8 for w in ws)
                         or all(any(match(p, w) for p, _ in VRTTA.values()) for w in ws))


def identify(lines):
    """Identify metre of a verse given its physical lines.

    Returns dict: metre, padas [(text, weights, label)], issues [str], yati.
    """
    lines = list(lines)
    res = {'padas': [], 'issues': [], 'metre': None, 'yati': (), 'extra': None}
    if lines and norm(lines[0]).startswith('ओम् ') and not _fits(lines):
        res['extra'] = 'ॐ'  # extra-metrical invocation: recited, not counted
        lines[0] = norm(lines[0])[len('ओम् '):]
    padas = [p for p in split_padas(lines) if p]
    ws = [weights(p) for p in padas]
    lens = [len(w) for w in ws]
    if lens == [8, 8, 8]:  # tripadA gAyatrI (Ch.5 yA devI mantras): syllable count only
        res['metre'] = 'gAyatrI'
        res['padas'] = [(p, w, 'gAyatrI') for p, w in zip(padas, ws)]
        return res
    if lens and all(n in (8, 9) for n in lens):
        labels = []
        for i, w in enumerate(ws):
            ok, lab = anushtubh_pada(w, odd=(i % 2 == 0))
            labels.append(lab)
            if not ok:
                res['issues'].append(f'pada {i + 1}: {lab}')
        res['metre'] = 'anuShTubh'
        res['padas'] = list(zip(padas, ws, labels))
        return res
    names = []
    for i, w in enumerate(ws):
        hit = [n for n, (p, _) in VRTTA.items() if match(p, w)]
        if not hit:
            best = min(((len(mismatches(p, w) or [0] * 99), n) for n, (p, _) in VRTTA.items()
                        if mismatches(p, w) is not None), default=(None, None))
            if best[0] is not None and best[0] <= 2:
                res['issues'].append(f'pada {i + 1}: near {best[1]} (positions {mismatches(VRTTA[best[1]][0], w)})')
                hit = [best[1]]
            else:
                res['issues'].append(f'pada {i + 1}: {len(w)} syllables, no metre matched')
                hit = ['?']
        names.append(hit[0])
    base = {n.split(':')[0] for n in names}
    if len(base) == 1:
        res['metre'] = base.pop()
    elif {FAMILIES.get(n) for n in names} - {None} and len({FAMILIES.get(n) for n in names}) == 1:
        res['metre'] = FAMILIES[names[0]]
    else:
        res['metre'] = '+'.join(dict.fromkeys(names))
    res['yati'] = VRTTA.get(names[0], ('', ()))[1] if names and names[0] in VRTTA else ()
    res['padas'] = list(zip(padas, ws, names))
    return res
