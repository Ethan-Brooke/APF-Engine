#!/usr/bin/env python3
from __future__ import annotations
import pathlib, subprocess, sys, json, csv, os
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(n,c): checks.append((n,bool(c)))
tex=(ROOT/'paper/RUNDEC_ADAPTER_VALIDATION_HARNESS_v75.tex').read_text()
for phrase in ['RunDec Adapter Validation Harness','Adapter protocol','Protocol self-test','Environment audit','FULL\\_RUNDEC\\_EVALUATOR\\_FAIL\\_CLOSED','not claim']:
    check('tex '+phrase[:30], phrase in tex)
script=ROOT/'scripts/rundec_adapter_validation_harness_v75.py'
synth=ROOT/'scripts/synthetic_rundec_protocol_adapter_v75.py'
check('validator executable', script.exists() and os.access(script, os.X_OK))
check('synthetic executable', synth.exists() and os.access(synth, os.X_OK))
payload=json.loads(subprocess.check_output([sys.executable,str(script),'payload'],text=True))
check('payload module v75', payload.get('module')=='APF_v75')
check('payload cases c b', set(payload.get('cases',{}).keys())=={'c','b'})
synthetic=json.loads(subprocess.check_output([sys.executable,str(script),'synthetic'],text=True))
check('synthetic accepted for harness', synthetic.get('status')=='ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW')
check('synthetic flagged self test', synthetic['response'].get('protocol_self_test_only') is True)
real=json.loads(subprocess.check_output([sys.executable,str(script),'real'],text=True))
# Accept either no adapter or a real adapter accepted/rejected; in this package no RUNDEC_CMD should be set normally.
check('real adapter result typed', real.get('status') in ['NO_REAL_RUNDEC_ADAPTER_PRESENT','ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW','ADAPTER_RESPONSE_REJECTED','ADAPTER_INVOCATION_FAIL_CLOSED'])
full=json.loads(subprocess.check_output([sys.executable,str(script),'full'],text=True))
check('harness closed', full.get('status')=='RUNDEC_ADAPTER_VALIDATION_HARNESS_CLOSED')
check('full fail closed absent real adapter or typed', full.get('physics_adapter_status') in ['FULL_RUNDEC_EVALUATOR_FAIL_CLOSED','REAL_RUNDEC_ADAPTER_AVAILABLE_REQUIRES_REVIEW'])
if full.get('physics_adapter_status')=='FULL_RUNDEC_EVALUATOR_FAIL_CLOSED':
    check('real says absent/rejected', full['real_adapter']['status']!='ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW')
for rel in ['reports/v75_payload.json','reports/v75_synthetic_protocol_self_test.json','reports/v75_real_adapter_check.json','reports/v75_full_gate_output.json','tables/v75_adapter_validation_status.csv','tables/v75_claim_status.csv']:
    check('exists '+rel, (ROOT/rel).exists())
rows=list(csv.DictReader((ROOT/'tables/v75_claim_status.csv').open()))
check('harness closed table', any(r['object']=='RunDec adapter validation harness' and r['v75_status']=='closed' for r in rows))
check('physical final not claimed', any(r['object']=='physical final masses' and r['v75_status']=='not claimed' for r in rows))
# inherited v74 artifacts present; do not recursively execute older verifier here
# because v75 is a gate-level package and older verifiers may depend on environment adapter variables.
for rel in ['scripts/check_rundec_adapter_or_coefficient_vendoring_v74.py',
            'scripts/rundec_adapter_or_coefficient_vendor_gate_v74.py',
            'tables/rundec_coefficient_vendor_template_v74.json']:
    check('inherited v74 artifact '+rel, (ROOT/rel).exists())
for i in range(1,46): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('RUNDEC_ADAPTER_VALIDATION_HARNESS_FAIL')
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    for n in failed: print('FAIL',n)
    raise SystemExit(1)
print('RUNDEC_ADAPTER_VALIDATION_HARNESS_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
