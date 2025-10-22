from typing import Dict, List
from src.common.models import Finding

class GovernanceAgent:
    def check(self, row: Dict) -> List[Finding]:
        findings = []
        # Simple governance example: flag unknown protocols for review
        if not row.get('protocol_name'):
            findings.append(Finding(
                study_uid=str(row.get('study_uid','?')), series_uid=row.get('series_uid'),
                agent='governance', severity='info', category='governance',
                metric='protocol_name', actual='missing', expected='non-empty',
                explanation='Protocol name missing - review taxonomy / scanner config'
            ))
        return findings
