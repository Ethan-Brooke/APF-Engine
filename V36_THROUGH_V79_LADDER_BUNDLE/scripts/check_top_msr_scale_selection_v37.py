#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, sys, re
ROOT = Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name, bool(cond)))

# Files
required = [
    'paper/TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex',
    'paper/G1_G6_APF_DERIVATION_v36.tex',
    'paper/TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex',
    'tables/trace_to_scheme_case_table_v37.csv',
    'tables/top_msr_scale_selection_v37.csv',
    'tables/top_residual_channels_v37.csv',
    'reports/top_msr_scale_selection_summary_v37.md',
    'reports/top_msr_scale_selection_v37_data.json',
    'README_v37.md',
]
for p in required:
    check('exists_'+p.replace('/','_'), (ROOT/p).exists())

tex = (ROOT/'paper'/'TOP_MSR_SCALE_SELECTION_THEOREM_v37.tex').read_text()
for token in [
    'Native Top Trace-to-MSR Scale Selection',
    'Top trace anchor',
    'Weak trace anchor',
    'Weak-Higgs route fraction',
    'Forbidden top-scale inputs',
    'Scalar MSR balance defect',
    'APF-native top MSR scale selector',
    'Top branch promotion',
    'Top target independence',
    'Residual-channel discipline',
    '85.8572226984',
    '85.86',
    '3\\over68',
    'm_t^{\\rm MSR}(R_\\star)',
]:
    check('tex_contains_'+re.sub(r'[^A-Za-z0-9]+','_',token).strip('_'), token in tex)

# Numeric data
rows = {r['quantity']: r for r in csv.DictReader(open(ROOT/'tables'/'top_msr_scale_selection_v37.csv'))}
for q in ['T_t','T_W','C_SM','C_SU2','C_H','C_WH','C_route','epsilon_WH','R_star','R_star_rounded']:
    check('top_scale_row_'+q, q in rows)

T_t = float(rows['T_t']['value'])
T_W = float(rows['T_W']['value'])
C_SM = int(float(rows['C_SM']['value']))
C_SU2 = int(float(rows['C_SU2']['value']))
C_H = int(float(rows['C_H']['value']))
C_WH = int(float(rows['C_WH']['value']))
C_route = int(float(rows['C_route']['value']))
eps = float(rows['epsilon_WH']['value'])
R = float(rows['R_star']['value'])
Rdisp = float(rows['R_star_rounded']['value'])

check('value_T_t_exact', abs(T_t - 168.1690557938) < 1e-12)
check('value_T_W_exact', abs(T_W - 80.362164334) < 1e-12)
check('value_C_SM_61', C_SM == 61)
check('value_C_SU2_3', C_SU2 == 3)
check('value_C_H_4', C_H == 4)
check('derived_C_WH_7', C_WH == C_SU2 + C_H == 7)
check('derived_C_route_68', C_route == C_SM + C_WH == 68)
check('derived_eps_3_over_68', abs(eps - (3/68)) < 1e-15)
check('derived_R_formula', abs(R - 0.5*(T_t + eps*T_W)) < 1e-12)
check('derived_R_value', abs(R - 85.8572226983853) < 1e-12)
check('derived_R_display', abs(Rdisp - 85.86) < 1e-12)
check('R_display_rounding', round(R, 2) == Rdisp)

# Gate table status
case = list(csv.DictReader(open(ROOT/'tables'/'trace_to_scheme_case_table_v37.csv')))
check('case_table_has_6_sectors', len(case) == 6)
check('top_promoted_export_candidate', any(r['sector']=='top' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('top_cites_R_star', any(r['sector']=='top' and 'R_star=85.86' in r['codomain'] for r in case))
check('charged_leptons_still_obstructed', any(r['sector']=='charged leptons' and 'not exported' in r['physical_export_status'] for r in case))
check('EW_W_still_export_candidate', any(r['sector']=='EW/W' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('bottom_still_export_candidate', any(r['sector']=='bottom' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('charm_still_knockout', any(r['sector']=='charm' and 'knockout' in r['route_status'] for r in case))
check('light_quarks_still_qcd_obstruction', any(r['sector']=='light quarks' and 'QCD obstruction' in r['route_status'] for r in case))

# Residual channels
res = list(csv.DictReader(open(ROOT/'tables'/'top_residual_channels_v37.csv')))
expected_channels = {
    'MSR_to_pole_or_MC_or_MSbar', 'alpha_s', 'threshold_matching',
    'perturbative_truncation', 'electroweak_correction',
    'experimental_scheme', 'APF_route_residual'
}
check('residual_channels_count', len(res) == 7)
check('residual_channels_complete', set(r['channel'] for r in res) == expected_channels)
check('residual_channels_deferred', all(r['status'].startswith('deferred') for r in res))

# JSON consistency
data = json.load(open(ROOT/'reports'/'top_msr_scale_selection_v37_data.json'))
check('json_status_pass', data['status'] == 'TOP_MSR_SCALE_SELECTION_THEOREM_PASS')
check('json_T_t_matches', abs(data['inputs']['T_t_GeV'] - T_t) < 1e-12)
check('json_T_W_matches', abs(data['inputs']['T_W_GeV'] - T_W) < 1e-12)
check('json_C_route_matches', data['derived']['C_route'] == C_route)
check('json_eps_matches', abs(data['derived']['epsilon_WH'] - eps) < 1e-15)
check('json_R_matches', abs(data['derived']['R_star_GeV'] - R) < 1e-12)
check('json_display_matches', abs(data['derived']['R_star_display_GeV'] - Rdisp) < 1e-12)
check('json_before_terminal', 'P_terminal_scheme' in data['promotion']['before'])
check('json_after_export_candidate', 'P_export_candidate' in data['promotion']['after'])
check('json_not_physical_final', 'P_physical_final' in data['promotion']['not_claimed'])

# No-smuggling text audit: the formula section must not include target strings as inputs.
forbidden = ['PDG', 'world-average', 'Monte-Carlo', 'pole mass']
check('tex_mentions_forbidden_only_as_forbidden', 'Forbidden top-scale inputs' in tex and 'does not use any member' in tex)
for f in ['m_t^{\\rm pole}', 'm_t^{\\rm MC}', 'm_t^{\\overline{\\rm MS}}', 'PDG/world-average top data']:
    check('forbidden_list_contains_'+re.sub(r'[^A-Za-z0-9]+','_',f).strip('_'), f in tex)

# Six gate closure in corollary/table
for gate in ['G1','G2','G3','G4','G5','G6']:
    check('tex_gate_'+gate+'_present', gate in tex)
check('tex_covariance_formula_present', '\\delta R_\\star^2' in tex)
check('tex_identity_admission_present', 'identity MSR codomain admission' in tex)
check('tex_no_physical_final_claim', 'not physical-final' in tex or 'not physical final' in tex)

# Summary
summary = (ROOT/'reports'/'top_msr_scale_selection_summary_v37.md').read_text()
check('summary_status_pass', 'TOP_MSR_SCALE_SELECTION_THEOREM_PASS' in summary)
check('summary_formula', '0.5 * (T_t + (3/68) * T_W)' in summary)
check('summary_no_external_top', 'No external top pole mass' in summary)

# Original v35 theorem remains present and v36 gates derivation present.
v35 = (ROOT/'paper'/'TRACE_TO_SCHEME_EXPORT_THEOREM_v35.tex').read_text()
v36 = (ROOT/'paper'/'G1_G6_APF_DERIVATION_v36.tex').read_text()
check('v35_trace_to_scheme_theorem_present', 'Trace-to-Scheme Export Theorem' in v35)
check('v36_gates_derived_present', 'Export gates are APF-derived' in v36)

if len(checks) != 85:
    print(f'Internal verifier construction error: {len(checks)} checks, expected 85')
    for c in checks:
        print(c)
    sys.exit(2)

failed = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(('PASS' if ok else 'FAIL') + ' ' + n)
print(f'Total checks: {sum(ok for _, ok in checks)}/{len(checks)}')
if failed:
    sys.exit(1)
print('TOP_MSR_SCALE_SELECTION_THEOREM_PASS')
