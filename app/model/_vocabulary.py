#
# from app import FlosettaException
# from ._quiz_metrics import QuizMetrics
# from ._workbook import import_spreadsheet
# from ._data_paths import VOCAB_FILE
# from collections import UserDict
# from typing import Optional
#
#
# class Word:
#
#     def __init__(self, english: str, romaji: str, kana: str, kanji: str,
#                  part_of_speech: str, tags: Optional[str], note: Optional[str]):
#         self._english: str = english
#         self._romaji: str = romaji
#         self._kana: str = kana
#         self._kanji: str = kanji
#         self._part_of_speech: str = part_of_speech
#         self._tags: Optional[list[str]] = [t.strip() for t in tags.split(';')] if tags else None
#         self._note: Optional[str] = note
#         self._quiz_metrics: Optional[QuizMetrics] = None
#
#     # TODO: I think there is motivation to create an ABC for words/characters; the "key" property is an
#     # TODO: example of a method that both Word & Kana classes need to implement; they both also need to
#     # TODO: have the same implementations of _quiz_metrics.
#     @property
#     def key(self) -> str:
#         return self._romaji
#
#     @property
#     def english(self) -> str:
#         return self._english
#
#     @property
#     def romaji(self) -> str:
#         return self._romaji
#
#     @property
#     def kana(self) -> str:
#         return self._kana
#
#     @property
#     def kanji(self) -> str:
#         return self._kanji
#
#     @property
#     def part_of_speech(self) -> str:
#         return self._part_of_speech
#
#     @property
#     def tags(self) -> Optional[list[str]]:
#         return self._tags
#
#     @property
#     def note(self) -> Optional[str]:
#         return self._note
#
#     @property
#     def metrics(self) -> Optional[QuizMetrics]:
#         return self._quiz_metrics
#
#
# class Vocabulary(UserDict):
#
#     _words: Optional[dict[str, Word]] = None
#
#     def __init__(self):
#
#         if Vocabulary._words is None:
#             dict_inst = _load_vocabulary()
#             super().__init__(dict_inst)
#             Vocabulary._words = dict_inst
#             self.data = Vocabulary._words
#         else:
#             super().__init__(Vocabulary._words)
#
#         return
#
#     def __setitem__(self, key, value):
#         if Vocabulary._words is None:
#             super().__setitem__(key, value)
#             return
#         else:
#             raise FlosettaException('modifying vocabulary is not allowed')
#
#

from ._entries import Word
from ._data_paths import VOCAB_FILE
from ._workbook import import_spreadsheet


def load_vocabulary() -> dict[str, Word]:

    workbook = import_spreadsheet(VOCAB_FILE)
    vocab: dict[str, Word] = {}

    for sheet in workbook.sheets:
        for table in sheet.tables:
            for row in table.rows:
                kana = row[2]
                vocab[kana] = Word(english=row[0], romaji=row[1], kana=kana, kanji=row[3],
                                   part_of_speech=row[4], tags=row[5], note=row[6])

        return vocab
