#!/usr/bin/env python3
import csv, json, math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond))); print(('PASS' if cond else 'FAIL'), name)
def rows(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def txt(path): return (ROOT/path).read_text(encoding='utf-8')
files=[
 'paper/TOP_MSR_FULL_QCD_CONVERSION_LEDGER_v59.tex',
 'tables/top_msr_full_qcd_conversion_ledger_v59.csv',
 'tables/top_msr_route_branch_map_v59.csv',
 'tables/top_msr_full_conversion_coefficient_manifest_v59.csv',
 'tables/top_msr_full_qcd_covariance_channels_v59.csv',
 'tables/top_msr_full_qcd_ledger_gates_v59.csv',
 'tables/top_msr_full_qcd_no_smuggling_matrix_v59.csv',
 'tables/global_trace_to_scheme_closure_registry_v59.csv',
 'tables/trace_to_scheme_case_table_v59.csv',
 'schemas/top_msr_full_qcd_conversion_evaluator_schema_v59.json',
 'reports/top_msr_full_qcd_conversion_ledger_v59_data.json',
 'reports/top_msr_full_qcd_conversion_ledger_summary_v59.md',
 'README_v59.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(txt(Path('reports/top_msr_full_qcd_conversion_ledger_v59_data.json')))
check('stamp', j['stamp']=='TOP_MSR_FULL_QCD_CONVERSION_LEDGER_PASS')
check('closed_status', j['closed_status']=='P_full_QCD_conversion_ledger_complete_numeric_final_blocked')
check('mt_source', abs(j['source']['m_t_MSR_Rstar_GeV']-168.1690557938)<1e-12)
check('rstar_source', abs(j['source']['Rstar_GeV']-85.8572226983853)<1e-9)
check('lo_witness_retained', 172.50<j['v58_LO_witness_retained']['top_pole_LO_witness_GeV']<172.51)
check('lo_residual_retained', abs(j['v58_LO_witness_retained']['residual_GeV']+0.053533404636)<1e-9)
for s in ['P_physical_final','exact_pole_mass','MC_mass_equality','full_multiloop_numeric_conversion','zero_residual']:
    check('not_claimed_'+s, s in j['not_claimed'])
# ledger
led=rows('top_msr_full_qcd_conversion_ledger_v59.csv')
check('ledger_min_rows', len(led)>=20)
blocks=set(r['block'] for r in led)
for b in ['APF source','QCD input','flavour scheme','color factors','beta coefficients','mass anomalous dimension','MSR coefficients','R-evolution','on-shell/MSbar','decoupling','top audit','ambiguity','MC boundary']:
    check('ledger_block_'+re.sub('[^A-Za-z0-9]+','_',b), b in blocks)
items={r['item']:r for r in led}
for item in ['m_t^MSR(R_star)','R_star','alpha_s(M_Z)','sigma_alpha_s(M_Z)','M_Z','n_f between R_star and M_Z','C_F','C_A','T_F','beta_0','beta_1','beta_2,beta_3,beta_4','gamma_m^0..gamma_m^4','delta_MSR coefficients a_1..a_4','gamma_R coefficients','OS-MSbar coefficients through four loops','zeta_g,zeta_m threshold matching','PDG direct top average','pole renormalon ambiguity','MC mass mapping']:
    check('ledger_item_'+re.sub('[^A-Za-z0-9]+','_',item), item in items)
check('beta0_value', abs(float(items['beta_0']['value'])-(11-2*5/3))<1e-12)
check('beta1_value', abs(float(items['beta_1']['value'])-(102-38*5/3))<1e-12)
check('mc_boundary_not_equal', 'not a field-theoretic equality' in items['MC mass mapping']['status'] or 'phenomenological boundary' in items['MC mass mapping']['value'])
check('audit_only', 'audit' in items['PDG direct top average']['status'])
# route branch map
routes=rows('top_msr_route_branch_map_v59.csv')
check('four_routes', len(routes)==4)
route_ids={r['route_id']:r for r in routes}
for rid in ['R1','R2','R3','R4']:
    check('route_'+rid, rid in route_ids)
check('R1_pole', route_ids['R1']['to']=='m_t^pole')
check('R2_MSbar', 'MSbar' in route_ids['R2']['to'])
check('R3_MC_boundary', 'MC' in route_ids['R3']['to'] and 'boundary' in route_ids['R3']['claim_status'])
check('R4_cross_section', 'cross-section' in route_ids['R4']['to'])
# coefficients
coeff=rows('top_msr_full_conversion_coefficient_manifest_v59.csv')
check('coefficient_rows_many', len(coeff)>=28)
families=set(r['family'] for r in coeff)
for fam in ['QCD beta function','mass anomalous dimension','MSR-pole difference','MSR R-evolution','OS-MSbar mass relation','threshold decoupling']:
    check('coeff_family_'+re.sub('[^A-Za-z0-9]+','_',fam), fam in families)
for sym in ['beta_0','beta_4','gamma_m^4','a_4^MSR','gamma_R^4','d_4','zeta_g^4','zeta_m^4']:
    check('coeff_symbol_'+re.sub('[^A-Za-z0-9]+','_',sym), any(r['coefficient']==sym for r in coeff))
check('all_coeff_no_smuggling', all('not fitted' in r['no_smuggling_note'] for r in coeff))
# covariance
cov=rows('top_msr_full_qcd_covariance_channels_v59.csv')
check('cov_rows_8', len(cov)==8)
covc={r['channel']:r for r in cov}
for c in ['alpha_s(M_Z)','R_star','MSR truncation order','R-evolution truncation','threshold matching','pole renormalon ambiguity','MC interpretation','PDF/collider extraction correlations']:
    check('cov_channel_'+re.sub('[^A-Za-z0-9]+','_',c), c in covc)
check('renormalon_boundary', 'boundary' in covc['pole renormalon ambiguity']['status'])
check('mc_audit_boundary', 'boundary' in covc['MC interpretation']['status'])
# gates
gates=rows('top_msr_full_qcd_ledger_gates_v59.csv')
check('eight_gates', len(gates)==8)
gd={r['gate']:r for r in gates}
for g in ['L1 source object','L2 branch codomains','L3 external constants','L4 coefficient families','L5 evaluator schema','L6 no-smuggling','L7 covariance','L8 numeric finality']:
    check('gate_'+re.sub('[^A-Za-z0-9]+','_',g), g in gd)
check('numeric_final_blocked', gd['L8 numeric finality']['v59_status']=='blocked by design')
check('schema_closed', gd['L5 evaluator schema']['v59_status']=='closed')
# no-smuggling
ns=rows('top_msr_full_qcd_no_smuggling_matrix_v59.csv')
check('nosmuggle_rows', len(ns)==6)
for phrase in ['choose R_star','fit alpha_s','select loop order','tune threshold','declare MC mass equal','hide residual']:
    check('nosmuggle_'+phrase.replace(' ','_'), any(phrase in r['forbidden_action'] for r in ns))
# schema
schema=json.loads(txt(Path('schemas/top_msr_full_qcd_conversion_evaluator_schema_v59.json')))
check('schema_name', schema['schema_name']=='APF_TOP_MSR_FULL_QCD_CONVERSION_EVALUATOR_SCHEMA_v59')
check('schema_source_mt', abs(schema['source_object']['m_t_MSR_Rstar_GeV']-168.1690557938)<1e-12)
for req in ['alpha_s(MZ)','beta_i','gamma_m_i','MSR_delta_coefficients','R_evolution_coefficients','OS_MSbar_coefficients','decoupling_zeta_g_zeta_m','covariance_matrix']:
    check('schema_required_'+re.sub('[^A-Za-z0-9]+','_',req), req in schema['external_inputs_required'])
for out in ['m_t_pole_L','mbar_t_MSbar_mbar_L','m_t_MC_proxy_audit','route_covariance','residual_channel_report']:
    check('schema_output_'+re.sub('[^A-Za-z0-9]+','_',out), out in schema['route_outputs'])
check('schema_blocks_numeric', 'numeric coefficient ingestion' in schema['blocked_until'])
check('schema_no_target_audit', 'target masses audit-only' in schema['no_smuggling_rules'])
# registries
reg=rows('global_trace_to_scheme_closure_registry_v59.csv')
check('registry_rows', len(reg)==6)
by={r['sector']:r for r in reg}
check('registry_top_v59', by['top']['highest_closed_status']=='P_full_QCD_conversion_ledger_complete_numeric_final_blocked')
check('registry_top_may_claim', 'complete full-QCD conversion ledger' in by['top']['may_claim'])
check('registry_top_next_evaluator', 'evaluator' in by['top']['boundary_or_next_gate'])
check('registry_top_no_final', 'physical-final top' in by['top']['must_not_claim'])
case=rows('trace_to_scheme_case_table_v59.csv')
check('case_rows', len(case)==6)
check('case_has_v59', 'v59_registry_status' in case[0])
check('case_top_v59', any(r['sector']=='top' and r['v59_registry_status']=='P_full_QCD_conversion_ledger_complete_numeric_final_blocked' for r in case))
# TeX/summary/readme content
tex=txt(Path('paper/TOP_MSR_FULL_QCD_CONVERSION_LEDGER_v59.tex'))
for phrase in ['Top MSR Full QCD Conversion Ledger','Full conversion ledger','full-ledger closure','No-smuggling and boundary proof','Evaluator boundary','does not claim a physical-final top mass']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
for branch in ['m_t^{\\rm MSR}(R_\\star)\\to m_t^{\\rm pole}', 'm_t^{\\rm MSR}(R_\\star)\\to \\overline m_t(\\overline m_t)', 'm_t^{\\rm MSR}(R_\\star)\\to m_t^{\\rm MC\\ proxy}']:
    check('tex_branch_'+str(len(branch)), branch in tex)
summary=txt(Path('reports/top_msr_full_qcd_conversion_ledger_summary_v59.md'))
check('summary_stamp', 'TOP_MSR_FULL_QCD_CONVERSION_LEDGER_PASS' in summary)
check('summary_full_ledger', 'full QCD conversion ledger complete' in summary)
readme=txt(Path('README_v59.md'))
check('readme_status', 'P_{full QCD conversion ledger complete}' in readme)
# inherited scripts and reports
for f in ['scripts/check_top_msr_to_pole_lo_transport_witness_v58.py','scripts/check_heavy_qcd_final_covariance_ledger_v57.py','scripts/check_w_trace_to_onshell_ew_covariance_closure_v56.py']:
    check('inherited_'+f.replace('/','_'), (ROOT/f).exists())
# no-overclaim aggregate
check('next_v60', j['next']=='APF_v60_TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION')
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('TOP_MSR_FULL_QCD_CONVERSION_LEDGER_PASS')
