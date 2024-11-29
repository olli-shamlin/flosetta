
from app import FlosettaException
# TODO OBSOLETE CORPORA: from app.model._cache import Vocabulary
from app.corpora import Corpus
from app.corpora import CorpusType
import pytest


def test_vocabulary():

    # TODO OBSOLETE CORPORA: vocab = Vocabulary()
    corpus = Corpus(CorpusType.VOCABULARY)
    vocab = {word.kana: word for word in corpus}

    word = vocab['kana 1']
    assert word.english == 'english 1'
    assert word.romaji == 'romaji 1'
    assert word.kana == 'kana 1'
    # TODO OBSOLETE CORPORA: assert word.kanji == 'kanji 1'
    # TODO OBSOLETE CORPORA: assert word.part_of_speech == 'pos-a'
    assert word.kanji is None
    assert word.part_of_speech == 'pos 2'
    # TODO OBSOLETE CORPORA: assert word.tags == ['tag-a']
    assert word.tags == tuple(['tag 1'])
    assert word.note is None

    # word = vocab['kana 33']
    # assert word.english == 'english 33'
    # assert word.romaji == 'romaji 33'
    # assert word.kana == 'kana 33'
    # assert word.kanji == 'kanji 33'
    # assert word.part_of_speech == 'pos-c'
    # assert word.tags == ['tag-a']
    # assert word.note is None
    #
    # word = vocab['kana 60']
    # assert word.english == 'english 60'
    # assert word.romaji == 'romaji 60'
    # assert word.kana == 'kana 60'
    # assert word.kanji == 'kanji 60'
    # assert word.part_of_speech is None
    # assert word.tags is None
    # assert word.note is None
    #
    # word = vocab['kana 59']
    # assert word.english == 'english 59'
    # assert word.romaji == 'romaji 59'
    # assert word.kana == 'kana 59'
    # assert word.kanji == 'kanji 59'
    # assert word.part_of_speech == 'pos-d'
    # assert word.tags == ['tag-a', 'tag-b', 'tag-c']
    # assert word.note == 'note 59'
    #
    return


def test_setters(create_test_data):

    # TODO OBSOLETE CORPORA: vocab = Vocabulary()
    # TODO OBSOLETE CORPORA:
    # TODO OBSOLETE CORPORA: with pytest.raises(FlosettaException) as excinfo:
    # TODO OBSOLETE CORPORA:     vocab['kana 36'] = None
    # TODO OBSOLETE CORPORA: assert str(excinfo.value) == 'key "kana 36" already exists in FrozenDict instance and cannot be modified'

    corpus = Corpus(CorpusType.VOCABULARY)

    with pytest.raises(TypeError) as excinfo:
        corpus[0] = None
    assert str(excinfo.value) == "'Corpus' object does not support item assignment"

    return


