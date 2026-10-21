import pytest

pytest.importorskip('torchaudio')
pytest.importorskip('pylibrb')

from chandi.audio.align import check_rhythm  # noqa: E402
from chandi.audio.render import matras_for, split_yati  # noqa: E402


def test_matras_pada_final_is_guru():
    assert matras_for('GLGL') == [2, 1, 2, 2]
    assert matras_for('GLGL', pada_final=False) == [2, 1, 2, 1]


def test_check_rhythm_exact_and_tempo_invariant():
    m = [2, 1, 2, 2, 1, 2, 1, 2]
    ok, u, rec, errs = check_rhythm([0.3 * x for x in m], m)
    assert ok and abs(u - 0.3) < 1e-9 and rec == 'GLGGLGLG'


def test_check_rhythm_rejects_swapped_weights():
    m = [2, 1, 2, 2, 1, 2, 1, 2]
    d = [0.2 * x for x in m]
    d[1], d[2] = d[2], d[1]  # a laghu held as guru and vice versa
    assert not check_rhythm(d, m)[0]


def test_split_yati_only_at_word_boundary():
    w = 'GGGLLGLGLLLGGGLGGLG'
    # yati after 12 falls inside "parighAJchUlaM": no split
    pada = 'खड्गं चक्रगदेषुचापपरिघाञ्छूलं भुशुण्डीं शिरः'
    assert split_yati(pada, w, (12,)) == [(pada, w)]
    # yati after 12 at a word boundary: split
    pada = 'शङ्खं सन्दधतीं करैस्त्रिनयनां सर्वाङ्गभूषावृताम्'
    (a, wa), (b, wb) = split_yati(pada, w, (12,))
    assert a.endswith('नयनां') and b.startswith('सर्वा') and (wa, wb) == (w[:12], w[12:])
