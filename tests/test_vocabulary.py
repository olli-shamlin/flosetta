
from app import FlosettaException
from app.model._cache import Vocabulary
import pytest


def test_vocabulary():

    vocab = Vocabulary()

    word = vocab['kana 1']
    assert word.english == 'english 1'
    assert word.romaji == 'romaji 1'
    assert word.kana == 'kana 1'
    assert word.kanji == 'kanji 1'
    assert word.part_of_speech == 'pos-a'
    assert word.tags == ['tag-a']
    assert word.note == 'note 1'

    word = vocab['kana 33']
    assert word.english == 'english 33'
    assert word.romaji == 'romaji 33'
    assert word.kana == 'kana 33'
    assert word.kanji == 'kanji 33'
    assert word.part_of_speech == 'pos-c'
    assert word.tags == ['tag-a']
    assert word.note is None

    word = vocab['kana 60']
    assert word.english == 'english 60'
    assert word.romaji == 'romaji 60'
    assert word.kana == 'kana 60'
    assert word.kanji == 'kanji 60'
    assert word.part_of_speech is None
    assert word.tags is None
    assert word.note is None

    word = vocab['kana 59']
    assert word.english == 'english 59'
    assert word.romaji == 'romaji 59'
    assert word.kana == 'kana 59'
    assert word.kanji == 'kanji 59'
    assert word.part_of_speech == 'pos-d'
    assert word.tags == ['tag-a', 'tag-b', 'tag-c']
    assert word.note == 'note 59'

    return


def test_setters():

    vocab = Vocabulary()

    with pytest.raises(FlosettaException) as excinfo:
        vocab['kana 36'] = None
    assert str(excinfo.value) == 'key "kana 36" already exists in FrozenDict instance and cannot be modified'

    return


