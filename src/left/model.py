from __future__ import annotations
from functools import cache
from typing import List, Optional
from uuid import uuid4

from .app import LeftApp


class LeftModel:
    """Simple, database agnostic baseclass for CRUD models. Loosely applicable to most document databases."""
    __pk__ = "id"  # use this to override the name of the primary index key

    @staticmethod
    @cache
    def _get_db_service():
        return LeftApp.get_app().services.get("database")

    @staticmethod
    def create_key():
        """Create a new unique key. Returns an UID, but override if numeric key desired."""
        return str(uuid4())

    @property
    def key(self):
        return getattr(self, self.__pk__)

    @key.setter
    def key(self, v):
        setattr(self, self.__pk__, v)

    def upsert(self):
        """If the key field is None, create a key and insert, otherwise, update and return the updated object"""
        if self.key is None:
            self.key = str(uuid4())
            self._get_db_service().create(**self.to_dict())
            return self
        self._get_db_service().update(self.key, self.__pk__, **self.to_dict())
        return self

    @classmethod
    def get(cls, key: str) -> LeftModel:
        """Return the first object with the matching key"""
        query = {cls.__pk__: key}
        record = cls._get_db_service().read(keyname=cls.__pk__, **query)[0]
        return cls.from_dict(record)

    @classmethod
    def all(cls) -> List[LeftModel]:
        """Return all records of this type"""
        records = cls._get_db_service().read(keyname=cls.__pk__)
        return [cls.from_dict(record) for record in records]

    @classmethod
    def get_where(cls, **kwargs) -> List[LeftModel]:
        """Return a list of all records of this type with matching attributes as specified"""
        records = cls._get_db_service().read(keyname=cls.__pk__, **kwargs)
        return [cls.from_dict(record) for record in records]

    def delete(self):
        """Delete the record with the matching key from the database"""
        self._get_db_service().destroy(self.key, self.__pk__)
