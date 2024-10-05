"""
Stand-in for TinyDb in situations where the app is to be deployed in read-only mode from a static JSON file
(in tinydb format)
"""

from __future__ import annotations
from typing import Optional, List, Dict, Callable
from json import load

from .documentrecordservice import DocumentRecordService


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


class ReadOnlyJSONDBResource(DocumentRecordService):
    def __init__(self, resource, key_name):
        self.resource = Resource(resource)
        self.key_name = key_name

    def create(self, **kwargs) -> str:
        raise NotImplementedError("create() not available on a read only db")

    def read(self,
             offset: Optional[int] = None,
             limit: Optional[int] = None,
             operator="and", **kwargs) -> List[Dict]:

        condition = Where(self.key_name).exists()
        i = 0
        for k, v in kwargs.items():
            if callable(v):
                if operator == "or" and i > 0:
                    condition = condition | (Where(k).test(v))
                else:
                    condition = condition & (Where(k).test(v))
                i = i + 1
                continue
            if operator == "or" and i > 0:
                condition = condition | Where(k).test(v)
            else:
                condition = condition & Where(k).test(v)
            i = i + 1
        items = self.resource.search(condition)
        if offset is not None:
            if limit is not None:
                return items[offset: offset+limit]
            return items[offset:]
        elif limit is not None:
            return items[:limit]
        return items

    def update(self, key_value, **kwargs):
        raise NotImplementedError("update() not available on a read only db")

    def destroy(self, key_value):
        raise NotImplementedError("destroy() not available on a read only db")

    def bulk_insert(self, docs_to_insert):
        raise NotImplementedError("bulk_insert() not available on a read only db")
