from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Page:
    number: int
    text: str

@dataclass
class Document:
    filename: str
    metadata: Dict
    pages: List[Page] = field(default_factory=list)

    def full_text(self) -> str:
        return "\n".join(page.text for page in self.pages)
