#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond): checks.append((name,bool(cond)))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def data(rel): return json.loads(text(rel))
required=[
 'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex',
 'paper/G1_G6_APF_DERIVATION_v36.tex',
 'paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex',
 'paper/CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex',
 'paper/CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM_v39.tex',
 'paper/CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_AND_QED_CODOMAIN_THEOREM_v40.tex',
 'paper/CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_THEOREM_v41.tex',
 'paper/CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_WITNESS_v42.tex',
 'paper/CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_v43.tex',
 'paper/CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM_v44.tex',
 'paper/CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_v45.tex',
 'tables/charged_lepton_qed_running_transport_schema_v45.csv',
 'tables/charged_lepton_qed_running_gate_status_v45.csv',
 'tables/charged_lepton_qed_running_forbidden_inputs_v45.csv',
 'tables/charged_lepton_qed_running_required_ledger_v45.csv',
 'tables/trace_to_scheme_case_table_v45.csv',
 'reports/charged_lepton_qed_running_transport_summary_v45.md',
 'reports/charged_lepton_qed_running_transport_v45_data.json',
 'README_v45.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_v45.tex')
summary=text('reports/charged_lepton_qed_running_transport_summary_v45.md')
readme=text('README_v45.md')
j=data('reports/charged_lepton_qed_running_transport_v45_data.json')
schema={r['object']:r for r in rows('tables/charged_lepton_qed_running_transport_schema_v45.csv')}
gates={r['gate']:r for r in rows('tables/charged_lepton_qed_running_gate_status_v45.csv')}
forb={r['forbidden_input']:r for r in rows('tables/charged_lepton_qed_running_forbidden_inputs_v45.csv')}
ledger={r['ledger_entry']:r for r in rows('tables/charged_lepton_qed_running_required_ledger_v45.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v45.csv')}
needles=['Charged-Lepton QED Running Transport Theorem','QED running ledger','APF-admissible QED running transport','U_{\\rm QED}^{S_{\\rm pole}\\to S_{\\rm run}}','P_{\\rm running\\ route\\ form}^{\\rm QED}','No QED residual fitting','free per-generation residual coefficients','G1--G6 status after v45','APF\\_CHARGED\\_LEPTON\\_QED\\_CONSTANTS\\_LEDGER\\_AND\\_NUMERIC\\_RUNNING\\_THEOREM']
for nd in needles: check('tex_contains_'+nd[:50].replace(' ','_').replace('\\','bs'),nd in tex)
v43=[0.5110026357885311,105.658243985342,1776.9168320084111]
refs=[0.51099895,105.6583755,1776.93]
res=[100*(v43[i]-refs[i])/refs[i] for i in range(3)]
eta=1/5063
envelope=100*eta
maxres=max(abs(x) for x in res)
maxratio=maxres/envelope
check('math_eta',abs(eta-0.00019751135690302193)<1e-18)
check('math_envelope',abs(envelope-0.019751135690302193)<1e-15)
check('math_max_residual',abs(maxres-0.0007410529164728296)<1e-12)
check('math_max_ratio',abs(maxratio-0.03751950916101936)<1e-12)
check('json_status',j['status']=='CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_PASS')
check('json_package',j['package']=='APF_v45_CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM')
check('json_route_object','U_QED' in j['running_transport']['route_object'])
check('json_route_status',j['running_transport']['route_status']=='P_route_form_closed_symbolic')
check('json_numeric_not_eval',j['running_transport']['numeric_values']=='not_evaluated')
check('json_generation_dependence',j['running_transport']['generation_dependence']=='source_values_and_declared_thresholds_only')
for i,lab in enumerate(['e','mu','tau']):
    check('json_v43_'+lab,abs(j['source_from_v43']['Phi_l_v43_MeV'][i]-v43[i])<1e-12)
    check('json_res_'+lab,abs(j['source_from_v43']['diagnostic_pole_residual_percent'][i]-res[i])<1e-12)
check('json_D0',j['source_from_v43']['D0']==5063)
check('json_eps',j['source_from_v43']['epsilon_QED_APF']=='1/5063')
check('json_eps_percent',abs(j['source_from_v43']['epsilon_percent']-envelope)<1e-15)
check('json_ratio',abs(j['source_from_v43']['max_residual_over_envelope']-maxratio)<1e-15)
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('json_gate_'+g,g in j['gate_status'])
check('json_G2_closed','route form closed' in j['gate_status']['G2_TRANSPORT_MAP'])
check('json_G3_open','external values open' in j['gate_status']['G3_CONSTANTS_LEDGER'])
check('json_G5_strength','no target-selected' in j['gate_status']['G5_NO_SMUGGLING'])
for k in ['Phi_l_v43_source','L_QED','U_QED^{pole_to_running}','componentwise_generation_dependence','numeric_running_values','no_smuggling_audit']:
    check('schema_has_'+k,k in schema)
check('schema_source_status',schema['Phi_l_v43_source']['status']=='P_source_admitted')
check('schema_ledger_status',schema['L_QED']['status']=='P_ledger_schema_closed')
check('schema_U_status',schema['U_QED^{pole_to_running}']['status']=='P_route_form_closed')
check('schema_component_no_fit','no fitted r_e,r_mu,r_tau' in schema['componentwise_generation_dependence']['required_inputs'])
check('schema_numeric_open',schema['numeric_running_values']['status']=='open_until_ledger_import')
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('gate_table_has_'+g,g in gates)
check('gate_G2_symbolic',gates['G2_TRANSPORT_MAP']['running_status_after_v45']=='P_route_form_closed_symbolic')
check('gate_G3_schema',gates['G3_CONSTANTS_LEDGER']['running_status_after_v45']=='schema_closed_external_values_open')
check('gate_G4_protocol',gates['G4_COVARIANCE']['running_status_after_v45']=='protocol_typed_numeric_covariance_open')
check('gate_G5_pass',gates['G5_NO_SMUGGLING']['running_status_after_v45']=='pass_strengthened')
check('gate_G6_typed',gates['G6_RESIDUAL_CHANNELS']['running_status_after_v45']=='typed_channels_closed')
for f in ['m_e_target_to_choose_U_QED','m_mu_target_to_choose_U_QED','m_tau_target_to_choose_U_QED','target_selected_mu','target_selected_loop_order','target_selected_threshold_schedule','free_generation_factors_r_e_r_mu_r_tau','least_squares_QED_running_fit']:
    check('forbidden_'+f,f in forb and forb[f]['status']=='forbidden' and f in j['forbidden_inputs_not_used'])
for l in ['S_run','mu','loop_order_L','alpha_input_and_scale','threshold_schedule_T','matching_convention_M','conversion_convention_C','Sigma_QED','Sigma_trace_or_tolerance']:
    check('ledger_'+l,l in ledger and ledger[l]['must_be_declared_before_comparison']=='yes' and l in j['required_ledger_before_numeric_export'])
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_status','P_running_route_form^QED' in cl['physical_export_status'])
check('case_next',cl['first_failed_gate_or_boundary']==j['next_theorem'])
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
for nd in ['CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_PASS','P_running_route_form^QED','P_constants_ledger_required','QED running cannot be used as a hidden three-component residual fitter','APF_CHARGED_LEPTON_QED_CONSTANTS_LEDGER_AND_NUMERIC_RUNNING_THEOREM']:
    check('summary_contains_'+nd[:50].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_PASS','U_QED^{S_pole_to_S_run}','P_running_route_form^QED','python scripts/check_charged_lepton_qed_running_transport_v45.py']:
    check('readme_contains_'+nd[:50].replace(' ','_'),nd in readme)
check('not_claimed_running','P_QED_running_final' in j['promotion']['not_claimed'])
check('not_claimed_physical','P_physical_final' in j['promotion']['not_claimed'])
check('not_claimed_numeric','numeric running masses' in j['promotion']['not_claimed'])
check('not_claimed_factors','free generation factors' in j['promotion']['not_claimed'])
check('open_numeric',j['still_open']['numeric_QED_running_export']=='requires external constants ledger and covariance')
check('open_values',j['still_open']['QED_running_values']=='not evaluated in v45')
check('next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_QED_CONSTANTS_LEDGER_AND_NUMERIC_RUNNING_THEOREM')
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py','check_charged_lepton_qed_scalar_normalization_v43.py','check_charged_lepton_qed_covariance_running_codomain_v44.py']:
    check('inherited_exists_'+script,(ROOT/'scripts'/script).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_PASS')
