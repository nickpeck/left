from typing import Optional, List, Dict

from tinydb import where
from tinyrecord import transaction

from ..documentrecordservice import DocumentRecordService, KeyNotExists
from ..resourcelock import resource_lock


class TinyDBResource(DocumentRecordService):
    def __init__(self, resource, key_name):
        self.resource = resource
        self.key_name = key_name
        self._where = where

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
        condition = self._where(self.key_name).exists()
        i = 0
        for k, v in kwargs.items():
            if callable(v):
                if operator == "or" and i > 0:
                    condition = condition | (self._where(k).test(v))
                else:
                    condition = condition & (self._where(k).test(v))
                i = i + 1
                continue
            if operator == "or" and i > 0:
                condition = condition | (self._where(k) == v)
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
                self._where(self.key_name) == key_value)

    @resource_lock
    def destroy(self, key_value):
        with transaction(self.resource) as tr:
            tr.remove(self._where(self.key_name) == key_value)

    @resource_lock
    def bulk_insert(self, docs_to_insert):
        with transaction(self.resource):
            self.resource.insert_multiple(docs_to_insert)
