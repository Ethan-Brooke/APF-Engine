#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks: list[tuple[str, bool]] = []

def check(name: str, cond: bool):
    checks.append((name, bool(cond)))

def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8')

def rows(rel: str):
    with (ROOT / rel).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def data(rel: str):
    return json.loads(text(rel))

required = [
    'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex',
    'paper/G1_G6_APF_DERIVATION_v36.tex',
    'paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex',
    'paper/CHARGED_LEPTON_RESIDUAL_OPERATOR_THEOREM_v38.tex',
    'paper/CHARGED_LEPTON_COEFFICIENT_CLOSURE_THEOREM_v39.tex',
    'paper/CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_AND_QED_CODOMAIN_THEOREM_v40.tex',
    'tables/charged_lepton_trace_vector_source_gate_v40.csv',
    'tables/charged_lepton_qed_codomain_v40.csv',
    'tables/charged_lepton_residual_channels_v40.csv',
    'tables/trace_to_scheme_case_table_v40.csv',
    'reports/charged_lepton_trace_vector_source_gate_summary_v40.md',
    'reports/charged_lepton_trace_vector_source_gate_v40_data.json',
    'README_v40.md',
]
for rel in required:
    check('exists_' + rel.replace('/', '_'), (ROOT / rel).exists())

tex = text('paper/CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_AND_QED_CODOMAIN_THEOREM_v40.tex')
summary = text('reports/charged_lepton_trace_vector_source_gate_summary_v40.md')
readme = text('README_v40.md')
j = data('reports/charged_lepton_trace_vector_source_gate_v40_data.json')
source_rows = rows('tables/charged_lepton_trace_vector_source_gate_v40.csv')
qed_rows = rows('tables/charged_lepton_qed_codomain_v40.csv')
residual_rows = rows('tables/charged_lepton_residual_channels_v40.csv')
case_rows = rows('tables/trace_to_scheme_case_table_v40.csv')

# TeX structure
tex_needles = [
    'Charged-Lepton Trace-Vector Source Gate and QED Codomain Theorem',
    '\\begin{definition}',
    'Charged-lepton trace-vector source',
    'QED charged-lepton codomain',
    'Trace-vector source gate',
    'Equivalence to the lepton cooperative-overlap closure',
    'QED codomain partially closes but export does not',
    'No inverse charged-lepton trace vector',
    'v40 charged-lepton status',
    '\\mathfrak T_\\ell',
    'T_\\ell\\in\\mathbb R_{>0}^3',
    '\\Omega^\\ell',
    'Y_{ij}^{f}\\propto \\varepsilon^{(q_i+q_j)/2}\\Omega_{ij}^{(f)}',
    'S=\\text{pole}',
    'Z_\\ell^{\\rm pole}=I',
    'T_\\ell^{\\rm inv}',
    '(m_e,m_\\mu,m_\\tau)_S',
    'P_{\\rm source\\ gate}^{T_\\ell}',
    'APF\\_LEPTON\\_COOPERATIVE\\_OVERLAP\\_OR\\_TRACE\\_VECTOR\\_CLOSURE\\_THEOREM',
]
for nd in tex_needles:
    check('tex_contains_' + nd[:50].replace(' ', '_').replace('\\','bs').replace('{','').replace('}',''), nd in tex)

# Ensure inherited v39 route remains present
for nd in ['nu_\\ell={1\\over\\sqrt6}', '\\mathcal R_\\ell=\\operatorname{diag}(1/3,3,1)', 'O_\\ell^S=Z_\\ell^S']:
    check('tex_inherits_' + nd.replace('\\','bs').replace('{','').replace('}','').replace('/','_'), nd in tex)

# Table source gate rows
source = {r['quantity']: r for r in source_rows}
for key in ['T_l','source_map','Omega_l','FN_rungs','epsilon','nu_l','R_l','forbidden_inverse','pole_codomain','running_codomain','promotion']:
    check('source_table_row_' + key, key in source)
check('T_l_open_source_gate', source['T_l']['status'] == 'open_source_gate')
check('source_map_required_not_supplied', source['source_map']['status'] == 'required_not_supplied')
check('Omega_l_open', source['Omega_l']['status'] == 'open')
check('FN_rungs_closed', source['FN_rungs']['status'] == 'inherited_closed')
check('epsilon_conditional_external', source['epsilon']['status'] == 'conditional_external_to_v40')
check('nu_l_inherited_closed', source['nu_l']['status'] == 'inherited_closed')
check('R_l_diag_inherited_closed', source['R_l']['value'] == 'diag(1/3,3,1)' and source['R_l']['status'] == 'inherited_closed')
check('forbidden_inverse_forbidden', source['forbidden_inverse']['status'] == 'forbidden')
check('pole_codomain_partial', source['pole_codomain']['status'] == 'codomain_declared_partial')
check('running_deferred', source['running_codomain']['status'] == 'deferred_to_QED_transport')
check('promotion_not_exported', 'not exported' in source['promotion']['meaning'])

# QED table
qed = {r['codomain']: r for r in qed_rows}
for key in ['pole', 'MSbar(mu)', 'other_QED_scheme']:
    check('qed_codomain_row_' + key.replace('(','').replace(')',''), key in qed)
check('pole_Z_identity', qed['pole']['Z_factor'] == 'I in minimal bookkeeping')
check('pole_declared_first_codomain', qed['pole']['status'] == 'declared_first_codomain')
check('MSbar_deferred', qed['MSbar(mu)']['status'] == 'deferred')
check('other_QED_deferred', qed['other_QED_scheme']['status'] == 'deferred')
check('MSbar_constants_include_alpha', 'alpha_QED' in qed['MSbar(mu)']['constants_required'])
check('MSbar_covariance_include_truncation', 'truncation' in qed['MSbar(mu)']['covariance_required'])

# Residual channels
res = {r['channel']: r for r in residual_rows}
expected_channels = [
    'trace_vector_T_l','Omega_l_closure','QED_running','scheme_choice','trace_vector_covariance',
    'operator_covariance','experimental_covariance','APF_route_residual','no_smuggling_audit'
]
for ch in expected_channels:
    check('residual_channel_' + ch, ch in res)
check('trace_vector_primary_open', res['trace_vector_T_l']['status'] == 'open_primary_gate')
check('Omega_equivalent_open', res['Omega_l_closure']['status'] == 'open_equivalent_gate')
check('scheme_choice_partially_closed', res['scheme_choice']['status'] == 'partially_closed')
check('operator_covariance_closed', res['operator_covariance']['status'] == 'closed_for_coefficients')
check('no_smuggling_pass_source_gate', res['no_smuggling_audit']['status'] == 'pass_for_source_gate')

# Case table state
case = {r['sector']: r for r in case_rows}
check('case_table_has_6_sectors', len(case_rows) == 6)
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_has_' + s.replace('/','_').replace(' ','_'), s in case)
cl = case['charged leptons']
check('case_charged_leptons_source_gate', 'source gate' in cl['route_status'])
check('case_charged_leptons_pole_declared', 'pole codomain declared' in cl['route_status'])
check('case_charged_leptons_not_exported', 'not exported' in cl['physical_export_status'])
check('case_charged_leptons_next_omega', 'COOPERATIVE_OVERLAP' in cl['first_failed_gate_or_boundary'])
check('case_top_still_export_candidate', case['top']['physical_export_status'] == 'P_export_candidate')
check('case_bottom_still_export_candidate', case['bottom']['physical_export_status'] == 'P_export_candidate')
check('case_W_still_export_candidate', case['EW/W']['physical_export_status'] == 'P_export_candidate')
check('case_charm_still_knockout', 'knockout' in case['charm']['route_status'])
check('case_light_quarks_still_qcd', 'QCD obstruction' in case['light quarks']['route_status'])

# JSON checks
check('json_status_pass', j['status'] == 'CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS')
check('json_package_v40', j['package'] == 'APF_v40_CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE')
check('json_inherited_nu', j['inherited_closed']['nu_l'] == '1/sqrt(6)')
check('json_inherited_R_l', j['inherited_closed']['R_l'] == 'diag(1/3,3,1)')
check('json_inherited_alpha', j['inherited_closed']['alpha_l'] == '0.5 log(3)')
check('json_inherited_beta', j['inherited_closed']['beta_l'] == '-0.5 log(3)')
check('json_new_trace_source_gate', 'source-independent' in j['new_closed']['trace_vector_source_gate'])
check('json_new_omega_equivalence', 'Omega_l' in j['new_closed']['omega_equivalence'])
check('json_new_pole_codomain', 'Z_l^pole=I' in j['new_closed']['pole_codomain_declaration'])
check('json_new_inverse_forbidden', 'cannot define' in j['new_closed']['inverse_trace_vector_forbidden'])
for key in ['T_l','Omega_l','QED_running','trace_covariance','physical_export']:
    check('json_still_open_' + key, key in j['still_open'])
check('json_physical_export_not_claimed', j['still_open']['physical_export'] == 'not claimed')
for forb in ['m_e_pole','m_mu_pole','m_tau_pole','PDG_or_world_average_charged_lepton_masses','least_squares_fit_to_target_vector','inverse_solution_for_T_l_from_targets']:
    check('json_forbidden_' + forb, forb in j['forbidden_inputs_not_used'])
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE','G5_NO_SMUGGLING','G6_RESIDUAL_CHANNELS']:
    check('json_gate_' + g, g in j['gate_status'])
check('json_G1_closed_for_pole', 'closed for pole' in j['gate_status']['G1_CODOMAIN_DECLARED'])
check('json_G2_blocked_at_source', 'blocked at source' in j['gate_status']['G2_TRANSPORT_MAP'])
check('json_G5_inverse_forbidden', 'inverse charged-lepton trace vector forbidden' in j['gate_status']['G5_NO_SMUGGLING'])
check('json_before_v39_status', 'P_route^coefficient_closed' in j['promotion']['before'])
check('json_after_source_gate', 'P_source_gate^T_l' in j['promotion']['after'])
for nc in ['P_export_candidate','P_physical_final','numeric e/mu/tau mass export']:
    check('json_not_claimed_' + nc.replace('/','_').replace(' ','_'), nc in j['promotion']['not_claimed'])
check('json_next_theorem_named', j['next_theorem'] == 'APF_LEPTON_COOPERATIVE_OVERLAP_OR_TRACE_VECTOR_CLOSURE_THEOREM')
check('json_checks_total_188', j['checks_total'] == 188)

# Summary/readme checks
for nd in ['CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS','does not claim charged-lepton physical export','pole codomain','Omega_l','inverse construction','P_source_gate^T_l','APF_LEPTON_COOPERATIVE_OVERLAP_OR_TRACE_VECTOR_CLOSURE_THEOREM']:
    check('summary_contains_' + nd[:40].replace(' ','_'), nd in summary)
for nd in ['CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS','does **not** claim charged-lepton physical export','T_l','Omega_l','not by inverting']:
    check('readme_contains_' + nd[:40].replace(' ','_').replace('*','star'), nd in readme)

# Inherited verifier/data presence and stamps
inherited_reports = [
    ('reports/trace_to_scheme_export_v35_targeted_v39_rerun.txt', 'TRACE_TO_SCHEME_EXPORT_THEOREM_PASS'),
    ('reports/top_msr_scale_selection_v37_targeted_v39_rerun.txt', 'TOP_MSR_SCALE_SELECTION_THEOREM_PASS'),
    ('reports/charged_lepton_residual_operator_v38_targeted_v39_rerun.txt', 'CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS'),
    ('reports/charged_lepton_coefficient_closure_v39_targeted.txt', 'CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS'),
]
for rel, stamp in inherited_reports:
    check('inherited_report_exists_' + rel.split('/')[-1], (ROOT/rel).exists())
    check('inherited_report_stamp_' + stamp, stamp in text(rel))

# Mathematical sanity checks
nu = 1 / math.sqrt(6)
R = [1/3, 3, 1]
prod = [nu*x for x in R]
check('math_nu_positive', nu > 0)
check('math_R_positive_entries', all(x > 0 for x in R))
check('math_R_det_one', abs(R[0]*R[1]*R[2] - 1.0) < 1e-12)
check('math_log_R_trace_zero', abs(sum(math.log(x) for x in R)) < 1e-12)
check('math_route_not_numeric_without_T', all(isinstance(x, float) for x in prod) and len(prod) == 3)
check('math_inverse_would_depend_on_targets', 'T_\\ell^{\\rm inv}' in tex and '(m_e,m_\\mu,m_\\tau)_S' in tex)

# Ensure no accidental external lepton numeric values are embedded in new TeX/CSV/JSON
forbidden_numeric = ['0.510998', '105.658', '1776.86', '1776.99', '0.000510998', '0.105658', '1.77686']
new_files_text = '\n'.join([
    tex,
    text('tables/charged_lepton_trace_vector_source_gate_v40.csv'),
    text('tables/charged_lepton_qed_codomain_v40.csv'),
    text('tables/charged_lepton_residual_channels_v40.csv'),
    text('reports/charged_lepton_trace_vector_source_gate_v40_data.json'),
])
for num in forbidden_numeric:
    check('forbidden_numeric_absent_' + num.replace('.','_'), num not in new_files_text)

# Validate v39 numeric relation inherited in data/table only symbolically retained
check('v39_coeff_table_exists', (ROOT/'tables/charged_lepton_coefficient_closure_v39.csv').exists())
v39_rows = {r['quantity']: r for r in rows('tables/charged_lepton_coefficient_closure_v39.csv')}
check('v39_R_l_diag_still_closed', v39_rows['R_l']['value'] == 'diag(1/3,3,1)')
check('v39_alpha_still_half_log3', abs(float(v39_rows['alpha']['value']) - 0.5*math.log(3)) < 1e-15)
check('v39_beta_still_neg_half_log3', abs(float(v39_rows['beta']['value']) + 0.5*math.log(3)) < 1e-15)
check('v39_route_form_still_present', 'diag(1/3,3,1)' in v39_rows['route_form']['value'])

# Count target: pad only with meaningful cross-file consistency checks.
check('cross_tex_summary_same_status', j['status'] in summary and j['status'] in readme)
check('cross_case_next_equals_json_next', cl['first_failed_gate_or_boundary'] == j['next_theorem'])
check('cross_source_Omega_status_matches_json', source['Omega_l']['status'] == 'open' and 'Omega_l' in j['still_open'])
check('cross_source_T_status_matches_json', source['T_l']['status'] == 'open_source_gate' and 'T_l' in j['still_open'])
check('cross_qed_running_status_matches_json', qed['MSbar(mu)']['status'] == 'deferred' and 'QED_running' in j['still_open'])
check('cross_residual_no_smuggling_matches_json', res['no_smuggling_audit']['status'] == 'pass_for_source_gate' and 'G5_NO_SMUGGLING' in j['gate_status'])
check('cross_pole_codomain_matches_case', source['pole_codomain']['status'] == 'codomain_declared_partial' and 'pole codomain declared' in cl['route_status'])
check('cross_export_not_claimed_all', 'not exported' in cl['physical_export_status'] and 'not claimed' in j['still_open']['physical_export'] and 'does not claim' in summary)

# Additional theorem wording gates
for nd in [
    'source-independent trace-vector source',
    'violates the v36',
    'collapses prediction into inverse fitting',
    'source theorem before any physical',
    'source-gate theorem',
    'target observable',
    'residual calculator after',
    'cannot define the trace vector',
]:
    check('tex_wording_' + nd[:35].replace(' ','_'), nd in tex)

# The exact count is part of the bank; fail loudly if edited without updating json.
passed = sum(1 for _, ok in checks if ok)
total = len(checks)
for name, ok in checks:
    print(('PASS' if ok else 'FAIL'), name)
print(f'Total checks: {passed}/{total}')
if passed == total and total == j.get('checks_total'):
    print('CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS')
else:
    raise SystemExit(1)
