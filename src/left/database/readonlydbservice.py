"""
Stand-in for TinyDb in situations where the app is to be deployed in read-only mode from a static JSON file
(in tinydb format)
"""

from __future__ import annotations
from typing import List, Dict, Callable
from json import load

from .tinydbservice import TinyDBResource


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


class Resource:
    def __init__(self, data: Dict):
        self.data = data

    def search(self, condition: Condition) -> List:
        return list(filter(lambda o: condition(o), self.data))


class Condition:
    def __init__(self, f: Callable):
        self.f = f

    def __call__(self, resource: Dict) -> bool:
        return self.f(resource)

    def __or__(self, other: Condition) -> Condition:
        def f(resource):
            return self(resource) or other(resource)
        return Condition(f)

    def __and__(self, other: Condition) -> Condition:
        def f(resource):
            return self(resource) and other(resource)
        return Condition(f)


class Where:
    def __init__(self, key):
        self.key = key

    def exists(self) -> Condition:
        def f(resource):
            return self.key in resource
        return Condition(f)

    def test(self, value) -> Condition:
        def f(resource):
            try:
                return resource[self.key] == value
            except KeyError:
                return False
        return Condition(f)


class ReadOnlyJSONDBResource(TinyDBResource):
    def __init__(self, resource, key_name):
        super().__init__(Resource(resource), key_name)
        self._where = Where

    def create(self, **kwargs) -> str:
        raise NotImplementedError("create() not available on a read only db")

    def update(self, key_value, **kwargs):
        raise NotImplementedError("update() not available on a read only db")

    def destroy(self, key_value):
        raise NotImplementedError("destroy() not available on a read only db")

    def bulk_insert(self, docs_to_insert):
        raise NotImplementedError("bulk_insert() not available on a read only db")
