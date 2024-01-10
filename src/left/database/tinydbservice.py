from typing import Optional, List, Dict

from tinydb import TinyDB, where
from tinyrecord import transaction

from .documentrecordservice import DocumentRecordService


class TinyDBService(DocumentRecordService):
    def __init__(self, db_file):
        self.db = TinyDB(db_file)

    def create(self, **kwargs) -> str:
        with transaction(self.db) as _tr:
            self.db.insert(kwargs)

    def read(self, keyname: str, offset: Optional[int] = None, limit: Optional[int] = None, **kwargs) -> List[Dict]:
        condition = where(keyname).exists()
        for k, v in kwargs.items():
            condition = condition & (where(k) == v)
        items = self.db.search(condition)
        if offset is not None:
            if limit is not None:
                return items[offset: offset+limit]
            return items[offset:]
        return items

    def update(self, uid, keyname="uid", **kwargs):
        with transaction(self.db) as _tr:
            self.db.update(
                kwargs,
                where(keyname) == uid)

    def destroy(self, uid, keyname="uid"):
        with transaction(self.db) as _tr:
            self.db.remove(where(keyname) == uid)