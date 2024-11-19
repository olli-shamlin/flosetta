
import os


class Config:
    SECRET_KEY = os.environ.get('FLOSETTA_SECRET_KEY') or 'you-will-never-guess'
    TRACE = True if os.environ.get('FLOSETTA_TRACE') else False
    TEST_MODE = True if os.environ.get('FLOSETTA_TEST_MODE') else False
    DATA_DIRECTORY = os.environ.get('FLOSETTA_SECRET_KEY') or '/Users/david/Documents/pycharm-projects/flosetta/data'
