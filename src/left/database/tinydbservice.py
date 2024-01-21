import logging
from typing import Optional, List, Dict
from threading import Lock, get_ident

from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinyrecord import transaction

from .documentrecordservice import DocumentRecordService

LOCK = Lock()
LOCK_TIMEOUT = -1


def resource_lock(f):
    def call(*args, **kwargs):
        logging.getLogger().debug(
            f"thread {get_ident()} waiting to acquire lock to run {f.__name__} with ({args} {kwargs})")
        LOCK.acquire(timeout=LOCK_TIMEOUT)
        logging.getLogger().debug(f"thread {get_ident()} has acquired lock")
        result = f(*args, **kwargs)
        LOCK.release()
        logging.getLogger().debug(
            f"thread {get_ident()} released lock")
        return result
    return call


class TinyDBService(DocumentRecordService):
    def __init__(self, db_file):
        self.db = TinyDB(db_file, storage=CachingMiddleware(JSONStorage))

    @resource_lock
    def create(self, **kwargs) -> str:
        with transaction(self.db):
            self.db.insert(kwargs)

    @resource_lock
    def read(self, keyname: str,
             offset: Optional[int] = None,
             limit: Optional[int] = None,
             operator="and", **kwargs) -> List[Dict]:
        condition = where(keyname).exists()
        i = 0
        for k, v in kwargs.items():
            if callable(v):
                if operator == "or" and i > 0:
                    condition = condition | (where(k).test(v))
                else:
                    condition = condition & (where(k).test(v))
                i = i + 1
                continue
            if operator == "or" and i > 0:
                condition = condition | (where(k) == v)
            else:
                condition = condition & (where(k) == v)
            i = i + 1
        items = self.db.search(condition)
        if offset is not None:
            if limit is not None:
                return items[offset: offset+limit]
            return items[offset:]
        elif limit is not None:
            return items[:limit]
        return items

    @resource_lock
    def update(self, uid, keyname="uid", **kwargs):
        with transaction(self.db) as tr:
            tr.update(
                kwargs,
                where(keyname) == uid)

    @resource_lock
    def destroy(self, uid, keyname="uid"):
        with transaction(self.db) as tr:
            tr.remove(where(keyname) == uid)

    @resource_lock
    def bulk_insert(self, docs_to_insert):
        with transaction(self.db):
            self.db.insert_multiple(docs_to_insert)

    @resource_lock
    def flush(self):
        self.db.storage.flush()

    @resource_lock
    def close(self):
        self.db.close()
