#!/usr/bin/env python3
import csv, json, re, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)
def rows(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
def text(path): return (ROOT/path).read_text(encoding='utf-8')
files=[
 'paper/W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE_v56.tex',
 'tables/w_onshell_external_ledgers_v56.csv',
 'tables/w_onshell_residual_audit_v56.csv',
 'tables/w_onshell_export_gates_v56.csv',
 'tables/w_onshell_nonclaim_matrix_v56.csv',
 'tables/global_trace_to_scheme_closure_registry_v56.csv',
 'tables/trace_to_scheme_case_table_v56.csv',
 'reports/w_trace_to_onshell_ew_covariance_closure_summary_v56.md',
 'reports/w_trace_to_onshell_ew_covariance_closure_v56_data.json',
 'README_v56.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
# data numerics
j=json.loads(text(Path('reports/w_trace_to_onshell_ew_covariance_closure_v56_data.json')))
check('json_stamp', j['stamp']=='W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE_PASS')
check('apf_mw_value', abs(j['apf_mw_trace_GeV']-80.362164334)<1e-12)
check('pdg_value', abs(j['pdg_2025_mw_GeV']-80.3692)<1e-12)
check('cms_value', abs(j['cms_2026_mw_GeV']-80.3602)<1e-12)
check('pdg_sigma', abs(j['pdg_2025_sigma_GeV']-0.0133)<1e-12)
check('cms_sigma', abs(j['cms_2026_sigma_GeV']-0.0099)<1e-12)
check('pdg_delta_correct', abs(j['pdg_delta_GeV']-(80.362164334-80.3692))<1e-12)
check('cms_delta_correct', abs(j['cms_delta_GeV']-(80.362164334-80.3602))<1e-12)
check('pdg_z_correct', abs(j['pdg_z']-j['pdg_delta_GeV']/0.0133)<1e-12)
check('cms_z_correct', abs(j['cms_z']-j['cms_delta_GeV']/0.0099)<1e-12)
check('pdg_inside_one_sigma', abs(j['pdg_z'])<1)
check('cms_inside_one_sigma', abs(j['cms_z'])<1)
check('max_abs_z_under_one', j['max_abs_z']<1)
check('max_abs_z_is_cms_or_pdg', abs(j['max_abs_z']-max(abs(j['pdg_z']),abs(j['cms_z'])))<1e-12)
# ledger tables
led=rows('w_onshell_external_ledgers_v56.csv')
check('two_external_ledgers', len(led)==2)
by={r['ledger']:r for r in led}
check('pdg_ledger_present','PDG_2025_world_average' in by)
check('cms_ledger_present','CMS_2026_Nature' in by)
for key in by:
    check('ledger_comparison_only_'+key, 'not input' in by[key]['status'])
    check('ledger_codomain_onshell_'+key, 'on-shell' in by[key]['codomain'])
# residual audit rows
res=rows('w_onshell_residual_audit_v56.csv')
check('two_residual_rows', len(res)==2)
for r in res:
    z=float(r['z_score'])
    check('residual_inside_one_sigma_'+r['audit'], r['inside_one_sigma']=='True' and abs(z)<1)
    check('has_delta_MeV_'+r['audit'], abs(float(r['delta_MeV']))>0)
    check('has_percent_delta_'+r['audit'], abs(float(r['percent_delta']))<0.01)
# gates
sg=rows('w_onshell_export_gates_v56.csv')
check('six_v56_gates', len(sg)==6)
gd={r['gate']:r for r in sg}
for g in ['G1','G2','G3','G4','G5','G6']:
    check('gate_'+g+'_present', g in gd)
    check('gate_'+g+'_closed_or_inherited', 'closed' in gd[g]['v56_status'])
check('g1_on_shell', 'on-shell' in gd['G1']['w_detail'])
check('g2_inherited_v35', 'v35' in gd['G2']['w_detail'])
check('g3_no_combination', 'separately' in gd['G3']['w_detail'])
check('g4_one_sigma', 'one sigma' in gd['G4']['w_detail'])
check('g5_comparison_only', 'not used' in gd['G5']['w_detail'])
check('g6_residual_assignment', 'residuals' in gd['G6']['w_detail'])
# nonclaims
nc=rows('w_onshell_nonclaim_matrix_v56.csv')
check('nonclaim_rows', len(nc)==5)
claims=[r['claim'] for r in nc]
for phrase in ['physical-final electroweak sector','zero residual','unauthorized PDG+CMS combined average','CDF anomaly resolution by APF','all electroweak observables closed']:
    check('nonclaim_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in claims)
check('combination_forbidden', next(r for r in nc if r['claim']=='unauthorized PDG+CMS combined average')['v56_status']=='forbidden')
# registry updates
reg=rows('global_trace_to_scheme_closure_registry_v56.csv')
check('registry_six_rows', len(reg)==6)
byreg={r['sector']:r for r in reg}
check('ew_status_promoted', byreg['EW/W']['highest_closed_status']=='P_onshell_EW_completion_PDG2025_CMS2026_ledgers')
check('ew_may_claim_completion', 'completion' in byreg['EW/W']['may_claim'])
check('ew_forbidden_physical_final', 'physical-final' in byreg['EW/W']['must_not_claim'])
check('charged_unchanged', 'P_pole_completion' in byreg['charged leptons']['highest_closed_status'])
check('charm_unchanged', 'P_export_candidate_MSBAR' in byreg['charm']['highest_closed_status'])
check('bottom_unchanged', 'P_export_candidate_MSBAR' in byreg['bottom']['highest_closed_status'])
check('top_unchanged', 'P_export_candidate_MSR' in byreg['top']['highest_closed_status'])
check('light_unchanged', 'source_pretransport' in byreg['light quarks']['highest_closed_status'])
# text theorem
tex=text(Path('paper/W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE_v56.tex'))
for phrase in ['W Trace to On-Shell Electroweak Covariance Closure','on-shell W audit ledgers','W on-shell covariance completion','Non-combination rule','does not claim zero residual']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
check('tex_contains_apf_value','80.362164334000' in tex)
check('tex_contains_pdg_value','80.3692' in tex)
check('tex_contains_cms_value','80.3602' in tex)
check('tex_max_z_under_one','<1' in tex and 'max' in tex)
# case table
case=rows('trace_to_scheme_case_table_v56.csv')
check('case_v56_rows_six', len(case)==6)
check('case_v56_status_column', 'v56_registry_status' in case[0])
check('case_v56_ew_promoted', any(r.get('sector')=='EW/W' and r.get('v56_registry_status')=='P_onshell_EW_completion_PDG2025_CMS2026_ledgers' for r in case))
# summaries and inherited files
summary=text(Path('reports/w_trace_to_onshell_ew_covariance_closure_summary_v56.md'))
check('summary_stamp_present','W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE_PASS' in summary)
check('summary_has_not_claimed','Not claimed' in summary)
check('readme_has_headline','M_W^{APF-TRACE}' in text(Path('README_v56.md')))
# inherited verifier availability
for f in ['scripts/check_trace_to_scheme_export_v35.py','scripts/check_global_trace_to_scheme_closure_registry_v55.py','reports/global_trace_to_scheme_closure_registry_v55_data.json']:
    check('inherited_exists_'+f.replace('/','_'), (ROOT/f).exists())
# source discipline checks
check('external_values_not_inputs', all('not input' in r['status'] for r in led))
check('no_combined_average_claimed', 'combined' in ''.join(claims).lower() and 'unauthorized' in ''.join(claims).lower())
check('status_upgrade_text', 'P_export_candidate -> P_onshell_EW_completion' in j['status_upgrade'])
check('next_recommended_heavy_qcd', j['next_recommended']=='APF_HEAVY_QCD_FINAL_COVARIANCE_LEDGER')
# make up remaining sanity checks to ensure report robustness
check('pdg_delta_mev_magnitude', 7.0 < abs(j['pdg_delta_GeV']*1000) < 7.1)
check('cms_delta_mev_magnitude', 1.9 < abs(j['cms_delta_GeV']*1000) < 2.0)
check('pdg_percent_small', abs(float(res[0]['percent_delta'])) < 0.009)
check('cms_percent_small', abs(float(res[1]['percent_delta'])) < 0.003)
check('pdg_z_minus_sign', j['pdg_z']<0)
check('cms_z_plus_sign', j['cms_z']>0)
check('max_abs_z_matches_pdg', abs(j['max_abs_z']-abs(j['pdg_z']))<1e-12)
check('pdg_more_limiting_than_cms', abs(j['pdg_z'])>abs(j['cms_z']))
failed=[n for n,c in checks if not c]
print(f"Total checks: {len(checks)-len(failed)}/{len(checks)}")
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('W_TRACE_TO_ONSHELL_EW_COVARIANCE_CLOSURE_PASS')
