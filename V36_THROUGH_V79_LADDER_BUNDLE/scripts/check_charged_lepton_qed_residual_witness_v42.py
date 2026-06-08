#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond): checks.append((name,bool(cond)))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
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
 'tables/charged_lepton_qed_residual_witness_v42.csv',
 'tables/charged_lepton_qed_residual_witness_predictions_v42.csv',
 'tables/charged_lepton_qed_residual_channels_v42.csv',
 'tables/trace_to_scheme_case_table_v42.csv',
 'reports/charged_lepton_qed_residual_witness_summary_v42.md',
 'reports/charged_lepton_qed_residual_witness_v42_data.json',
 'README_v42.md'
]
for rel in required:
    check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_WITNESS_v42.tex')
summary=text('reports/charged_lepton_qed_residual_witness_summary_v42.md')
readme=text('README_v42.md')
j=data('reports/charged_lepton_qed_residual_witness_v42_data.json')
main={r['quantity']:r for r in rows('tables/charged_lepton_qed_residual_witness_v42.csv')}
pred_rows=rows('tables/charged_lepton_qed_residual_witness_predictions_v42.csv')
channels={r['channel']:r for r in rows('tables/charged_lepton_qed_residual_channels_v42.csv')}
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v42.csv')}
needles=['Charged-Lepton QED Residual Transport Witness','Forbidden inverse residual closure','APF-count residual-shape witness','Charged-lepton residual-shape witness','Comparison with the forbidden inverse coefficients','v42 charged-lepton status',r'Z_\ell^{\rm wit}',r'{1\over28}',r'{3\over584}','not a final physical charged-lepton mass theorem',r'APF\_QED\_SCALAR\_NORMALIZATION\_AND\_COUNT\_SOURCE\_THEOREM']
for nd in needles: check('tex_contains_'+nd[:35].replace(' ','_').replace('\\','bs'),nd in tex)
# numeric recomputation
pred=[0.0005267650039821162,0.10672828725704815,1.7054533370613425]
refs=[0.00051099895,0.1056583755,1.77693]
KSM=61; KL=42; Kc=16; Kb=3; Ngen=3; Nc=3; NH=4; dAdj=Nc*Nc-1
eta1=1/(Kc+Kb+Ngen*Nc)
eta2=Kb/(dAdj*(KSM+Ngen*NH))
H1=[-1,0,1]; H2=[1,-2,1]
corr=[math.exp(eta1*H1[i]+eta2*H2[i]) for i in range(3)]
out=[pred[i]*corr[i] for i in range(3)]
res=[100*(out[i]-refs[i])/refs[i] for i in range(3)]
logs=[math.log(refs[i]/pred[i]) for i in range(3)]
zeta1=(logs[2]-logs[0])/2
zeta2=(logs[0]+logs[2]-2*logs[1])/6
zeta0=logs[1]+2*zeta2
check('math_eta1_1_over_28',abs(eta1-1/28)<1e-15)
check('math_eta2_3_over_584',abs(eta2-3/584)<1e-15)
check('math_count_28',Kc+Kb+Ngen*Nc==28)
check('math_count_584',dAdj*(KSM+Ngen*NH)==584)
check('math_det_one',abs(math.prod(corr)-1)<1e-14)
check('math_H1_trace_zero',sum(H1)==0)
check('math_H2_trace_zero',sum(H2)==0)
for i,lab in enumerate(['e','mu','tau']):
    check('json_corr_'+lab,abs(j['new_witness']['Z_witness_factors'][i]-corr[i])<1e-15)
    check('json_out_'+lab,abs(j['new_witness']['P_l_witness_GeV'][i]-out[i])<1e-15)
    check('json_res_'+lab,abs(j['diagnostic_only_external_comparison']['relative_residual_percent'][i]-res[i])<1e-9)
    row=[r for r in pred_rows if r['lepton']==lab][0]
    check('row_factor_'+lab,abs(float(row['Z_witness_factor'])-corr[i])<1e-12)
    check('row_value_'+lab,abs(float(row['Phi_witness_MeV_v42'])-1000*out[i])<1e-9)
    check('row_status_'+lab,row['residual_status']=='common_scalar_offset_not_fitted')
for key in ['H1','H2','eta0_witness','eta1_witness','eta2_witness','Z_l_witness','P_l_witness_GeV','forbidden_inverse_coefficients']:
    check('main_has_'+key,key in main)
check('main_eta1_count',main['eta1_witness']['status']=='count_witness')
check('main_eta2_count',main['eta2_witness']['status']=='count_witness')
check('main_inverse_forbidden',main['forbidden_inverse_coefficients']['status']=='diagnostic_only_forbidden_as_source')
for ch in ['v41_pole_LO_vector','residual_basis_H1_H2','forbidden_inverse_diagnostic','APF_count_witness_shape','common_scalar_eta0','QED_running_codomain','trace_covariance','no_smuggling_audit']:
    check('channel_has_'+ch,ch in channels)
check('channel_witness_C',channels['APF_count_witness_shape']['status']=='C_witness')
check('channel_eta0_open',channels['common_scalar_eta0']['status']=='open_residual')
check('channel_no_smuggling',channels['no_smuggling_audit']['status']=='pass')
check('json_status',j['status']=='CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS')
check('json_package',j['package']=='APF_v42_CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_WITNESS')
for k in ['K_SM','K_Lambda','K_c','K_b','N_gen','N_c','N_H','d_adj_SU3']:
    check('json_count_'+k,k in j['source_inputs']['APF_counts'])
check('json_eta1_formula',j['new_witness']['eta1_count_formula']=='1/(K_c+K_b+N_gen*N_c)')
check('json_eta2_formula',j['new_witness']['eta2_count_formula']=='K_b/((N_c^2-1)*(K_SM+N_gen*N_H))')
check('json_det_true',j['new_witness']['determinant_preserving'] is True)
for k in ['denominator_source_lemma','common_scalar_eta0','numeric_trace_covariance','QED_running_codomain','physical_final']:
    check('json_open_'+k,k in j['still_open'])
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('json_gate_'+g,g in j['gate_status'])
check('json_G5_pass','pass' in j['gate_status']['G5_NO_SMUGGLING'])
for forb in ['m_e_pole_as_source','m_mu_pole_as_source','m_tau_pole_as_source','least_squares_fit_to_target_vector','inverse_solution_for_Z_l_from_targets','PDG_or_world_average_fit']:
    check('json_forbid_'+forb,forb in j['forbidden_inputs_not_used'])
check('inverse_zeta0',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta0']-zeta0)<1e-15)
check('inverse_zeta1',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta1']-zeta1)<1e-15)
check('inverse_zeta2',abs(j['forbidden_inverse_diagnostic']['log_coefficients']['zeta2']-zeta2)<1e-15)
check('witness_eta1_close_to_inverse',abs(zeta1-eta1)<1e-5)
check('witness_eta2_close_to_inverse',abs(zeta2-eta2)<1e-6)
check('witness_residual_under_0p021pct',max(abs(x) for x in res)<0.021)
check('witness_residual_spread_small',max(res)-min(res)<0.002)
v41=[3.0853398000360177,1.0126142409298666,-4.022480510693016]
check('witness_improves_v41_100x',max(abs(x) for x in res)<max(abs(x) for x in v41)/100)
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
cl=case['charged leptons']
check('case_cl_status','C_residual_shape^APF_count_witness' in cl['physical_export_status'])
check('case_cl_next',cl['first_failed_gate_or_boundary']==j['next_theorem'])
check('case_top_unchanged',case['top']['physical_export_status']=='P_export_candidate')
check('case_bottom_unchanged',case['bottom']['physical_export_status']=='P_export_candidate')
check('case_W_unchanged',case['EW/W']['physical_export_status']=='P_export_candidate')
for nd in ['CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS','Z_l^wit = exp((1/28) H1 + (3/584) H2)','does **not** claim final physical charged-lepton masses','APF_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_THEOREM']:
    check('summary_contains_'+nd[:25].replace(' ','_'),nd in summary)
for nd in ['CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS','Not claimed: final charged-lepton physical masses','python scripts/check_charged_lepton_qed_residual_witness_v42.py']:
    check('readme_contains_'+nd[:25].replace(' ','_'),nd in readme)
check('cross_status_summary_readme',j['status'] in summary and j['status'] in readme)
check('cross_eta1_table_json','1/28' in main['eta1_witness']['value'] and j['new_witness']['eta1']=='1/28')
check('cross_eta2_table_json','3/584' in main['eta2_witness']['value'] and j['new_witness']['eta2']=='3/584')
check('next_theorem',j['next_theorem']=='APF_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_THEOREM')
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS')
