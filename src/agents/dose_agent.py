from typing import Dict, List
from src.common.models import Finding

class DoseAgent:
    def __init__(self, thresholds: Dict):
        self.t = thresholds.get('dose', {})
    def check(self, row: Dict) -> List[Finding]:
        # demo: no real dose values in sample CSV; pretend CT studies have synthetic dose
        findings = []
        if row.get('modality') == 'CT':
            # fake values for demo
            ctdi = 22.5 if row['study_uid']=='1' else 10.0
            if 'ctdi_vol_max_mgy' in self.t and ctdi > float(self.t['ctdi_vol_max_mgy']):
                findings.append(Finding(
                    study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                    agent='dose', severity='high', category='dose',
                    metric='CTDIvol', actual=ctdi, expected=f'≤ {self.t["ctdi_vol_max_mgy"]} mGy',
                    explanation='CT dose index above site threshold'
                ))
        return findings
