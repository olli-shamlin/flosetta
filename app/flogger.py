
from logging import DEBUG, INFO, WARN, WARNING, ERROR
import inspect

from app import app


class _AppLog:

    @staticmethod
    def trace(msg: str) -> None:
        if app.config['TRACE']:
            app.logger.debug(f'{msg}')

    @staticmethod
    def debug(msg: str) -> None:

        if app.logger.level == DEBUG:
            stack = inspect.stack()
            frame_info = stack[1]
            mod = inspect.getmodule(frame_info[0])

            fnc_name = frame_info[3]
            mod_name = mod.__name__
            cls_name = ''
            if 'self' in frame_info.frame.f_locals.keys():
                cls_name = '.' + frame_info.frame.f_locals['self'].__class__.__name__

            app.logger.debug(f'{mod_name}{cls_name}.{fnc_name}(): {msg}')

    @staticmethod
    def note(msg: str) -> None:

        if app.logger.level in [DEBUG, INFO, WARNING, WARN, ERROR]:

            stack = inspect.stack()
            frame_info = stack[1]
            mod = inspect.getmodule(frame_info[0])

            fnc_name = frame_info[3]
            mod_name = mod.__name__
            cls_name = ''
            if 'self' in frame_info.frame.f_locals.keys():
                cls_name = '.' + frame_info.frame.f_locals['self'].__class__.__name__

            app.logger.info(f'{mod_name}{cls_name}.{fnc_name}(): {msg}')

    @staticmethod
    def error(msg: str) -> None:
        stack = inspect.stack()
        frame_info = stack[1]
        mod = inspect.getmodule(frame_info[0])

        fnc_name = frame_info[3]
        mod_name = mod.__name__
        cls_name = ''
        if 'self' in frame_info.frame.f_locals.keys():
            cls_name = '.' + frame_info.frame.f_locals['self'].__class__.__name__

        app.logger.error(f'{mod_name}{cls_name}.{fnc_name}(): {msg}')


flogger = _AppLog()


def tracer(func):

    def wrapper(*args, **kwargs):

        msg = ''
        if app.config['TRACE']:
            # Get the second frame (frame_info instance actually) on the top of the stack
            stack = inspect.stack()
            frame_info = stack[1]

            # Extract the info we want to include on the trace line from the frame
            fnc_name = func.__name__
            fname_split = func.__globals__['__file__'].split('/')
            filename = fname_split[-1]  # frame_info.filename.split('/')[-1]
            if filename == '__init__.py':
                filename = fname_split[-2] + '/' +  filename

            mod_name = '__main__'
            if __name__ != '__main__':
                mod_name = func.__module__  # inspect.getmodule(frame_info[0]).__name__

            cls_name = ''
            if args:
                mbrs = dict(inspect.getmembers(args[0]))
                if '__class__' in mbrs.keys():
                    cls_name = mbrs['__class__'].__name__ + '.'

            msg = f'{filename}: {mod_name}.{cls_name}{fnc_name}()'

            _AppLog.trace(f'➡️ entering {msg}')

        answer = func(*args, **kwargs)

        if app.config['TRACE']:
            _AppLog.trace(f'⬅️ exiting {msg}')

        return answer

    return wrapper
