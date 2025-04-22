from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class KeyNotExists(Exception):
    pass


class DocumentRecordService(ABC):

    @abstractmethod
    def create(self, **kwargs) -> str:
        raise NotImplementedError()

    @abstractmethod
    def read(self, offset: Optional[int] = None, limit: Optional[int] = None, **kwargs) -> List[Dict]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, uid, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def destroy(self, uid):
        raise NotImplementedError()

    @abstractmethod
    def bulk_insert(self, docs_to_insert: List[Dict]):
        raise NotImplementedError()
