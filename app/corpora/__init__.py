
from dataclasses import asdict as _asdict
from dataclasses import dataclass as _dataclass
from datetime import date as _date
from enum import Enum as _Enum
from typing import Optional as _Optional

from ._store import character_store_key
from ._store import word_store_key
from ._store import load_syllabary as _load_syllabary
from ._store import load_vocabulary as _load_vocabulary
from ._store import save_metrics as _save_metrics


class CorpusType(_Enum):
    VOCABULARY = 'vocabulary'
    SYLLABARY = 'syllabary'


@_dataclass
class Metrics:
    key: str
    quizzed_count: int = 0
    correct_count: int = 0
    consecutive_correct: int = 0
    consecutive_incorrect: int = 0
    last_quizzed: _Optional[_date] = None

    def increment(self, answered_correct: bool = False) -> None:
        self.quizzed_count += 1
        if answered_correct:
            self.correct_count += 1
            self.consecutive_correct += 1
            self.consecutive_incorrect = 0
        else:
            self.consecutive_correct = 0
            self.consecutive_incorrect += 1
        self.last_quizzed = _date.today()

    @property
    def as_dict(self) -> dict:
        return _asdict(self)

    def __repr__(self) -> str:
        return f'Metrics(key="{self.key}")'


@_dataclass
class Element:
    corpus_key: int
    store_key: str
    metrics: _Optional[Metrics]

    @property
    def as_dict(self) -> dict:
        return _asdict(self)

    def increment_metrics(self, answered_correct: bool = False) -> None:
        if self.metrics is None:
            self.metrics = Metrics(key=self.store_key)
        self.metrics.increment(answered_correct)


class Corpus(tuple[Element]):

    def __new__(cls, corpus_type: CorpusType):
        elements = fetch(corpus_type)
        return super().__new__(cls, elements)

    def __init__(self, corpus_type: CorpusType):
        self._corpus_type: CorpusType = corpus_type

    def flush(self) -> None:
        """Saves all Elements' non-None Metrics."""
        return flush(self._corpus_type)


@_dataclass
class Character(Element):
    romaji: str
    katakana: str
    hiragana: str
    category: str
    hiragana_note: _Optional[str]
    katakana_note: _Optional[str]

    @property
    def as_dict(self) -> dict:
        return {'key': self.corpus_key, 'romaji': self.romaji, 'katakana': self.katakana, 'hiragana': self.hiragana}


@_dataclass
class Word(Element):
    english: str
    romaji: str
    kana: str
    kanji: _Optional[str]
    part_of_speech: str
    tags: _Optional[tuple[str]]
    note: _Optional[str]

    @property
    def as_dict(self) -> dict:
        return {'key': self.corpus_key, 'english': self.english, 'romaji': self.romaji,
                'kana': self.kana, 'kanji': self.kanji}


def fetch(corpus_id: CorpusType):

    if corpus_id not in _CACHE.keys():
        records = _LOADER[corpus_id]()
        elements = _ELEMENT_FACTORY[corpus_id](records)
        _CACHE[corpus_id] = elements

    return _CACHE[corpus_id]


def flush(corpus_id: CorpusType) -> None:

    if corpus_id not in _CACHE.keys():
        raise KeyError(f'corpora._factory.flush(): nothing in cache for "{corpus_id.name}"')

    non_none_metrics = [e.metrics for e in _CACHE[corpus_id] if e.metrics]
    if len(non_none_metrics):
        _save_metrics(corpus_id, non_none_metrics)

    return


# ===================================================================================================================
# Private API
# -----------
# ===================================================================================================================

_CACHE: dict[CorpusType, list] = {}
_LOADER = {
    CorpusType.SYLLABARY: _load_syllabary,
    CorpusType.VOCABULARY: _load_vocabulary,
}
_ELEMENT_FACTORY = {
    CorpusType.SYLLABARY: lambda records: _character_factory(records),
    CorpusType.VOCABULARY: lambda records: _word_factory(records),
}


def _character_factory(records: list[tuple[dict, _Optional[dict]]]) -> tuple[Character]:

    elements: list[Character] = []

    for next_element_rec, next_metrics_rec in records:

        new_metrics = Metrics(**next_metrics_rec) if next_metrics_rec else None
        payload = {'corpus_key': len(elements), 'store_key': character_store_key(next_element_rec),
                   'metrics': new_metrics} | next_element_rec
        elements.append(Character(**payload))

    return tuple(elements)


def _word_factory(records: list[tuple[dict, _Optional[dict]]]) -> list[Word]:

    elements: list[Word] = []

    for next_element_rec, next_metrics_rec in records:

        if next_element_rec['tags']:
            if type(next_element_rec['tags']) is not str:
                raise Exception('words.factory(): unexpected type "' +
                                str(type(next_element_rec['tags'])) + '" for tags field')
            next_element_rec['tags'] = tuple(tag.strip() for tag in next_element_rec['tags'].split(';'))

        new_metrics = Metrics(**next_metrics_rec) if next_metrics_rec else None
        payload = {'corpus_key': len(elements), 'store_key': word_store_key(next_element_rec),
                   'metrics': new_metrics} | next_element_rec
        new_element = Word(**payload)
        elements.append(new_element)

    return elements
