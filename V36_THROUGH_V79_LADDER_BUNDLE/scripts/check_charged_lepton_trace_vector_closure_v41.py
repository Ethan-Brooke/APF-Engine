#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math
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
 'tables/charged_lepton_trace_vector_closure_v41.csv',
 'tables/charged_lepton_pole_candidate_v41.csv',
 'tables/charged_lepton_residual_channels_v41.csv',
 'tables/trace_to_scheme_case_table_v41.csv',
 'reports/charged_lepton_trace_vector_closure_summary_v41.md',
 'reports/charged_lepton_trace_vector_closure_v41_data.json',
 'README_v41.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_THEOREM_v41.tex')
summary=text('reports/charged_lepton_trace_vector_closure_summary_v41.md')
readme=text('README_v41.md')
j=data('reports/charged_lepton_trace_vector_closure_v41_data.json')
closure={r['quantity']:r for r in rows('tables/charged_lepton_trace_vector_closure_v41.csv')}
pole_rows=rows('tables/charged_lepton_pole_candidate_v41.csv')
res={r['channel']:r for r in rows('tables/charged_lepton_residual_channels_v41.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v41.csv')}
# TeX content gates
needles=[
    r'Charged-Lepton Trace-Vector Closure from the Down-Family Trace Source',
    r'Down-family APF trace source',
    r'Charged-lepton source map',
    r'Charged-lepton trace-vector source closure',
    r'Leading pole-route candidate',
    r'No double application of the residual operator',
    r'No inverse and no double-count gates',
    r'v41 charged-lepton status',
    r'T_\ell^{\rm APF}:=\mathcal R_{d\to\ell}T_d^{\rm APF}',
    r'\mathcal R_{d\to\ell}',
    r'\operatorname{diag}\!\left({1\over3},3,1\right)',
    r'\nu_\ell={1\over\sqrt6}',
    r'P_{\rm export\ candidate}^{\rm pole,LO}',
    r'APF\_CHARGED\_LEPTON\_QED\_RESIDUAL\_TRANSPORT\_THEOREM',
]
for nd in needles: check('tex_contains_'+nd[:45].replace(' ','_').replace('\\','bs'), nd in tex)
# Numeric constants
md=0.003870916422334; ms=0.087143281633652; mb=4.1774904559271
nu=1/math.sqrt(6); R=[1/3,3,1]; Tl=[md/3,3*ms,mb]; pred=[nu*x for x in Tl]
poles=[0.00051099895,0.1056583755,1.77693]
rel=[(pred[i]-poles[i])/poles[i] for i in range(3)]
# Math closure table
for key in ['T_d','R_d_to_l','T_l','nu_l','Phi_pole_LO_GeV','Phi_pole_LO_MeV','forbidden_inverse','forbidden_double_R']:
    check('closure_table_'+key,key in closure)
check('closure_Td_inherited', closure['T_d']['status']=='inherited_APF_TRACE_source')
check('closure_R_retyped', closure['R_d_to_l']['status']=='closed_v39_retyped')
check('closure_Tl_closed', closure['T_l']['status']=='closed_v41')
check('closure_pole_candidate', closure['Phi_pole_LO_GeV']['status']=='pole_LO_export_candidate')
check('closure_forbid_inverse', closure['forbidden_inverse']['status']=='forbidden')
check('closure_forbid_double', closure['forbidden_double_R']['status']=='forbidden')
# exact numeric calculations from table strings via JSON
check('math_Tl_e', abs(j['new_closed']['T_l_APF_TRACE_GeV'][0]-Tl[0])<1e-15)
check('math_Tl_mu', abs(j['new_closed']['T_l_APF_TRACE_GeV'][1]-Tl[1])<1e-15)
check('math_Tl_tau', abs(j['new_closed']['T_l_APF_TRACE_GeV'][2]-Tl[2])<1e-13)
for i,n in enumerate(['e','mu','tau']):
    check('math_pred_'+n, abs(j['new_closed']['pole_LO_prediction_GeV'][i]-pred[i])<1e-15)
    check('math_rel_'+n, abs(j['diagnostic_only_external_comparison']['relative_residual_percent'][i]-100*rel[i])<1e-9)
# Pole rows
check('pole_rows_three', len(pole_rows)==3)
for i,lab in enumerate(['e','mu','tau']):
    row=[r for r in pole_rows if r['lepton']==lab][0]
    check('pole_row_'+lab+'_assigned', row['residual_status']=='assigned_not_fitted')
    check('pole_row_'+lab+'_Tl', abs(float(row['T_l_APF_TRACE_GeV'])-Tl[i])<1e-12)
    check('pole_row_'+lab+'_pred', abs(float(row['Phi_pole_LO_MeV'])-1000*pred[i])<1e-6)
# Residual channels
for ch in ['source_trace_T_d','source_map_R_d_to_l','scalar_normalization_nu_l','pole_codomain','covariance_protocol','QED_pole_finite_transport','APF_route_residual','experimental_covariance','no_smuggling_audit','no_double_count_audit']:
    check('residual_channel_'+ch,ch in res)
check('res_source_closed', res['source_trace_T_d']['status']=='closed')
check('res_map_closed', res['source_map_R_d_to_l']['status']=='closed')
check('res_qed_open', res['QED_pole_finite_transport']['status']=='open_residual')
check('res_no_smuggling_pass', res['no_smuggling_audit']['status']=='pass')
check('res_no_double_pass', res['no_double_count_audit']['status']=='pass')
# Case table
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']: check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_cl_export_candidate_LO','P_export_candidate^pole_LO' in cl['physical_export_status'])
check('case_cl_next_qed','QED_RESIDUAL_TRANSPORT' in cl['first_failed_gate_or_boundary'])
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_bottom_unchanged',case['bottom']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
# JSON status
check('json_status',j['status']=='CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS')
check('json_package',j['package']=='APF_v41_CHARGED_LEPTON_TRACE_VECTOR_CLOSURE')
for k in ['T_d_APF_TRACE_GeV','N_c','R_d_to_l','nu_l','pole_codomain']: check('json_source_'+k,k in j['source_inputs'])
check('json_Nc_3',j['source_inputs']['N_c']==3)
for k in ['T_l_APF_TRACE_GeV','source_map','pole_LO_prediction_GeV','no_double_count_gate','G1_G2_status']: check('json_new_'+k,k in j['new_closed'])
for k in ['QED_pole_finite_transport','numeric_trace_covariance','running_codomain','physical_final']: check('json_open_'+k,k in j['still_open'])
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']: check('json_gate_'+g,g in j['gate_status'])
check('json_G2_closed_LO','Phi=nu_l R_d_to_l T_d' in j['gate_status']['G2_TRANSPORT_MAP'])
check('json_G5_pass','pass' in j['gate_status']['G5_NO_SMUGGLING'])
check('json_promotion_after','P_export_candidate^pole_LO' in j['promotion']['after'])
for nc in ['P_physical_final','P_QED_running_final','zero residual','pole mass derivation to experimental precision']:
    check('json_not_claimed_'+nc.replace(' ','_'), nc in j['promotion']['not_claimed'])
check('json_next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_THEOREM')
# Summary/readme stamps
for nd in ['CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS','T_l = diag(1/3,3,1) T_d','P_export_candidate^pole_LO','Not claimed','APF_CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_THEOREM']:
    check('summary_contains_'+nd[:35].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS','does **not** claim final physical charged-lepton masses','T_l = diag(1/3,3,1) T_d','Phi_l^pole,LO']:
    check('readme_contains_'+nd[:35].replace(' ','_').replace('*','star'),nd in readme)
# No smuggling strings
for forb in ['m_e_pole_as_source','m_mu_pole_as_source','m_tau_pole_as_source','least_squares_fit_to_target_vector','inverse_solution_for_T_l_from_targets']:
    check('json_forbidden_'+forb,forb in j['forbidden_inputs_not_used'])
# Inherited v40+ reports present
inherited=[('reports/trace_to_scheme_export_v35_targeted_v40_rerun.txt','TRACE_TO_SCHEME_EXPORT_THEOREM_PASS'),('reports/top_msr_scale_selection_v37_targeted_v40_rerun.txt','TOP_MSR_SCALE_SELECTION_THEOREM_PASS'),('reports/charged_lepton_residual_operator_v38_targeted_v40_rerun.txt','CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS'),('reports/charged_lepton_coefficient_closure_v39_targeted_v40_rerun.txt','CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS'),('reports/charged_lepton_trace_vector_source_gate_v40_targeted.txt','CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS')]
for relpath,stamp in inherited:
    check('inherited_exists_'+relpath.split('/')[-1],(ROOT/relpath).exists())
    check('inherited_stamp_'+stamp,stamp in text(relpath))
# Cross consistency
check('cross_status_summary_readme',j['status'] in summary and j['status'] in readme)
check('cross_case_next_json',cl['first_failed_gate_or_boundary']==j['next_theorem'])
check('cross_closure_json_Tl','closed_v41'==closure['T_l']['status'] and 'T_l_APF_TRACE_GeV' in j['new_closed'])
check('cross_no_double_tex_table','forbidden_double_R' in closure and 'double-counts' in closure['forbidden_double_R']['meaning'] and 'double-counts' in tex)
check('cross_QED_open_json_res',res['QED_pole_finite_transport']['status']=='open_residual' and 'QED_pole_finite_transport' in j['still_open'])
# Sanity: R determinant and log trace
check('math_R_det_one',abs(R[0]*R[1]*R[2]-1)<1e-15)
check('math_R_log_trace_zero',abs(sum(math.log(x) for x in R))<1e-15)
check('math_nu_positive',nu>0)
check('math_predictions_positive',all(x>0 for x in pred))
check('math_residuals_small_candidate',max(abs(x) for x in rel)<0.05)
# Current count must match JSON
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if not (passed==total and total==j.get('checks_total')):
    raise SystemExit(1)
print('CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS')
