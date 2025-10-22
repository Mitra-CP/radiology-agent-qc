import csv
from typing import Dict, Iterator

def read_sample_events(path: str) -> Iterator[Dict]:
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
