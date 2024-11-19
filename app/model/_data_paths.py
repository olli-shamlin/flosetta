
from app import app


_DATA_PATH = app.config['DATA_DIRECTORY']
_SPREADSHEET_EXT = 'numbers'
_JSON_EXT = 'json'
_VOCAB_NAME = 'vocabulary'
_KANA_NAME = 'syllabary'
_TEST_PREFIX = 'test_' if app.config['TEST_MODE'] else ''
VOCAB_FILE = f'{_DATA_PATH}/{_TEST_PREFIX}{_VOCAB_NAME}.{_SPREADSHEET_EXT}'
KANA_FILE = f'{_DATA_PATH}/{_TEST_PREFIX}{_KANA_NAME}.{_JSON_EXT}'
VOCAB_METRICS_FILE = f'{_DATA_PATH}/{_TEST_PREFIX}{_VOCAB_NAME}_metrics.{_JSON_EXT}'
KANA_METRICS_FILE = f'{_DATA_PATH}/{_TEST_PREFIX}{_KANA_NAME}_metrics.{_JSON_EXT}'
