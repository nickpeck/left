from typing import Optional, List, Dict

from tinydb import TinyDB, where
from tinyrecord import transaction

from .documentrecordservice import DocumentRecordService


class TinyDBService(DocumentRecordService):
    def __init__(self, db_file):
        self.db = TinyDB(db_file)

    def create(self, **kwargs) -> str:
        with transaction(self.db):
            self.db.insert(kwargs)

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

    def update(self, uid, keyname="uid", **kwargs):
        with transaction(self.db):
            self.db.update(
                kwargs,
                where(keyname) == uid)

    def destroy(self, uid, keyname="uid"):
        with transaction(self.db):
            self.db.remove(where(keyname) == uid)

    def bulk_insert(self, docs_to_insert):
        with transaction(self.db) as _tr:
            self.db.insert_multiple(docs_to_insert)
