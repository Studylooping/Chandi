from chandi.prosody import identify, weights


def test_weights_basic():
    # long vowel, anusvara/visarga, conjunct (also across a word boundary) make guru
    assert weights('सावर्णिः सूर्यतनयो') == 'GGGGLLLG'
    assert weights('यो मनुः कथ्यतेऽष्टमः') == 'GLGGLGLG'
    assert weights('तत् स') == 'GL'
    assert weights('ॐ') == 'G'


def test_vasantatilaka():
    r = identify(['देव्या यया ततमिदं जगदात्मशक्त्या', 'निःशेषदेवगणशक्तिसमूहमूर्त्या ।',
                  'तामम्बिकामखिलदेवमहर्षिपूज्यां', 'भक्त्या नताः स्म विदधातु शुभानि सा नः ॥'])
    assert r['metre'] == 'vasantatilakA' and not r['issues']


def test_upajati():
    r = identify(['देवि प्रपन्नार्तिहरे प्रसीद', 'प्रसीद मातर्जगतोऽखिलस्य ।',
                  'प्रसीद विश्वेश्वरि पाहि विश्वं', 'त्वमीश्वरी देवि चराचरस्य ॥'])
    assert r['metre'] == 'upajAti' and not r['issues']


def test_anushtubh_and_vipula():
    r = identify(['सावर्णिः सूर्यतनयो यो मनुः कथ्यतेऽष्टमः ।', 'निशामय तदुत्पत्तिं विस्तराद्गदतो मम ॥'])
    assert r['metre'] == 'anuShTubh' and not r['issues']
    assert [p[2] for p in r['padas']] == ['na-vipulA', 'pathyA', 'pathyA', 'pathyA']


def test_om_is_extrametrical():
    r = identify(['ॐ खड्गं चक्रगदेषुचापपरिघाञ्छूलं भुशुण्डीं शिरः', 'शङ्खं सन्दधतीं करैस्त्रिनयनां सर्वाङ्गभूषावृताम् ।',
                  'नीलाश्मद्युतिमास्यपाददशकां सेवे महाकालिकां', 'यामस्तौत्स्वपिते हरौ कमलजो हन्तुं मधुं कैटभम् ॥'])
    assert r['extra'] == 'ॐ' and r['metre'] == 'shArdUlavikrIDita' and not r['issues']


def test_tripada_gayatri():
    r = identify(['या देवी सर्वभूतेषु विष्णुमायेति शब्दिता ।', 'नमस्तस्यै नमो नमः ॥'])
    assert r['metre'] == 'gAyatrI' and [len(w) for _, w, _ in r['padas']] == [8, 8, 8]
