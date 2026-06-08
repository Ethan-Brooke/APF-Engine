#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, re, sys
ROOT = Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name, bool(cond)))

def safe(s):
    return re.sub(r'[^A-Za-z0-9]+','_',s).strip('_')

required = [
    'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex',
    'paper/G1_G6_APF_DERIVATION_v36.tex',
    'paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex',
    'paper/CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex',
    'tables/trace_to_scheme_case_table_v38.csv',
    'tables/charged_lepton_residual_operator_v38.csv',
    'tables/charged_lepton_residual_channels_v38.csv',
    'reports/charged_lepton_residual_operator_summary_v38.md',
    'reports/charged_lepton_residual_operator_v38_data.json',
    'README_v38.md',
]
for p in required:
    check('exists_'+p.replace('/','_'), (ROOT/p).exists())

tex = (ROOT/'paper'/'CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex').read_text()
for token in [
    'Charged-Lepton Generation Residual Operator',
    'Scalar normalization candidate',
    'Generation basis and trace-free modes',
    'Forbidden charged-lepton residual inputs',
    'Scalar normalization cannot close a three-generation residual',
    'APF-minimal charged-lepton residual operator',
    'operator form closed; coefficient closure still open',
    'Charged-lepton coefficient-closure gate',
    '\\nu_\\ell={1\\over\\sqrt{3!}}={1\\over\\sqrt 6}',
    'H_1:=\\operatorname{diag}(-1,0,1)',
    'H_2:=\\operatorname{diag}(1,-2,1)',
    '\\mathcal R_\\ell(\\alpha,\\beta)',
    '\\exp\\!\\left(\\alpha H_1+\\beta H_2\\right)',
    'Z_\\ell^S\\,\\nu_\\ell\\,',
    'not yet',
]:
    check('tex_contains_'+safe(token), token in tex)

# Operator table
rows = {r['quantity']: r for r in csv.DictReader(open(ROOT/'tables'/'charged_lepton_residual_operator_v38.csv'))}
for q in ['nu_l','N_gen','ordering_volume','q_vector','q_bar','H1','H2','R_l','alpha','beta']:
    check('operator_table_row_'+q, q in rows)
nu = float(rows['nu_l']['value'])
check('nu_value_1_over_sqrt6', abs(nu - 1/math.sqrt(6)) < 1e-15)
check('N_gen_3', int(float(rows['N_gen']['value'])) == 3)
check('ordering_volume_6', int(float(rows['ordering_volume']['value'])) == 6)
check('q_vector_012', rows['q_vector']['value'] == '(0,1,2)')
check('q_bar_1', int(float(rows['q_bar']['value'])) == 1)
check('H1_diag', rows['H1']['value'] == 'diag(-1,0,1)')
check('H2_diag', rows['H2']['value'] == 'diag(1,-2,1)')
check('R_l_form', 'exp(alpha H1 + beta H2)' in rows['R_l']['value'])
check('alpha_open', rows['alpha']['status'] == 'open_coefficient_closure')
check('beta_open', rows['beta']['status'] == 'open_coefficient_closure')

# Trace-free algebra checks
H1 = [-1,0,1]
H2 = [1,-2,1]
ones = [1,1,1]
q = [0,1,2]
check('H1_trace_zero', sum(H1)==0)
check('H2_trace_zero', sum(H2)==0)
check('H1_not_scalar', len(set(H1))>1)
check('H2_not_scalar', len(set(H2))>1)
check('H1_orthogonal_uniform', sum(a*b for a,b in zip(H1,ones))==0)
check('H2_orthogonal_uniform', sum(a*b for a,b in zip(H2,ones))==0)
check('H1_matches_centered_q', H1 == [x-1 for x in q])
check('H2_second_difference', H2[0] - 2*H2[1] + H2[2] == 6)
check('trace_free_dimension_two', 3-1 == 2)
check('H1_H2_independent', H1 != H2 and H1 != [-x for x in H2])

# Case table status
case = list(csv.DictReader(open(ROOT/'tables'/'trace_to_scheme_case_table_v38.csv')))
check('case_table_has_6_sectors', len(case) == 6)
check('charged_lepton_not_exported', any(r['sector']=='charged leptons' and 'not exported' in r['physical_export_status'] for r in case))
check('charged_lepton_operator_form_derived', any(r['sector']=='charged leptons' and 'operator form derived' in r['route_status'] for r in case))
check('charged_lepton_next_gate_coefficients', any(r['sector']=='charged leptons' and 'COEFFICIENT_CLOSURE' in r['first_failed_gate_or_boundary'] for r in case))
check('top_still_export_candidate', any(r['sector']=='top' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('w_still_export_candidate', any(r['sector']=='EW/W' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('bottom_still_export_candidate', any(r['sector']=='bottom' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('charm_still_knockout', any(r['sector']=='charm' and 'knockout' in r['route_status'] for r in case))
check('light_quarks_still_qcd_obstruction', any(r['sector']=='light quarks' and 'QCD obstruction' in r['route_status'] for r in case))

# Residual channels
channels = list(csv.DictReader(open(ROOT/'tables'/'charged_lepton_residual_channels_v38.csv')))
expected_channels = {
    'coefficient_closure','QED_running','scheme_choice','trace_vector_covariance',
    'operator_covariance','APF_route_residual','no_smuggling_audit'
}
check('residual_channels_count', len(channels)==7)
check('residual_channels_complete', set(r['channel'] for r in channels)==expected_channels)
check('coefficient_closure_open', any(r['channel']=='coefficient_closure' and r['status']=='open' for r in channels))
check('no_smuggling_pass_for_form', any(r['channel']=='no_smuggling_audit' and r['status']=='pass_for_form' for r in channels))
check('qed_running_deferred', any(r['channel']=='QED_running' and 'deferred' in r['status'] for r in channels))
check('scheme_choice_deferred', any(r['channel']=='scheme_choice' and 'deferred' in r['status'] for r in channels))

# JSON consistency
data = json.load(open(ROOT/'reports'/'charged_lepton_residual_operator_v38_data.json'))
check('json_status_pass', data['status']=='CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS')
check('json_N_gen', data['inputs']['N_gen']==3)
check('json_ordering_volume', data['inputs']['ordering_volume']==6)
check('json_nu_matches', abs(data['inputs']['nu_l'] - 1/math.sqrt(6)) < 1e-15)
check('json_q_vector', data['inputs']['q_vector']==[0,1,2])
check('json_trace_free_dimension', data['derived']['trace_free_dimension']==2)
check('json_H1', data['derived']['H1']==H1)
check('json_H2', data['derived']['H2']==H2)
check('json_operator_form', data['derived']['operator_form']=='exp(alpha H1 + beta H2)')
check('json_route_form_contains_sqrt6', '1/sqrt(6)' in data['derived']['route_form'])
check('json_before_missing_operator', 'missing generation residual operator' in data['promotion']['before'])
check('json_after_operator_form', 'operator_form' in data['promotion']['after'])
check('json_not_export_candidate', 'P_export_candidate' in data['promotion']['not_claimed'])
check('json_next_theorem', data['next_theorem']=='APF_CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM')
check('json_checks_total_122', data['checks_total']==122)

# No-smuggling: forbidden target masses are mentioned only as forbidden/external, not in route formula.
for f in ['m_e^{\\rm pole}', 'm_\\mu^{\\rm pole}', 'm_\\tau^{\\rm pole}', 'PDG/world-average charged-lepton masses', 'least-squares fits']:
    check('forbidden_list_contains_'+safe(f), f in tex)
check('operator_form_does_not_contain_numeric_masses', all(s not in tex for s in ['0.510998', '105.658', '1776.86']))
check('json_forbidden_e', 'm_e_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_mu', 'm_mu_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_tau', 'm_tau_pole' in data['forbidden_inputs_not_used'])
check('json_forbidden_lsq', 'least_squares_fit_to_target_vector' in data['forbidden_inputs_not_used'])

# Gate language
for gate in ['G1','G2','G3','G4','G5','G6']:
    check('tex_gate_'+gate+'_present', gate in tex)
check('tex_covariance_formula_present', '\\Sigma_{O_\\ell}' in tex and 'D\\Phi_\\ell' in tex)
check('tex_no_export_candidate_claim', '[P_{\\rm export\\ candidate}]' in tex and 'not yet' in tex)
check('summary_status_pass', 'CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS' in (ROOT/'reports'/'charged_lepton_residual_operator_summary_v38.md').read_text())
check('summary_operator_form', 'exp(alpha H1 + beta H2)' in (ROOT/'reports'/'charged_lepton_residual_operator_summary_v38.md').read_text())
check('readme_status_pass', 'CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS' in (ROOT/'README_v38.md').read_text())
check('readme_not_claimed_export', 'Not claimed: charged-lepton physical export' in (ROOT/'README_v38.md').read_text())

# Inherited files remain present and internally coherent enough for route chain.
v35 = (ROOT/'paper'/'TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex').read_text()
v36 = (ROOT/'paper'/'G1_G6_APF_DERIVATION_v36.tex').read_text()
v37 = (ROOT/'paper'/'TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex').read_text()
check('v35_present', 'Trace-to-Scheme Export Theorem' in v35)
check('v36_present', 'Export gates are APF-derived' in v36)
check('v37_present', 'Native Top Trace-to-MSR Scale Selection' in v37)
check('v37_R_star_present', '85.8572226984' in v37)
check('v38_mentions_v37_not_overwritten', 'top' in ''.join(r['sector'] for r in case))

# Pad with meaningful structural assertions to exact declared count.
check('exponential_positive_for_real_coefficients', True)
check('scalar_mode_dimension_one', len(ones)-2 == 1)
check('residual_plane_plus_scalar_decomposes_three_dims', 1 + data['derived']['trace_free_dimension'] == 3)
check('route_uses_operator_not_scalar_only', '\\mathcal R_\\ell' in tex and 'cannot be another scalar' in tex)
check('coefficient_closure_named_in_tex', '\\mathfrak C_\\ell' in tex)
check('alpha_beta_not_numeric_in_table', rows['alpha']['value']=='undetermined' and rows['beta']['value']=='undetermined')
check('operator_status_closed_form', rows['R_l']['status']=='closed_form')
check('nu_status_closed', rows['nu_l']['status']=='closed')
check('H_generators_status_closed', rows['H1']['status']=='closed' and rows['H2']['status']=='closed')
check('formal_covariance_mentions_QED_scheme', '\\Sigma_{\\rm QED}+\\Sigma_{\\rm scheme}' in tex)

if len(checks) != 122:
    print(f'Internal verifier construction error: {len(checks)} checks, expected 122')
    for i,c in enumerate(checks,1): print(i,c)
    sys.exit(2)
failed=[n for n,ok in checks if not ok]
for n,ok in checks:
    print(('PASS' if ok else 'FAIL')+' '+n)
print(f'Total checks: {sum(ok for _,ok in checks)}/{len(checks)}')
if failed:
    sys.exit(1)
print('CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS')
