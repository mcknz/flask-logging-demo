from functools import wraps
import logging

class LogDecorator:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug('entering %s; args: %s; kwargs: %s', fn.__name__, args, kwargs)
                result = fn(*args, **kwargs)
                self.logger.debug('exiting %s', fn.__name__)
            except Exception as ex:
                self.logger.error('Exception %s', ex)
                raise ex
            return result
        return wrapper
