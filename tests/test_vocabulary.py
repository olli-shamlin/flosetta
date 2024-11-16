
from app import FlosettaException
from app.model._cache import Vocabulary
import pytest


def test_vocabulary():

    vocab = Vocabulary()

    word = vocab['すこし']
    assert word.english == 'a bit'
    assert word.romaji == 'su ko shi'
    assert word.kana == 'すこし'
    assert word.kanji is None
    assert word.part_of_speech == 'adverb'
    assert word.tags == ['tag-1', 'tag-2']
    assert word.note is None

    word = vocab['はちがつ']
    assert word.english == 'august'
    assert word.romaji == 'ha chi ga tsu'
    assert word.kana == 'はちがつ'
    assert word.kanji == '八月'
    assert word.part_of_speech == 'adverbial noun'
    assert word.tags is None
    assert word.note == 'The month of August'

    return


def test_setters():

    vocab = Vocabulary()

    with pytest.raises(FlosettaException) as excinfo:
        vocab['いろいろ'] = None
    assert str(excinfo.value) == 'key "いろいろ" already exists in FrozenDict instance and cannot be modified ' \
                                 '(raised by app.model._cache.Vocabulary.__setitem__())'

    return


