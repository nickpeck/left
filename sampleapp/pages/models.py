from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Optional
from slugify import slugify

from left.model import LeftModel


@dataclass_json
@dataclass
class Page(LeftModel):
    __pk__ = "page_id"
    title: str = ""
    text: str = ""
    keywords: List[str] = field(default_factory=lambda: [])
    page_id: Optional[str] = None

    @property
    def title_slug(self):
        if self.title is None:
            return ""
        return slugify(self.title)

    @property
    def short_text(self):
        if len(self.text) > 20:
            return self.text[:20] + "..."
        return self.text
