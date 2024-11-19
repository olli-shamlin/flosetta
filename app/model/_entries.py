
from ._quiz_metrics import QuizMetrics
from abc import ABC
from abc import abstractmethod
from typing import Optional


class Entry(ABC):

    def __init__(self):
        self._metrics: Optional[QuizMetrics] = None

    @property
    @abstractmethod
    def key(self) -> str:
        ...

    @property
    def metrics(self) -> QuizMetrics:
        return self._metrics


class Character(Entry):

    def __init__(self, romaji: str, hiragana: str, katakana: str, category: str,
                 hiragana_note: Optional[str], katakana_note: Optional[str], metrics: Optional[QuizMetrics] = None):
        super().__init__()
        self._romaji: str = romaji
        self._hiragana: str = hiragana
        self._katakana: str = katakana
        self._category: str = category
        self._hiragana_note: Optional[str] = hiragana_note
        self._katakana_note: Optional[str] = katakana_note
        self._quiz_metrics: Optional[QuizMetrics] = metrics

    @property
    def key(self) -> str:
        return self._romaji

    @property
    def romaji(self) -> str:
        return self._romaji

    @property
    def hiragana(self) -> str:
        return self._hiragana

    @property
    def katakana(self) -> str:
        return self._katakana

    @property
    def category(self) -> str:
        return self._category

    @property
    def hiragana_note(self) -> Optional[str]:
        return self._hiragana_note

    @property
    def katakana_note(self) -> Optional[str]:
        return self._katakana_note

    @property
    def metrics(self) -> QuizMetrics:
        if self._quiz_metrics is None:
            self._quiz_metrics = QuizMetrics()
        return self._quiz_metrics


class Word(Entry):

    def __init__(self, english: str, romaji: str, kana: str, kanji: str,
                 part_of_speech: str, tags: Optional[str], note: Optional[str], metrics: Optional[QuizMetrics] = None):
        super().__init__()
        self._english: str = english
        self._romaji: str = romaji
        self._kana: str = kana
        self._kanji: str = kanji
        self._part_of_speech: str = part_of_speech
        self._tags: Optional[list[str]] = [t.strip() for t in tags.split(';')] if tags else None
        self._note: Optional[str] = note
        self._quiz_metrics: Optional[QuizMetrics] = metrics

    @property
    def key(self) -> str:
        return self._kana

    @property
    def english(self) -> str:
        return self._english

    @property
    def romaji(self) -> str:
        return self._romaji

    @property
    def kana(self) -> str:
        return self._kana

    @property
    def kanji(self) -> str:
        return self._kanji

    @property
    def part_of_speech(self) -> str:
        return self._part_of_speech

    @property
    def tags(self) -> Optional[list[str]]:
        return self._tags

    @property
    def note(self) -> Optional[str]:
        return self._note

    @property
    def metrics(self) -> QuizMetrics:
        if self._quiz_metrics is None:
            self._quiz_metrics = QuizMetrics()
        return self._quiz_metrics
