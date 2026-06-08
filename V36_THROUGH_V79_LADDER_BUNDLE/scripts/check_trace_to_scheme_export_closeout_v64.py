#!/usr/bin/env python3
import csv, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
def txt(rel): return (ROOT/rel).read_text(encoding='utf-8')
files=[
 'paper/TRACE_TO_SCHEME_EXPORT_CLOSEOUT_v64.tex',
 'tables/claim_ladder_definitions_v64.csv',
 'tables/trace_to_scheme_closeout_registry_v64.csv',
 'tables/trace_to_scheme_accomplishments_v64.csv',
 'tables/no_smuggling_closeout_matrix_v64.csv',
 'tables/export_gate_closeout_v64.csv',
 'tables/post_closeout_next_queue_v64.csv',
 'reports/trace_to_scheme_export_closeout_v64_data.json',
 'reports/trace_to_scheme_export_closeout_summary_v64.md',
 'README_v64.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
# data
j=json.loads(txt('reports/trace_to_scheme_export_closeout_v64_data.json'))
check('json_stamp', j['stamp']=='TRACE_TO_SCHEME_EXPORT_CLOSEOUT_PASS')
check('json_version_v64', j['version']=='v64')
check('architecture_closed', j['architecture_closed'] is True)
check('no_global_physical_final', j['global_physical_final_claimed'] is False)
check('no_sector_physical_final', j['physical_final_assigned'] is False)
check('sector_count_six', j['sector_count']==6)
check('physical_final_count_zero', j['status_counts']['physical_final']==0)
# ladder
lad=rows('tables/claim_ladder_definitions_v64.csv')
statuses=[r['status'] for r in lad]
for s in ['P_trace','P_source','P_route','P_export_candidate','P_covariance_admitted','P_codomain_completion','P_external_ledger_boundary','P_physical_final']:
    check('ladder_has_'+s, s in statuses)
check('ladder_rank_order', [r['rank'] for r in lad]==[str(i) for i in range(8)])
check('physical_final_not_assigned_text', next(r for r in lad if r['status']=='P_physical_final')['promotion_rule']=='not assigned in v64')
# registry
reg=rows('tables/trace_to_scheme_closeout_registry_v64.csv')
check('registry_six_rows', len(reg)==6)
by={r['sector']:r for r in reg}
for s in ['EW/W','charged leptons','charm','bottom','top','light quarks']:
    check('sector_registered_'+re.sub('[^A-Za-z0-9]+','_',s), s in by)
check('w_completion', 'on_shell_EW' in by['EW/W']['highest_closeout_status'])
check('leptons_qed_boundary', 'QED_boundary' in by['charged leptons']['highest_closeout_status'])
check('charm_covariance_admitted', 'P_covariance_admitted' in by['charm']['highest_closeout_status'])
check('bottom_covariance_admitted', 'P_covariance_admitted' in by['bottom']['highest_closeout_status'])
check('top_direct_msr_completion', 'direct_MSR' in by['top']['highest_closeout_status'])
check('top_pole_branch_knockout', 'pole branch' in by['top']['may_claim'] or 'pole branch' in by['top']['highest_closeout_status'])
check('light_chilat_boundary', 'external_chiral_lattice_boundary' in by['light quarks']['highest_closeout_status'])
for r in reg:
    safe = 'P_physical_final' not in r['highest_closeout_status'] and 'physical-final' not in r['may_claim']
    check('no_physical_final_registry_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), safe)
    check('must_not_claim_populated_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['must_not_claim'])>20)
    check('open_boundary_populated_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['open_boundary'])>20)
# gates
gates=rows('tables/export_gate_closeout_v64.csv')
check('six_gates', len(gates)==6)
gd={r['gate']:r for r in gates}
for g in ['G1','G2','G3','G4','G5','G6']:
    check('gate_present_'+g, g in gd)
check('g1_codomain', 'codomain' in gd['G1']['name'])
check('g2_transport', 'transport' in gd['G2']['name'])
check('g3_ledger', 'ledger' in gd['G3']['name'])
check('g4_covariance', 'covariance' in gd['G4']['name'])
check('g5_smuggling', 'smuggling' in gd['G5']['name'])
check('g6_residual', 'residual' in gd['G6']['name'])
# no smuggling
ns=rows('tables/no_smuggling_closeout_matrix_v64.csv')
check('no_smuggling_six_rules', len(ns)==6)
rule_text=' '.join(r['rule']+' '+r['blocked_example'] for r in ns)
for phrase in ['inverse solving','identity transport','direct/MC top','QED/QCD running','unauthorized averaging','light-quark export']:
    check('no_smuggling_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in rule_text)
# accomplishments
acc=rows('tables/trace_to_scheme_accomplishments_v64.csv')
check('accomplishments_has_export_architecture', any(r['item']=='export architecture' and r['status']=='closed' for r in acc))
check('accomplishments_has_global_not_claimed', any(r['item']=='global physical final' and 'not claimed' in r['status'] for r in acc))
# next queue
nq=rows('tables/post_closeout_next_queue_v64.csv')
check('next_queue_has_manuscript', any('manuscript' in r['program'] for r in nq))
check('next_queue_has_chilat', any('chiral-lattice' in r['program'] for r in nq))
# tex content
tex=txt('paper/TRACE_TO_SCHEME_EXPORT_CLOSEOUT_v64.tex')
for phrase in ['Trace-to-Scheme Export Closeout','No sector is assigned','m_t^{\\rm MSR}(R_{\\rm EW})','pole-branch knockout','no inverse solving','Final closeout theorem','TRACE_TO_SCHEME_EXPORT_CLOSEOUT_PASS']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
# values exact-ish in text
check('tex_has_top_msr_value', '172.564754410708' in tex)
check('tex_has_top_pole_knockout', '174.016604383647' in tex)
check('tex_has_rew_value', '12.790035691319' in tex)
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed)
    sys.exit(1)
print('TRACE_TO_SCHEME_EXPORT_CLOSEOUT_PASS')
