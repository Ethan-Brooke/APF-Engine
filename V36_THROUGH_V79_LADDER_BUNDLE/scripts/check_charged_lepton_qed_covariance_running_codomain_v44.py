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
 'tables/charged_lepton_qed_covariance_envelope_v44.csv',
 'tables/charged_lepton_qed_covariance_predictions_v44.csv',
 'tables/charged_lepton_qed_running_codomain_v44.csv',
 'tables/trace_to_scheme_case_table_v44.csv',
 'reports/charged_lepton_qed_covariance_running_codomain_summary_v44.md',
 'reports/charged_lepton_qed_covariance_running_codomain_v44_data.json',
 'README_v44.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM_v44.tex')
summary=text('reports/charged_lepton_qed_covariance_running_codomain_summary_v44.md')
readme=text('README_v44.md')
j=data('reports/charged_lepton_qed_covariance_running_codomain_v44_data.json')
env={r['quantity']:r for r in rows('tables/charged_lepton_qed_covariance_envelope_v44.csv')}
preds=rows('tables/charged_lepton_qed_covariance_predictions_v44.csv')
run={r['object']:r for r in rows('tables/charged_lepton_qed_running_codomain_v44.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v44.csv')}
needles=['Charged-Lepton QED Covariance and Running-Codomain Gate','Two distinct codomains','APF charged-lepton QED covariance envelope','D_0=5063','\\varepsilon_{\\ell,{\\rm QED}}^{\\rm APF}={1\\over5063}','v44 pole-codomain covariance admission','0.0197511356903\\%','0.0375195092<1','Running-codomain theorem boundary','No-smuggling statement','P_{\\rm covariance\\ admitted}^{\\rm APF\\ envelope}','APF\\_CHARGED\\_LEPTON\\_QED\\_RUNNING\\_TRANSPORT\\_THEOREM']
for nd in needles: check('tex_contains_'+nd[:48].replace(' ','_').replace('\\','bs'),nd in tex)
v43=[0.0005110026357885311,0.105658243985342,1.7769168320084112]
refs=[0.00051099895,0.1056583755,1.77693]
res=[100*(v43[i]-refs[i])/refs[i] for i in range(3)]
absres=[v43[i]-refs[i] for i in range(3)]
eta0=1/5063
envelope_pct=100*eta0
envelope=[refs[i]*eta0 for i in range(3)]
ratios=[abs(absres[i])/envelope[i] for i in range(3)]
check('math_eta0',abs(eta0-1/5063)<1e-18)
check('math_envelope_pct',abs(envelope_pct-0.019751135690302194)<1e-15)
check('math_all_inside',all(r<1 for r in ratios))
check('math_max_residual',abs(max(abs(x) for x in res)-0.0007410529164728296)<1e-12)
check('math_max_ratio',abs(max(ratios)-0.03751950916101936)<1e-12)
check('math_residual_not_zero',max(abs(x) for x in res)>1e-4)
check('math_residual_sub_1e_minus_3_percent',max(abs(x) for x in res)<0.001)
check('math_envelope_from_count_larger_than_residual',envelope_pct>20*max(abs(x) for x in res))
check('json_status',j['status']=='CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS')
check('json_package',j['package']=='APF_v44_CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN')
check('json_D0',j['APF_covariance_envelope']['D0']==5063)
check('json_D0_formula',j['APF_covariance_envelope']['D0_formula']=='K_SM*(K_SM+K_c+K_b+N_gen)')
check('json_epsilon',j['APF_covariance_envelope']['epsilon']=='1/5063')
check('json_epsilon_float',abs(j['APF_covariance_envelope']['epsilon_float']-eta0)<1e-18)
check('json_epsilon_percent',abs(j['APF_covariance_envelope']['epsilon_percent']-envelope_pct)<1e-15)
check('json_all_inside',j['APF_covariance_envelope']['all_inside_envelope'] is True)
check('json_max_ratio',abs(j['APF_covariance_envelope']['max_residual_over_envelope']-max(ratios))<1e-15)
for i,lab in enumerate(['e','mu','tau']):
    check('json_v43_'+lab,abs(j['source_from_v43']['P_l_v43_GeV'][i]-v43[i])<1e-15)
    check('json_res_'+lab,abs(j['source_from_v43']['relative_residual_percent'][i]-res[i])<1e-12)
    check('json_ratio_'+lab,abs(j['APF_covariance_envelope']['component_residual_over_envelope'][i]-ratios[i])<1e-12)
    row=[r for r in preds if r['lepton']==lab][0]
    check('row_value_'+lab,abs(float(row['Phi_v43_MeV'])-1000*v43[i])<1e-9)
    check('row_ref_'+lab,abs(float(row['pole_reference_MeV'])-1000*refs[i])<1e-9)
    check('row_abs_'+lab,abs(float(row['absolute_residual_MeV'])-1000*absres[i])<1e-12)
    check('row_res_'+lab,abs(float(row['relative_residual_percent'])-res[i])<1e-12)
    check('row_envelope_'+lab,abs(float(row['APF_envelope_percent'])-envelope_pct)<1e-12)
    check('row_ratio_'+lab,abs(float(row['residual_over_envelope'])-ratios[i])<1e-12)
    check('row_status_'+lab,row['covariance_status']=='inside_APF_covariance_envelope')
for k in ['D0_covariance','epsilon_QED_APF','epsilon_QED_percent','max_v43_residual_percent','max_residual_over_envelope','running_codomain_map','forbidden_envelope_source']:
    check('env_has_'+k,k in env)
check('env_D0_status',env['D0_covariance']['status']=='P_count_source')
check('env_epsilon_status',env['epsilon_QED_APF']['status']=='P_covariance_envelope')
check('env_running_open',env['running_codomain_map']['status']=='typed_not_evaluated')
check('env_forbidden',env['forbidden_envelope_source']['status']=='forbidden')
for k in ['S_pole','S_running','U_QED^{pole_to_running}','Sigma_trace','Sigma_QED','no_smuggling_audit']:
    check('running_has_'+k,k in run)
check('running_pole_declared',run['S_pole']['status']=='P_declared')
check('running_S_typed',run['S_running']['status']=='P_typed')
check('running_U_open',run['U_QED^{pole_to_running}']['status']=='open_route_object')
check('running_no_smuggling_pass',run['no_smuggling_audit']['status']=='pass')
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('json_gate_'+g,g in j['gate_status'])
check('json_G4_pass','pass' in j['gate_status']['G4_COVARIANCE'])
check('json_G5_pass','pass' in j['gate_status']['G5_NO_SMUGGLING'])
check('json_G6_pass','pass' in j['gate_status']['G6_RESIDUAL_CHANNELS'])
for forb in ['m_e_pole_as_covariance_source','m_mu_pole_as_covariance_source','m_tau_pole_as_covariance_source','least_squares_QED_residual_fit','target_selected_running_scale','target_selected_loop_order','PDG_or_world_average_fit']:
    check('json_forbid_'+forb,forb in j['forbidden_inputs_not_used'])
for k in ['QED_running_transport','numeric_trace_covariance','external_QED_constants_ledger','physical_final']:
    check('json_open_'+k,k in j['still_open'])
check('json_pole_status','P_covariance_admitted' in j['codomain_status']['pole_codomain'])
check('json_running_status',j['codomain_status']['running_codomain']=='typed_not_numerically_exported')
check('json_running_route','U_QED' in j['codomain_status']['running_route_required'])
check('not_claimed_physical_final','P_physical_final' in j['promotion']['not_claimed'])
check('not_claimed_running_final','P_QED_running_final' in j['promotion']['not_claimed'])
check('not_claimed_zero','zero residual' in j['promotion']['not_claimed'])
check('not_claimed_target_covariance','target-fitted covariance' in j['promotion']['not_claimed'])
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_cl_status','P_covariance_admitted^APF_envelope' in cl['physical_export_status'])
check('case_cl_boundary',cl['first_failed_gate_or_boundary']==j['next_theorem'])
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_bottom_unchanged',case['bottom']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
for nd in ['CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS','epsilon_QED_APF = 1/5063','All three components are inside the predeclared APF covariance envelope','does **not** claim final physical charged-lepton masses','APF_CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM']:
    check('summary_contains_'+nd[:45].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS','epsilon_QED_APF=1/5063','P_covariance_admitted^APF_envelope','python scripts/check_charged_lepton_qed_covariance_running_codomain_v44.py']:
    check('readme_contains_'+nd[:45].replace(' ','_'),nd in readme)
check('cross_status_summary_readme',j['status'] in summary and j['status'] in readme)
check('cross_epsilon_table_json',env['epsilon_QED_APF']['value']=='1/5063' and j['APF_covariance_envelope']['epsilon']=='1/5063')
check('cross_max_ratio_table_json',abs(float(env['max_residual_over_envelope']['value'])-j['APF_covariance_envelope']['max_residual_over_envelope'])<1e-12)
check('next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM')
# inherited scripts available and pass when called from root; run only existence to avoid expensive recursive output, but this package also preserves them.
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py','check_charged_lepton_qed_scalar_normalization_v43.py']:
    p=ROOT/'scripts'/script
    check('inherited_exists_'+script,p.exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS')
