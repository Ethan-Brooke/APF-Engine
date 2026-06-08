#!/usr/bin/env python3
from pathlib import Path
import csv, sys, re
ROOT = Path(__file__).resolve().parents[1]
tex = (ROOT/'paper'/'TRACE_TO_SCHEME_EXPORT_MANUSCRIPT_INTEGRATION_v69.tex').read_text()
reg = list(csv.DictReader((ROOT/'registry'/'manuscript_integration_registry_v69.csv').open()))
checks = []
def check(name, cond):
    checks.append((name, bool(cond)))
check('pass_stamp', 'TRACE_TO_SCHEME_MANUSCRIPT_INTEGRATION_PASS' in tex)
check('no_physical_final_assignment', 'not assigned' in tex and '[P_{\\rm physical\\ final}]' in tex)
check('active_top_v67_value', '172.716805649486' in tex)
check('historical_top_v63_absent_as_active', '172.564754410708' in tex and 'historical witness' in tex)
check('pole_branch_blocked', '174.016604383647' in tex and 'blocked' in tex)
check('claim_ladder_present', '[P_{\\rm trace}]' in tex and '[P_{\\rm codomain\\ completion}]' in tex)
check('gates_or_route_formula_present', 'codomain' in tex and 'transport' in tex and 'covariance' in tex and 'no-smuggling' in tex)
check('all_sectors_registry', len(reg)==6)
sectors = {r['sector'] for r in reg}
check('sector_W', 'W/EW' in sectors)
check('sector_charged_leptons', 'charged_leptons' in sectors)
check('sector_charm', 'charm' in sectors)
check('sector_bottom', 'bottom' in sectors)
check('sector_top', 'top' in sectors)
check('sector_light_quarks', 'light_quarks' in sectors)
check('top_registry_current_value', any(r['sector']=='top' and '172.716805649486' in r['active_value'] for r in reg))
check('light_quark_boundary', any(r['sector']=='light_quarks' and 'chiral/lattice' in r['boundary'] for r in reg))
check('charged_qed_boundary', any(r['sector']=='charged_leptons' and 'QED' in r['boundary'] for r in reg))
check('no_smuggling_rules', 'No inverse solving' in tex and 'No identity transport' in tex and 'No use of QED/QCD running' in tex)
check('manuscript_structure', 'Recommended manuscript structure' in tex and 'Top codomain lesson' in tex)
failed = [n for n,c in checks if not c]
print(f'TRACE_TO_SCHEME_MANUSCRIPT_INTEGRATION_{"PASS" if not failed else "FAIL"}')
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:')
    for n in failed: print(' -', n)
    sys.exit(1)
