from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Finding:
    study_uid: str
    series_uid: Optional[str]
    agent: str
    severity: str  # info|warn|high|critical
    category: str  # protocol|dose|image_quality|metadata|drift|governance
    metric: str
    actual: Any
    expected: Any
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
