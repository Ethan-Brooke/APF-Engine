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
def text(path):
    return (ROOT/path).read_text(encoding='utf-8')
files=[
 'paper/HEAVY_QCD_FINAL_COVARIANCE_LEDGER_v57.tex',
 'tables/heavy_qcd_external_ledger_v57.csv',
 'tables/heavy_qcd_residual_audit_v57.csv',
 'tables/top_msr_boundary_v57.csv',
 'tables/heavy_qcd_export_gates_v57.csv',
 'tables/heavy_qcd_status_ladder_v57.csv',
 'tables/heavy_qcd_nonclaim_matrix_v57.csv',
 'tables/global_trace_to_scheme_closure_registry_v57.csv',
 'tables/trace_to_scheme_case_table_v57.csv',
 'reports/heavy_qcd_final_covariance_ledger_summary_v57.md',
 'reports/heavy_qcd_final_covariance_ledger_v57_data.json',
 'README_v57.md'
]
for f in files:
    check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(text(Path('reports/heavy_qcd_final_covariance_ledger_v57_data.json')))
check('stamp', j['stamp']=='HEAVY_QCD_FINAL_COVARIANCE_LEDGER_PASS')
check('charm_apf', abs(j['charm']['apf_GeV']-1.272334177712)<1e-12)
check('bottom_apf', abs(j['bottom']['apf_GeV']-4.177490455927)<1e-12)
check('charm_pdg', abs(j['charm']['pdg_GeV']-1.2730)<1e-12)
check('bottom_pdg', abs(j['bottom']['pdg_GeV']-4.183)<1e-12)
check('charm_err90', abs(j['charm']['pdg_error_90CL_GeV']-0.0046)<1e-12)
check('bottom_err90', abs(j['bottom']['pdg_error_90CL_GeV']-0.007)<1e-12)
check('charm_delta', abs(j['charm']['delta_GeV']-(1.272334177712-1.2730))<1e-12)
check('bottom_delta', abs(j['bottom']['delta_GeV']-(4.177490455927-4.183))<1e-12)
check('charm_inside_90', j['charm']['inside_quoted_90CL'] is True)
check('bottom_inside_90', j['bottom']['inside_quoted_90CL'] is True)
check('charm_ratio_under_one', abs(j['charm']['ratio_to_90CL'])<1)
check('bottom_ratio_under_one', abs(j['bottom']['ratio_to_90CL'])<1)
check('max_ratio_under_one', j['max_abs_ratio_to_quoted_90CL']<1)
check('z90_constant_charm', abs(j['charm']['gaussian_equiv_sigma_GeV']-0.0046/1.6448536269514722)<1e-12)
check('z90_constant_bottom', abs(j['bottom']['gaussian_equiv_sigma_GeV']-0.007/1.6448536269514722)<1e-12)
check('charm_zeq_correct', abs(j['charm']['gaussian_equiv_z']-j['charm']['delta_GeV']/j['charm']['gaussian_equiv_sigma_GeV'])<1e-12)
check('bottom_zeq_correct', abs(j['bottom']['gaussian_equiv_z']-j['bottom']['delta_GeV']/j['bottom']['gaussian_equiv_sigma_GeV'])<1e-12)
check('bottom_zeq_about_1p29', 1.29 < abs(j['bottom']['gaussian_equiv_z']) < 1.30)
check('top_Rstar', abs(j['top']['R_star_GeV']-85.8572226983853)<1e-9)
check('top_boundary_text', 'conversion ledger required' in j['top']['boundary'])
# tables
led=rows('heavy_qcd_external_ledger_v57.csv')
check('three_ledger_rows', len(led)==3)
by={r['sector']:r for r in led}
for s in ['charm','bottom','top']:
    check('ledger_has_'+s, s in by)
check('charm_codomain_msbar', 'MSbar self-scale' in by['charm']['codomain'])
check('bottom_codomain_msbar', 'MSbar self-scale' in by['bottom']['codomain'])
check('top_codomain_msr', 'MSR' in by['top']['codomain'])
check('charm_not_input', 'not input' in by['charm']['ledger_status'])
check('bottom_not_input', 'not input' in by['bottom']['ledger_status'])
check('top_boundary', 'boundary' in by['top']['ledger_status'])
check('charm_alpha_line', abs(float(by['charm']['alpha_s_at_scale'])-0.38)<1e-12)
check('bottom_alpha_line', abs(float(by['bottom']['alpha_s_at_scale'])-0.223)<1e-12)
res=rows('heavy_qcd_residual_audit_v57.csv')
check('two_residual_rows', len(res)==2)
for r in res:
    check('inside_90_'+r['sector'], r['inside_quoted_90CL']=='True')
    check('ratio_under_one_'+r['sector'], abs(float(r['ratio_to_quoted_90CL']))<1)
    check('delta_nonzero_'+r['sector'], abs(float(r['delta_GeV']))>0)
    check('has_gaussian_z_'+r['sector'], abs(float(r['gaussian_equiv_z']))>0)
check('charm_percent', -0.053 < float(res[0]['percent_delta']) < -0.052)
check('bottom_percent', -0.132 < float(res[1]['percent_delta']) < -0.131)
# gates
sg=rows('heavy_qcd_export_gates_v57.csv')
check('six_qcd_gates', len(sg)==6)
gd={r['gate']:r for r in sg}
for g in ['G1','G2','G3','G4','G5','G6']:
    check('gate_'+g+'_present', g in gd)
check('g1_msbar_and_msr', 'MSbar' in gd['G1']['charm'] and 'MSR' in gd['G1']['top'])
check('g2_sqrt72', 'sqrt(7/2)' in gd['G2']['charm'])
check('g3_alpha_lines', 'alpha_s' in gd['G3']['charm'] and 'alpha_s' in gd['G3']['bottom'])
check('g4_90cl', '90% CL' in gd['G4']['charm'])
check('g5_no_smuggling', 'not used' in gd['G5']['charm'] and 'not used' in gd['G5']['bottom'])
check('g6_top_boundary', 'not evaluated' in gd['G6']['top'])
# top boundary table
b=rows('top_msr_boundary_v57.csv')
check('one_top_boundary_row', len(b)==1)
check('top_forbidden_route_mentions_pdg', 'PDG' in b[0]['forbidden_route'])
check('top_allowed_route_mentions_alpha', 'alpha_s' in b[0]['allowed_next_route'])
check('top_reason_codomain', 'not m_t^MSR' in b[0]['boundary_reason'])
# status ladder
st=rows('heavy_qcd_status_ladder_v57.csv')
check('three_status_rows', len(st)==3)
sd={r['sector']:r for r in st}
check('charm_status_v57', sd['charm']['v57_status']=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90')
check('bottom_status_v57', sd['bottom']['v57_status']=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90')
check('top_status_v57', sd['top']['v57_status']=='P_MSR_Rstar_boundary_same_codomain_required')
check('top_nonclaim_direct', 'direct PDG' in sd['top']['nonclaim'])
# nonclaims
nc=rows('heavy_qcd_nonclaim_matrix_v57.csv')
check('six_nonclaims', len(nc)==6)
claims=[r['claim'] for r in nc]
for phrase in ['heavy-QCD physical finality','zero residual for charm or bottom','top pole/MC mass prediction','direct top comparison to PDG listings','using PDG c,b masses as inputs','full alpha_s covariance final']:
    check('nonclaim_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in claims)
check('direct_top_forbidden', next(r for r in nc if r['claim']=='direct top comparison to PDG listings')['v57_status']=='forbidden')
check('pdg_input_forbidden', next(r for r in nc if r['claim']=='using PDG c,b masses as inputs')['v57_status']=='forbidden')
# registry
reg=rows('global_trace_to_scheme_closure_registry_v57.csv')
check('registry_six_rows', len(reg)==6)
byreg={r['sector']:r for r in reg}
check('registry_charm_promoted', byreg['charm']['highest_closed_status']=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90')
check('registry_bottom_promoted', byreg['bottom']['highest_closed_status']=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90')
check('registry_top_boundary', byreg['top']['highest_closed_status']=='P_MSR_Rstar_boundary_same_codomain_required')
check('registry_EW_unchanged', 'P_onshell_EW_completion' in byreg['EW/W']['highest_closed_status'])
check('registry_leptons_unchanged', 'P_pole_completion' in byreg['charged leptons']['highest_closed_status'])
check('registry_light_unchanged', 'source_pretransport' in byreg['light quarks']['highest_closed_status'])
# case table
case=rows('trace_to_scheme_case_table_v57.csv')
check('case_table_six_rows', len(case)==6)
check('case_has_v57_status', 'v57_registry_status' in case[0])
check('case_charm_promoted', any(r.get('sector')=='charm' and r.get('v57_registry_status')=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90' for r in case))
check('case_bottom_promoted', any(r.get('sector')=='bottom' and r.get('v57_registry_status')=='P_MSBAR_self_scale_covariance_admitted_PDG2025_CL90' for r in case))
check('case_top_boundary', any(r.get('sector')=='top' and r.get('v57_registry_status')=='P_MSR_Rstar_boundary_same_codomain_required' for r in case))
# tex and summary
tex=text(Path('paper/HEAVY_QCD_FINAL_COVARIANCE_LEDGER_v57.tex'))
for phrase in ['Heavy-QCD Final Covariance Ledger','Charm and bottom covariance admission','Top MSR codomain boundary','v57 claim ladder','does not claim physical-final']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
check('tex_contains_charm_value','1.272334177712' in tex)
check('tex_contains_bottom_value','4.177490455927' in tex)
check('tex_contains_Rstar','85.857222698385' in tex)
check('tex_contains_90CL','90\%' in tex or '90%' in tex)
summary=text(Path('reports/heavy_qcd_final_covariance_ledger_summary_v57.md'))
check('summary_stamp','HEAVY_QCD_FINAL_COVARIANCE_LEDGER_PASS' in summary)
check('summary_contains_top_boundary','MSR(R_*)' in summary)
check('readme_headline','P_{\overline{MS} self-scale covariance admitted}' in text(Path('README_v57.md')))
# inherited verifier availability
for f in ['scripts/check_trace_to_scheme_export_v35.py','scripts/check_w_trace_to_onshell_ew_covariance_closure_v56.py','scripts/check_bottom_top_charm_shared_qcd_covariance_ledger_v51.py']:
    check('inherited_exists_'+f.replace('/','_'), (ROOT/f).exists())
# overall no-overclaim/source discipline
check('status_upgrade_mentions_top_boundary','top codomain boundary hardened' in j['status_upgrade'])
check('next_recommended_present', j['next_recommended']=='APF_TOP_MSR_CONVERSION_LEDGER_OR_PUBLICATION_SCORECARD')
check('not_claimed_physical_final','P_physical_final' in j['not_claimed'])
check('not_claimed_zero','zero_residual' in j['not_claimed'])
check('not_claimed_top','top_pole_or_MC_mass' in j['not_claimed'])
check('max_90_is_bottom', abs(j['max_abs_ratio_to_quoted_90CL']-abs(j['bottom']['ratio_to_90CL']))<1e-12)
check('max_zeq_is_bottom', abs(j['max_abs_gaussian_equiv_z']-abs(j['bottom']['gaussian_equiv_z']))<1e-12)
check('charm_residual_smaller_than_bottom', abs(j['charm']['delta_GeV']) < abs(j['bottom']['delta_GeV']))
check('both_same_codomain_closed', 'same-codomain' in summary and 'MSbar' in summary)
failed=[n for n,c in checks if not c]
print(f"Total checks: {len(checks)-len(failed)}/{len(checks)}")
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('HEAVY_QCD_FINAL_COVARIANCE_LEDGER_PASS')
