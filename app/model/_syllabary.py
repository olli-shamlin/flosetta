
from app import FlosettaException
from ._quiz import QuizMetrics
from collections import UserDict
from typing import Optional
from ._workbook import import_spreadsheet
from ._data_paths import KANA_FILE


class Kana:

    def __init__(self, romaji: str, hiragana: str, katakana: str, category: str,
                 hiragana_note: Optional[str], katakana_note: Optional[str]):
        self._romaji: str = romaji
        self._hiragana: str = hiragana
        self._katakana: str = katakana
        self._category: str = category
        self._hiragana_note: Optional[str] = hiragana_note
        self._katakana_note: Optional[str] = katakana_note
        self._quiz_metrics: Optional[QuizMetrics] = None

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
    def metrics(self) -> Optional[QuizMetrics]:
        return self._quiz_metrics


class Syllabary(UserDict):

    _kana: Optional[dict[str, Kana]] = None

    def __init__(self):

        if Syllabary._kana is None:
            dict_inst = _load_syllabary()
            super().__init__(dict_inst)
            Syllabary._kana = dict_inst
            self.data = Syllabary._kana

        return

    def __setitem__(self, key, value):
        if Syllabary._kana is None:
            super().__setitem__(key, value)
            return
        else:
            raise FlosettaException('modifying syllabary is not allowed')


def _load_syllabary() -> dict[str, Kana]:

    workbook = import_spreadsheet(KANA_FILE)

    kana: dict[str, dict] = {}
    map_hiragana = {}
    map_katakana = {}
    for table in workbook.sheets[0].tables:
        for row in table.rows:
            character = {'romaji': row[0], 'hiragana': row[1], 'katakana': row[2], 'category': table.name,
                         'hiragana_note': None, 'katakana_note': None}
            kana[character['romaji']] = character
            map_hiragana[character['hiragana']] = character['romaji']
            map_katakana[character['katakana']] = character['romaji']

    for row in workbook.sheets[1].tables[0].rows:
        kana_character = row[0]
        note = row[1]
        if kana_character in map_hiragana.keys():
            kana[map_hiragana[kana_character]]['hiragana_note'] = note
        if kana_character in map_katakana.keys():
            kana[map_katakana[kana_character]]['katakana_note'] = note

    dict_inst: dict[str, Kana] = \
        {k.lower(): Kana(v['romaji'], v['hiragana'], v['katakana'], v['category'],
                         v['hiragana_note'], v['katakana_note']) for k, v in kana.items()}

    return dict_inst
