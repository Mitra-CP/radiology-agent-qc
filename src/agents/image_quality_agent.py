from typing import Dict, List
import numpy as np
from src.common.models import Finding
from src.common.metrics import entropy_focus_criterion, fber

class ImageQualityAgent:
    def __init__(self, thresholds: Dict):
        self.t = thresholds.get('image_quality', {})
    def evaluate(self, row: Dict) -> List[Finding]:
        # This demo computes metrics on synthetic arrays (no pixels in CSV). Replace with real pixel reads.
        rng = np.random.RandomState(abs(hash(row['study_uid'])) % (2**32))
        img = rng.rand(128,128)
        bg = rng.rand(128,128)*0.1
        efc = entropy_focus_criterion(img)
        fber_v = fber(img, bg)
        findings = []
        if 'efc_max' in self.t and efc > float(self.t['efc_max']):
            findings.append(Finding(
                study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                agent='image_quality', severity='warn', category='image_quality',
                metric='EFC', actual=round(efc,4), expected=f'≤ {self.t["efc_max"]}',
                explanation='High motion/blur likelihood by EFC proxy'
            ))
        if 'fber_min' in self.t and fber_v < float(self.t['fber_min']):
            findings.append(Finding(
                study_uid=str(row['study_uid']), series_uid=row.get('series_uid'),
                agent='image_quality', severity='warn', category='image_quality',
                metric='FBER', actual=round(fber_v,4), expected=f'≥ {self.t["fber_min"]}',
                explanation='Low foreground energy vs background'
            ))
        return findings
