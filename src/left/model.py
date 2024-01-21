from __future__ import annotations
from functools import cache
from typing import List, Optional
from uuid import uuid4

from .app import LeftApp


class LeftModel:
    """Simple, database agnostic baseclass for CRUD models. Loosely applicable to most document databases."""
    __pk__ = "id"  # use this to override the name of the primary index key

    @classmethod
    @cache
    def get_resource_for_cls(cls):
        return LeftApp.get_app().services.get("database").get_resource(table_name=cls.__name__, key_name=cls.__pk__)

    @classmethod
    def _get_db_service(cls):
        return cls.get_resource_for_cls()

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
            self.get_resource_for_cls().create(**self.to_dict())
            return self
        payload = self.to_dict()
        self.get_resource_for_cls().update(key_value=self.key, **payload)
        return self

    @classmethod
    def get(cls, key: str) -> LeftModel:
        """Return the first object with the matching key"""
        key_query = {cls.__pk__: key}
        record = cls.get_resource_for_cls().read(**key_query)[0]
        return cls.from_dict(record)

    @classmethod
    def all(cls) -> List[LeftModel]:
        """Return all records of this type"""
        records = cls.get_resource_for_cls().read()
        return [cls.from_dict(record) for record in records]

    @classmethod
    def get_where(cls, **kwargs) -> List[LeftModel]:
        """Return a list of all records of this type with matching attributes as specified, chained in AND syntax"""
        records = cls.get_resource_for_cls().read(**kwargs)
        return [cls.from_dict(record) for record in records]

    @classmethod
    def search(cls, **kwargs) -> List[LeftModel]:
        """Return a list of all records of this type with matching attributes as specified, chained in OR syntax"""
        records = cls.get_resource_for_cls().read(operator="or", **kwargs)
        return [cls.from_dict(record) for record in records]

    def delete(self):
        """Delete the record with the matching key from the database"""
        self.get_resource_for_cls().destroy(key_value=self.key)
