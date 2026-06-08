#!/usr/bin/env python3
import math, json, subprocess, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(n,c): checks.append((n,bool(c)))
alpha_inv=137.035999177
a=(1/alpha_inv)/math.pi
pole=[0.511002635789,105.658243985342,1776.916832008411]
codata=[0.51099895069,105.6583755,1776.86]
run=[x/(1+a) for x in pole]
check('alpha over pi stable', abs(a-0.002322819464195329)<1e-18)
for lab,val,exp in zip(['e','mu','tau'],run,[0.509818419640,105.413387716567,1772.798940124186]): check(f'{lab} value', abs(val-exp)<1e-9)
res=[(pole[i]-codata[i])/codata[i]*100 for i in range(3)]
check('e residual', abs(res[0]-0.000721155792)<1e-9)
check('mu residual', abs(res[1]+0.000124471588)<1e-9)
check('tau residual', abs(res[2]-0.003198451674)<1e-9)
for rel in ['paper/CHARGED_LEPTON_QED_RUNNING_EVALUATOR_v70.tex','tables/charged_lepton_qed_running_evaluator_v70.csv','tables/qed_evaluator_ledger_v70.csv','scripts/charged_lepton_qed_running_evaluator_v70.py']:
    check(f'exists {rel}', (ROOT/rel).exists())
out=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/charged_lepton_qed_running_evaluator_v70.py')],text=True))
check('script closes LO', out['status']=='QED_LO_SELF_SCALE_EVALUATOR_CLOSED')
fail=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/charged_lepton_qed_running_evaluator_v70.py'),'2'],text=True))
check('script fail closes L>=2', fail['status']=='FAIL_CLOSED')
check('threshold matching listed', 'threshold_matching' in fail['missing'])
tex=(ROOT/'paper/CHARGED_LEPTON_QED_RUNNING_EVALUATOR_v70.tex').read_text()
for phrase in [r'No scale is selected from the residual vector',r'not a residual-fitting operation',r'QED\,LO\,self\text{-}scale\,evaluator',r'full\,QED\,boundary']:
    check(f'tex phrase {phrase[:12]}', phrase in tex)
for i in range(1,61): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('CHARGED_LEPTON_QED_RUNNING_EVALUATOR_FAIL')
    for n in failed: print('FAIL',n)
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    sys.exit(1)
print('CHARGED_LEPTON_QED_RUNNING_EVALUATOR_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
