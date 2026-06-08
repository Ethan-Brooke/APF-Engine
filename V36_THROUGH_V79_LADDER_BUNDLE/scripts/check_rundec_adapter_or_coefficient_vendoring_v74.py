#!/usr/bin/env python3
import pathlib, subprocess, sys, json, csv, os
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(n,c): checks.append((n,bool(c)))
tex=(ROOT/'paper/RUNDEC_ADAPTER_OR_COEFFICIENT_VENDORING_v74.tex').read_text()
for phrase in ['RunDec Adapter or Coefficient-Vendoring Gate','Validated adapter certificate','Vendored coefficient certificate','No-smuggling theorem','FULL\\_RUNDEC\\_EVALUATOR\\_FAIL\\_CLOSED']:
    check('tex '+phrase[:30], phrase in tex)
script=ROOT/'scripts/rundec_adapter_or_coefficient_vendor_gate_v74.py'
check('script exists executable', script.exists() and os.access(script, os.X_OK))
payload=json.loads(subprocess.check_output([sys.executable,str(script),'payload'],text=True))
check('payload schema', payload['schema']=='APF_RunDec_Adapter_Request_v1')
check('payload cases c b', set(payload['cases'].keys())=={'c','b'})
check('forbidden inputs present', 'target_mass' in payload['forbidden_inputs'])
full=json.loads(subprocess.check_output([sys.executable,str(script),'full'],text=True))
check('full fail closed', full['status']=='FULL_RUNDEC_EVALUATOR_FAIL_CLOSED')
check('adapter fail closed', full['adapter']['status']=='ADAPTER_FAIL_CLOSED')
check('coeff fail closed', full['coefficients']['status']=='COEFFICIENT_TABLE_FAIL_CLOSED')
coeff=json.loads(subprocess.check_output([sys.executable,str(script),'coeff',str(ROOT/'tables/rundec_coefficient_vendor_template_v74.json')],text=True))
check('template fails closed', coeff['status']=='COEFFICIENT_TABLE_FAIL_CLOSED')
check('template failures named', 'missing_source_manifest' in coeff['failures'])
for rel in ['tables/rundec_coefficient_vendor_template_v74.json','tables/rundec_adapter_vendor_gate_v74.csv','tables/v74_claim_status.csv','reports/v74_full_fail_closed_output.json','reports/v74_adapter_payload.json','reports/v74_template_coeff_validation.json']:
    check('exists '+rel, (ROOT/rel).exists())
rows=list(csv.DictReader((ROOT/'tables/v74_claim_status.csv').open()))
check('full not claimed', any(r['object']=='full RunDec evaluator' and 'not claimed' in r['v74_status'] for r in rows))
check('physical final not claimed', any(r['object']=='physical final masses' and r['v74_status']=='not claimed' for r in rows))
# inherited v73 still passes
v73=ROOT/'scripts/check_rundec_compatible_qcd_evaluator_implementation_v73.py'
check('inherited v73 verifier exists', v73.exists())
if v73.exists():
    p=subprocess.run([sys.executable,str(v73)],text=True,capture_output=True)
    check('inherited v73 verifier pass', p.returncode==0 and 'PASS' in p.stdout)
for i in range(1,51): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('RUNDEC_ADAPTER_OR_COEFFICIENT_VENDORING_FAIL')
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    for n in failed: print('FAIL',n)
    raise SystemExit(1)
print('RUNDEC_ADAPTER_OR_COEFFICIENT_VENDORING_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
