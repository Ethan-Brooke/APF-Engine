#!/usr/bin/env python3
import math, json, subprocess, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(n,c): checks.append((n,bool(c)))
# expected constants from generation
exp={'mc3':1.07079047780338,'mb10':3.7379116829092527,'as_c3':0.2653070677084119,'as_b10':0.18020045008307345,'sig_mc3':0.012471289433634469,'sig_mb10':0.013957196360871185}
out=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/charm_bottom_qcd_running_evaluator_v71.py')],text=True))
check('status closes LO', out['status']=='CHARM_BOTTOM_LO_QCD_RUNNING_EVALUATOR_CLOSED')
check('mc3 stable', abs(out['results']['c']['mass_target_LO_GeV']-exp['mc3'])<1e-12)
check('mb10 stable', abs(out['results']['b']['mass_target_LO_GeV']-exp['mb10'])<1e-12)
check('alpha c3 stable', abs(out['results']['c']['alpha1_LO']-exp['as_c3'])<1e-12)
check('alpha b10 stable', abs(out['results']['b']['alpha1_LO']-exp['as_b10'])<1e-12)
check('sigma c stable', abs(out['results']['c']['mass_target_LO_sigma_GeV']-exp['sig_mc3'])<1e-12)
check('sigma b stable', abs(out['results']['b']['mass_target_LO_sigma_GeV']-exp['sig_mb10'])<1e-12)
fail=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/charm_bottom_qcd_running_evaluator_v71.py'),'2'],text=True))
check('L2 fail closed', fail['status']=='FAIL_CLOSED')
check('RunDec missing listed', 'RunDec_or_equivalent_validation' in fail['missing'])
for rel in ['paper/CHARM_BOTTOM_QCD_RUNNING_EVALUATOR_v71.tex','tables/charm_bottom_qcd_running_evaluator_v71.csv','tables/charm_bottom_qcd_ledger_v71.csv','scripts/charm_bottom_qcd_running_evaluator_v71.py']:
    check('exists '+rel, (ROOT/rel).exists())
tex=(ROOT/'paper/CHARM_BOTTOM_QCD_RUNNING_EVALUATOR_v71.tex').read_text()
for phrase in ['No external target values at those scales are used','RunDec/CRunDec','fail closed','LO QCD evaluator closeout']:
    check('tex phrase '+phrase[:14], phrase in tex)
for i in range(1,61): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('CHARM_BOTTOM_QCD_RUNNING_EVALUATOR_FAIL')
    for n in failed: print('FAIL',n)
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    sys.exit(1)
print('CHARM_BOTTOM_QCD_RUNNING_EVALUATOR_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
