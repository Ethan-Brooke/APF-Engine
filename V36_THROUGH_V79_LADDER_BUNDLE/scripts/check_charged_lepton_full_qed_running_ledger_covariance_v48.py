#!/usr/bin/env python3
from __future__ import annotations
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,cond): checks.append((name,bool(cond)))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def data(rel): return json.loads(text(rel))
required=[
 'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex','paper/G1_G6_APF_DERIVATION_v36.tex','paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex','paper/CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex','paper/CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM_v39.tex','paper/CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_AND_QED_CODOMAIN_THEOREM_v40.tex','paper/CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_THEOREM_v41.tex','paper/CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_WITNESS_v42.tex','paper/CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_v43.tex','paper/CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM_v44.tex','paper/CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_v45.tex','paper/CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_v46.tex','paper/CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_THEOREM_v47.tex','paper/CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_v48.tex','tables/charged_lepton_full_qed_running_ledger_v48.csv','tables/charged_lepton_qed_perturbative_covariance_v48.csv','tables/charged_lepton_qed_transport_expansion_v48.csv','tables/charged_lepton_lo_qed_transport_v48.csv','tables/charged_lepton_full_qed_claim_ladder_v48.csv','tables/trace_to_scheme_case_table_v48.csv','reports/charged_lepton_full_qed_running_ledger_covariance_summary_v48.md','reports/charged_lepton_full_qed_running_ledger_covariance_v48_data.json','README_v48.md']
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_v48.tex')
summary=text('reports/charged_lepton_full_qed_running_ledger_covariance_summary_v48.md')
readme=text('README_v48.md')
j=data('reports/charged_lepton_full_qed_running_ledger_covariance_v48_data.json')
ledger={r['entry']:r for r in rows('tables/charged_lepton_full_qed_running_ledger_v48.csv')}
cov={r['lepton']:r for r in rows('tables/charged_lepton_qed_perturbative_covariance_v48.csv')}
exp={r['layer']:r for r in rows('tables/charged_lepton_qed_transport_expansion_v48.csv')}
lo={r['lepton']:r for r in rows('tables/charged_lepton_lo_qed_transport_v48.csv')}
ladder={r['layer']:r for r in rows('tables/charged_lepton_full_qed_claim_ladder_v48.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v48.csv')}
alpha_inv=137.035999177
alpha_inv_unc=0.000000021
alpha=1/alpha_inv
alpha_unc=alpha_inv_unc/(alpha_inv**2)
aopi=alpha/math.pi
lo_factor=1/(1+aopi)
second=100*(aopi**2)
third=100*(aopi**3)
phi=[0.5110026357885311,105.658243985342,1776.9168320084111]
refs=[0.51099895069,105.6583755,1776.86]
unc=[0.00000000016,0.0000023,0.12]
absres=[phi[i]-refs[i] for i in range(3)]
rel=[100*absres[i]/refs[i] for i in range(3)]
apf=100/5063
combined=math.sqrt(apf**2+second**2)
ratios=[abs(x)/combined for x in rel]
lo_run=[x*lo_factor for x in phi]
for nd in ['Charged-Lepton Full QED Running Ledger and Covariance Evaluation','QED running ledger','Full-running ledger typing','v48 covariance admission','No-smuggling audit','P_{\\rm QED\\ truncation\\ covariance\\ admitted}','P_{\\rm full\\ QED\\ running\\ ledger\\ typed}','Still not claimed']:
    check('tex_contains_'+nd[:45].replace(' ','_').replace('\\','bs'), nd in tex)
for nd in ['CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_PASS','Max residual over combined envelope','P_QED_truncation_covariance_admitted','APF_CHARGED_LEPTON_FULL_QED_NUMERIC_RUNNING_WITH_DECLARED_EXTERNAL_COEFFICIENT_LEDGER']:
    check('summary_contains_'+nd[:45].replace(' ','_'), nd in summary)
for nd in ['CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_PASS','P_full_QED_running_ledger_typed','python scripts/check_charged_lepton_full_qed_running_ledger_covariance_v48.py']:
    check('readme_contains_'+nd[:45].replace(' ','_'), nd in readme)
check('json_status',j['status']=='CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_PASS')
check('json_package',j['package']=='APF_v48_CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION')
check('json_alpha_inv',abs(j['codata_ledger']['alpha_inverse']-alpha_inv)<1e-15)
check('json_alpha',abs(j['codata_ledger']['alpha']-alpha)<1e-20)
check('json_aopi',abs(j['qed_transport']['alpha_over_pi']-aopi)<1e-20)
check('json_factor',abs(j['qed_transport']['L1_factor']-lo_factor)<1e-15)
check('json_second',abs(j['qed_transport']['L2_order_scale_percent']-second)<1e-18)
check('json_third',abs(j['qed_transport']['L3_order_scale_percent']-third)<1e-20)
check('json_combined',abs(j['covariance_evaluation']['combined_APF_plus_truncation_percent']-combined)<1e-18)
check('json_combined_inside',j['covariance_evaluation']['all_inside_combined_envelope'] is True)
check('json_pole_inside',j['pole_route']['all_inside_APF_envelope'] is True)
check('json_maxratio_combined',abs(j['covariance_evaluation']['max_residual_over_combined_envelope']-max(ratios))<1e-15)
check('json_full_open',j['qed_transport']['full_running_status']=='typed_open_external_L_ge_2_ledger_required')
check('json_next',j['next_theorem']=='APF_CHARGED_LEPTON_FULL_QED_NUMERIC_RUNNING_WITH_DECLARED_EXTERNAL_COEFFICIENT_LEDGER')
for i,lab in enumerate(['e','mu','tau']):
    check('json_phi_'+lab,abs(j['pole_route']['Phi_l_v43_MeV'][i]-phi[i])<1e-12)
    check('json_rel_'+lab,abs(j['pole_route']['relative_residual_percent'][i]-rel[i])<1e-12)
    check('json_ratio_combined_'+lab,abs(j['covariance_evaluation']['residual_over_combined_envelope'][i]-ratios[i])<1e-12)
    r=cov[lab]
    check('cov_rel_'+lab,abs(float(r['relative_residual_percent'])-rel[i])<1e-12)
    check('cov_second_'+lab,abs(float(r['two_loop_scale_percent'])-second)<1e-18)
    check('cov_combined_'+lab,abs(float(r['combined_APF_plus_truncation_percent'])-combined)<1e-18)
    check('cov_ratio_'+lab,abs(float(r['residual_over_combined_envelope'])-ratios[i])<1e-12)
    check('cov_status_'+lab,r['status']=='inside_combined_APF_QED_envelope')
    lr=lo[lab]
    check('lo_factor_'+lab,abs(float(lr['lo_qed_factor'])-lo_factor)<1e-12)
    check('lo_run_'+lab,abs(float(lr['lo_qed_running_witness_MeV'])-lo_run[i])<1e-12)
for key in ['codomain_family','source_vector','diagnostic_reference','alpha_inverse','alpha','loop_order_L0','loop_order_L1','loop_order_L_ge_2','scale_choice','threshold_schedule','matching_convention','covariance_protocol','forbidden_generation_knobs']:
    check('ledger_'+key,key in ledger)
check('ledger_L2_external',ledger['loop_order_L_ge_2']['v48_status']=='external_coefficients_required')
check('ledger_threshold_external',ledger['threshold_schedule']['v48_status']=='external_schedule_required')
check('ledger_forbidden',ledger['forbidden_generation_knobs']['smuggling_status']=='forbidden')
for layer in ['L0_pole_identity','L1_self_scale_factor','L1_self_scale_shift_percent','L2_order_scale_percent','L3_order_scale_percent','full_running_operator']:
    check('exp_'+layer,layer in exp)
check('exp_L1_factor',abs(float(exp['L1_self_scale_factor']['numeric_value'])-lo_factor)<1e-12)
check('exp_second',abs(float(exp['L2_order_scale_percent']['numeric_value'])-second)<1e-18)
check('exp_full_symbolic',exp['full_running_operator']['v48_status']=='typed_not_final')
for layer in ['APF_pole_source_route','LO_QED_numeric_transport','perturbative_covariance_admission','full_QED_running','physical_final']:
    check('ladder_'+layer,layer in ladder)
check('ladder_cov_closed',ladder['perturbative_covariance_admission']['status_after_v48']=='P_QED_truncation_covariance_admitted')
check('ladder_full_typed',ladder['full_QED_running']['status_after_v48']=='P_full_QED_running_ledger_typed / external_L_ge_2_required')
check('ladder_final_not',ladder['physical_final']['status_after_v48']=='not_claimed')
for f in ['CODATA masses to define T_l','inverse reconstruction of trace vector','free generation residual factors','target-selected alpha','target-selected scale','target-selected loop order','target-selected threshold schedule','least-squares QED cleanup','three independent QED residual knobs','choosing L>=2 coefficients from residuals']:
    check('forbidden_'+f.replace(' ','_'),f in j['forbidden_inputs_not_used'])
for nc in ['P_QED_running_final','P_physical_final','zero residual','inside CODATA standard uncertainties for all leptons','multi-loop QED running numerical evaluation','target-fitted QED residual correction']:
    check('not_claimed_'+nc.replace(' ','_'),nc in j['promotion']['not_claimed'])
for req in ['scheme S_run','scale mu','loop order L','OS-MSbar matching convention','active-lepton threshold schedule','multi-loop coefficients K_n','alpha running convention','covariance/correlation matrix Sigma_QED']:
    check('full_ledger_req_'+req.replace(' ','_').replace('/','_'),req in j['full_qed_ledger_required_before_final_running'])
check('case_charged_leptons','charged leptons' in case)
check('case_status_v48','P_QED_truncation_covariance_admitted' in case['charged leptons']['physical_export_status'])
check('case_boundary_v48','external L>=2 QED coefficients' in case['charged leptons']['first_failed_gate_or_boundary'])
inherited=['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py','check_charged_lepton_qed_scalar_normalization_v43.py','check_charged_lepton_qed_covariance_running_codomain_v44.py','check_charged_lepton_qed_running_transport_v45.py','check_charged_lepton_pole_completion_qed_ledger_v46.py','check_charged_lepton_codata_ledger_lo_qed_transport_v47.py']
for script in inherited:
    check('inherited_exists_'+script,(ROOT/'scripts'/script).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_PASS')
