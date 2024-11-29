
from config import Config  # importing config instead of app b/c app.__init__.py is not fully loaded before this module


def character_store_key(rec: dict) -> str:
    return rec['romaji'].replace(' ', '')


def word_store_key(element_rec: dict) -> str:
    return element_rec['english'].replace(' ', '') + element_rec['romaji'].replace(' ', '')


_ROOT_DIR = '/Users/david/Documents/pycharm-projects/flosetta/tests/data' \
    if Config.TEST_MODE else '/Users/david/Documents/pycharm-projects/flosetta/app/data'
DATE_SUBSTITUTION_MARKER = '[DATE]'
VOCABULARY_FILE = f"{_ROOT_DIR}/vocabulary.json" if Config.TEST_MODE else Config.VOCAB_FILE
SYLLABARY_FILE = _ROOT_DIR + "/syllabary.json"
VOCABULARY_METRICS_FILE = _ROOT_DIR + f"/vocabulary_metrics_{DATE_SUBSTITUTION_MARKER}.json"
SYLLABARY_METRICS_FILE = _ROOT_DIR + f"/syllabary_metrics_{DATE_SUBSTITUTION_MARKER}.json"
METRICS_RETENTION_LIMIT = 5 if Config.TEST_MODE else 90
