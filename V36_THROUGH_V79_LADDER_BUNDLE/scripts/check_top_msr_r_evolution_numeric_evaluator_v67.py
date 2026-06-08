#!/usr/bin/env python3
import csv,json,subprocess,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; checks=[]
def check(n,c): checks.append((n,bool(c))); print(('PASS' if c else 'FAIL'), n)
def txt(p): return (ROOT/p).read_text(encoding='utf-8')
def rows(p):
    with (ROOT/p).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def js(p): return json.loads(txt(p))
files=['paper/TOP_MSR_R_EVOLUTION_COEFFICIENT_INGESTION_EVALUATOR_v67.tex','coefficients/top_msr_r_evolution_coefficients_v67.json','scripts/top_msr_r_evolution_numeric_evaluator_v67.py','tables/top_msr_r_evolution_loop_convergence_v67.csv','tables/top_msr_r_evolution_uncertainty_channels_v67.csv','tables/top_msr_r_evolution_status_v67.csv','reports/top_msr_r_evolution_numeric_evaluator_v67_data.json','reports/top_msr_r_evolution_numeric_evaluator_summary_v67.md','registry/top_route_registry_update_v67.csv','README_v67.md']
for f in files: check('exists_'+f.replace('/','_'),(ROOT/f).exists())
d=js('reports/top_msr_r_evolution_numeric_evaluator_v67_data.json')
check('stamp',d['stamp']=='TOP_MSR_R_EVOLUTION_COEFFICIENT_INGESTION_EVALUATOR_PASS')
check('numeric_closed',d['numeric_R_evolution_evaluator_closed'] is True)
check('no_physical_final',d['physical_final_assigned'] is False and d['pole_final_assigned'] is False and d['MC_equality_assigned'] is False)
check('fixed_nf_no_threshold',d['nf_fixed']==5 and d['threshold_crossed'] is False)
check('rew_value',abs(d['R_EW_GeV']-12.790035691319)<1e-12)
check('m_rew_range',172.70<d['m_t_MSR_REW_4loop_GeV']<172.73)
check('delta_range',4.54<d['delta_R_evolution_4loop_GeV']<4.56)
check('z_inside_1',abs(d['z_vs_direct_sigma'])<1)
check('z_comb_inside_1',abs(d['z_combined_audit'])<1)
check('pole_blocked',abs(d['pole_branch_blocked_GeV']-174.016604383647)<1e-12)
loops=rows('tables/top_msr_r_evolution_loop_convergence_v67.csv'); check('loop_rows',len(loops)==4)
vals=[float(r['m_t_MSR_REW_GeV']) for r in loops]
check('loop2_to_4_stable_200MeV',max(vals[1:])-min(vals[1:])<0.20)
unc=rows('tables/top_msr_r_evolution_uncertainty_channels_v67.csv'); check('unc_rows',len(unc)==6)
coeff=js('coefficients/top_msr_r_evolution_coefficients_v67.json')
check('coeff_nf',coeff['nf']==5); check('gamma0',abs(coeff['gamma_R_coefficients']['gamma0']-16/3)<1e-12); check('gamma3_negative',coeff['gamma_R_coefficients']['gamma3_central']<0)
r=subprocess.run(['python',str(ROOT/'scripts/top_msr_r_evolution_numeric_evaluator_v67.py'),'--loops','4'],capture_output=True,text=True)
check('evaluator_runs',r.returncode==0); out=json.loads(r.stdout)
check('eval_stamp',out['stamp']=='TOP_MSR_R_EVOLUTION_NUMERIC_EVALUATOR_V67')
check('eval_value',abs(out['m_t_MSR_REW_GeV']-d['m_t_MSR_REW_4loop_GeV'])<1e-10)
check('eval_not_final',out['physical_final'] is False and out['not_pole_mass'] is True and out['not_MC_equality'] is True)
r1=subprocess.run(['python',str(ROOT/'scripts/top_msr_r_evolution_numeric_evaluator_v67.py'),'--loops','1'],capture_output=True,text=True); out1=json.loads(r1.stdout)
check('eval_L1_runs',r1.returncode==0); check('eval_L1_lower',out1['m_t_MSR_REW_GeV']<out['m_t_MSR_REW_GeV'])
tex=txt('paper/TOP_MSR_R_EVOLUTION_COEFFICIENT_INGESTION_EVALUATOR_v67.tex')
for phrase in ['Coefficient Ingestion','Pole branch remains blocked','TOP\\_MSR\\_R\\_EVOLUTION\\_COEFFICIENT\\_INGESTION\\_EVALUATOR\\_PASS']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase),phrase in tex)
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed: print('FAILED:',failed); sys.exit(1)
print('TOP_MSR_R_EVOLUTION_COEFFICIENT_INGESTION_EVALUATOR_PASS')
