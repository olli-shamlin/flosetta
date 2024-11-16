
from app import FlosettaException
from app.model import CacheItem
from app.model import fetch_from_cache
import pytest


def test_syllabary():

    syllabary = fetch_from_cache(CacheItem.SYLLABARY)

    kana = syllabary['a']
    assert kana.category == 'Basic'
    assert kana.romaji == 'a'
    assert kana.hiragana == 'あ'
    assert kana.katakana == 'ア'
    assert kana.hiragana_note == 'Ah! You found the letter A. Look for the letter A.'
    assert kana.katakana_note == 'Ark. Think of Noah’s Ark.'

    kana = syllabary['ka']
    assert kana.category == 'Basic'
    assert kana.romaji == 'ka'
    assert kana.hiragana == 'か'
    assert kana.katakana == 'カ'
    assert kana.hiragana_note == 'Batman will never Katch the Jo-KA! Think of Batman punching the Joker’s face. KA-POW!'
    assert kana.katakana_note == 'Batman will never Katch the Jo-KA! Think of the Joker’s face.'

    kana = syllabary['a']
    assert kana.category == 'Basic'
    assert kana.romaji == 'a'
    assert kana.hiragana == 'あ'
    assert kana.katakana == 'ア'
    assert kana.hiragana_note == 'Ah! You found the letter A. Look for the letter A.'
    assert kana.katakana_note == 'Ark. Think of Noah’s Ark.'

    kana = syllabary['ga']
    assert kana.category == 'Dakuten'
    assert kana.romaji == 'ga'
    assert kana.hiragana == 'が'
    assert kana.katakana == 'ガ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    kana = syllabary['po']
    assert kana.category == 'Dakuten'
    assert kana.romaji == 'po'
    assert kana.hiragana == 'ぽ'
    assert kana.katakana == 'ポ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    kana = syllabary['rya']
    assert kana.category == 'Modified YA'
    assert kana.romaji == 'rya'
    assert kana.hiragana == 'りゃ'
    assert kana.katakana == 'リャ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    kana = syllabary['dzyu']
    assert kana.category == 'Modified YU'
    assert kana.romaji == 'dzyu'
    assert kana.hiragana == 'ぢゅ'
    assert kana.katakana == 'ヂュ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    kana = syllabary['myo']
    assert kana.category == 'Modified YO'
    assert kana.romaji == 'myo'
    assert kana.hiragana == 'みょ'
    assert kana.katakana == 'ミョ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    return


def test_setters():

    syllabary = fetch_from_cache(CacheItem.SYLLABARY)

    kana = syllabary['myo']
    assert kana.category == 'Modified YO'
    assert kana.romaji == 'myo'
    assert kana.hiragana == 'みょ'
    assert kana.katakana == 'ミョ'
    assert kana.hiragana_note is None
    assert kana.katakana_note is None

    # with pytest.raises(FlosettaException) as excinfo:
    #     syllabary['a'] = None
    # assert str(excinfo.value) == \
    #        'modifying syllabary is not allowed (raised by app.model._syllabary.Syllabary.__setitem__())'

    assert False == 'This test is incomplete pending ability to prohibit updating syllabary entries'

    return
