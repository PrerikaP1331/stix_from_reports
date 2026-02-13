from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class IOC:
    type: str
    value: str
    context: Optional[str] = None
    source: Optional[str] = None
    enrichment: Dict = field(default_factory=dict)
    confidence: Optional[int] = None
