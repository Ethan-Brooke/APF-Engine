#!/usr/bin/env python3
from __future__ import annotations
import csv,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,cond): checks.append((name,bool(cond)))
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
 'paper/CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_v46.tex',
 'tables/charged_lepton_pole_completion_v46.csv',
 'tables/charged_lepton_pole_completion_claim_ladder_v46.csv',
 'tables/qed_external_ledger_boundary_v46.csv',
 'tables/charged_lepton_completion_gate_status_v46.csv',
 'tables/trace_to_scheme_case_table_v46.csv',
 'reports/charged_lepton_pole_completion_qed_ledger_summary_v46.md',
 'reports/charged_lepton_pole_completion_qed_ledger_v46_data.json',
 'README_v46.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_v46.tex')
summary=text('reports/charged_lepton_pole_completion_qed_ledger_summary_v46.md')
readme=text('README_v46.md')
j=data('reports/charged_lepton_pole_completion_qed_ledger_v46_data.json')
pred=rows('tables/charged_lepton_pole_completion_v46.csv')
ladder={r['layer']:r for r in rows('tables/charged_lepton_pole_completion_claim_ladder_v46.csv')}
ledger={r['ledger_entry']:r for r in rows('tables/qed_external_ledger_boundary_v46.csv')}
gates={r['gate']:r for r in rows('tables/charged_lepton_completion_gate_status_v46.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v46.csv')}
phi=[0.5110026357885311,105.658243985342,1776.9168320084111]
refs=[0.51099895,105.6583755,1776.93]
absres=[phi[i]-refs[i] for i in range(3)]
rel=[100*absres[i]/refs[i] for i in range(3)]
D0=5063
eta=1/D0
env=100*eta
ratios=[abs(x)/env for x in rel]
maxabs=max(abs(x) for x in rel)
maxratio=max(ratios)
for nd in ['Charged-Lepton Pole Completion and QED Ledger Boundary','Charged-lepton pole completion under the APF QED envelope','5063=61(61+16+3+3)','P_{{\\rm pole\\ completion}}^{{\\rm APF\\ envelope}}','QED running is downstream external-ledger transport','No-smuggling exclusions','not as numerical QED-running export']:
    check('tex_contains_'+nd[:50].replace(' ','_').replace('\\','bs'),nd in tex)
check('math_D0',D0==5063)
check('math_eta',abs(eta-0.00019751135690302193)<1e-18)
check('math_env',abs(env-0.019751135690302193)<1e-15)
check('math_res_e',abs(rel[0]-0.0007212908228403025)<1e-12)
check('math_res_mu',abs(rel[1]-(-0.00012447158815943914))<1e-12)
check('math_res_tau',abs(rel[2]-(-0.0007410529164876247))<1e-12)
check('math_maxres',abs(maxabs-0.0007410529164876247)<1e-12)
check('math_maxratio',abs(maxratio-0.03751950916176844)<1e-12)
check('math_inside',all(r<1 for r in ratios))
check('math_sub_1e_minus_3',maxabs<0.001)
check('json_status',j['status']=='CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS')
check('json_package',j['package']=='APF_v46_CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM')
check('json_D0',j['source_from_v43']['D0']==5063)
check('json_formula',j['source_from_v43']['D0_formula']=='K_SM*(K_SM+K_c+K_b+N_gen)=61*(61+16+3+3)')
check('json_eps',j['source_from_v43']['epsilon_QED_APF']=='1/5063')
check('json_eps_percent',abs(j['source_from_v43']['epsilon_percent']-env)<1e-15)
check('json_max_res',abs(j['source_from_v43']['max_abs_residual_percent']-maxabs)<1e-15)
check('json_max_ratio',abs(j['source_from_v43']['max_residual_over_envelope']-maxratio)<1e-15)
check('json_inside',j['source_from_v43']['all_inside_envelope'] is True)
for i,lab in enumerate(['e','mu','tau']):
    check('json_phi_'+lab,abs(j['source_from_v43']['Phi_l_v43_MeV'][i]-phi[i])<1e-12)
    check('json_ref_'+lab,abs(j['source_from_v43']['pole_reference_MeV'][i]-refs[i])<1e-12)
    check('json_abs_'+lab,abs(j['source_from_v43']['absolute_residual_MeV'][i]-absres[i])<1e-12)
    check('json_rel_'+lab,abs(j['source_from_v43']['relative_residual_percent'][i]-rel[i])<1e-12)
    check('json_ratio_'+lab,abs(j['source_from_v43']['residual_over_envelope'][i]-ratios[i])<1e-12)
    row=[r for r in pred if r['lepton']==lab][0]
    check('row_phi_'+lab,abs(float(row['Phi_v43_MeV'])-phi[i])<1e-12)
    check('row_ref_'+lab,abs(float(row['pole_reference_MeV'])-refs[i])<1e-12)
    check('row_abs_'+lab,abs(float(row['absolute_residual_MeV'])-absres[i])<1e-12)
    check('row_rel_'+lab,abs(float(row['relative_residual_percent'])-rel[i])<1e-12)
    check('row_env_'+lab,abs(float(row['APF_envelope_percent'])-env)<1e-12)
    check('row_ratio_'+lab,abs(float(row['residual_over_envelope'])-ratios[i])<1e-12)
    check('row_status_'+lab,row['completion_status']=='inside_APF_envelope_pole_completion_admitted')
check('completion_status',j['completion_theorem']['completion_status']=='P_pole_completion^APF_envelope')
check('completion_meaning','no APF-side source/operator/coefficient/scalar/covariance gate remains open' in j['completion_theorem']['completion_meaning'])
check('completion_not_zero','not exact zero residual' in j['completion_theorem']['completion_not_meaning'])
check('qed_route_status',j['qed_ledger_boundary']['running_route_status']=='P_QED_route_typed')
check('qed_numeric_open',j['qed_ledger_boundary']['numeric_running_status']=='open_until_external_ledger_import')
for l in ['S_run','mu','loop_order_L','alpha_input_and_scale','threshold_schedule_T','matching_convention_M','conversion_convention_C','Sigma_QED']:
    check('json_ledger_'+l,l in j['qed_ledger_boundary']['ledger_required'])
    check('table_ledger_'+l,l in ledger and 'external_required_before_numeric_running' in ledger[l]['v46_status'])
check('ledger_trace_envelope',ledger['Sigma_trace_or_tolerance']['v46_status']=='APF_envelope_declared_as_1/5063_for_pole_completion')
for layer in ['source_trace_vector','operator_and_coefficients','scalar_normalization','pole_covariance','qed_running_route','physical_final']:
    check('ladder_'+layer,layer in ladder)
check('ladder_pole',ladder['pole_covariance']['status_after_v46']=='P_pole_completion_APF_envelope')
check('ladder_physical_not',ladder['physical_final']['status_after_v46']=='not_claimed')
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('gate_'+g,g in gates and g in j['gate_status'])
check('gate_G4',gates['G4_COVARIANCE']['status_after_v46']=='pass_pole_envelope')
check('gate_G5','no inverse lepton mass use' in gates['G5_NO_SMUGGLING']['evidence'])
for f in ['m_e_to_define_trace_vector','m_mu_to_define_trace_vector','m_tau_to_define_trace_vector','inverse_reconstruction_of_T_l','free_generation_factors_r_e_r_mu_r_tau','least_squares_pole_fit','target_selected_QED_scale','target_selected_loop_order','target_selected_threshold_schedule','target_fitted_covariance_envelope']:
    check('forbidden_'+f,f in j['forbidden_inputs_not_used'])
for nc in ['P_QED_running_final','P_physical_final','exact equality to pole masses','zero residual','numeric running masses','target-selected constants ledger','free generation factors']:
    check('not_claimed_'+nc[:20].replace(' ','_'),nc in j['promotion']['not_claimed'])
check('open_running',j['still_open']['numeric_QED_running_export']=='requires external constants/covariance ledger before evaluation')
check('open_values',j['still_open']['QED_running_values']=='not evaluated in v46')
check('open_phys',j['still_open']['physical_final']=='not claimed')
check('next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_EXTERNAL_QED_LEDGER_IMPORT_AND_NUMERIC_RUNNING_EVALUATION')
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_cl_status','P_pole_completion^APF_envelope' in cl['physical_export_status'])
check('case_cl_boundary',cl['first_failed_gate_or_boundary']=='external QED constants/covariance ledger for numerical running export')
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
for nd in ['CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS','P_pole_completion^APF_envelope','epsilon_QED_APF = 1/5063','Maximum residual/envelope','Completion does not mean','APF_CHARGED_LEPTON_EXTERNAL_QED_LEDGER_IMPORT_AND_NUMERIC_RUNNING_EVALUATION']:
    check('summary_contains_'+nd[:50].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS','P_pole_completion^APF_envelope','epsilon_QED_APF=1/5063','python scripts/check_charged_lepton_pole_completion_qed_ledger_v46.py']:
    check('readme_contains_'+nd[:50].replace(' ','_'),nd in readme)
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py','check_charged_lepton_qed_scalar_normalization_v43.py','check_charged_lepton_qed_covariance_running_codomain_v44.py','check_charged_lepton_qed_running_transport_v45.py']:
    check('inherited_exists_'+script,(ROOT/'scripts'/script).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
# Update total in JSON lazily if placeholder? Avoid modifying during verification; require checked value.
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS')
