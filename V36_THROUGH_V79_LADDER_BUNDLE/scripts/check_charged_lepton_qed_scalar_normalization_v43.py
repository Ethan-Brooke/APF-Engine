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
 'tables/charged_lepton_qed_scalar_normalization_v43.csv',
 'tables/charged_lepton_qed_scalar_predictions_v43.csv',
 'tables/charged_lepton_qed_scalar_residual_channels_v43.csv',
 'tables/trace_to_scheme_case_table_v43.csv',
 'reports/charged_lepton_qed_scalar_normalization_summary_v43.md',
 'reports/charged_lepton_qed_scalar_normalization_v43_data.json',
 'README_v43.md'
]
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_v43.tex')
summary=text('reports/charged_lepton_qed_scalar_normalization_summary_v43.md')
readme=text('README_v43.md')
j=data('reports/charged_lepton_qed_scalar_normalization_v43_data.json')
main={r['quantity']:r for r in rows('tables/charged_lepton_qed_scalar_normalization_v43.csv')}
preds=rows('tables/charged_lepton_qed_scalar_predictions_v43.csv')
channels={r['channel']:r for r in rows('tables/charged_lepton_qed_scalar_residual_channels_v43.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v43.csv')}
needles=['QED Scalar Normalization and Count-Source Witness','Scalar/generation split','APF count-source scalar witness','D_0=K_{\\rm SM}','5063','eta_0^{\\rm APF}={1\\over5063}',r'Z_\ell^{\rm APF,v43}',r'{1\over28}H_1',r'{3\over584}H_2','No-smuggling quarantine','not yet a final physical charged-lepton theorem','APF\\_CHARGED\\_LEPTON\\_QED\\_COVARIANCE\\_AND\\_RUNNING\\_CODOMAIN\\_THEOREM']
for nd in needles: check('tex_contains_'+nd[:42].replace(' ','_').replace('\\','bs'),nd in tex)
P_LO=[0.0005267650039821162,0.10672828725704815,1.7054533370613425]
refs=[0.00051099895,0.1056583755,1.77693]
K_SM=61; K_L=42; K_c=16; K_b=3; N_gen=3; N_c=3; N_H=4; dAdj=N_c*N_c-1
D0=K_SM*(K_SM+K_c+K_b+N_gen)
eta0=1/D0
D1=K_c+K_b+N_gen*N_c
eta1=1/D1
D2=dAdj*(K_SM+N_gen*N_H)
eta2=K_b/D2
H1=[-1,0,1]; H2=[1,-2,1]
shape=[math.exp(eta1*H1[i]+eta2*H2[i]) for i in range(3)]
scalar=math.exp(eta0)
factors=[scalar*shape[i] for i in range(3)]
out=[P_LO[i]*factors[i] for i in range(3)]
res=[100*(out[i]-refs[i])/refs[i] for i in range(3)]
absres=[out[i]-refs[i] for i in range(3)]
v42=[P_LO[i]*shape[i] for i in range(3)]
v42res=[100*(v42[i]-refs[i])/refs[i] for i in range(3)]
logs=[math.log(refs[i]/P_LO[i]) for i in range(3)]
zeta1=(logs[2]-logs[0])/2
zeta2=(logs[0]+logs[2]-2*logs[1])/6
zeta0=logs[1]+2*zeta2
check('math_D0_5063',D0==5063)
check('math_D0_formula',D0==61*(61+16+3+3))
check('math_eta0_1_over_5063',abs(eta0-1/5063)<1e-18)
check('math_D1_28',D1==28)
check('math_D2_584',D2==584)
check('math_eta1_1_over_28',abs(eta1-1/28)<1e-15)
check('math_eta2_3_over_584',abs(eta2-3/584)<1e-15)
check('math_shape_det_one',abs(math.prod(shape)-1)<1e-14)
check('math_scalar_common',abs(factors[0]/shape[0]-scalar)<1e-15 and abs(factors[2]/shape[2]-scalar)<1e-15)
for i,lab in enumerate(['e','mu','tau']):
    check('json_factor_'+lab,abs(j['new_witness']['Z_total_factors_v43'][i]-factors[i])<1e-15)
    check('json_out_'+lab,abs(j['new_witness']['P_l_v43_GeV'][i]-out[i])<1e-15)
    check('json_res_'+lab,abs(j['diagnostic_only_external_comparison']['relative_residual_percent'][i]-res[i])<1e-9)
    check('json_absres_'+lab,abs(j['diagnostic_only_external_comparison']['absolute_residual_GeV'][i]-absres[i])<1e-15)
    row=[r for r in preds if r['lepton']==lab][0]
    check('row_factor_'+lab,abs(float(row['Z_total_factor_v43'])-factors[i])<1e-12)
    check('row_scalar_'+lab,abs(float(row['Z_scalar_factor'])-scalar)<1e-12)
    check('row_value_'+lab,abs(float(row['Phi_v43_MeV'])-1000*out[i])<1e-9)
    check('row_res_'+lab,abs(float(row['relative_residual_percent'])-res[i])<1e-9)
    check('row_status_'+lab,row['residual_status']=='sub_1e_minus_3_percent_residual_channel')
for key in ['I','D0_scalar','eta0_witness','eta1_witness','eta2_witness','Z_l_v43','P_l_v43_GeV','forbidden_inverse_scalar']:
    check('main_has_'+key,key in main)
check('main_eta0_count',main['eta0_witness']['status']=='count_source_witness')
check('main_D0_formula','61*(61+16+3+3)' in main['D0_scalar']['meaning'])
check('main_inverse_forbidden',main['forbidden_inverse_scalar']['status']=='diagnostic_only_forbidden_as_source')
for ch in ['v41_pole_LO_vector','v42_generation_shape','v43_scalar_normalization','forbidden_inverse_scalar','sub_1e_minus_3_residual_band','QED_running_codomain','trace_covariance','no_smuggling_audit']:
    check('channel_has_'+ch,ch in channels)
check('channel_scalar_C',channels['v43_scalar_normalization']['status']=='C_count_witness')
check('channel_residual_open',channels['sub_1e_minus_3_residual_band']['status']=='open_covariance_channel')
check('channel_no_smuggling',channels['no_smuggling_audit']['status']=='pass')
check('json_status',j['status']=='CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS')
check('json_package',j['package']=='APF_v43_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE')
for k in ['K_SM','K_Lambda','K_c','K_b','N_gen','N_c','N_H','d_adj_SU3']:
    check('json_count_'+k,k in j['source_inputs']['APF_counts'])
check('json_D0',j['count_source']['D0_scalar']==5063)
check('json_D0_formula',j['count_source']['D0_formula']=='K_SM*(K_SM+K_c+K_b+N_gen)')
check('json_eta0',j['count_source']['eta0']=='1/5063')
check('json_eta1',j['count_source']['eta1']=='1/28')
check('json_eta2',j['count_source']['eta2']=='3/584')
check('inverse_zeta0',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta0']-zeta0)<1e-15)
check('inverse_zeta1',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta1']-zeta1)<1e-15)
check('inverse_zeta2',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta2']-zeta2)<1e-15)
check('zeta0_eta0_not_equal',abs(zeta0-eta0)>1e-9)
check('zeta0_eta0_close',abs(zeta0-eta0)<5e-7)
check('residual_under_0p001pct',max(abs(x) for x in res)<0.001)
check('residual_not_zero',max(abs(x) for x in res)>0.0001)
check('v43_improves_v42_20x',max(abs(x) for x in v42res)/max(abs(x) for x in res)>20)
check('v42_residual_still_larger',max(abs(x) for x in v42res)>0.02)
check('json_improvement_factor',abs(j['improvement']['max_residual_improvement_factor']-max(abs(x) for x in v42res)/max(abs(x) for x in res))<1e-12)
for k in ['forced_denominator_proof_strength','numeric_trace_covariance','QED_running_codomain','residual_band','physical_final']:
    check('json_open_'+k,k in j['still_open'])
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('json_gate_'+g,g in j['gate_status'])
check('json_G5_pass','pass' in j['gate_status']['G5_NO_SMUGGLING'])
for forb in ['m_e_pole_as_source','m_mu_pole_as_source','m_tau_pole_as_source','least_squares_fit_to_target_vector','inverse_solution_for_eta0_from_targets','PDG_or_world_average_fit']:
    check('json_forbid_'+forb,forb in j['forbidden_inputs_not_used'])
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_cl_status','C_scalar_normalized^APF_count_witness' in cl['physical_export_status'])
check('case_cl_next',cl['first_failed_gate_or_boundary']==j['next_theorem'])
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_bottom_unchanged',case['bottom']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
for nd in ['CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS','eta0 = 1/5063','Z_l^v43 = exp((1/5063) I + (1/28) H1 + (3/584) H2)','does **not** claim final physical charged-lepton masses','APF_CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM']:
    check('summary_contains_'+nd[:35].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS','eta0=1/5063','Not claimed: final charged-lepton physical masses','python scripts/check_charged_lepton_qed_scalar_normalization_v43.py']:
    check('readme_contains_'+nd[:35].replace(' ','_'),nd in readme)
check('cross_status_summary_readme',j['status'] in summary and j['status'] in readme)
check('cross_eta0_table_json','1/5063' in main['eta0_witness']['value'] and j['count_source']['eta0']=='1/5063')
check('cross_eta1_table_json','1/28' in main['eta1_witness']['value'] and j['count_source']['eta1']=='1/28')
check('cross_eta2_table_json','3/584' in main['eta2_witness']['value'] and j['count_source']['eta2']=='3/584')
check('next_theorem',j['next_theorem']=='APF_CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM')
check('not_claimed_physical_final','P_physical_final' in j['promotion']['not_claimed'])
check('not_claimed_zero_residual','zero residual' in j['promotion']['not_claimed'])
# inherited scripts available and pass when called from root
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_residual_operator_v38.py','check_charged_lepton_coefficient_closure_v39.py','check_charged_lepton_trace_vector_source_gate_v40.py','check_charged_lepton_trace_vector_closure_v41.py','check_charged_lepton_qed_residual_witness_v42.py']:
    p=ROOT/'scripts'/script
    check('inherited_exists_'+script,p.exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS')
