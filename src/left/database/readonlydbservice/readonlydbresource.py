from left.database import TinyDBResource
from .readonlyquerytools import SearchableData, Where


class ReadOnlyJSONDBResource(TinyDBResource):
    def __init__(self, resource, key_name):
        super().__init__(SearchableData(resource), key_name)
        self._where = Where

    def create(self, **kwargs) -> str:
        raise NotImplementedError("create() not available on a read only db")

    def update(self, key_value, **kwargs):
        raise NotImplementedError("update() not available on a read only db")

    def destroy(self, key_value):
        raise NotImplementedError("destroy() not available on a read only db")

    def bulk_insert(self, docs_to_insert):
        raise NotImplementedError("bulk_insert() not available on a read only db")
