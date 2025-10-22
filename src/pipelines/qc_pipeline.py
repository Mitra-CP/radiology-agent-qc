import csv, os, json
from typing import List, Dict, Any
from fastapi import FastAPI
from src.common.rules import load_rules
from src.agents.protocol_agent import ProtocolAgent
from src.agents.image_quality_agent import ImageQualityAgent
from src.agents.dose_agent import DoseAgent
from src.agents.metadata_agent import MetadataAgent
from src.agents.drift_agent import DriftAgent
from src.agents.governance_agent import GovernanceAgent
from src.common.models import Finding

app = FastAPI(title="Radiology Agent QC")

class QCPipeline:
    def __init__(self, rules_path: str):
        self.rules = load_rules(rules_path)
        self.protocol = ProtocolAgent(self.rules)
        self.iq = ImageQualityAgent(self.rules.get('thresholds', {}))
        self.dose = DoseAgent(self.rules.get('thresholds', {}))
        self.meta = MetadataAgent()
        self.drift = DriftAgent()
        self.gov = GovernanceAgent()
        self.findings: List[Dict[str, Any]] = []

    def process_row(self, row: Dict[str, Any]):
        # Normalize types
        if 'slice_thickness_mm' in row and row['slice_thickness_mm']:
            try:
                row['slice_thickness_mm'] = float(row['slice_thickness_mm'])
            except:
                pass
        agents = [
            self.protocol.check(row),
            self.iq.evaluate(row),
            self.dose.check(row),
            self.meta.validate(row),
            self.drift.assess(row),
            self.gov.check(row),
        ]
        for flist in agents:
            for f in flist:
                self.findings.append(f.to_dict())

    def write_outputs(self, out_dir: str = "outputs"):
        os.makedirs(out_dir, exist_ok=True)
        # CSV
        if self.findings:
            fieldnames = list(self.findings[0].keys())
            with open(os.path.join(out_dir, "findings.csv"), "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(self.findings)
        # JSONL audit
        with open(os.path.join(out_dir, "audit.jsonl"), "w", encoding="utf-8") as f:
            for rec in self.findings:
                f.write(json.dumps(rec) + "\n")

pipeline = None

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/findings")
def get_findings():
    global pipeline
    return {"count": 0 if pipeline is None else len(pipeline.findings),
            "data": [] if pipeline is None else pipeline.findings}

@app.get("/stats")
def stats():
    global pipeline
    if pipeline is None:
        return {}
    # Simple stats by category
    by_cat = {}
    for f in pipeline.findings:
        by_cat[f['category']] = by_cat.get(f['category'], 0) + 1
    return {"by_category": by_cat}
