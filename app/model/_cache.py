
from ._entries import Entry
from ._syllabary import load_syllabary
from ._vocabulary import load_vocabulary
from enum import Enum


class CacheItem(Enum):
    VOCABULARY = 'vocab'
    SYLLABARY = 'kana'


_CACHE: dict[CacheItem, dict[str, Entry]] = {}
_LOADERS = {
    CacheItem.SYLLABARY: load_syllabary,
    CacheItem.VOCABULARY: load_vocabulary,
}


def fetch(item: CacheItem):

    if item not in _CACHE.keys():
        _CACHE[item] = _LOADERS[item]()

    return _CACHE[item]
