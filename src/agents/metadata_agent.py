from typing import Dict, List
from src.common.models import Finding

REQUIRED = ['study_uid','series_uid','modality','protocol_name','patient_sex','study_date']

class MetadataAgent:
    def validate(self, row: Dict) -> List[Finding]:
        findings = []
        for k in REQUIRED:
            if row.get(k) in (None, '', 'NaN'):
                findings.append(Finding(
                    study_uid=str(row.get('study_uid','?')), series_uid=row.get('series_uid'),
                    agent='metadata', severity='warn', category='metadata',
                    metric=k, actual='missing', expected='present',
                    explanation=f'Missing required metadata: {k}'
                ))
        # Simple laterality/body part check example
        return findings
