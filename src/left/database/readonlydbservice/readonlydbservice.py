from __future__ import annotations
from json import load

from .readonlydbresource import ReadOnlyJSONDBResource


class ReadOnlyJSONDBService:
    def __init__(self, db_file):
        try:
            self._data = load(db_file)
        except (TypeError, AttributeError):
            self._data = load(open(db_file))

    def get_resource(self, table_name=None, key_name="uid") -> ReadOnlyJSONDBResource:
        resource = self._data
        if table_name is not None:
            resource = self._data[table_name].values()
        return ReadOnlyJSONDBResource(resource, key_name)

    def __getattr__(self, item):
        return getattr(self.get_resource(), item)

    def flush(self):
        raise NotImplementedError("flush() not available on a read only db")

    def close(self):
        pass
