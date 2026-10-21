"""Parse durga700.itx (ITRANS) into a structured corpus of recitation units.

Each unit: section, kind, id (e.g. "1.2"), mantra count, bija prefix/suffix, lines (Devanagari).
kind is one of: viniyoga, dhyana, invocation, uvaca, half, shloka, tripada, verse (numbered verse of an
anga-stotra), refrain (extra unnumbered line), prose.
"""
import json
import pathlib
import re

from indic_transliteration import sanscript

from chandi.fetch import fetch, fetch_rahasya

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTION_RE = re.compile(r"\\section\{\|\|\s*(.*?)\s*\|\|\}")
NUM_RE = re.compile(r"\|\|\s*(\d+)(?:\\\.(\d+))?(?:\\-(\d+))?\s*\|\|\s*$")
TALLY_RE = re.compile(r"evamAditaH\s*\|\|\s*(\d+)\s*\|\|")
BIJA_HEAD_RE = re.compile(r"^OM(?:\s+(?:aiM|hrIM|klIM))?\s+")
BIJA_TAIL_RE = re.compile(r"\|\|\s*((?:aiM|hrIM|klIM)\s+OM)\s*\|\|\s*$")
STANDALONE_RE = re.compile(r"(namaH|kAyai|uvAcha|ovAcha|UchuH)\s*\|\|$")
UVACA_RE = re.compile(r"(uvAcha|ovAcha|UchuH)\s*$")  # ovAcha: rAjovAcha, brahmovAcha

# Source-text fixes, each verified against the Gita Press edition (archive.org scan,
# "ExEg_shri-durga-saptashati-gita-press-gorakhpur"). (section, kind or id, wrong, right)
CORRECTIONS = [
    ("ch12", "dhyana", "vilasadhastA", "vilasaddhastA"),  # GP: करवालखेटविलसद्धस्ताभिरासेविताम्
    ("ch8", "dhyana", "bANAchApa", "bANachApa"),  # GP: धृतपाशाङ्कुशबाणचापहस्ताम्
    ("pradhanika", "6", "taptak~nchana", "taptakA~nchana"),  # GP: तप्तकाञ्चनभूषणा
    ("pradhanika", "13", "guNeneduprabhraM", "guNenenduprabhaM"),  # GP: गुणेनेन्दुप्रभं दधौ
    ("vaikritika", "5", "shUlasha~NkhachakrabhushuDibhR^it", "shUlachakrasha~NkhabhushuNDibhR^it"),  # GP: …शूलचक्रशङ्खभुशुण्डिभृत्
    ("murti", "20", "chaDikAyAH", "chaNDikAyAH"),  # GP: जगन्मातुश्चण्डिकायाः
]
PEEL_RE = re.compile(r"^(?:OM\s+)?(namashchaNDikAyai|[^|]*(?:uvAcha|ovAcha|UchuH))\s*\|$")

# Section titles in the file -> stable keys, in file order.
SECTION_KEYS = [
    ("atha argalAstotram", "argala"),
    ("atha kIlakastotram", "kilaka"),
    ("atha devI kavacham", "kavacha"),
    ("devI mAhAtmyam", "intro"),
    ("atha aparAdhakShamApaNastotram", "aparadha"),
    ("atha devIsUktam", "devisukta"),
]


def to_deva(itrans):
    s = itrans.replace("\\-", "").replace("\\,", ",").replace("\\.", ".").replace(".h", "")
    s = s.replace("RRi", "R^i").replace("RRI", "R^I")
    return sanscript.transliterate(s, sanscript.ITRANS, sanscript.DEVANAGARI)


def section_key(title):
    m = re.match(r"(\d+)\\\.", title)
    if m:
        return f"ch{int(m.group(1))}"
    if "ekAdasho.adhyAyaH" in title or "aikAdasho.adhyAyaH" in title:  # the file omits "11." in this heading
        return "ch11"
    for t, k in SECTION_KEYS:
        if title == t:
            return k
    raise ValueError(f"unknown section {title!r}")


def split_sections(text):
    body = text.split("\\begin{document}", 1)[1]
    parts = SECTION_RE.split(body)
    out = [("pre", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((section_key(parts[i]), parts[i + 1]))
    return out


def clean_lines(block):
    lines = []
    for ln in block.splitlines():
        ln = ln.rstrip()
        if not ln.strip():
            lines.append("")  # blank line: ends an unnumbered dhyana block
            continue
        if ln.lstrip().startswith(("%", "\\")) or ln.strip() in ("##",) or ln.lstrip().startswith("samastA "):
            continue
        lines.append(ln.strip())
    return lines


def parse_section(key, block):
    units, buf, tallies = [], [], []
    mode = None  # 'viniyoga' | 'dhyana' | 'colophon'

    def flush(kind, ident=None, count=0, head=None, tail=None):
        nonlocal buf
        for sec, which, wrong, right in CORRECTIONS:
            if sec == key and which in (kind, ident):
                buf = [x.replace(wrong, right) for x in buf]
        if kind == "verse":  # anga-stotras: "namashchaNDikAyai | mArkaNDeya uvAcha |" open verse 1
            while len(buf) > 1 and PEEL_RE.match(buf[0]):
                m = PEEL_RE.match(buf[0])
                sub = "invocation" if m.group(1) == "namashchaNDikAyai" else "uvaca"
                units.append({"section": key, "kind": sub, "id": None, "count": 0, "bija_head": head,
                              "bija_tail": None, "itrans": [buf[0]], "lines": [to_deva(buf[0])]})
                head, buf = None, buf[1:]
                hm = BIJA_HEAD_RE.match(buf[0])
                if hm:
                    head, buf[0] = hm.group(0).strip(), buf[0][hm.end():]
        if buf:
            units.append({"section": key, "kind": kind, "id": ident, "count": count,
                          "bija_head": head, "bija_tail": tail,
                          "itrans": list(buf), "lines": [to_deva(x) for x in buf]})
        buf = []

    for ln in clean_lines(block):
        if ln.startswith("iti shrImArkaNDeya"):  # Rahasya colophon: the rest is credits
            mode = "end"
        if ln == "":
            if mode == "dhyana" and buf:
                flush("dhyana"); mode = None
            continue
        if mode == "end":
            continue
        if ln.startswith("|| OM tat sat"):
            mode = "end"; continue
        if ln.startswith("|| svasti") or ln.startswith("|| iti") or mode == "colophon":
            mode = "colophon"
            t = TALLY_RE.search(ln)
            if t:
                tallies.append(int(t.group(1)))
                mode = None
            elif ln.endswith("samAptam ||") or "adhyAyaH ||" in ln:
                mode = None if key.startswith("ch") is False else mode
            continue
        if ln.startswith("||") and ln.endswith("||") and not NUM_RE.search(ln[2:]):
            if "dhyAnam" in ln:
                mode = "dhyana"
            continue  # standalone headings like "|| shrI ||"
        if ln == "viniyogaH" or ln.startswith("OM asya") or ln.startswith("asya shrI"):
            mode = "viniyoga"
        if ln.startswith(". dhyAnam") or ln == "athavA":
            mode = "dhyana"
            continue
        if ln in (". aiM OM |", ". hrIM OM |"):
            continue
        buf.append(ln)

        if mode == "viniyoga":
            if "viniyogaH" in ln and ln.endswith("|") or ln.endswith("viniyogaH ||") or ln.endswith("japye viniyogaH |"):
                flush("viniyoga"); mode = None
            continue

        m = NUM_RE.search(ln)
        bt = BIJA_TAIL_RE.search(ln)
        if m:
            a, b, c = m.group(1), m.group(2), m.group(3)
            buf[-1] = NUM_RE.sub("||", ln).rstrip()
            head = None
            hm = BIJA_HEAD_RE.match(buf[0])
            if hm and mode != "dhyana":
                head = hm.group(0).strip(); buf[0] = buf[0][hm.end():]
            if b is None:  # anga-stotra verse number "|| 7||"
                flush("verse", a, 1, head)
            else:
                ident = f"{a}.{b}" + (f"-{c}" if c else "")
                n = int(c) - int(b) + 1 if c else 1
                joined = " ".join(buf)
                if c:
                    kind = "tripada"
                elif UVACA_RE.search(joined.replace("||", "").strip()):
                    kind = "uvaca"
                elif len(buf) == 1 and "|" not in buf[0].replace("||", ""):
                    kind = "half"
                else:
                    kind = "shloka"
                flush(kind, ident, n, head)
            mode = None
        elif bt:
            buf[-1] = BIJA_TAIL_RE.sub("||", ln)
            flush("refrain", None, 0, None, bt.group(1))
        elif ln.endswith("||") and mode != "dhyana" and len(buf) == 1 and STANDALONE_RE.search(ln):
            # "OM namashchaNDikAyai ||", "rAjovAcha ||"; any other unnumbered "||" is a mid-verse typo
            flush("uvaca" if UVACA_RE.search(ln.rstrip("| ")) else "invocation")
    if buf:
        flush("prose")
    return units, tallies


def build():
    text = fetch().read_text(encoding="utf-8")
    corpus, tallies = [], {}
    for key, block in split_sections(text):
        units, t = parse_section(key, block)
        corpus.extend(units)
        if t:
            tallies[key] = t
    for key, path in fetch_rahasya().items():
        body = path.read_text(encoding="utf-8").split("\\begin{document}", 1)[1]
        units, _ = parse_section(key, body)
        corpus.extend(units)
    return corpus, tallies


def validate(corpus, tallies):
    expected = [104, 69, 44, 42, 129, 24, 27, 63, 41, 32, 55, 41, 29]
    problems, running = [], 0
    for ch, exp in enumerate(expected, 1):
        units = [u for u in corpus if u["section"] == f"ch{ch}" and u["id"]]
        got = sum(u["count"] for u in units)
        running += got
        # numbers must run 1..exp without gaps
        nums = []
        for u in units:
            a, _, rest = u["id"].partition(".")
            lo, _, hi = rest.partition("-")
            nums.extend(range(int(lo), int(hi or lo) + 1))
        if got != exp or nums != list(range(1, exp + 1)):
            problems.append(f"ch{ch}: got {got} mantras, expected {exp}")
        if tallies.get(f"ch{ch}") and tallies[f"ch{ch}"][-1] != running:
            problems.append(f"ch{ch}: running total {running} != colophon {tallies[f'ch{ch}'][-1]}")
    kinds = {}
    for u in corpus:
        if u["section"].startswith("ch") and u["id"]:
            kinds[u["kind"]] = kinds.get(u["kind"], 0) + u["count"]
    return problems, kinds, running


if __name__ == "__main__":
    corpus, tallies = build()
    problems, kinds, total = validate(corpus, tallies)
    out = ROOT / "data" / "corpus.json"
    out.write_text(json.dumps(corpus, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(corpus)} units -> {out}")
    print("mantra total:", total, "by kind:", kinds)
    print("problems:", problems or "none")
