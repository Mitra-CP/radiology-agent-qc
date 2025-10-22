from typing import Dict, List
from src.common.models import Finding

class DriftAgent:
    def __init__(self):
        self.baselines = {'protocol_adherence_rate': 0.98}
    def assess(self, row: Dict) -> List[Finding]:
        # demo: no stateful drift tracking; placeholder
        return []
