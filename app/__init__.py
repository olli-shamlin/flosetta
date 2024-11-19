
from flask import Flask
from flask_bootstrap import Bootstrap5
from config import Config
import inspect
import logging


class FlosettaException(Exception):
    # def __init__(self, msg):
    #
    #     # Get the second frame (frame_info instance actually) on the top of the stack
    #     stack = inspect.stack()
    #     frame_info = stack[1]
    #     mod = inspect.getmodule(frame_info[0])
    #
    #     fnc_name = frame_info[3]
    #     mod_name = mod.__name__
    #     cls_name = ''
    #     if 'self' in frame_info.frame.f_locals.keys():
    #         cls_name = frame_info.frame.f_locals['self'].__class__.__name__
    #
    #     self.message = f'{msg} (raised by {mod_name}.{cls_name}.{fnc_name}())'
    #     super().__init__(self.message)
    pass


app = Flask(__name__)

bootstrap = Bootstrap5(app)
app.config.from_object(Config)

# app.logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('[%(name)s %(levelname)s] %(message)s')
# handler.setFormatter(formatter)
# app.logger.addHandler(handler)

from app import routes
