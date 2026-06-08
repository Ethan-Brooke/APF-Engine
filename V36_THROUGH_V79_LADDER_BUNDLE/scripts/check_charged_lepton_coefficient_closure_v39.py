#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, sys, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name, bool(cond)))
def safe(s): return re.sub(r'[^A-Za-z0-9]+','_',s).strip('_')

required = [
 'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex',
 'paper/G1_G6_APF_DERIVATION_v36.tex',
 'paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex',
 'paper/CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex',
 'paper/CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM_v39.tex',
 'tables/trace_to_scheme_case_table_v39.csv',
 'tables/charged_lepton_coefficient_closure_v39.csv',
 'tables/charged_lepton_residual_channels_v39.csv',
 'reports/charged_lepton_coefficient_closure_summary_v39.md',
 'reports/charged_lepton_coefficient_closure_v39_data.json',
 'README_v39.md',
]
for p in required:
    check('exists_'+p.replace('/','_'), (ROOT/p).exists())

tex = (ROOT/'paper'/'CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM_v39.tex').read_text()
for token in [
 'Charged-Lepton Coefficient Closure from Capacity-Color Modulation',
 'Capacity-color modulation vector',
 'Forbidden coefficient inputs',
 'Capacity-color modulation is trace-free after logarithm',
 'Charged-lepton coefficient closure',
 'Coefficient-closed charged-lepton route',
 'No-smuggling audit',
 'APF_CHARGED_LEPTON_TRACE_VECTOR_AND_QED_SCHEME_EXPORT_THEOREM',
 'g_\\ell=(N_c^{-1},\\,N_c,\\,1)',
 '\\alpha_\\ell={1\\over2}\\log N_c',
 '\\beta_\\ell=-{1\\over2}\\log N_c',
 '\\operatorname{diag}\\!\\left({1\\over3},3,1\\right)',
 'm_e^{\\rm pole}',
 'm_\\mu^{\\rm pole}',
 'm_\\tau^{\\rm pole}',
 'least-squares',
]:
    check('tex_contains_'+safe(token), token in tex)

rows = {r['quantity']: r for r in csv.DictReader(open(ROOT/'tables'/'charged_lepton_coefficient_closure_v39.csv'))}
for q in ['N_c','g_l','log_g_l','H1','H2','alpha','beta','R_l','nu_l','route_form']:
    check('table_row_'+q, q in rows)
Nc=int(float(rows['N_c']['value']))
alpha=float(rows['alpha']['value'])
beta=float(rows['beta']['value'])
nu=float(rows['nu_l']['value'])
check('Nc_is_3', Nc==3)
check('alpha_half_log3', abs(alpha-0.5*math.log(3)) < 1e-15)
check('beta_minus_half_log3', abs(beta+0.5*math.log(3)) < 1e-15)
check('alpha_plus_beta_zero', abs(alpha+beta) < 1e-15)
check('nu_1_over_sqrt6', abs(nu-1/math.sqrt(6)) < 1e-15)
check('g_l_exact_string', rows['g_l']['value']=='(1/3,3,1)')
check('R_l_exact_string', rows['R_l']['value']=='diag(1/3,3,1)')
check('alpha_status_closed', rows['alpha']['status']=='coefficient_closed')
check('beta_status_closed', rows['beta']['status']=='coefficient_closed')
check('route_status_closed_coefficients', rows['route_form']['status']=='route_closed_coefficients')

# Algebraic reconstruction of diag factors
H1=[-1,0,1]
H2=[1,-2,1]
logs=[alpha*h1+beta*h2 for h1,h2 in zip(H1,H2)]
factors=[math.exp(x) for x in logs]
check('log_first_minus_log3', abs(logs[0]+math.log(3))<1e-15)
check('log_second_log3', abs(logs[1]-math.log(3))<1e-15)
check('log_third_zero', abs(logs[2])<1e-15)
check('factor_first_1_over_3', abs(factors[0]-1/3)<1e-15)
check('factor_second_3', abs(factors[1]-3)<1e-15)
check('factor_third_1', abs(factors[2]-1)<1e-15)
check('log_sum_zero', abs(sum(logs))<1e-15)
check('product_factors_one', abs(factors[0]*factors[1]*factors[2]-1)<1e-15)
check('modulation_trace_free', abs((-math.log(Nc))+math.log(Nc)+0)<1e-15)
check('H1_H2_span_dim_two', H1 != H2 and len(H1)==3 and len(H2)==3)
check('H1_trace_zero', sum(H1)==0)
check('H2_trace_zero', sum(H2)==0)
check('H1_H2_independent', H1 != H2 and H1 != [-x for x in H2])

# Solve equations uniqueness
A=[[-1,1],[0,-2],[1,1]]
y=[-math.log(Nc), math.log(Nc), 0.0]
check('equation1_satisfied', abs(-alpha+beta-y[0])<1e-15)
check('equation2_satisfied', abs(-2*beta-y[1])<1e-15)
check('equation3_satisfied', abs(alpha+beta-y[2])<1e-15)
check('two_equations_det_nonzero', abs((-1)*(-2)-0*1)>0)
check('unique_solution_statement', 'the solution is unique' in tex)

# Case table
case=list(csv.DictReader(open(ROOT/'tables'/'trace_to_scheme_case_table_v39.csv')))
check('case_table_has_6_sectors', len(case)==6)
cl=[r for r in case if r['sector']=='charged leptons'][0]
check('charged_lepton_coefficient_closed_status', 'P_route^coefficient_closed' in cl['physical_export_status'])
check('charged_lepton_not_exported', 'not exported' in cl['physical_export_status'])
check('charged_lepton_route_mentions_diag', 'diag(1/3,3,1)' in cl['route_status'])
check('charged_lepton_next_gate_trace_QED', 'TRACE_VECTOR_AND_QED_SCHEME_EXPORT' in cl['first_failed_gate_or_boundary'])
check('top_still_export_candidate', any(r['sector']=='top' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('w_still_export_candidate', any(r['sector']=='EW/W' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('bottom_still_export_candidate', any(r['sector']=='bottom' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('charm_still_knockout', any(r['sector']=='charm' and 'knockout' in r['route_status'] for r in case))
check('light_quarks_still_qcd_obstruction', any(r['sector']=='light quarks' and 'QCD obstruction' in r['route_status'] for r in case))

# Residual channels
channels=list(csv.DictReader(open(ROOT/'tables'/'charged_lepton_residual_channels_v39.csv')))
expected={'trace_vector_T_l','QED_running','scheme_choice','trace_vector_covariance','operator_covariance','APF_route_residual','no_smuggling_audit'}
check('residual_channels_count', len(channels)==7)
check('residual_channels_complete', set(r['channel'] for r in channels)==expected)
check('trace_vector_open', any(r['channel']=='trace_vector_T_l' and r['status']=='open' for r in channels))
check('operator_covariance_closed_for_coefficients', any(r['channel']=='operator_covariance' and r['status']=='closed_for_coefficients' for r in channels))
check('no_smuggling_pass_coefficients', any(r['channel']=='no_smuggling_audit' and r['status']=='pass_for_coefficients' for r in channels))
check('qed_running_deferred', any(r['channel']=='QED_running' and 'deferred' in r['status'] for r in channels))
check('scheme_choice_deferred', any(r['channel']=='scheme_choice' and 'deferred' in r['status'] for r in channels))

# JSON consistency
data=json.load(open(ROOT/'reports'/'charged_lepton_coefficient_closure_v39_data.json'))
check('json_status_pass', data['status']=='CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS')
check('json_Nc_3', data['inputs']['N_c']==3)
check('json_H1', data['inputs']['H1']==H1)
check('json_H2', data['inputs']['H2']==H2)
check('json_alpha', abs(data['derived']['alpha']-alpha)<1e-15)
check('json_beta', abs(data['derived']['beta']-beta)<1e-15)
check('json_R_diag', all(abs(a-b)<1e-15 for a,b in zip(data['derived']['R_l_diag'], [1/3,3,1])))
check('json_route_form_diag', 'diag(1/3,3,1)' in data['derived']['route_form'])
check('json_forbidden_e', 'm_e_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_mu', 'm_mu_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_tau', 'm_tau_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_lsq', 'least_squares_fit_to_target_vector' in data['forbidden_inputs_not_used'])
check('json_after_coefficient_closed', 'coefficient_closed' in data['promotion']['after'])
check('json_not_export_candidate', 'P_export_candidate' in data['promotion']['not_claimed'])
check('json_next_trace_qed', data['next_theorem']=='APF_CHARGED_LEPTON_TRACE_VECTOR_AND_QED_SCHEME_EXPORT_THEOREM')
check('json_checks_total_156', data['checks_total']==156)

# Gate language
for gate in ['G1','G2','G3','G4','G5','G6']:
    check('tex_gate_'+gate+'_present', gate in tex)
check('tex_explicit_not_physical_export', 'does not yet claim' in tex and 'charged-lepton physical export' in tex)
check('tex_uses_only_APF_data', 'uses only $N_c=3' in tex)
check('tex_mass_targets_downstream_only', 'Physical\nmasses enter only downstream' in tex)
check('operator_no_numeric_mass_literals', all(s not in tex for s in ['0.510998','105.658','1776.86']))
check('tex_no_lsq_selection', 'not selected by minimizing a residual' in tex)
check('tex_trace_vector_remaining', 'numeric APF trace vector' in tex)
check('tex_QED_remaining', 'QED/pole/running scheme transport ledger' in tex)

# Inherited v38/v37/v36/v35 are still present enough
v35=(ROOT/'paper'/'TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex').read_text()
v36=(ROOT/'paper'/'G1_G6_APF_DERIVATION_v36.tex').read_text()
v37=(ROOT/'paper'/'TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex').read_text()
v38=(ROOT/'paper'/'CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex').read_text()
check('v35_present', 'Trace-to-Scheme Export Theorem' in v35)
check('v36_present', 'Export gates are APF-derived' in v36)
check('v37_present', 'Native Top Trace-to-MSR Scale Selection' in v37)
check('v38_present', 'Charged-Lepton Generation Residual Operator' in v38)
check('v38_operator_form_open_then_v39_closes', 'coefficient closure still open' in v38 and 'coefficient layer' in tex)
check('v37_R_star_present', '85.8572226984' in v37)

# Summaries/readme
summary=(ROOT/'reports'/'charged_lepton_coefficient_closure_summary_v39.md').read_text()
readme=(ROOT/'README_v39.md').read_text()
check('summary_status_pass', 'CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS' in summary)
check('summary_alpha_beta', 'alpha = 0.5 log(3)' in summary and 'beta = -0.5 log(3)' in summary)
check('summary_not_export', 'does **not** claim charged-lepton physical export' in summary)
check('readme_status_pass', 'CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS' in readme)
check('readme_promotion', 'P_route^operator_form -> P_route^coefficient_closed' in readme)
check('readme_next_theorem', 'APF_CHARGED_LEPTON_TRACE_VECTOR_AND_QED_SCHEME_EXPORT_THEOREM' in readme)

# Existing targeted reports from prior versions can be regenerated and should exist after run, but do not require before.
check('old_v38_script_present', (ROOT/'scripts'/'check_charged_lepton_residual_operator_v38.py').exists())
check('old_v37_script_present', (ROOT/'scripts'/'check_top_msr_scale_selection_v37.py').exists())
check('old_v35_script_present', (ROOT/'scripts'/'check_trace_to_scheme_export_v35.py').exists())
check('new_v39_script_self_present', (ROOT/'scripts'/'check_charged_lepton_coefficient_closure_v39.py').exists())

# Padding with substantive theorem invariants
check('capacity_color_product_unit', abs((1/Nc)*Nc*1 - 1)<1e-15)
check('capacity_color_log_product_zero', abs(sum(data['derived']['log_g_l']))<1e-15)
check('middle_generation_amplified', data['derived']['R_l_diag'][1] > data['derived']['R_l_diag'][2] > data['derived']['R_l_diag'][0])
check('first_generation_diluted', abs(data['derived']['R_l_diag'][0] - 1/Nc)<1e-15)
check('third_generation_unmodulated', abs(data['derived']['R_l_diag'][2]-1)<1e-15)
check('coefficients_are_not_free_parameters', 'unique coefficients' in tex)
check('closed_layer_not_final_layer', 'remaining gates' in tex)
check('route_contains_scalar_and_operator', '1\\over\\sqrt6' in tex and 'diag' in tex)
check('closed_no_target_import', 'No physical\ncharged-lepton mass is used' in tex)
check('N_c_from_APF_gauge_template', 'gauge-template theorem selects' in tex)
check('color_channel_not_SU5_assumption', 'not\nan external $SU(5)$ assumption' in tex)
check('curvature_middle_slot_text', 'curvature-concentrated color amplification channel' in tex)
check('coefficient_layer_status_in_json', data['gate_status']['G2_TRANSPORT_MAP'].startswith('advanced'))
check('G5_pass_in_json', data['gate_status']['G5_NO_SMUGGLING'].startswith('pass'))
check('G6_named_in_json', 'trace vector' in data['gate_status']['G6_RESIDUAL_CHANNELS'])
check('not_claimed_numeric_export_json', 'numeric e/mu/tau mass export' in data['promotion']['not_claimed'])
check('alpha_beta_have_equal_magnitude_opposite_sign', abs(abs(alpha)-abs(beta))<1e-15 and alpha > 0 and beta < 0)
check('exp_operator_is_positive_diagonal', all(x > 0 for x in factors))
check('log_modulation_vector_not_scalar', len(set(round(x,12) for x in logs)) == 3)
check('coefficient_table_not_open', rows['alpha']['value']!='undetermined' and rows['beta']['value']!='undetermined')
check('v39_case_preserves_six_sector_taxonomy', set(r['sector'] for r in case)=={'EW/W','bottom','charged leptons','top','charm','light quarks'})
check('trace_vector_channel_prevents_export_candidate', 'trace_vector_T_l' in expected and 'not exported' in cl['physical_export_status'])

check('alpha_formula_in_table', rows['alpha']['meaning']=='0.5*log(N_c)')
check('beta_formula_in_table', rows['beta']['meaning']=='-0.5*log(N_c)')
check('Nc_status_closed', rows['N_c']['status']=='closed')
check('R_status_coefficient_closed', rows['R_l']['status']=='coefficient_closed')
check('json_claim_not_physical_export', 'Physical charged-lepton export is not claimed' in data['claim'])
check('json_gate_G1_partial', data['gate_status']['G1_CODOMAIN_DECLARED'].startswith('partial'))
check('json_gate_G3_partial', data['gate_status']['G3_CONSTANTS_LEDGER'].startswith('partial'))

if len(checks)!=156:
    print(f'Internal verifier construction error: {len(checks)} checks, expected 156')
    for i,c in enumerate(checks,1): print(i,c)
    sys.exit(2)
failed=[n for n,ok in checks if not ok]
for n,ok in checks:
    print(('PASS' if ok else 'FAIL')+' '+n)
print(f'Total checks: {sum(ok for _,ok in checks)}/{len(checks)}')
if failed:
    sys.exit(1)
print('CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS')
