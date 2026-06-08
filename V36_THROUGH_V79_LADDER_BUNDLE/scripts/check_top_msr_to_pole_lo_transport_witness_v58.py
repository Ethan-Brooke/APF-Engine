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
 'paper/TOP_MSR_TO_POLE_LO_TRANSPORT_WITNESS_v58.tex',
 'tables/top_msr_to_pole_lo_ledger_v58.csv',
 'tables/top_msr_to_pole_lo_calculation_v58.csv',
 'tables/top_msr_to_pole_lo_gates_v58.csv',
 'tables/top_msr_to_pole_residual_channels_v58.csv',
 'tables/top_msr_to_pole_lo_nonclaim_matrix_v58.csv',
 'tables/global_trace_to_scheme_closure_registry_v58.csv',
 'tables/trace_to_scheme_case_table_v58.csv',
 'reports/top_msr_to_pole_lo_transport_witness_v58_data.json',
 'reports/top_msr_to_pole_lo_transport_witness_summary_v58.md',
 'README_v58.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(txt(Path('reports/top_msr_to_pole_lo_transport_witness_v58_data.json')))
check('stamp', j['stamp']=='TOP_MSR_TO_POLE_LO_TRANSPORT_WITNESS_PASS')
check('mt_msr', abs(j['apf_msr_Rstar_GeV']-168.1690557938)<1e-12)
check('rstar', abs(j['R_star_GeV']-85.8572226983853)<1e-9)
check('alpha_mz', abs(j['alpha_s_MZ']-0.1180)<1e-12)
check('alpha_err', abs(j['alpha_s_MZ_error']-0.0009)<1e-12)
check('mz', abs(j['MZ_GeV']-91.1876)<1e-12)
check('nf', j['n_f']==5)
check('beta0', abs(j['beta0']-(11-10/3))<1e-12)
check('cf', abs(j['C_F']-4/3)<1e-12)
alpha_r=j['alpha_s_MZ']/(1+j['alpha_s_MZ']*j['beta0']/(2*math.pi)*math.log(j['R_star_GeV']/j['MZ_GeV']))
check('alpha_r_formula', abs(j['alpha_s_Rstar_1loop']-alpha_r)<1e-15)
delta=j['R_star_GeV']*j['C_F']*j['alpha_s_Rstar_1loop']/math.pi
check('delta_formula', abs(j['delta_m_LO_GeV']-delta)<1e-12)
check('pole_formula', abs(j['top_pole_LO_witness_GeV']-(j['apf_msr_Rstar_GeV']+j['delta_m_LO_GeV']))<1e-12)
check('pole_near_172_5', 172.50<j['top_pole_LO_witness_GeV']<172.51)
check('pdg_direct', abs(j['pdg_direct_average_GeV']-172.56)<1e-12)
check('pdg_error', abs(j['pdg_direct_error_GeV']-0.31)<1e-12)
check('residual_formula', abs(j['residual_GeV']-(j['top_pole_LO_witness_GeV']-172.56))<1e-12)
check('residual_small', abs(j['residual_GeV'])<0.06)
check('ratio_under_one', abs(j['residual_over_pdg_error'])<1)
check('ratio_formula', abs(j['residual_over_pdg_error']-j['residual_GeV']/0.31)<1e-12)
check('alpha_cov_positive', j['alpha_covariance_GeV']>0)
check('alpha_cov_about_33MeV', 0.033<j['alpha_covariance_GeV']<0.034)
check('trunc_positive', j['truncation_scale_LO_GeV']>0)
check('trunc_about_220MeV', 0.21<j['truncation_scale_LO_GeV']<0.23)
combined=math.sqrt(0.31**2+j['alpha_covariance_GeV']**2+j['truncation_scale_LO_GeV']**2)
check('combined_formula', abs(j['combined_witness_envelope_GeV']-combined)<1e-12)
check('combined_z_under_one', abs(j['residual_over_combined_envelope'])<1)
check('combined_z_formula', abs(j['residual_over_combined_envelope']-j['residual_GeV']/j['combined_witness_envelope_GeV'])<1e-12)
# ledger table
led=rows('top_msr_to_pole_lo_ledger_v58.csv')
check('ledger_rows', len(led)==10)
items={r['item']:r for r in led}
for item in ['m_t^MSR(R_star)','R_star','alpha_s(M_Z)','sigma_alpha_s(M_Z)','M_Z','n_f','beta_0','C_F','PDG direct top average','PDG direct top uncertainty']:
    check('ledger_item_'+re.sub('[^A-Za-z0-9]+','_',item), item in items)
check('pdg_audit_only', 'audit' in items['PDG direct top average']['role'])
check('source_not_pole', 'not a pole' in items['m_t^MSR(R_star)']['role'])
check('alpha_external', 'external' in items['alpha_s(M_Z)']['role'])
# calc table
calc=rows('top_msr_to_pole_lo_calculation_v58.csv')
check('calc_rows', len(calc)==9)
calcq={r['quantity']:r for r in calc}
check('calc_has_pole', 'm_t^pole,LO witness' in calcq)
check('calc_pole_matches_json', abs(float(calcq['m_t^pole,LO witness']['value'])-j['top_pole_LO_witness_GeV'])<1e-12)
check('calc_residual_matches_json', abs(float(calcq['residual vs PDG direct average']['value'])-j['residual_GeV'])<1e-12)
# gates
sg=rows('top_msr_to_pole_lo_gates_v58.csv')
check('six_gates', len(sg)==6)
for g in ['G1','G2','G3','G4','G5','G6']:
    check('gate_'+g, any(r['gate']==g for r in sg))
gd={r['gate']:r for r in sg}
check('g2_mentions_one_loop', 'one-loop' in gd['G2']['detail'])
check('g5_mentions_not_used', 'not used' in gd['G5']['detail'])
check('g6_channels', 'higher-loop' in gd['G6']['detail'])
# residual channels
rc=rows('top_msr_to_pole_residual_channels_v58.csv')
check('six_residual_channels', len(rc)==6)
channels=[r['channel'] for r in rc]
for c in ['alpha_s(MZ) uncertainty','LO truncation scale','PDG direct/MC-proxy uncertainty','MC-to-pole interpretation ambiguity','higher-loop MSR R-evolution and matching','threshold/matching/PDF/correlation covariance']:
    check('channel_'+re.sub('[^A-Za-z0-9]+','_',c), c in channels)
# nonclaims
nc=rows('top_msr_to_pole_lo_nonclaim_matrix_v58.csv')
check('seven_nonclaims', len(nc)==7)
ncd={r['claim']:r for r in nc}
check('pdg_input_forbidden', ncd['using PDG top average as input']['v58_status']=='forbidden')
check('alpha_fit_forbidden', ncd['choosing alpha_s to fit top']['v58_status']=='forbidden')
check('final_not_claimed', ncd['top physical-final mass']['v58_status']=='not claimed')
# registry and case table
reg=rows('global_trace_to_scheme_closure_registry_v58.csv')
check('registry_rows', len(reg)==6)
by={r['sector']:r for r in reg}
check('registry_top_promoted', by['top']['highest_closed_status']=='P_MSR_Rstar_plus_LO_pole_transport_witness')
check('registry_top_may_claim', 'one-loop pole/MC-proxy transport witness' in by['top']['may_claim'])
check('registry_top_must_not', 'physical-final top' in by['top']['must_not_claim'])
case=rows('trace_to_scheme_case_table_v58.csv')
check('case_rows', len(case)==6)
check('case_has_v58', 'v58_registry_status' in case[0])
check('case_top_v58', any(r.get('sector')=='top' and r.get('v58_registry_status')=='P_MSR_Rstar_plus_LO_pole_transport_witness' for r in case))
# tex/summary/readme
tex=txt(Path('paper/TOP_MSR_TO_POLE_LO_TRANSPORT_WITNESS_v58.tex'))
for phrase in ['Top MSR-to-Pole One-Loop Transport Witness','one-loop QCD transport witness','Phi_t','No-smuggling audit','does not claim a physical-final top mass']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
check('tex_pole_number', '172.506466595364' in tex)
check('tex_residual_number', '-0.053533404636' in tex)
summary=txt(Path('reports/top_msr_to_pole_lo_transport_witness_summary_v58.md'))
check('summary_stamp','TOP_MSR_TO_POLE_LO_TRANSPORT_WITNESS_PASS' in summary)
check('summary_claim','P_{MSR}(R_*) + P_{pole,LO witness}' in summary)
readme=txt(Path('README_v58.md'))
check('readme_headline','P_{MSR}(R_*) + P_{pole,LO witness}' in readme)
# inherited scripts
for f in ['scripts/check_heavy_qcd_final_covariance_ledger_v57.py','scripts/check_w_trace_to_onshell_ew_covariance_closure_v56.py','scripts/check_global_trace_to_scheme_closure_registry_v55.py']:
    check('inherited_'+f.replace('/','_'), (ROOT/f).exists())
# no-overclaim aggregate
check('status_upgrade', j['status_upgrade']=='t:P_MSR_Rstar_boundary -> P_MSR_Rstar_plus_LO_pole_transport_witness')
for s in ['P_physical_final','exact_pole_mass','MC_mass_equality','zero_residual','full_multiloop_MSR_conversion']:
    check('not_claimed_'+s, s in j['not_claimed'])
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('TOP_MSR_TO_POLE_LO_TRANSPORT_WITNESS_PASS')
