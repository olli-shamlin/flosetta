
from app import app
from app import FlosettaException
from app.flogger import flogger
from app.flogger import tracer
from ._entries import Entry
from ._entries import Word
from ._entries import Character
from ._quiz_metrics import deserialize as deserialize_metrics
from ._workbook import import_spreadsheet
from app.data_paths import SYLLABARY_FILE
from app.data_paths import SYLLABARY_METRICS_FILE
from app.data_paths import VOCABULARY_FILE
from app.data_paths import VOCABULARY_METRICS_FILE
from enum import Enum
import json
import os


@tracer
def load_metrics_file(filename: str) -> dict[str, object]:

    metrics_dict_out = {}

    # Read the vocabulary metrics file if it exists
    if os.path.exists(filename):
        with open(filename, 'r') as fh:
            metrics_dict_in = json.load(fh)

        # A metrics file did exist, so we create a dict character key/QuizMetric objects
        # that will be merged into the syllabary data we store in dict_out below
        for key, metrics_dict in metrics_dict_in.items():
            metrics_dict_out[key] = deserialize_metrics(metrics_dict)

    flogger.debug(f'metrics file loaded: {filename}')
    return metrics_dict_out


@tracer
def load_vocabulary() -> dict[str, Word]:

    metrics = load_metrics_file(VOCABULARY_METRICS_FILE)

    # Read the vocabulary file
    if not os.path.exists(VOCABULARY_FILE):
        raise FlosettaException(f'syllabary source file does not exist: {VOCABULARY_FILE}')
    workbook = import_spreadsheet(VOCABULARY_FILE)

    vocab: dict[str, Word] = {}

    for sheet in workbook.sheets:
        for table in sheet.tables:
            for row in table.rows:
                kana = row[2]
                vocab[kana] = Word(english=row[0], romaji=row[1], kana=kana, kanji=row[3],
                                   part_of_speech=row[4], tags=row[5], note=row[6],
                                   metrics=metrics[kana] if kana in metrics.keys() else None)

    flogger.debug('vocabulary spreadsheet loaded')
    return vocab


@tracer
def load_syllabary() -> dict[str, Character]:

    metrics = load_metrics_file(SYLLABARY_METRICS_FILE)

    # Read the syllabary file
    if not os.path.exists(SYLLABARY_FILE):
        raise FlosettaException(f'syllabary source file does not exist: {SYLLABARY_FILE}')
    with open(SYLLABARY_FILE, 'r') as fh:
        dict_in = json.load(fh)

    dict_out: dict[str, Character] = {
        k: Character(v['romaji'], v['hiragana'], v['katakana'], v['category'],
                     v['hiragana_note'], v['katakana_note'],
                     metrics=metrics[k] if k in metrics.keys() else None)
        for k, v in dict_in.items()
    }

    flogger.debug('vocabulary spreadsheet loaded')
    return dict_out


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
        flogger.debug(f'cache hit: {item.name}')

    return CACHE[item]


class _FrozenDict(dict):

    def __init__(self, other=None, **kwargs):
        super().__init__()
        self.update(other, **kwargs)
        return

    def __setitem__(self, key, value):
        if key in self:
            raise FlosettaException(f'key "{key}" already exists in FrozenDict instance and cannot be modified')
        super().__setitem__(key, value)

    @tracer
    def save(self, out_filename: str) -> None:

        out_dict = {p.key: p.metrics.serialized for p in self.values() if p.metrics.is_non_zero}

        if len(out_dict):
            out_json = json.dumps(out_dict, indent=3)
            with open(out_filename, 'w') as fh:
                fh.write(out_json)

        flogger.debug(f'file saved: {out_filename}')
        return


class Vocabulary(_FrozenDict):

    def __init__(self):
        vocab = fetch(CacheItem.VOCABULARY)
        super().__init__(other=vocab)
        flogger.debug('vocabulary instance initialized')

    @tracer
    def save(self) -> None:
        super().save(VOCAB_METRICS_FILE)


class Syllabary(_FrozenDict):

    def __init__(self):
        kana = fetch(CacheItem.SYLLABARY)
        super().__init__(other=kana)
        flogger.debug('syllabary instance initialized')

    @tracer
    def save(self) -> None:
        super().save(KANA_METRICS_FILE)


def purge_cache() -> None:

    if not app.config['TEST_MODE']:
        raise FlosettaException('cache can only be purged when running in TEST_MODE')

    for k, v in CACHE.items():
        del v
        flogger.debug(f'{k.value} cache item deleted')

    CACHE.clear()
    flogger.debug('cache purged')

    return
