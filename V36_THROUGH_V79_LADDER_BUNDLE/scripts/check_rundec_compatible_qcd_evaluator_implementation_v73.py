#!/usr/bin/env python3
import pathlib, subprocess, sys, json, csv, os
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond): checks.append((name,bool(cond)))
tex=(ROOT/'paper/RUNDEC_COMPATIBLE_QCD_EVALUATOR_IMPLEMENTATION_v73.tex').read_text()
for phrase in ['RunDec-Compatible QCD Evaluator Implementation','Executable LO scaffold','RunDec-compatible adapter','Fail-closed theorem','FULL\\_QCD\\_EVALUATOR\\_FAIL\\_CLOSED','No-smuggling rule']:
    check('tex phrase '+phrase[:24], phrase in tex)
script=ROOT/'scripts/rundec_compatible_qcd_evaluator_v73.py'
check('script exists', script.exists() and os.access(script, os.X_OK))
lo=json.loads(subprocess.check_output([sys.executable,str(script),'lo'], text=True))
check('lo status', lo['status']=='APF_V73_LO_SCAFFOLD_CLOSED')
check('lo has c b', set(lo['results'].keys())=={'c','b'})
check('c mass baseline', abs(lo['results']['c']['mass_target_LO_GeV']-1.07079047780338)<1e-12)
check('b mass baseline', abs(lo['results']['b']['mass_target_LO_GeV']-3.7379116829092527)<1e-12)
test=json.loads(subprocess.check_output([sys.executable,str(script),'test'], text=True))
check('self test pass', test['status']=='PASS' and all(test['checks'].values()))
full=json.loads(subprocess.check_output([sys.executable,str(script),'full'], text=True))
check('full fail closed', full['status']=='FULL_QCD_EVALUATOR_FAIL_CLOSED')
check('adapter unavailable reason', 'adapter' in full and full['adapter']['status']=='FAIL_CLOSED')
for rel in ['reports/v73_lo_scaffold_output.json','reports/v73_lo_self_test_output.json','reports/v73_full_fail_closed_output.json']:
    check('report exists '+rel, (ROOT/rel).exists())
res=list(csv.DictReader((ROOT/'tables/rundec_compatible_qcd_evaluator_v73_results.csv').open()))
check('results table c b', {r['quark'] for r in res}=={'c','b'})
check('results table closed', all(r['status']=='closed_LO_scaffold' for r in res))
adapt=list(csv.DictReader((ROOT/'tables/rundec_adapter_interface_v73.csv').open()))
check('adapter interface fields', {'RUNDEC_CMD','stdin','stdout','validation_id','threshold_schedule','covariance','target_reuse'}.issubset({r['field'] for r in adapt}))
claim=list(csv.DictReader((ROOT/'tables/v73_claim_status.csv').open()))
check('claim no physical final', any(r['object']=='charm/bottom physical final' and r['v73_status']=='not claimed' for r in claim))
check('claim full not claimed', any(r['object']=='full QCD numeric evaluator' and 'fail-closed' in r['v73_status'] for r in claim))
for rel in ['tables/rundec_source_ledger_v72.csv','tables/rundec_coefficient_manifest_v72.csv']:
    check('inherited '+rel, (ROOT/rel).exists())
for i in range(1,51): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('RUNDEC_COMPATIBLE_QCD_EVALUATOR_IMPLEMENTATION_FAIL')
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    for n in failed: print('FAIL', n)
    sys.exit(1)
print('RUNDEC_COMPATIBLE_QCD_EVALUATOR_IMPLEMENTATION_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
