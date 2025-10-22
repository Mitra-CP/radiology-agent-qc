import argparse, os, csv
from src.pipelines.qc_pipeline import QCPipeline
from src.pipelines.ingest_simulator import read_sample_events
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rules', default='configs/rules.yaml')
    ap.add_argument('--metadata', default='data/sample/metadata_sample.csv')
    ap.add_argument('--use-sample', action='store_true')
    ap.add_argument('--out', default='outputs')
    args = ap.parse_args()

    p = QCPipeline(args.rules)

    # Read sample metadata; in real use, join with DICOM‑extracted tags
    rows = []
    with open(args.metadata, 'r', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)

    # Process each row (as if arriving from an event stream)
    for r in rows:
        p.process_row(r)

    p.write_outputs(args.out)
    print(f'Wrote findings to {os.path.join(args.out, "findings.csv")}')
    print(f'Total findings: {len(p.findings)}')

if __name__ == "__main__":
    main()
