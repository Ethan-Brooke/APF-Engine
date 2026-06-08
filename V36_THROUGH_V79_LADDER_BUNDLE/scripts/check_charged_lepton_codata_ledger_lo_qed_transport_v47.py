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
 'paper/CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_THEOREM_v47.tex',
 'tables/charged_lepton_codata_ledger_v47.csv',
 'tables/charged_lepton_codata_reaudit_v47.csv',
 'tables/charged_lepton_lo_qed_transport_v47.csv',
 'tables/charged_lepton_qed_claim_ladder_v47.csv',
 'tables/trace_to_scheme_case_table_v47.csv',
 'reports/charged_lepton_codata_ledger_lo_qed_transport_summary_v47.md',
 'reports/charged_lepton_codata_ledger_lo_qed_transport_v47_data.json',
 'README_v47.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_THEOREM_v47.tex')
summary=text('reports/charged_lepton_codata_ledger_lo_qed_transport_summary_v47.md')
readme=text('README_v47.md')
j=data('reports/charged_lepton_codata_ledger_lo_qed_transport_v47_data.json')
ledger={r['entry']:r for r in rows('tables/charged_lepton_codata_ledger_v47.csv')}
reaudit={r['lepton']:r for r in rows('tables/charged_lepton_codata_reaudit_v47.csv')}
lo={r['lepton']:r for r in rows('tables/charged_lepton_lo_qed_transport_v47.csv')}
ladder={r['layer']:r for r in rows('tables/charged_lepton_qed_claim_ladder_v47.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v47.csv')}
alpha_inv=137.035999177
alpha_inv_unc=0.000000021
alpha=1/alpha_inv
alpha_unc=alpha_inv_unc/(alpha_inv**2)
api=alpha/math.pi
factor=1/(1+api)
phi=[0.5110026357885311,105.658243985342,1776.9168320084111]
refs=[0.51099895069,105.6583755,1776.86]
unc=[0.00000000016,0.0000023,0.12]
absres=[phi[i]-refs[i] for i in range(3)]
rel=[100*absres[i]/refs[i] for i in range(3)]
env=100/5063
ratios=[abs(x)/env for x in rel]
sigma=[abs(absres[i])/unc[i] for i in range(3)]
lo_run=[x*factor for x in phi]
maxabs=max(abs(x) for x in rel)
maxratio=max(ratios)
for nd in ['Charged-Lepton CODATA Ledger Import and Leading-Order QED Transport','CODATA-ledger re-audit of the charged-lepton pole route','Leading-order declared QED running witness','0.997682563522362','P_{\\rm LO\\ QED\\ numeric\\ transport\\ witness}','No-smuggling audit','Still not claimed']:
    check('tex_contains_'+nd[:48].replace(' ','_').replace('\\','bs'),nd in tex)
check('alpha_math',abs(alpha-0.0072973525643314245)<1e-20)
check('alpha_unc_math',abs(alpha_unc-1.1182784434112427e-12)<1e-24)
check('api_math',abs(api-0.0023228194641953287)<1e-20)
check('factor_math',abs(factor-0.997682563522362)<1e-15)
check('env_math',abs(env-0.019751135690302193)<1e-15)
check('maxabs_math',abs(maxabs-0.003198451673807737)<1e-15)
check('maxratio_math',abs(maxratio-0.16193760824488573)<1e-15)
check('inside_envelope',all(x<1 for x in ratios))
check('not_inside_all_codata_sigma',not all(s<1 for s in sigma))
check('tau_inside_codata_sigma',sigma[2]<1)
check('electron_not_sigma',sigma[0]>1000)
check('mu_not_sigma',sigma[1]>10)
check('json_status',j['status']=='CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS')
check('json_package',j['package']=='APF_v47_CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT')
check('json_alpha_inv',abs(j['codata_ledger']['alpha_inverse']-alpha_inv)<1e-15)
check('json_alpha_inv_unc',abs(j['codata_ledger']['alpha_inverse_uncertainty']-alpha_inv_unc)<1e-15)
check('json_alpha',abs(j['codata_ledger']['alpha']-alpha)<1e-20)
check('json_alpha_unc',abs(j['codata_ledger']['alpha_uncertainty']-alpha_unc)<1e-24)
check('json_refs',j['codata_ledger']['charged_lepton_reference_MeV']==refs)
check('json_unc',j['codata_ledger']['charged_lepton_uncertainty_MeV']==unc)
check('json_inside',j['codata_reaudit']['all_inside_APF_envelope'] is True)
check('json_maxres',abs(j['codata_reaudit']['max_abs_residual_percent']-maxabs)<1e-15)
check('json_maxratio',abs(j['codata_reaudit']['max_residual_over_APF_envelope']-maxratio)<1e-15)
check('json_metrology_warning','not the same as being inside CODATA' in j['codata_reaudit']['metrology_warning'])
check('json_formula','Phi_i_v43/(1+alpha/pi)' in j['lo_qed_transport_witness']['formula'])
check('json_factor',abs(j['lo_qed_transport_witness']['factor']-factor)<1e-15)
for i,lab in enumerate(['e','mu','tau']):
    check('json_phi_'+lab,abs(j['codata_reaudit']['Phi_l_v43_MeV'][i]-phi[i])<1e-12)
    check('json_abs_'+lab,abs(j['codata_reaudit']['absolute_residual_MeV'][i]-absres[i])<1e-12)
    check('json_rel_'+lab,abs(j['codata_reaudit']['relative_residual_percent'][i]-rel[i])<1e-12)
    check('json_ratio_'+lab,abs(j['codata_reaudit']['residual_over_APF_envelope'][i]-ratios[i])<1e-12)
    check('json_sigma_'+lab,abs(j['codata_reaudit']['metrology_sigma_count'][i]-sigma[i])<1e-9)
    check('json_lo_run_'+lab,abs(j['lo_qed_transport_witness']['running_witness_MeV'][i]-lo_run[i])<1e-12)
    rr=reaudit[lab]
    check('reaudit_rel_'+lab,abs(float(rr['relative_residual_percent'])-rel[i])<1e-12)
    check('reaudit_ratio_'+lab,abs(float(rr['residual_over_APF_envelope'])-ratios[i])<1e-12)
    check('reaudit_sigma_'+lab,abs(float(rr['metrology_sigma_count'])-sigma[i])<1e-9)
    check('reaudit_status_'+lab,rr['v47_status']=='inside_APF_envelope_CODATA_ledger_reaudit')
    lr=lo[lab]
    check('lo_factor_'+lab,abs(float(lr['lo_qed_factor'])-factor)<1e-12)
    check('lo_run_'+lab,abs(float(lr['lo_qed_running_witness_MeV'])-lo_run[i])<1e-12)
    check('lo_status_'+lab,lr['v47_status']=='numeric_transport_witness_not_final_running')
for key in ['alpha_inverse','alpha','electron_mass_energy_equivalent','muon_mass_energy_equivalent','tau_mass_energy_equivalent','scheme','loop_order','scale_convention','threshold_schedule']:
    check('ledger_'+key,key in ledger)
check('ledger_alpha_status',ledger['alpha_inverse']['v47_status']=='imported_external_constant_not_fit')
check('ledger_scheme_before',ledger['scheme']['v47_status']=='declared_before_evaluation')
check('ledger_threshold_deferred',ledger['threshold_schedule']['v47_status']=='deferred_to_final_QED_ledger')
for layer in ['APF_pole_source_route','LO_QED_numeric_transport','full_QED_running','physical_final']:
    check('ladder_'+layer,layer in ladder)
check('ladder_pole',ladder['APF_pole_source_route']['status_after_v47']=='P_pole_completion_APF_envelope_CODATA2022_survives')
check('ladder_lo',ladder['LO_QED_numeric_transport']['status_after_v47']=='P_LO_QED_numeric_transport_witness')
check('ladder_full_open',ladder['full_QED_running']['status_after_v47']=='open_full_external_ledger_required')
check('ladder_final_not',ladder['physical_final']['status_after_v47']=='not_claimed')
for f in ['CODATA masses to define T_l','inverse reconstruction of trace vector','free generation residual factors','target-selected alpha','target-selected scale','target-selected loop order','target-selected threshold schedule','least-squares QED cleanup','three independent QED residual knobs']:
    check('forbidden_'+f.replace(' ','_'),f in j['forbidden_inputs_not_used'])
for nc in ['P_QED_running_final','P_physical_final','zero residual','inside CODATA standard uncertainties for all leptons','multi-loop QED running','target-fitted QED residual correction']:
    check('not_claimed_'+nc.replace(' ','_'),nc in j['promotion']['not_claimed'])
check('claimed_status','P_LO_QED_numeric_transport_witness' in j['promotion']['claimed'])
check('next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION')
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_'+s.replace('/','_').replace(' ','_'),s in case)
check('case_cl_status','P_LO_QED_numeric_transport_witness' in case['charged leptons']['physical_export_status'])
check('case_cl_boundary',case['charged leptons']['first_failed_gate_or_boundary']=='full multi-loop QED external constants/covariance ledger for final running export')
for nd in ['CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS','Max residual/envelope','LO QED numeric transport witness','not CODATA metrological-sigma agreement','APF_CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION']:
    check('summary_contains_'+nd[:45].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS','P_LO_QED_numeric_transport_witness','CODATA 2022 ledger import','python scripts/check_charged_lepton_codata_ledger_lo_qed_transport_v47.py']:
    check('readme_contains_'+nd[:45].replace(' ','_'),nd in readme)
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py','check_charged_lepton_qed_scalar_normalization_v43.py','check_charged_lepton_qed_covariance_running_codomain_v44.py','check_charged_lepton_qed_running_transport_v45.py','check_charged_lepton_pole_completion_qed_ledger_v46.py']:
    check('inherited_exists_'+script,(ROOT/'scripts'/script).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS')
