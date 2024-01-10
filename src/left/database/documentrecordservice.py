from typing import Optional, List, Dict


class DocumentRecordService:

    def create(self, **kwargs) -> str:
        raise NotImplementedError()

    def read(self, offset: Optional[int] = None, limit: Optional[int] = None, **kwargs) -> List[Dict]:
        raise NotImplementedError()

    def update(self, uid, **kwargs):
        raise NotImplementedError()

    def destroy(self, uid):
        raise NotImplementedError()
