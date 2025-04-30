from __future__ import annotations
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from ..resourcelock import resource_lock
from .tinydbresource import TinyDBResource


class TinyDBService:
    def __init__(self, db_file, write_through_caching=True, read_query_cache_size=30):
        middleware = CachingMiddleware(JSONStorage)
        if write_through_caching:
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

