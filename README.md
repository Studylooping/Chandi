# Chandi — metre-faithful Durgā Saptaśatī recitation

Goal: a learning-reference audio recitation of the Devī Māhātmya (Durgā Saptaśatī, 700 mantras,
Gita Press arrangement) in which every verse is recited according to its actual chandas:
laghu = 1 mātrā, guru = 2 mātrās, yati and pāda pauses per metre.

## Pipeline
1. `python -m chandi.corpus` downloads the source (`chandi/fetch.py`, pinned by sha256) and parses it
   into recitation units. Validated against the Gita Press tallies: 700 mantras =
   57 uvāca + 42 ardha-śloka + 535 śloka + 66 avadāna (22 *yā devī* verses × 3).
2. `python -m chandi.analyze` scans every verse (laghu/guru) and identifies its metre. Irregular
   verses are listed and each one is reviewed against the Gita Press scan (`REVIEWED` in
   `chandi/analyze.py`); source errors found this way are fixed in `CORRECTIONS` in `chandi/corpus.py`.
3. `python -m chandi.audio.recite --section ch1 [--ids 1.1-1.10] [--u 0.2]` renders audio plus a
   per-pada compliance report (`out/*.json`). For every pada:
   - synthesise (Indic Parler-TTS, male voice "Aryan"; needs a Hugging Face token, the model is gated);
   - force-align syllables (torchaudio MMS_FA) and measure each syllable as the interval from its
     vowel onset to the next one;
   - time-stretch (Rubber Band R3, formant-preserving) so laghu = 1 u and guru = 2 u exactly, the
     pada-final syllable held as guru;
   - re-align the result and **verify**: the measured pattern must equal the metre's laghu/guru
     pattern and every syllable must be within ±20% of its target; otherwise refine / re-synthesise,
     and report the pada as non-compliant if it still fails.
   Pauses: yati 1 u (only where it falls on a word boundary), pada 2 u, half-verse 3 u, verse 5 u.
   uvāca lines and other prose are read naturally at the same tempo.

## Source text
sanskritdocuments.org `durga700.itx` (follows Gita Press numbering). Its terms do not allow
reposting, so the text is **not** stored in this repository; it is downloaded into `data/`.

## Metres found (excluding the uvāca prose lines)
- Anuṣṭubh throughout, except:
- Ch.4 4.2–4.23 Vasantatilakā; Ch.5 5.81 Vaṃśastha, 5.82 Indravaṃśā; Ch.11 11.2–11.6 and
  11.29–11.33 Upajāti (Indravajrā/Upendravajrā), 11.34 Vasantatilakā.
- Dhyāna ślokas: Śārdūlavikrīḍita (1, 2, 3, 5, 6, 12), Sragdharā (4, 7), Aupacchandasika (8),
  Vasantatilakā (9, 10), Dodhaka (11), Anuṣṭubh (13).
- The viniyoga names Gāyatrī / Uṣṇik / Anuṣṭubh for the three caritras. These do not describe the
  verses' syllable structure (no 3×8 or 8+8+12 verses occur in Ch.1–4; Ch.5–13 also contain
  non-Anuṣṭubh metres). Source of the assignment: Bhāskararāya's *Guptavatī* (prayoga-vidhi) quotes
  the ṛṣyādi of the **Navārṇa mantra** — "नवाक्षरस्य ऋषयो ब्रह्मविष्णुमहेश्वराः । छन्दांस्युक्तानि
  मुनिभिर्गायत्र्युष्णिगनुष्टुभः ॥ … नन्दाशाकम्भरीभीमाः शक्तयो … रक्तदन्तिकादुर्गाभ्रामर्यो बीजसन्ततिः ।
  अग्निर्वायुः सूर्यस्तत्त्वं फलं वेदत्रयोद्भवम्" — exactly the ṛṣi/chandas/devatā/śakti/bīja/tattva/veda
  triads that the three caritra viniyogas distribute, one per caritra (with bījas ऐं/ह्रीं/क्लीं before
  1.1/2.1/5.1). Other tantras quoted in the same edition assign different chandas to the same verses
  (Ḍāmara: Gāyatrī/Uṣṇik/**Triṣṭubh**; another: the whole Saptaśatī as one mālā-mantra in Gāyatrī),
  which confirms the assignment is a mantra attribute for nyāsa, not the verse metre.
  Edition: *Durgāsaptaśatī with seven commentaries* (Guptavatī, Nāgojībhaṭṭī, Śāntanavī, …),
  https://archive.org/details/saptashati-7-teeka-1 (vol. 1; quotes are from its OCR, lightly normalised).
- The Ṛgvedic Devīsūkta needs Vedic svaras, which the source does not mark; it is not recited by this pipeline.

## Tests
`python -m pytest tests`
