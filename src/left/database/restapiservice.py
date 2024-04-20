from __future__ import annotations
from typing import Optional, List, Dict
import json

# noinspection PyUnresolvedReferences
from pyodide.http import pyfetch  # bundled automatically when using 'flet build web'

from .documentrecordservice import DocumentRecordService, KeyNotExists


class RESTfulService:
    def __init__(self, api_base: str):
        self.api_base = api_base

    def get_resource(self, table_name=None, key_name="uid") -> RESTfulResource:
        return RESTfulResource(self.api_base, table_name, key_name)

    def __getattr__(self, item):
        return getattr(self.get_resource(), item)


class RESTfulResource(DocumentRecordService):
    def __init__(self, api_base, resource, key_name):
        self.resource = f"{api_base}/{resource}/"
        self.key_name = key_name

    async def create(self, **kwargs) -> str:
        if self.key_name not in kwargs:
            raise KeyNotExists(f"Missing key {self.key_name} in payload {kwargs}")
        response = await pyfetch(
            self.resource,
            body=json.dumps(kwargs),
            method="PUT"
        )
        if response.status not in [200, 201]:
            raise Exception("Resource creation failed")
        return await response.json()

    async def read(self,
                   offset: Optional[int] = None,
                   limit: Optional[int] = None,
                   operator="and", **kwargs) -> List[Dict]:
        url = self.resource
        if self.key_name in kwargs:
            url = f"{self.resource_base}{kwargs[self.key_name]}"
        response = await pyfetch(
            url,
            method="GET"
        )
        if response.status not in [200]:
            raise Exception("Resource read failed")
        items = await response.json()
        if offset is not None:
            if limit is not None:
                return items[offset: offset + limit]
            return items[offset:]
        elif limit is not None:
            return items[:limit]
        return items

    async def update(self, key_value, **kwargs):
        url = f"{self.resource}/{key_value}"
        response = await pyfetch(
            url,
            body=json.dumps(kwargs),
            method="PATCH"
        )
        if response.status not in [200]:
            raise Exception("Resource creation failed")

    async def destroy(self, key_value):
        response = await pyfetch(
            f"{self.resource_base}/{key_value}",
            method="DELETE"
        )
        if response.status not in [200]:
            raise Exception("Resource deletion failed")

    async def bulk_insert(self, docs_to_insert):
        response = await pyfetch(
            self.resource,
            body=json.dumps(docs_to_insert),
            method="PUT"
        )
        if response.status not in [200, 201]:
            raise Exception("Resource bulk insert failed")
        return await response.json()
