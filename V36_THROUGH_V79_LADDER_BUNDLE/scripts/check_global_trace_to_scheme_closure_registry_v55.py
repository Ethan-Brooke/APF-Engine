#!/usr/bin/env python3
import csv, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)
def rows(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
def text(path): return (ROOT/path).read_text(encoding='utf-8')
# files
files=[
 'paper/GLOBAL_TRACE_TO_SCHEME_CLOSURE_REGISTRY_v55.tex',
 'tables/global_trace_to_scheme_closure_registry_v55.csv',
 'tables/claim_ladder_definitions_v55.csv',
 'tables/route_gate_status_v55.csv',
 'tables/next_push_queue_v55.csv',
 'tables/no_overclaim_matrix_v55.csv',
 'tables/registry_summary_counts_v55.csv',
 'tables/trace_to_scheme_case_table_v55.csv',
 'reports/global_trace_to_scheme_closure_registry_v55_data.json',
 'reports/global_trace_to_scheme_closure_registry_summary_v55.md',
 'reports/v55_verifier_chain_summary.txt',
 'README_v55.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
# registry rows
reg=rows('global_trace_to_scheme_closure_registry_v55.csv')
check('six_registry_sectors', len(reg)==6)
by={r['sector']:r for r in reg}
for s in ['EW/W','charged leptons','charm','bottom','top','light quarks']:
    check('sector_registered_'+re.sub('[^A-Za-z0-9]+','_',s), s in by)
# statuses
check('ew_export_candidate', by['EW/W']['highest_closed_status']=='P_export_candidate')
check('charged_pole_boundary', 'P_pole_completion' in by['charged leptons']['highest_closed_status'])
check('charm_export_candidate', 'P_export_candidate_MSBAR' in by['charm']['highest_closed_status'])
check('bottom_export_candidate', 'P_export_candidate_MSBAR' in by['bottom']['highest_closed_status'])
check('top_msr_candidate', 'P_export_candidate_MSR' in by['top']['highest_closed_status'])
check('light_external_chilat_required', 'external_chilat_required' in by['light quarks']['highest_closed_status'])
# no physical final
for r in reg:
    check('no_physical_final_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), 'P_physical_final' not in r['highest_closed_status'])
    check('has_allowed_claim_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['may_claim'])>10)
    check('has_forbidden_claim_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['must_not_claim'])>10)
    check('has_boundary_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['boundary_or_next_gate'])>10)
# claim ladder
lad=rows('claim_ladder_definitions_v55.csv')
lad_status=[r['status'] for r in lad]
expected=['P_trace','P_source','P_route','P_export_candidate','P_pole_completion','P_external_ledger_boundary','P_physical_final']
check('claim_ladder_length', len(lad)==7)
for e in expected: check('claim_ladder_has_'+e, e in lad_status)
check('physical_final_defined_but_unassigned', 'P_physical_final' in lad_status and all('P_physical_final' not in r['highest_closed_status'] for r in reg))
# route gates
gates=rows('route_gate_status_v55.csv')
gd={r['gate']:r for r in gates}
for g in ['G1','G2','G3','G4','G5','G6']:
    check('gate_registered_'+g, g in gd)
check('g5_no_smuggling_global', 'no-smuggling' in gd['G5']['object'])
check('g6_residual_global', 'residual' in gd['G6']['object'])
# next queue
queue=rows('next_push_queue_v55.csv')
check('next_queue_has_v56', any(r['version']=='v56' and 'W_TRACE' in r['theorem_program'] for r in queue))
check('next_queue_has_v57', any(r['version']=='v57' and 'HEAVY_QCD' in r['theorem_program'] for r in queue))
check('v56_highest_priority', next(r for r in queue if r['version']=='v56')['priority']=='highest')
# no overclaim
no=rows('no_overclaim_matrix_v55.csv')
check('no_overclaim_rows', len(no)==6)
for r in no:
    check('no_overclaim_for_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), 'physical-final' in r['forbidden_v55_claim'] or 'physical' in r['forbidden_v55_claim'] or 'final' in r['forbidden_v55_claim'])
# case table continuation
case=rows('trace_to_scheme_case_table_v55.csv')
check('case_table_v55_six_rows', len(case)==6)
check('case_table_has_v55_status', 'v55_registry_status' in case[0])
# text content
tex=text(Path('paper/GLOBAL_TRACE_TO_SCHEME_CLOSURE_REGISTRY_v55.tex'))
for phrase in ['Global Trace-to-Scheme Closure Registry','No sector is registered as','APF_W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE','forbids']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
# data JSON
j=json.loads(text(Path('reports/global_trace_to_scheme_closure_registry_v55_data.json')))
check('json_stamp', j['stamp']=='GLOBAL_TRACE_TO_SCHEME_CLOSURE_REGISTRY_PASS')
check('json_sector_count', j['sector_count']==6)
check('json_next_recommended_w', 'W_TRACE' in j['next_recommended'])
check('json_no_physical_final_not_claimed', 'P_physical_final' in j['not_claimed'])
# summary counts
cnt=rows('registry_summary_counts_v55.csv')
check('summary_counts_nonempty', len(cnt)>=8)
check('summary_total_six', any(r['category']=='sector_count' and r['key']=='total' and r['count']=='6' for r in cnt))
failed=[n for n,c in checks if not c]
print(f"Total checks: {len(checks)-len(failed)}/{len(checks)}")
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('GLOBAL_TRACE_TO_SCHEME_CLOSURE_REGISTRY_PASS')
