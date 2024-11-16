
import os


class Config:
    SECRET_KEY = os.environ.get('FLOSETTA_SECRET_KEY') or 'you-will-never-guess'
    TRACE = os.environ.get('FLOSETTA_TRACE') or True
