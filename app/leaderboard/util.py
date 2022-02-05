import logging
from functools import wraps
from time import perf_counter

logger = logging.getLogger("django")

#time thing
def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = perf_counter()
        result = f(*args, **kw)
        te = perf_counter()
        logger.info(f'func:{f.__name__} args:[{args}, {kw}] took: {te-ts:2.4f} sec')
        return result
    return wrap
