
from app import FlosettaException
from app.flogger import flogger
from app.flogger import tracer
from ._entries import Entry
from ._entries import Word
from ._entries import Character
from ._workbook import import_spreadsheet
from ._data_paths import KANA_FILE
from ._data_paths import VOCAB_FILE
from enum import Enum


@tracer
def load_vocabulary() -> dict[str, Word]:

    workbook = import_spreadsheet(VOCAB_FILE)
    vocab: dict[str, Word] = {}

    for sheet in workbook.sheets:
        for table in sheet.tables:
            for row in table.rows:
                kana = row[2]
                vocab[kana] = Word(english=row[0], romaji=row[1], kana=kana, kanji=row[3],
                                   part_of_speech=row[4], tags=row[5], note=row[6])

    flogger.debug('vocabulary spreadsheet loaded')

    return vocab


@tracer
def load_syllabary() -> dict[str, Character]:

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

    dict_inst: dict[str, Character] = \
        {k.lower(): Character(v['romaji'], v['hiragana'], v['katakana'], v['category'],
                              v['hiragana_note'], v['katakana_note']) for k, v in kana.items()}

    flogger.debug('kana spreadsheet loaded')

    return dict_inst


class CacheItem(Enum):
    VOCABULARY = 'vocab'
    SYLLABARY = 'kana'


CACHE: dict[CacheItem, dict[str, Entry]] = {}
LOADERS = {
    CacheItem.SYLLABARY: load_syllabary,
    CacheItem.VOCABULARY: load_vocabulary,
}


@tracer
def fetch(item: CacheItem):

    if item not in CACHE.keys():
        CACHE[item] = LOADERS[item]()
    else:
        flogger.debug('cache hit!')

    return CACHE[item]


class _FrozenDict(dict):

    def __init__(self, other=None, **kwargs):
        super().__init__()
        self.update(other, **kwargs)

    def __setitem__(self, key, value):
        if key in self:
            raise FlosettaException(f'key "{key}" already exists in FrozenDict instance and cannot be modified')
        super().__setitem__(key, value)


class Vocabulary(_FrozenDict):

    def __init__(self):
        vocab = fetch(CacheItem.VOCABULARY)
        super().__init__(other=vocab)

    @tracer
    def save(self) -> None:
        pass


class Syllabary(_FrozenDict):

    def __init__(self):
        kana = fetch(CacheItem.SYLLABARY)
        super().__init__(other=kana)

    @tracer
    def save(self) -> None:
        pass

