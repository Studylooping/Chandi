# 1. The Navārṇa mantra: its form, extraction, attributes and sources

**ऐं ह्रीं क्लीं चामुण्डायै विच्चे** (*aiṃ hrīṃ klīṃ cāmuṇḍāyai vicce*)

How to read this file:
- **[TEXT]**: what a primary text says (the Devī Atharvaśīrṣa, the Mārkaṇḍeya-Purāṇa text, or tantras *as quoted*).
- **[COMMENTARY]**: what the traditional commentators say (Bhāskararāya's *Guptavatī*, Nāgojībhaṭṭa's commentary, and others in the same edition).
- **[ACADEMIC]**: what modern scholarship says. For this question I found **no academic study** and consulted none (see §8).

Sigla:
- **DSS7**: *Durgāsaptaśatī with seven commentaries* (Guptavatī, Caturdharī, Śāntanavī, Nāgojībhaṭṭī, Jagaccandracandrikā, Daṃśoddhāra, Durgāpradīpa). The edition is on archive.org: <https://archive.org/details/saptashati-7-teeka-1>. "Vol. 1" is the file `saptashati-7-teeka-1_text.pdf` and "Vol. 3" is `saptashati-7-teeka-3_text.pdf`. "p." is the printed page and "PDF" is the page index in that file.
- Every DSS7 quotation was read from the page image (pdftoppm at 240–260 dpi), not only from the OCR. Where a few akṣaras were unclear, the reading is marked `[?]`. Spelling is lightly normalised (anusvāra and visarga sandhi as printed).
- **AŚ**: *Devyatharvaśīrṣa* (Devī Upaniṣad), sanskritdocuments.org `deviiatharva.itx`, <https://sanskritdocuments.org/doc_devii/deviiatharva.itx>. Verse numbers follow that file.
- **GP**: Gita Press verse numbering of the Saptaśatī, as in sanskritdocuments.org `durga700.itx` (sha256 `1ea0e4f2…`, the revision the repo pins).

---

## 1. The form of the mantra

**[COMMENTARY]** Nāgojībhaṭṭa's *prayoga-vidhi* (DSS7 Vol. 1, p. 66, PDF 47), in the section he introduces as the Ḍāmara-kalpa procedure:
> ऐंह्रींक्लींचामुण्डायैविच्चे इति नवाक्षरो मन्त्रः ।

"*aiṃ hrīṃ klīṃ cāmuṇḍāyai vicce*: this is the nine-syllable mantra."

**Why "nine"?** Written out, the mantra has more than nine letters. Bhāskararāya says so himself (DSS7 Vol. 1, p. 10, PDF 21):
> तत्राद्यस्य चतुर्विंशतिवर्णात्मत्वेऽपि व्यञ्जनानां स्वराङ्गत्वेन स्वातन्त्र्येणाक्षरसंख्याव्यवहारानुपयोगित्वेन 'एष वै सप्तदशः प्रजापतिर्यज्ञेऽन्वायत्तः' इत्यादाविव स्वरसंख्ययैव नवार्णता । अर्णशब्दोऽपि वर्णपरः …

"Although the first [mantra, the Navārṇa] consists of twenty-four letters, consonants are subordinate to vowels and so are not counted on their own. As in the Vedic 'This Prajāpati, seventeenfold, is bound up with the sacrifice', the count is by vowels only, which gives 'nine-*arṇa*'. The word *arṇa* also means 'letter'."

The nine vowel-bearing syllables are ऐं / ह्रीं / क्लीं / चा / मुं / डा / यै / वि / च्चे. This syllable division is exactly the one used in the uddhāra verse in §2.

**Observation on the text file (not a claim about manuscripts).** The `durga700.itx` file contains the Kavaca, Argalā, Kīlaka and the 13 chapters. It does not contain the string `vichche` anywhere. The three bījas appear only at the heads of the three caritras: "OM aiM mArkaNDeya uvAcha" (1.1), "OM hrIM R^iShiruvAcha" (2.1), "OM klIM R^iShiruvAcha" (5.1), plus "klIM OM" at the very end (after 13.29). So the full Navārṇa is **not** part of the 700 verses. It is a separate mantra attached to the recitation.

---

## 2. Uddhāra: how the letters are extracted

### 2.1 The source verse: Devī Atharvaśīrṣa 20

**[TEXT]** AŚ v. 18–20 (sanskritdocuments `deviiatharva.itx`). Variants given in that file are in brackets.
> वियदीकारसंयुक्तं वीतिहोत्रसमन्वितम् । अर्धेन्दुलसितं देव्या बीजं सर्वार्थसाधकम् ॥ १८ ॥
> एवमेकाक्षरं मन्त्रं [var. ब्रह्म] यतयः शुद्धचेतसः । ध्यायन्ति परमानन्दमया ज्ञानाम्बुराशयः ॥ १९ ॥
> वाङ्माया ब्रह्मसूस्तस्मात् षष्ठं वक्त्रसमन्वितम् । सूर्योऽवामश्रोत्रबिन्दुसंयुक्तष्टात्तृतीयकः । नारायणेन संमिश्रो वायुश्चाधरयुक्ततः । विच्चे नवार्णकोऽर्णः स्यान्महदानन्ददायकः ॥ २० ॥

- v. 18: "Sky (*ha*) joined with *ī*, accompanied by fire (*ra*), shining with the half-moon (*bindu*): the goddess's bīja, which accomplishes every aim." That is ह्रीं.
- v. 20: "Speech, Māyā, Brahma-sū; then the sixth from that, joined with 'mouth'; Sun with right-ear and bindu; the third from ṭa, mixed with Nārāyaṇa; Wind joined with 'lower lip'; *vicce*. This is the nine-letter mantra, giver of great bliss."

### 2.2 Bhāskararāya's gloss on AŚ 20

**[COMMENTARY]** DSS7 Vol. 1, p. 10, PDF 21. He first places the passage in the Upaniṣad:
> तदुद्धारस्तु देव्यथर्वशीर्षोपनिषदि ।

"Its extraction is in the Devī-Atharvaśīrṣa Upaniṣad."

He says the Upaniṣad first extracts the Śrīvidyā (AŚ 14, कामो योनिः कमला …). It then gives the śakti-bīja (हृल्लेखा, i.e. ह्रीं) separately in v. 18 (वियदीकारसंयुक्तम्). Finally:
> तादृशबीजत्रयघटितो नवार्णो मन्त्र उद्धृतः ।

"…[and then] the Navārṇa, made up of those three bījas, is extracted."

His word-by-word gloss, same page:

| AŚ code word | Bhāskararāya's gloss (verbatim) | Result |
|---|---|---|
| वाक् | वाग्भवबीजम् | ऐं |
| माया | शक्तिः हृल्लेखैव | ह्रीं |
| ब्रह्मसूः | कामः | क्लीं |
| तस्मात् षष्ठं वक्त्रसमन्वितम् | कामबीजात् तत्र प्रथमोपस्थितात् ककारात् षष्ठमक्षरं चकारः, वक्त्रेण मुखवृत्तेन आकारेण समन्वितम् | चा |
| सूर्यः अवामश्रोत्रबिन्दुसंयुक्तः | 'सूर्यो' मः, 'अवामश्रोत्रं' पञ्चमस्वरः, 'बिन्दु'रनुस्वारः | मुं |
| टात् तृतीयकः नारायणेन संमिश्रः | टकारात् तृतीयको वर्णो डकारः, स च 'नारायणेना'ऽऽकारेण संमिश्रः | डा |
| वायुः अधरयुक्तः | 'वायु'र्यकारः, स 'चाधरेणा'ऽधरोष्ठेन द्वादशस्वरेण युक्तः | यै |
| विच्चे | इति स्वरूपम् | विच्चे |
| अर्णः (var. अणुः) | 'अणु'र्मन्त्रः | "the mantra" |

He paraphrases the result as **महतामुपासकानामानन्ददायकः ब्रह्मसायुज्यप्रदः**: "giver of bliss to great worshippers, giver of union with Brahman."

### 2.3 A second, verse-form uddhāra (Ḍāmara-kalpa, as quoted by Nāgojībhaṭṭa)

**[TEXT as quoted]** DSS7 Vol. 1, p. 66, PDF 47:
> अथैतस्य स्तोत्रस्य पाठे डामरकल्पोक्तो नवार्णसंपुटीकरणप्रयोगविधिः । तत्रादौ तदुद्धारः । ऐंबीजमादाविन्दुसमानदीप्ति ह्रीं सूर्यतेजोद्युतिमद्द्वितीयम् । क्लींमूर्तिवैश्वानरतुल्यरूपं तृतीयमानन्त्यसुखाय चिन्त्यम् ॥ १ ॥ चां शुद्धजाम्बूनदकान्ति तुर्यं मुं पञ्चमं रक्ततरं प्रकल्प्यम् । डा षष्ठमुग्रार्तिहरं सलीलं यै सप्तमं कृष्णतरं रिपुघ्नम् ॥ २ ॥ विपाण्डुरं त्वष्टममासि सिद्धं [च्चे] धूम्रवर्णं नवमं विशालम् ।

This version gives each of the nine syllables a colour for meditation. In order:
1. ऐं is moon-bright.
2. ह्रीं has the brilliance of the sun.
3. क्लीं has the form of fire.
4. चां is pure gold.
5. मुं is deep red.
6. डा removes fierce affliction.
7. यै is very dark and destroys enemies.
8. वि is pale white.
9. च्चे is smoke-coloured.

The ninth syllable is cut off in the print. I read `[च्चे] धूम्रवर्णं` from the context.

### 2.4 The 24 letters also extracted from the Saptaśatī itself (Bhāskararāya's reading)

**[COMMENTARY]** DSS7 Vol. 1, p. 12, PDF 23:
> 'यस्याः प्रभावमतुलं भगवाननन्तो ब्रह्मा हरश्च नहि वक्तुमलं बलं च । सा चण्डिका' इत्यत्र नवार्णमन्त्रगतानां चतुर्विंशतिवर्णानामुद्धारः ।

"In [DM 4.4, GP] 'yasyāḥ prabhāvam atulaṃ …' the twenty-four letters of the Navārṇa are extracted."

He adds:
> अनन्तादिपदत्रयस्य नवार्णमन्त्रद्रष्टृऋषिपरत्वेनापि पुनरन्वयात्

That is, the words Ananta, Brahmā and Hara in that verse are *also* to be read as the seers who saw the Navārṇa. He then generalises:
> एवमन्यत्राप्यम्बानुग्रहपात्रतातारतम्येन सर्वमिदं स्तोत्रं मन्त्रोद्धारगर्भितमेव दृश्यते ।

"Likewise elsewhere, to the degree one is a vessel of the Mother's grace, this whole hymn is seen to be pregnant with mantra-extractions."

He supports this with a verse he attributes to a *Vedāgama*: निर्विशेषपरा मन्त्राः सविशेषपराश्च ये । प्रत्यध्यायं निगूढास्ते तेनेयं सर्वतः परा.

He also reports (p. 11, PDF 22) that other commentators extract the bīja from the first verse, **सावर्णिः सूर्यतनयो यो मनुः कथ्यतेऽष्टमः** (GP 1.2). They follow "Dīkṣita's" *Devīcandrakalāstava* (देवीचन्द्रकलास्तवे दीक्षितैः प्रदर्शितम्), and *yaḥ* → *ha* + *sūryatanaya* → *ra* + *sāvarṇi* → *ī* gives a bindu-less ह्री(ं). He accepts this only as "somehow appropriate, since ṛṣi-utterances face every direction" (आर्षवाक्यानां सर्वतोमुखत्वादस्तु कथंचिद्युक्तमेवैतत्) and then gives his own alternative extractions. I did not identify the author "Dīkṣita" or locate the *Devīcandrakalāstava* (**UNVERIFIED**).

---

## 3. Ṛṣi, chandas, devatā and the other attributes (ṛṣyādi)

### 3.1 The verse

**[TEXT as quoted]** It is quoted, with minor variants, in two places in DSS7 Vol. 1:

**(a) Guptavatī**, p. 12, PDF 23 (bottom). Bhāskararāya introduces it without naming its source: "उभयथापि नवार्णस्य संक्षेपेण साधनप्रकार इह वक्तव्य एवेत्युच्यते".
> नवाक्षरस्य ऋषयो ब्रह्मविष्णुमहेश्वराः । छन्दांस्युक्तानि मुनिभिर्गायत्र्युष्णिगनुष्टुभः ॥ देव्यः प्रोक्ता महापूर्वाः काली लक्ष्मीः सरस्वती । नन्दाशाकम्भरीभीमाः शक्तयोऽस्य मनोः स्मृताः ॥ स्याद्रक्तदन्तिकादुर्गाभ्रामर्यो बीजसन्ततिः । अग्निर्वायुः सूर्यस्तत्त्वं फलं वेदत्रयोद्भवम् ॥ सर्वाभीष्टप्रसिद्ध्यर्थे विनियोग उदाहृतः । ऋषिच्छन्दोदैवतानि शिरो-मुख-हृदि न्यसेत् ॥ शक्तिबीजानि स्तनयोस्तत्त्वानि हृदये पुनः । ह्रीं चण्डिकायै व्यस्तेन सर्वेण च षडङ्गकौ ॥

**(b) Nāgojībhaṭṭī**, p. 66–67, PDF 47–48. Here the verse sits inside the "डामरकल्पोक्तो नवार्णसंपुटीकरणप्रयोगविधिः" (see §2.3). Variants:
- शक्तयश्च मुनिस्मृताः
- बीजसंचयः
- अग्निवायुभगास्तत्त्वं … । भगः सूर्यः
- सर्वाभीष्टसिद्ध्यर्थं च विनियोग उदाहृतः

Immediately before the verse, the same Ḍāmara passage says:
> अस्मिन्नवाक्षरे मन्त्रे महालक्ष्मीर्व्यवस्थिता । तस्मात्सुसिद्धिः सर्वेषां सर्वदिक्षु प्रदीपकः । अतोऽत्र सिद्धादिविचारो नास्तीति ज्ञापितम् ।

"In this nine-syllable mantra Mahālakṣmī is established. Hence it is easily perfected by everyone… so here there is no need to examine [whether the mantra is] *siddha* etc. [for the practitioner]."

So the verse's **source**, as far as these two commentators let us see, is the Ḍāmara tantra/kalpa. That attribution comes from Nāgojī's framing. Bhāskararāya does not name a source at this point. I have not seen any independent text of a "Ḍāmara-kalpa" (**UNVERIFIED**).

### 3.2 The attributes in table form

| Attribute | Value (in the order of the three bījas / caritras) |
|---|---|
| ṛṣi | Brahmā, Viṣṇu, Maheśvara |
| chandas | Gāyatrī, Uṣṇik, Anuṣṭubh |
| devatā | Mahā-kālī, Mahā-lakṣmī, Mahā-sarasvatī ("महापूर्वाः") |
| śakti | Nandā, Śākambharī, Bhīmā |
| bīja | Raktadantikā, Durgā, Bhrāmarī |
| tattva | Agni, Vāyu, Sūrya (Nāgojī: Bhaga = Sūrya) |
| phala / viniyoga | "arising from the three Vedas"; for the attainment of all desires |
| nyāsa | ṛṣi→head, chandas→mouth, devatā→heart, śakti/bīja→breasts, tattva→heart again. Ṣaḍaṅga with ह्रीं चण्डिकायै, with the parts taken separately (व्यस्तेन) and as a whole |

**[TEXT] The same triads in the Gita Press caritra viniyogas** (`durga700.itx`):
- Ch. 1: "brahmA R^iShiH | mahAkAlI devatA | gAyatrI ChandaH | nandA shaktiH | raktadantikA bIjam | agnistattvam | R^igvedaH svarUpam".
- Ch. 2: "viShNurR^iShiH | shrImahAlakShmIrdevatA | uShNik ChandaH | shAkambharI shaktiH | durgA bIjam | vAyustattvam | yajurvedaH svarUpam".
- Ch. 5: "rudra R^iShiH | shrImahAsarasvatI devatA | anuShTup ChandaH | bhImA shaktiH | bhrAmarI bIjam | sUryastattvam | sAmavedaH svarUpam".

These are the Navārṇa ṛṣyādi triads distributed one per caritra. The Ḍāmara verse's "फलं वेदत्रयोद्भवम्" corresponds to the Ṛg/Yajur/Sāma *svarūpa*.

**[COMMENTARY] Nāgojībhaṭṭa rejects a variant of this distribution.** DSS7 Vol. 1, p. 68, PDF 49 (end of his prayoga-vidhi; page image checked). He quotes, as "said somewhere under the name of the Brahmāṇḍa Purāṇa" (ब्रह्माण्डपुराणनाम्ना … क्वचिदुक्ता), per-chapter verse counts, the ṛṣyādi of the Kavaca and Argalā, and then caritra viniyogas that **differ from the Gita Press set in the chandas**: "प्रथमचरित्रस्य ब्रह्मा ऋषिः । अनुष्टुप् छन्दः । महाकाली देवता । नन्दा शक्तिः । रक्तदन्तिका बीजम् । अग्निस्तत्त्वम् । पौष्टिके विनियोगः"; Viṣṇu/Mahālakṣmī/Śākambharī/Durgā/Uṣṇik/Vāyu ("ईप्सितप्राप्त्यर्थे"); Śiva/Mahāsarasvatī/"छन्दावनुष्टुब्जगत्यौ"/Bhīmā/Bhrāmarī/Sūrya ("उच्चाटनादौ"). Then he says:
> तत्तु कात्यायनीतन्त्रोक्तमन्त्रविभागेन विरोधात् निर्मूलमिति ध्येयम् ।

"But that should be regarded as baseless, because it conflicts with the mantra-division taught in the Kātyāyanī Tantra." The conflict he names is with the Kātyāyanī *mantra division* (most plausibly the verse counts quoted with it); he does not say this about the Gita Press viniyoga, whose first-caritra chandas (Gāyatrī) differs from the rejected variant (Anuṣṭubh).

**Other ṛṣyādi he records (p. 66, PDF 47):**
- For the caritras: Mārkaṇḍeya / Sumedhā / Śiva as ṛṣis; Anuṣṭubh / Anuṣṭubh / Anuṣṭubh-Jagatī as chandas; बीजs सौः / ह्रीं / क्लीं. He adds "ऐंमिति बीजमाद्यचरितस्येत्यन्यत्र" (elsewhere ऐं is the bīja of the first caritra). He sends the reader to the Kātyāyanī Tantra for their roots: "एतेषां मूलानि कात्यायनीतन्त्रे द्रष्टव्यानि".
- From "another tantra", for the whole Saptaśatī as a mālā-mantra: Nārāyaṇa ṛṣi, **Gāyatrī** chandas, devatā Śumbha-mardinī as Dakṣiṇāmūrti, bīja क्लीं, śakti सोऽहम्.

So the tradition itself does not have a single ṛṣyādi for the Saptaśatī.

**Interpretation.** The repo's README already notes the consequence: Gāyatrī/Uṣṇik/Anuṣṭubh here are **attributes of the Navārṇa for nyāsa**, not the metres of the verses.

---

## 4. Meaning of the mantra, according to the commentators

All of this section is **[COMMENTARY]**: Bhāskararāya, DSS7 Vol. 1, pp. 10–11, PDF 21–22.

**The three bījas as sat–cit–ānanda.**
> सच्चिदानन्दात्मकपरब्रह्मधर्मत्वादेव शक्तेरपि त्रिरूपत्वम् । तत्र चिद्रूपा महासरस्वती वाग्बीजेन सम्बोध्यते । … एतेन सद्रूपात्मकमहालक्ष्मीरूपस्य हृल्लेखया सम्बोधनमिति व्याख्यातम् । … तेन आनन्दप्रधानेन महाकालीस्वरूपस्य कामबीजेन सम्बोधनमुक्तम् ।

"Because Śakti is the property of the Brahman whose nature is being, consciousness and bliss, Śakti too is threefold. Mahāsarasvatī, consciousness, is addressed by the speech-bīja (ऐं). … Mahālakṣmī, being, is addressed by the hṛllekhā (ह्रीं). … Mahākālī, in whom bliss predominates, is addressed by the kāma-bīja (क्लीं)." Details are in file 02.

**Cāmuṇḍā.** Bhāskararāya gives several etymologies:
- "चामुण्डाशब्दो हि मोक्षकारणीभूतनिर्विकल्पकवृत्तिविशेषपरः … चमूं सेनां वियदादिसमूहरूपां डाति … नाशयतीति": the word denotes the non-conceptual mental mode that causes liberation; she "devours the army" made of space and the other elements.
- He cites DM 7.27 (GP): यस्माच्चण्डं च मुण्डं च गृहीत्वा त्वमुपागता । चामुण्डेति ततो लोके ख्याता देवी भविष्यसि.
- Alternatively, Cāmuṇḍā is simply the name of the deity Caṇḍikā (p. 11: चण्डिकारूपदेवतापर एव चामुण्डाशब्दः). The dative (-āyai) implies *namaḥ*, and in homa the offering formula is "चामुण्डाया इदम्".

**Vicce.**
- (i) Read as *vit* + *ca* + *i*, vocatives for consciousness, being and bliss: "विच्चे इति तु वित् च इ इति पदत्रयात्मकं बीजक्रमेणोक्तानां चित्सदानन्दानां वाचकं संबुध्यन्तम्".
- (ii) Read as an indeclinable meaning "release": "विच्चे इत्यप्यखण्डमव्ययं मोचनार्थकम्". The sense is then a prayer, "हे अम्ब बन्धनकारणीभूतामिमां रज्जुं ग्रन्थिविसर्जनादिना मोचय" ("O Mother, untie this rope that binds"). He supports this from Kannada and Telugu usage: "कर्णाटभाषाविद्भिरान्ध्रभाषाविद्भिश्च शिष्टैः प्रयोगेण शक्तिग्रहसम्भवात्".

**Summary meanings he quotes.**
- "Said there", i.e. in the Ḍāmara and other tantras: निर्धूतनिखिलध्वान्ते नित्यमुक्ते परात्परे । अखण्डब्रह्मविद्यायै चित्सदानन्दरूपिणि । अनुसंदध्महे नित्यं वयं त्वां हृदयाम्बुजे.
- His own summary: महासरस्वति चिते महालक्ष्मि सदात्मके । महाकाल्यानन्दरूपे त्वत्तत्त्वज्ञानसिद्धये । अनुसंदध्महे चण्डि वयं त्वां हृदयाम्बुजे.
- Another summary (p. 11): काल्यै लक्ष्म्यै सरस्वत्यै चण्डिकायै नमोऽस्तु ते । अविद्यापाशहृदयग्रन्थिं विस्रस्य मुञ्च माम्.
- The *Rahasya-tantra*, which he cites without verse, makes the meaning the identity of jīva and Brahman, like a *mahāvākya*: "रहस्यतन्त्रे तु महावाक्यस्येव जीवब्रह्मणोरभेद एव मन्त्रस्यार्थ इत्युक्तम्".

---

## 5. Textual sources: which tantras, and what I could verify

| Source | What it is said to contain | Where I saw it | Status |
|---|---|---|---|
| **Devī Atharvaśīrṣa** (Devī Upaniṣad) | the coded uddhāra of ह्रीं (v. 18) and of the full Navārṇa (v. 20) | AŚ text itself (sanskritdocuments); Guptavatī p. 10 names it as the uddhāra source | **Verified** in the e-text. The manuscript basis of that e-text was not checked. |
| **Ḍāmara tantra / Ḍāmara-kalpa** | the Navārṇa's greatness and meaning; the saṃpuṭa rule; the verse uddhāra; the ṛṣyādi verse; the verse count of the Saptaśatī (578 ślokas → 700 offerings) | Guptavatī p. 10 ("एतन्महिमातिशयो डामरादितन्त्रेषु द्रष्टव्यः") and p. 13; Nāgojī pp. 66–67 | **Cited by both commentators.** I did not locate an independent edition or manuscript (**UNVERIFIED**). |
| **Kātyāyanī Tantra** | the authoritative division of the Saptaśatī into 700 mantras (incl. 22 *tripāda-gāyatrī* mantras in Ch. 5); the roots of the caritra ṛṣyādi | Guptavatī p. 12, p. 14, p. 26 (PDF 37: "कात्यायनीतन्त्रोक्तपाठावलम्बे"); Nāgojī p. 66, p. 68 | **Cited.** I did not see the tantra itself (**UNVERIFIED**). In the passages I read, neither commentator cites it for the Navārṇa's uddhāra or ṛṣyādi. |
| **Marīci-kalpa** | the saṃpuṭa of the Saptaśatī with the Vedic Rātri-sūkta before and Devī-sūkta after: "रात्रिसूक्तं जपेदादौ मध्ये चण्डीस्तवं पठेत् । प्रान्ते तु जपनीयं वै देवीसूक्तमिति क्रमः" | Guptavatī p. 13, PDF 24 | **Cited.** In the quoted lines it concerns the Vedic sūktas, **not** the Navārṇa. |
| **Vārāhī, Marīci, Haragaurī, Lakṣmī tantras** | that the 13 chapters form one mālā-mantra | Guptavatī pp. 13–14 ("वाराहीतन्त्र-कात्यायनीतन्त्र-मरीचितन्त्र-हरगौरीतन्त्र-लक्ष्मीतन्त्रादीनां बहूनामैकमत्याच्च") | **Cited** as a list. Not checked in the tantras themselves. |
| **"Yāmala" tantras** | a recitation recension in which, to reach 700, the Navārṇa is inserted 32 times: "यामलादितन्त्रावलम्बितपाठयोर्मध्ये सप्तशतसंख्यापूर्त्यर्थमेकत्र द्वात्रिंशद्वारं नवार्णः शरणीक्रियते" | Guptavatī p. 26, PDF 37 (image-verified) | **Cited.** Which Yāmala is meant is not said there. |
| **Rudrayāmala (Gaurī-tantra)** | the *Siddha-kuñjikā-stotra*, which embeds the Navārṇa ("OM aiM hrIM klIM chAmuNDAyai vichche"). Colophon: "iti shrIrudrayAmale gaurItantre shivapArvatIsaMvAde kuJjikAstotraM sampUrNam", with variant "iti shrI DAmaratantre IshvarapArvatIsaMvAde …" | sanskritdocuments `siddhakunjikaa.itx`, <https://sanskritdocuments.org/doc_devii/siddhakunjikaa.itx> | The **colophon is verified** in that e-text. Whether any extant *Rudrayāmala* manuscript contains it is **UNVERIFIED**. The e-text itself gives two different attributions. |

---

## 6. Relation to the Saptaśatī: aṅga or aṅgin? The Saptaśatī as mālā-mantra

**[COMMENTARY] Two supreme mantras.** DSS7 Vol. 1, p. 10, PDF 21:
> ईदृशानामरूपोपाधिकस्य शक्तिरूपब्रह्मण उपासनाप्रकाशकेषु बहुषु मन्त्रेषु द्वावत्युत्तमौ । नवार्णः सप्तशती चेति ।

"Among the many mantras that teach the worship of Brahman as Śakti, two are supreme: the Navārṇa and the Saptaśatī."

**[TEXT as quoted] The saṃpuṭa rule from the Ḍāmara tantra.** Guptavatī p. 13, PDF 24:
> अयमुभयविधोऽपि जपः सप्तशतीस्तोत्रेण संपुटीकृतो विधेयः । तदुक्तं डामरतन्त्रे 'मार्कण्डेयपुराणोक्तं नित्यं चण्डीस्तवं पठन् । पुटितं मूलमन्त्रस्य जपेनाप्नोति वाञ्छितम्' इति ।

"This japa [of the Navārṇa], of either kind, is to be enclosed by the Saptaśatī hymn. As the Ḍāmara Tantra says: 'Reciting daily the Caṇḍī hymn told in the Mārkaṇḍeya Purāṇa, enclosed (*puṭita*) by japa of the root mantra, one obtains what one desires.'"

**[COMMENTARY] The aṅga–aṅgin dispute.** Guptavatī p. 13, PDF 24.

Bhāskararāya reports that some read *puṭitam* the other way: the Saptaśatī enclosed by the Navārṇa. He rejects this reversal of principal and subordinate:
> केचित्तु मूलमन्त्रस्य जपेन पुटितं चण्डीस्तवं पठन्निति प्रथमश्लोकं योजयन्तश्चरमश्लोके पुनर्विधानं संख्यामात्रपरमिति मन्यमानाः सप्तशतीस्तोत्रस्यैव मूलेन संपुटिताकारो विधीयत इत्यङ्गाङ्गिभाववैपरीत्यमिच्छन्ति । तदयुक्तम् । बहुषु तन्त्रेषु नवार्णं प्रकृत्य तत्प्रकरणे सप्तशतीपाठविधानेन नवार्णजपस्य प्राकरणिकत्वेनान्याङ्गत्वायोगात् ।

"That is wrong. In many tantras the Saptaśatī recitation is enjoined in a section that is *about* the Navārṇa. So Navārṇa japa is the topic of the section and cannot be subordinate to something else."

He adds the Marīci-kalpa rule (Rātri-sūkta / Caṇḍī-stava / Devī-sūkta) as further evidence that a saṃpuṭa does not make the hymn principal. Then he qualifies his position:
> परन्त्वन्वारम्भणीयेष्टिवन्नवार्णस्य स्तोत्रजपप्रारम्भमात्राङ्गत्वं जपाधिकारितावच्छेदकत्वं चेति बोध्यम् । रहस्यं तु कीलकाध्याये स्पष्टीभविष्यति । … इति नवार्णनिर्णयः ॥

"However, the Navārṇa is an aṅga only of the *beginning* of the hymn's japa, like the *anvārambhaṇīyā iṣṭi*. It is what qualifies one to do the japa. The secret will be made clear in the Kīlaka chapter. … Thus the settlement about the Navārṇa."

He had also noted (p. 12) that some say the Navārṇa is worshipped in two ways, independently and as an aṅga of the Saptaśatī. In his own view the [Navārṇa-]vidyā is to be worshipped *through* the Saptaśatī: "सप्तशत्यैव तु तद्विद्योपास्येति".

**[COMMENTARY] The Saptaśatī as one mālā-mantra.** Guptavatī p. 13, PDF 24:
> द्वितीयस्तु चारित्रत्रयात्मकः श्लोकसमूहरूपो मन्त्रः । स च वामनपुराणदेवीभागवतमार्कण्डेयपुराणादिषु लक्ष्मीतन्त्रादिषु च बहुविध उपलभ्यते । तथापि मार्कण्डेयपुराणस्य एव त्रिसप्तत्यध्यायोत्तरं षडशीतितमाध्यायान्तमभिव्याप्तः 'सावर्णिः सूर्यतनयः' इत्यारभ्य 'सावर्णिर्भविता मनुः' इत्यन्तत्रयोदशभिरध्यायैः परिच्छिन्नः श्लोकसमूहात्मको मालामन्त्रत्वेन मान्यः । पूर्वोक्तडामरतन्त्रवचनात् ।

"The second [supreme mantra] is a mantra made of a group of verses, consisting of the three caritras. Versions of it are found in many forms in the Vāmana Purāṇa, the Devībhāgavata, the Mārkaṇḍeya Purāṇa, and in the Lakṣmī Tantra and others. Yet the one to be accepted as the mālā-mantra is that of the Mārkaṇḍeya Purāṇa itself. It spans from after chapter 73 to the end of chapter 86, beginning 'sāvarṇiḥ sūryatanayaḥ' and ending 'sāvarṇir bhavitā manuḥ', bounded by thirteen chapters. [This follows] from the Ḍāmara Tantra passage cited above."

Two notes on this passage:
- **Chapter numbers.** Bhāskararāya's count is MP chapters 74–86. Other editions number these chapters differently. Pargiter's translation (Introduction p. iv, checked in OCR) has "Cantos 82-92, the Devi-mahatmya, a pure interpolation", with cantos 81 and 93 as the Suratha frame. See file 03 §2.
- **"Saptaśatī".** On p. 14 (PDF 25) he says the name is not a count of ślokas: "अस्य सप्तशतीति व्यवहारस्तु न श्लोकसंख्यया". It comes from dividing the one mālā-mantra into 700 for homa, like the Śatarudriya: "एकमन्त्रात्मकस्यापि मालामन्त्रस्य होमाङ्गेन सप्तशततया विभजनाच्छतरुद्रियस्येवैकानेकमन्त्रात्मकत्वे विरोधाभावात्".

**[TEXT as quoted] The Ḍāmara count.** Nāgojī p. 66, PDF 47 gives the Ḍāmara tantra's count by speaker. It opens: "अधुना देवि वक्ष्यामि मालामन्त्रं नवार्णजम्" ("Now, O Devī, I shall tell the mālā-mantra **born of the Navārṇa**"). It ends:
> एवं सप्तशतीसंख्या श्लोका अष्टौ च सप्ततिः । शतानि पञ्च देवेशि तेषां सप्तशताहुतिः ।

"Thus the Saptaśatī's count: 578 ślokas, O queen of gods, and from them 700 oblations."

In this tantra the 700-verse hymn is called "born of the Navārṇa" (*navārṇa-ja*). That is the closest any text I read comes to stating a genetic relation between the two.

---

## 7. Who "conceived" the mantra?

- **[TEXT]** No text I read narrates an origin event for the Navārṇa.
  - The Devī Atharvaśīrṣa presents it as revealed: the Devī answers the gods' question कासि त्वं महादेवि (v. 1) and then gives the mantra in code (v. 20).
  - The ṛṣyādi (Ḍāmara, as quoted) names its "seers" as **Brahmā, Viṣṇu, Maheśvara**. In the tradition, a ṛṣi is the one who "saw" a mantra, not an author.
  - Bhāskararāya additionally reads Ananta (= Viṣṇu), Brahmā and Hara in DM 4.4 as the Navārṇa's seers (§2.4).
- **[ACADEMIC]** I found no historical study of when or where the Navārṇa mantra was formulated. Its historical origin is therefore **unknown to me**. Neither commentator gives a date, and I am not offering one.
- I did not verify the dates of the commentators themselves (Bhāskararāya, Nāgojībhaṭṭa) from a source in this session. They are **UNVERIFIED** here and are deliberately not stated.

---

## 8. What I could not verify

- Independent texts of the Ḍāmara tantra/kalpa, Kātyāyanī Tantra, Marīci-kalpa/tantra, Vārāhī and Haragaurī tantras. They are known here only through quotations in DSS7.
- Whether the *Siddha-kuñjikā-stotra* belongs to any extant *Rudrayāmala*.
- The *Devīcandrakalāstava* and its author "Dīkṣita".
- The source of the *Rahasya-tantra* statement (jīva–brahma abheda) and of the *Vedāgama* verse.
- Any academic dating of the Devī Atharvaśīrṣa or of the Navārṇa mantra. **None was consulted. This gap is real, not filled.**
- One akṣara in the colour verse (§2.3, the ninth syllable), which is cut off in the print.
