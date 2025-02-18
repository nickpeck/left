from __future__ import annotations
import logging
from typing import Optional, List, Dict
from threading import Lock, get_ident

from tinydb import TinyDB, where, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinyrecord import transaction

from .documentrecordservice import DocumentRecordService, KeyNotExists

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


class TinyDBService:
    def __init__(self, db_file, write_through=True, read_query_cache_size=30):
        """
        :param db_file: name of the file where the JSON data will be stored
        :param write_through: if True (default) each write is written to the cache and saved straight away.
        Reads are always from the cache.
        """
        middleware = CachingMiddleware(JSONStorage)
        if write_through:
            middleware.WRITE_CACHE_SIZE = 1
        self.db = TinyDB(db_file, storage=middleware)
        self.read_query_cache_size = read_query_cache_size

    def get_resource(self, table_name=None, key_name="uid") -> TinyDBResource:
        resource = self.db
        if table_name is not None:
            resource = self.db.table(table_name, cache_size=self.read_query_cache_size)
        return TinyDBResource(resource, key_name)

    def __getattr__(self, item):
        return getattr(self.get_resource(), item)

    @resource_lock
    def flush(self):
        self.db.storage.flush()

    @resource_lock
    def close(self):
        self.db.close()


class TinyDBResource(DocumentRecordService):
    def __init__(self, resource, key_name):
        self.resource = resource
        self.key_name = key_name

    @resource_lock
    def create(self, **kwargs) -> str:
        if self.key_name not in kwargs:
            raise KeyNotExists(f"Missing key {self.key_name} in payload {kwargs}")
        with transaction(self.resource):
            self.resource.insert(kwargs)

    @resource_lock
    def read(self,
             offset: Optional[int] = None,
             limit: Optional[int] = None,
             operator="and", **kwargs) -> List[Dict]:
        condition = where(self.key_name).exists()
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
        items = self.resource.search(condition)
        if offset is not None:
            if limit is not None:
                return items[offset: offset+limit]
            return items[offset:]
        elif limit is not None:
            return items[:limit]
        return items

    @resource_lock
    def update(self, key_value, **kwargs):
        with transaction(self.resource) as tr:
            tr.update(
                kwargs,
                where(self.key_name) == key_value)

    @resource_lock
    def destroy(self, key_value):
        with transaction(self.resource) as tr:
            tr.remove(where(self.key_name) == key_value)

    @resource_lock
    def bulk_insert(self, docs_to_insert):
        with transaction(self.resource):
            self.resource.insert_multiple(docs_to_insert)
