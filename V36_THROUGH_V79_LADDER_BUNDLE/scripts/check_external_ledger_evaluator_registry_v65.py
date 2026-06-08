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
 'paper/EXTERNAL_LEDGER_AND_EVALUATOR_REGISTRY_v65.tex',
 'tables/external_source_manifest_v65.csv',
 'tables/external_ledger_registry_v65.csv',
 'tables/evaluator_registry_v65.csv',
 'tables/external_boundary_closeout_v65.csv',
 'tables/post_v65_evaluator_queue.csv',
 'reports/external_ledger_evaluator_registry_v65_data.json',
 'reports/external_ledger_evaluator_registry_summary_v65.md',
 'README_v65.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(txt('reports/external_ledger_evaluator_registry_v65_data.json'))
check('stamp', j['stamp']=='EXTERNAL_LEDGER_AND_EVALUATOR_REGISTRY_PASS')
check('version', j['version']=='v65')
check('registry_closed', j['registry_closed'] is True)
check('external_phase_open', j['external_evaluator_phase_open'] is True)
check('no_physical_final', j['physical_final_assigned'] is False)
check('sector_count_6', j['sector_count']==6)
check('evaluator_count_6', j['evaluator_count']==6)
check('source_count_ge_10', j['source_count']>=10)
check('top_value_retained', abs(j['top_msr_rew_gev']-172.564754410708)<1e-12)
check('top_pole_retained', abs(j['top_pole_branch_gev']-174.016604383647)<1e-12)
# sources
src=rows('tables/external_source_manifest_v65.csv')
sids={r['ref_id'] for r in src}
for rid in ['NIST_CODATA_2022','PDG_2025_W','CMS_2026_W_Nature','PDG_2025_C_QUARK','PDG_2025_B_QUARK','PDG_2025_T_QUARK','PDG_2025_QCD_REVIEW','MSR_HOANG_2017','RUNDEC_V3','TOP_MC_INTERPRETATION_HOANG_2020']:
    check('source_'+rid, rid in sids)
for r in src:
    check('source_url_'+r['ref_id'], r['url'].startswith('http'))
    check('source_use_'+r['ref_id'], len(r['use'])>10)
# ledger
led=rows('tables/external_ledger_registry_v65.csv')
check('ledger_rows_6', len(led)==6)
by={r['sector']:r for r in led}
for s in ['EW/W','charged_leptons','charm','bottom','top','light_quarks']:
    check('ledger_sector_'+re.sub('[^A-Za-z0-9]+','_',s), s in by)
check('w_has_cms_pdg', 'CMS_2026' in by['EW/W']['external_ledger'] and 'PDG_2025_W' in by['EW/W']['external_ledger'])
check('leptons_has_nist', 'NIST_CODATA_2022' in by['charged_leptons']['external_ledger'])
check('charm_has_pdg', 'PDG_2025_C_QUARK' in by['charm']['external_ledger'])
check('bottom_has_pdg', 'PDG_2025_B_QUARK' in by['bottom']['external_ledger'])
check('top_has_msr_rundec', 'MSR_HOANG_2017' in by['top']['external_ledger'] and 'RUNDEC_V3' in by['top']['external_ledger'])
check('light_external_required', 'external evaluator required' in by['light_quarks']['evaluator_status'])
for r in led:
    check('ledger_no_physical_final_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), 'physical-final' not in r['numeric_final'] and r['numeric_final']!='P_physical_final')
    check('ledger_next_action_'+re.sub('[^A-Za-z0-9]+','_',r['sector']), len(r['next_action'])>20)
# evaluators
ev=rows('tables/evaluator_registry_v65.csv')
check('evaluators_6', len(ev)==6)
eids={r['evaluator_id'] for r in ev}
for eid in ['E_EW_ONSHELL_W','E_QED_LEPTON_RUNNING','E_QCD_CB_SELF_SCALE','E_TOP_MSR_R_EVOLUTION','E_TOP_POLE_BRANCH','E_LIGHT_CHILAT']:
    check('evaluator_'+eid, eid in eids)
check('top_pole_blocked', next(r for r in ev if r['evaluator_id']=='E_TOP_POLE_BRANCH')['implementation_status']=='blocked_by_v61_audit')
check('top_r_evolution_not_final', 'full R-evolution implementation required' in next(r for r in ev if r['evaluator_id']=='E_TOP_MSR_R_EVOLUTION')['implementation_status'])
for r in ev:
    check('evaluator_fail_closed_'+r['evaluator_id'], len(r['fail_closed_condition'])>20)
    check('evaluator_sources_'+r['evaluator_id'], len(r['required_sources'])>10)
# boundaries
bd=rows('tables/external_boundary_closeout_v65.csv')
check('boundaries_6', len(bd)==6)
check('boundaries_all_closed', all(r['closed'].startswith('yes') for r in bd))
# queue
q=rows('tables/post_v65_evaluator_queue.csv')
check('queue_5', len(q)==5)
check('queue_top_first', q[0]['program']=='v66_TOP_MSR_R_EVOLUTION_EVALUATOR')
check('queue_qed', any('QED' in r['program'] for r in q))
check('queue_light', any('LIGHT_QUARK' in r['program'] for r in q))
# tex
tex=txt('paper/EXTERNAL_LEDGER_AND_EVALUATOR_REGISTRY_v65.tex')
for phrase in ['External Ledger and Evaluator Registry Closeout', 'No sector is assigned', 'm_t^{\\rm MSR}(R_{\\rm EW})', '174.016604383647', 'fail closed', 'EXTERNAL\\_LEDGER\\_AND\\_EVALUATOR\\_REGISTRY\\_PASS']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed)
    sys.exit(1)
print('EXTERNAL_LEDGER_AND_EVALUATOR_REGISTRY_PASS')
