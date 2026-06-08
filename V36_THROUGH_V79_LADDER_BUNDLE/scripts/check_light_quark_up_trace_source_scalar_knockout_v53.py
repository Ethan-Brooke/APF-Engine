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
 'paper/LIGHT_QUARK_UP_TRACE_SOURCE_AND_SCALAR_KNOCKOUT_v53.tex',
 'tables/light_quark_source_inventory_v53.csv',
 'tables/light_quark_source_vector_v53.csv',
 'tables/light_quark_identity_transport_knockout_v53.csv',
 'tables/light_quark_universal_scalar_transport_knockout_v53.csv',
 'tables/light_quark_ratio_diagnostics_v53.csv',
 'tables/light_quark_chiral_lattice_transport_schema_v53.csv',
 'tables/light_quark_export_gates_v53.csv',
 'tables/light_quark_forbidden_inputs_v53.csv',
 'tables/light_quark_residual_channels_v53.csv',
 'tables/trace_to_scheme_case_table_v53.csv',
 'reports/light_quark_up_trace_source_scalar_knockout_v53_data.json',
 'reports/light_quark_up_trace_source_scalar_knockout_summary_v53.md'
]: check('exists_'+rel.replace('/','_'), (ROOT/rel).exists())
tex=(ROOT/'paper/LIGHT_QUARK_UP_TRACE_SOURCE_AND_SCALAR_KNOCKOUT_v53.tex').read_text(encoding='utf-8')
for s in ['Light-Quark Up Trace Source','Scalar-Transport Knockout','T_{uds}^{\\rm APF}','No-smuggling','does not claim']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',s), s in tex)
# source vector
src=read_csv('light_quark_source_inventory_v53.csv')
status={r['source_object']:r['status'] for r in src}
check('source_Tu_closed', status.get('T_u^APF[1]')=='banked_trace_sector_import_v53')
check('source_Td_closed', status.get('T_d^APF[1]')=='banked_v41_down_family_trace')
check('source_Ts_closed', status.get('T_d^APF[2]')=='banked_v41_down_family_trace')
check('source_heavy_present', {'T_c^APF','T_b^APF','T_t^APF'}.issubset(set(status)))
vec=read_csv('light_quark_source_vector_v53.csv')
vv={r['component']:r for r in vec}
expected={'u':1.1532098523996768,'d':3.870916422334003,'s':87.14328163365137}
for q,v in expected.items():
    check('vec_has_'+q, q in vv)
    check('vec_value_'+q, abs(float(vv[q]['T_APF_MeV'])-v)<1e-12)
    check('vec_warning_'+q, 'not MSbar' in vv[q]['codomain_warning'])
# identity math
kn=read_csv('light_quark_identity_transport_knockout_v53.csv')
kr={r['component']:r for r in kn}
pdg={'u':2.16,'d':4.70,'s':93.5}
for q,t in expected.items():
    rel=100*(t-pdg[q])/pdg[q]
    factor=pdg[q]/t
    check('identity_value_'+q, abs(float(kr[q]['APF_trace_identity_MeV'])-t)<1e-12)
    check('identity_residual_'+q, abs(float(kr[q]['relative_residual_percent'])-rel)<1e-12)
    check('identity_factor_'+q, abs(float(kr[q]['target_over_trace'])-factor)<1e-12)
    check('identity_fails_label_'+q, 'fails' in kr[q]['diagnostic_status'])
check('identity_u_large', abs(float(kr['u']['relative_residual_percent']))>40)
check('identity_d_large', abs(float(kr['d']['relative_residual_percent']))>10)
check('identity_s_nonzero', abs(float(kr['s']['relative_residual_percent']))>5)
# scalar knockout
sc=read_csv('light_quark_universal_scalar_transport_knockout_v53.csv')
check('scalar_rows', len(sc)>=12)
rules=set(r['scalar_rule'] for r in sc)
for rule in ['least_squares_unweighted','log_geometric_component_mean','PDG_uncertainty_weighted']:
    check('scalar_rule_'+rule, rule in rules)
ls=[r for r in sc if r['scalar_rule']=='least_squares_unweighted']
lsq={r['component']:r for r in ls}
T=[expected[q] for q in ['u','d','s']]; P=[pdg[q] for q in ['u','d','s']]
k=sum(t*p for t,p in zip(T,P))/sum(t*t for t in T)
check('k_l2_math', abs(float(lsq['u']['kappa'])-k)<1e-12)
for q,t,p in zip(['u','d','s'],T,P):
    pred=k*t; rel=100*(pred-p)/p
    check('scalar_l2_pred_'+q, abs(float(lsq[q]['predicted_MeV'])-pred)<1e-12)
    check('scalar_l2_resid_'+q, abs(float(lsq[q]['relative_residual_percent'])-rel)<1e-12)
check('scalar_l2_u_bad', abs(float(lsq['u']['relative_residual_percent']))>40)
check('scalar_l2_d_bad', abs(float(lsq['d']['relative_residual_percent']))>10)
check('scalar_not_export_label', any(r['component']=='MAXABS' and float(r['relative_residual_percent'])>40 for r in sc if r['scalar_rule']=='least_squares_unweighted'))
# ratios
rat=read_csv('light_quark_ratio_diagnostics_v53.csv')
rr={r['ratio']:r for r in rat}
check('ratio_u_over_d', abs(float(rr['u_over_d']['APF_trace_ratio'])-(expected['u']/expected['d']))<1e-12)
check('ratio_s_over_d', abs(float(rr['s_over_d']['APF_trace_ratio'])-(expected['s']/expected['d']))<1e-12)
check('ratio_s_avg', abs(float(rr['s_over_ud_average']['APF_trace_ratio'])-(expected['s']/((expected['u']+expected['d'])/2)))<1e-12)
check('ratio_diagnostic_only', all('diagnostic only' in r['v53_use'] for r in rat))
# schema/gates
schema=read_csv('light_quark_chiral_lattice_transport_schema_v53.csv')
items={r['ledger_item']:r for r in schema}
for item in ['codomain','source_vector','identity_transport','universal_scalar_transport','chiral_lattice_map','lattice_scale_setting','chiral_fit','EM_isospin','renormalization_matching','covariance','no_target_inversion']:
    check('schema_has_'+item, item in items)
check('schema_source_closed', items['source_vector']['v53_status']=='closed_v53')
check('schema_identity_knockout', items['identity_transport']['v53_status']=='knockout_v53')
check('schema_scalar_knockout', items['universal_scalar_transport']['v53_status']=='knockout_v53')
check('schema_external_count', sum(1 for r in schema if r['v53_status']=='external_required')>=5)
check('schema_no_target_closed', items['no_target_inversion']['v53_status']=='closed_v53')
gates=read_csv('light_quark_export_gates_v53.csv')
g={r['gate']:r for r in gates}
for gate in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE_PROTOCOL','G5_NO_SMUGGLING_AUDIT','G6_RESIDUAL_CHANNELS','SOURCE_VECTOR']:
    check('gate_has_'+gate, gate in g)
check('gate_source_pass', g['SOURCE_VECTOR']['v53_status']=='pass')
check('gate_G2_not_evaluator', 'not_evaluator' in g['G2_TRANSPORT_MAP']['v53_status'])
check('gate_G5_pass', g['G5_NO_SMUGGLING_AUDIT']['v53_status']=='pass')
# forbidden
forb=read_csv('light_quark_forbidden_inputs_v53.csv')
check('forbidden_count', len(forb)>=10)
check('forbidden_blocked', all('blocked' in r['v53_audit'] for r in forb))
for needle in ['PDG m_u','least-squares','universal scalar','lattice scale','chiral ansatz','heavy up-family']:
    check('forbidden_mentions_'+needle.replace(' ','_'), any(needle in r['forbidden_input'] for r in forb))
# residual channels
channels=read_csv('light_quark_residual_channels_v53.csv')
ch={r['channel']:r for r in channels}
for key in ['source_T_u','source_T_d_T_s','identity_transport','universal_scalar_transport','chiral_lattice_transport','EM_isospin_corrections','MSbar_2GeV_matching','covariance','physical_export']:
    check('channel_has_'+key, key in ch)
check('channel_Tu_closed', ch['source_T_u']['status']=='closed_v53')
check('channel_identity_knockout', ch['identity_transport']['status']=='knockout')
check('channel_scalar_knockout', ch['universal_scalar_transport']['status']=='knockout')
check('channel_export_not_claimed', ch['physical_export']['status']=='not_claimed')
# case table
case=read_csv('trace_to_scheme_case_table_v53.csv')
light=[r for r in case if r['sector']=='light quarks'][0]
check('case_light_status_v53', light['physical_export_status']=='P_light_quark_source_closed_not_exported_v53')
check('case_light_route_mentions_scalar', 'scalar' in light['route_status'])
check('case_light_boundary_chilat', 'chiral/lattice' in light['first_failed_gate_or_boundary'])
for sector in ['EW/W','bottom','charged leptons','top','charm']:
    check('case_preserves_'+sector.replace('/','_').replace(' ','_'), any(r['sector']==sector for r in case))
# JSON and summary
p=ROOT/'reports/light_quark_up_trace_source_scalar_knockout_v53_data.json'
data=json.loads(p.read_text(encoding='utf-8'))
check('json_stamp', data['stamp']=='LIGHT_QUARK_UP_TRACE_SOURCE_AND_SCALAR_KNOCKOUT_PASS')
check('json_Tu_value', abs(data['Tuds_APF_MeV']['u']-expected['u'])<1e-12)
check('json_no_export', 'P_export_candidate_uds' in data['not_claimed'])
check('json_next', data['next_theorem']=='APF_LIGHT_QUARK_CHIRAL_LATTICE_EVALUATOR_AND_COVARIANCE_LEDGER')
summary=(ROOT/'reports/light_quark_up_trace_source_scalar_knockout_summary_v53.md').read_text(encoding='utf-8')
for term in ['T_u^APF','Identity residuals','Still not claimed','Next theorem']:
    check('summary_'+term.replace(' ','_'), term in summary)
# update count
passed=sum(1 for _,ok in checks if ok); total=len(checks)
data['checks_passed']=passed; data['checks_total']=total
p.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(f"\nTotal checks: {passed}/{total}")
if passed!=total:
    raise SystemExit(1)
print('LIGHT_QUARK_UP_TRACE_SOURCE_AND_SCALAR_KNOCKOUT_PASS')
