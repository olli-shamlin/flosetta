# This module encapsulates the names and locations (ie, directories) of files accessed by the app.
#
# The app reads/writes various files:
#   - Vocabulary words are stored in a spreadsheet (Apple Numbers file).
#   - Characters from the syllabary are stored in a json file.
#   - Quiz metrics are stored in json files; these are both read and written.
#   - Quiz "questions" are writen to JavaScript files that are also read by the HTML pages running in the browser.
#
# The code needs to access different versions of some of these files when it is running in "test" context than
# when it is running in "dev"/"prod" contexts.  This module defines a set of "constant" variables to define the
# names/locations of these files depending on the runtime context.
#
# Three directory locations are used:
#   1. The location the app will use to read/write files only it needs to know about.
#      These include quiz metric files and the file the contains the syllabary's character definitions
#      This location is defined by _APP_DATA_PATH.
#   2. The location the app will use to read/write generate JavaScript files (used when executing quizzes).
#      This location is defined by _APP_STATIC_PATH and this needs to "point to" the "static" folder found
#      inside the "app" folder.
#   3. The vocabulary spreadsheet.
#      The user "owns" this file; they can place it wherever they want on the file system. They make
#      its location know by defining an environment variable named "FLOSETTA_VOCAB_FILE" whose value
#      is the fully qualified name of their spreadsheet.

from app import app
import os

_APP_INSTALL_PATH = os.path.dirname(app.instance_path)
_APP_DATA_PATH = _APP_INSTALL_PATH + '/app/data'
_APP_TEST_PATH = _APP_INSTALL_PATH + '/tests/data'
_APP_STATIC_PATH = _APP_INSTALL_PATH + '/app/static'

_SPREADSHEET_EXT = 'numbers'
_JSON_EXT = 'json'
_JAVASCRIPT_EXT = 'js'
_VOCABULARY_NAME = 'vocabulary'
_SYLLABARY_NAME = 'syllabary'

VOCABULARY_FILE = app.config['VOCAB_FILE'] if not app.config['TEST_MODE'] \
    else f'{_APP_TEST_PATH}/{_VOCABULARY_NAME}.{_SPREADSHEET_EXT}'

_FLEX_PATH = _APP_TEST_PATH if app.config["TEST_MODE"] else _APP_DATA_PATH

VOCABULARY_METRICS_FILE = f'{_FLEX_PATH}/metrics_{_VOCABULARY_NAME}.{_JSON_EXT}'
SYLLABARY_FILE = f'{_FLEX_PATH}/{_SYLLABARY_NAME}.{_JSON_EXT}'
SYLLABARY_METRICS_FILE = f'{_FLEX_PATH}/metrics_{_SYLLABARY_NAME}.{_JSON_EXT}'

MCQ_ITEMS_FILE = f'{_APP_STATIC_PATH}/mcq_items.{_JAVASCRIPT_EXT}'
