#!/usr/bin/env python3
import csv, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
data = json.loads((root/'reports'/'fermion_sector_master_closure_v33_data.json').read_text())
checks = list(csv.DictReader(open(root/'tables'/'fermion_master_checks_v33.csv')))
assert data['status'] == 'FERMION_SECTOR_MASTER_CLOSURE_PASS'
assert data['checks_passed'] == data['checks_total']
assert len(data['sector_rows']) == 5
assert data['export_candidates'] == ['m_b_APF_to_MSbar(m_b)']
assert all(c['passed'] == 'True' for c in checks)
print('FERMION_SECTOR_MASTER_CLOSURE_PASS')
print(f"{data['checks_passed']}/{data['checks_total']} PASS")
