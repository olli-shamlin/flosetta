
from app import FlosettaException
# TODO OBSOLETE CORPORA: from app.model import Syllabary
from app.corpora import Corpus
from app.corpora import CorpusType
import pytest


def test_syllabary():

    # TODO OBSOLETE CORPORA: syllabary = Syllabary()
    corpus = Corpus(CorpusType.SYLLABARY)
    syllabary = {character.romaji: character for character in corpus}

    kana = syllabary['romaji 1']
    assert kana.category == 'category 1'
    assert kana.romaji == 'romaji 1'
    assert kana.hiragana == 'hiragana 1'
    assert kana.katakana == 'katakana 1'
    assert kana.hiragana_note == 'hiragana note 1'
    assert kana.katakana_note == 'katakana note 1'

    # TODO OBSOLETE CORPORA: kana = syllabary['a']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Basic'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'a'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'あ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ア'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note == 'Ah! You found the letter A. Look for the letter A.'
    # TODO OBSOLETE CORPORA: assert kana.katakana_note == 'Ark. Think of Noah’s Ark.'
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['ka']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Basic'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'ka'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'か'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'カ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note == 'Batman will never Katch the Jo-KA! Think of Batman punching the Joker’s face. KA-POW!'
    # TODO OBSOLETE CORPORA: assert kana.katakana_note == 'Batman will never Katch the Jo-KA! Think of the Joker’s face.'
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['a']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Basic'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'a'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'あ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ア'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note == 'Ah! You found the letter A. Look for the letter A.'
    # TODO OBSOLETE CORPORA: assert kana.katakana_note == 'Ark. Think of Noah’s Ark.'
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['ga']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Dakuten'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'ga'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'が'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ガ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note is None
    # TODO OBSOLETE CORPORA: assert kana.katakana_note is None
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['po']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Dakuten'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'po'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'ぽ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ポ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note is None
    # TODO OBSOLETE CORPORA: assert kana.katakana_note is None
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['rya']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Modified YA'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'rya'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'りゃ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'リャ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note is None
    # TODO OBSOLETE CORPORA: assert kana.katakana_note is None
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['dzyu']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Modified YU'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'dzyu'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'ぢゅ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ヂュ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note is None
    # TODO OBSOLETE CORPORA: assert kana.katakana_note is None
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: kana = syllabary['myo']
    # TODO OBSOLETE CORPORA: assert kana.category == 'Modified YO'
    # TODO OBSOLETE CORPORA: assert kana.romaji == 'myo'
    # TODO OBSOLETE CORPORA: assert kana.hiragana == 'みょ'
    # TODO OBSOLETE CORPORA: assert kana.katakana == 'ミョ'
    # TODO OBSOLETE CORPORA: assert kana.hiragana_note is None
    # TODO OBSOLETE CORPORA: assert kana.katakana_note is None
    # TODO OBSOLETE CORPORA:
    return


def test_setters():

    # TODO OBSOLETE CORPORA: syllabary = Syllabary()
    corpus = Corpus(CorpusType.SYLLABARY)

    with pytest.raises(TypeError) as excinfo:
        corpus[0] = None
    assert str(excinfo.value) == "'Corpus' object does not support item assignment"

    # with pytest.raises(FlosettaException) as excinfo:
    #     syllabary['a'] = None
    # assert str(excinfo.value) == 'key "a" already exists in FrozenDict instance and cannot be modified'

    return
