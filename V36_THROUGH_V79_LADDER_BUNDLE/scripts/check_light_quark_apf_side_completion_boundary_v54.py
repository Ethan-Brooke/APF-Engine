#!/usr/bin/env python3
import csv, json, math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)
def read_csv(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
# files
for rel in [
 'paper/LIGHT_QUARK_APF_SIDE_COMPLETION_BOUNDARY_v54.tex',
 'tables/light_quark_external_chiral_lattice_evaluator_ledger_v54.csv',
 'tables/light_quark_apf_side_completion_checklist_v54.csv',
 'tables/light_quark_no_free_evaluator_taxonomy_v54.csv',
 'tables/light_quark_residual_channel_assignment_v54.csv',
 'tables/trace_to_scheme_case_table_v54.csv',
 'reports/light_quark_apf_side_completion_boundary_v54_data.json',
 'reports/light_quark_apf_side_completion_boundary_summary_v54.md'
]: check('exists_'+rel.replace('/','_'), (ROOT/rel).exists())
tex=(ROOT/'paper/LIGHT_QUARK_APF_SIDE_COMPLETION_BOUNDARY_v54.tex').read_text(encoding='utf-8')
for s in ['Light-Quark APF-Side Completion Boundary','No APF-only light-quark export','U_{\\chi{\\rm lat}}','does not claim']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',s), s in tex)
# external ledger
ledger=read_csv('light_quark_external_chiral_lattice_evaluator_ledger_v54.csv')
items={r['ledger_item']:r for r in ledger}
for item in ['hadronic_calibration_set','lattice_spacing_and_scale_setting','lattice_action_and_ensembles','chiral_ansatz','em_isospin_convention','renormalization_factor','scheme_conversion','joint_covariance','source_independence_audit']:
    check('ledger_has_'+item, item in items)
check('ledger_external_count', sum(1 for r in ledger if r['v54_status']=='external_required')>=8)
check('ledger_audit_closed', items['source_independence_audit']['v54_status']=='closed_v54')
# checklist
cl=read_csv('light_quark_apf_side_completion_checklist_v54.csv')
cc={r['item']:r for r in cl}
for item in ['G1_codomain','source_Tu','source_Td_Ts','source_vector_Tuds','identity_transport','universal_scalar_transport','diagonal_fit_transport','source_independence','residual_assignment','physical_export_candidate']:
    check('checklist_has_'+item, item in cc)
check('checklist_source_closed', cc['source_vector_Tuds']['v54_status']=='closed_v53')
check('checklist_identity_knockout', cc['identity_transport']['v54_status']=='knockout_v53')
check('checklist_scalar_knockout', cc['universal_scalar_transport']['v54_status']=='knockout_v53')
check('checklist_export_not_claimed', cc['physical_export_candidate']['v54_status']=='not_claimed')
# no free evaluator
nf=read_csv('light_quark_no_free_evaluator_taxonomy_v54.csv')
nfd={r['route_class']:r for r in nf}
for route in ['identity','universal_scalar','diagonal_three_scalar','ratio_import','heavy_family_extrapolation','source_independent_chiral_lattice']:
    check('nofree_has_'+route, route in nfd)
check('nofree_identity_knocked', nfd['identity']['v54_status']=='knocked_out')
check('nofree_scalar_knocked', nfd['universal_scalar']['v54_status']=='knocked_out')
check('nofree_diagonal_forbidden', 'forbidden' in nfd['diagonal_three_scalar']['v54_status'])
check('nofree_chilat_next', nfd['source_independent_chiral_lattice']['v54_status']=='admissible_next')
# residual channels math
T={'u':1.1532098523996768,'d':3.870916422334003,'s':87.14328163365137}
P={'u':2.16,'d':4.70,'s':93.5}
idmax=max(abs(100*(T[q]-P[q])/P[q]) for q in T)
Tlist=[T[q] for q in ['u','d','s']]; Plist=[P[q] for q in ['u','d','s']]
k=sum(t*p for t,p in zip(Tlist,Plist))/sum(t*t for t in Tlist)
scmax=max(abs(100*(k*T[q]-P[q])/P[q]) for q in T)
ch=read_csv('light_quark_residual_channel_assignment_v54.csv')
cd={r['channel']:r for r in ch}
for channel in ['source','identity_codomain_mismatch','scalar_codomain_mismatch','chiral_lattice_evaluator','EM_isospin','renormalization_matching','joint_covariance']:
    check('channel_has_'+channel, channel in cd)
check('channel_source_closed', cd['source']['v54_status']=='closed')
check('channel_identity_math', abs(float(cd['identity_codomain_mismatch']['diagnostic_max_percent'])-idmax)<1e-12)
check('channel_scalar_math', abs(float(cd['scalar_codomain_mismatch']['diagnostic_max_percent'])-scmax)<1e-12)
check('channel_chilat_external', cd['chiral_lattice_evaluator']['v54_status']=='external_required')
# case table
case=read_csv('trace_to_scheme_case_table_v54.csv')
light=[r for r in case if r['sector']=='light quarks'][0]
check('case_status_v54', light['physical_export_status']=='P_light_quark_APF_side_complete_external_chilat_required_v54')
check('case_boundary_external', 'external' in light['first_failed_gate_or_boundary'])
check('case_route_pretransport', 'pretransport complete' in light['route_status'])
for sector in ['EW/W','bottom','charged leptons','top','charm']:
    check('case_preserves_'+sector.replace('/','_').replace(' ','_'), any(r['sector']==sector for r in case))
# JSON
p=ROOT/'reports/light_quark_apf_side_completion_boundary_v54_data.json'
data=json.loads(p.read_text(encoding='utf-8'))
check('json_stamp', data['stamp']=='LIGHT_QUARK_APF_SIDE_COMPLETION_BOUNDARY_PASS')
check('json_status', data['status']=='P_light_quark_APF_side_complete_external_chilat_required_v54')
check('json_external_required_count', len(data['external_required'])>=8)
check('json_not_claimed_export', 'P_export_candidate_uds' in data['not_claimed'])
check('json_next', data['next_theorem']=='APF_LIGHT_QUARK_EXTERNAL_CHIRAL_LATTICE_EVALUATOR_IMPORT')
summary=(ROOT/'reports/light_quark_apf_side_completion_boundary_summary_v54.md').read_text(encoding='utf-8')
for term in ['APF-side','Identity transport','Universal scalar','Still not claimed']:
    check('summary_'+term.replace(' ','_'), term in summary)
# inherited v53 files still present
for rel in ['reports/light_quark_up_trace_source_scalar_knockout_v53_data.json','scripts/check_light_quark_up_trace_source_scalar_knockout_v53.py']:
    check('inherits_'+rel.replace('/','_'), (ROOT/rel).exists())
passed=sum(1 for _,ok in checks if ok); total=len(checks)
data['checks_passed']=passed; data['checks_total']=total
p.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(f"\nTotal checks: {passed}/{total}")
if passed!=total:
    raise SystemExit(1)
print('LIGHT_QUARK_APF_SIDE_COMPLETION_BOUNDARY_PASS')
