import logging
from threading import Lock, get_ident

LOCK = Lock()
LOCK_TIMEOUT = 1


def resource_lock(f):
    def call(*args, **kwargs):
        logging.getLogger().debug(
            f"thread {get_ident()} waiting to acquire lock to run {f.__name__} with ({args} {kwargs})")
        LOCK.acquire(timeout=LOCK_TIMEOUT)
        logging.getLogger().debug(f"thread {get_ident()} has acquired lock")
        result = None
        ex = None
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            ex = e
            logging.getLogger().error(e)
        finally:
            LOCK.release()
            logging.getLogger().debug(f"thread {get_ident()} released lock")
        if ex:
            raise ex
        return result
    return call
