from typing import Dict, List
from src.common.models import Finding

class ProtocolAgent:
    def __init__(self, rules: Dict):
        self.rules = rules.get('protocols', {})
    def check(self, row: Dict) -> List[Finding]:
        findings = []
        proto = row.get('protocol_name')
        if proto in self.rules:
            exp = self.rules[proto]['expected']
            # slice thickness
            st = row.get('slice_thickness_mm')
            if st and isinstance(st, (int,float)):
                lo, hi = exp.get('slice_thickness_mm', [None, None])
                if lo is not None and hi is not None and not (lo <= float(st) <= hi):
                    findings.append(Finding(
                        study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                        agent='protocol', severity='high', category='protocol',
                        metric='slice_thickness_mm', actual=st, expected=f'{lo}-{hi}',
                        explanation=f'Slice thickness out of expected range for {proto}'
                    ))
            # contrast required
            if exp.get('contrast_required') is True:
                if str(row.get('contrast_bolus','')).lower() not in ('yes','true','1'):
                    findings.append(Finding(
                        study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                        agent='protocol', severity='high', category='protocol',
                        metric='contrast_bolus', actual=row.get('contrast_bolus'),
                        expected='Yes', explanation=f'Contrast required for {proto}'
                    ))
        else:
            # unknown protocol
            findings.append(Finding(
                study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                agent='protocol', severity='warn', category='protocol',
                metric='protocol_name', actual=proto, expected='in catalog',
                explanation='Protocol not in site catalog'
            ))
        return findings
