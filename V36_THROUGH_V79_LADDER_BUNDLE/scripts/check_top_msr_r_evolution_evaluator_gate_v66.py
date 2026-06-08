#!/usr/bin/env python3
import csv, json, subprocess, sys, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(n,c):
    checks.append((n,bool(c))); print(('PASS' if c else 'FAIL'), n)
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
def txt(rel): return (ROOT/rel).read_text(encoding='utf-8')
files=[
 'paper/TOP_MSR_R_EVOLUTION_EVALUATOR_GATE_v66.tex',
 'schemas/top_msr_r_evolution_evaluator_gate_v66.json',
 'scripts/top_msr_r_evolution_evaluator_gate_v66.py',
 'tables/top_msr_r_evolution_gate_v66.csv',
 'tables/top_msr_r_evolution_requirements_v66.csv',
 'reports/top_msr_r_evolution_evaluator_gate_v66_data.json',
 'reports/top_msr_r_evolution_evaluator_gate_summary_v66.md',
 'README_v66.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(txt('reports/top_msr_r_evolution_evaluator_gate_v66_data.json'))
check('stamp', j['stamp']=='TOP_MSR_R_EVOLUTION_EVALUATOR_GATE_PASS')
check('version', j['version']=='v66')
check('witness_retained', j['fixed_order_witness_retained'] is True)
check('no_full_final', j['full_r_evolution_numeric_final'] is False)
check('no_physical_final', j['physical_final_assigned'] is False)
check('fail_closed', j['fail_closed_full_r_evolution'] is True)
check('mt_value', abs(j['mt_msr_rew_fixed_order_witness_gev']-172.564754410708)<1e-12)
check('rew_value', abs(j['r_ew_gev']-12.790035691319)<1e-12)
check('pole_blocked_value', abs(j['pole_branch_blocked_gev']-174.016604383647)<1e-12)
schema=json.loads(txt('schemas/top_msr_r_evolution_evaluator_gate_v66.json'))
check('schema_stamp', schema['stamp']=='TOP_MSR_R_EVOLUTION_EVALUATOR_GATE_PASS')
check('schema_fail_closed', schema['fail_closed'] is True)
check('schema_no_physical_final', schema['physical_final_assigned'] is False)
check('schema_requirements_6', len(schema['full_r_evolution_requirements'])==6)
req=rows('tables/top_msr_r_evolution_requirements_v66.csv')
check('requirements_6', len(req)==6)
check('has_gamma_requirement', any('gamma_R' in r['requirement'] for r in req))
check('has_covariance_requirement', any('covariance' in r['requirement'] for r in req))
check('has_no_smuggling', any('no target residual tuning' in r['requirement'] for r in req))
# evaluator behavior
r=subprocess.run(['python', str(ROOT/'scripts/top_msr_r_evolution_evaluator_gate_v66.py'), '--mode', 'fixed_order_witness'], capture_output=True, text=True)
check('fixed_order_runs', r.returncode==0)
out=json.loads(r.stdout)
check('fixed_order_stamp', out['stamp']=='TOP_MSR_R_EVOLUTION_FIXED_ORDER_WITNESS')
check('fixed_order_not_final', out['physical_final'] is False and out['not_full_R_evolution'] is True)
r2=subprocess.run(['python', str(ROOT/'scripts/top_msr_r_evolution_evaluator_gate_v66.py'), '--mode', 'full_r_evolution'], capture_output=True, text=True)
check('full_r_fails_closed_rc', r2.returncode==2)
out2=json.loads(r2.stdout)
check('full_r_fail_closed_stamp', out2['stamp']=='TOP_MSR_R_EVOLUTION_FAIL_CLOSED')
check('full_r_missing_gamma', 'gamma_R coefficient table' in out2['missing'])
tex=txt('paper/TOP_MSR_R_EVOLUTION_EVALUATOR_GATE_v66.tex')
for phrase in ['Top MSR $R$-Evolution Evaluator Gate', '172.564754410708', '174.016604383647', 'fails closed', 'TOP\\_MSR\\_R\\_EVOLUTION\\_EVALUATOR\\_GATE\\_PASS']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed); sys.exit(1)
print('TOP_MSR_R_EVOLUTION_EVALUATOR_GATE_PASS')
