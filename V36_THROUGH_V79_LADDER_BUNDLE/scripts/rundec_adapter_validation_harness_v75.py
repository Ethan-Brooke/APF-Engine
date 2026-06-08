#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, subprocess, shlex, pathlib
BASE_SCRIPT = pathlib.Path(__file__).with_name('rundec_adapter_or_coefficient_vendor_gate_v74.py')
SYNTHETIC = pathlib.Path(__file__).with_name('synthetic_rundec_protocol_adapter_v75.py')
FORBIDDEN_KEYS = ['pdg_target','target_mass','fit','least_squares','observed_mass','m_c_pdg','m_b_pdg']
REQUIRED_TOP = ['schema','results','loop_order','threshold_schedule','matching_convention','covariance','validation_id','no_target_reuse']

def payload():
    # Inline the v74 adapter request rather than shelling out. This prevents
    # recursive or environment-dependent hangs while preserving the exact
    # RunDec-compatible request schema from v74.
    p={
        'schema':'APF_RunDec_Adapter_Request_v1',
        'module':'APF_v75',
        'cases':{
            'c': {'m0_GeV': 1.272334177712, 'mu0_GeV': 1.272334177712, 'mu1_GeV': 3.0, 'alpha0': 0.38, 'nf': 4},
            'b': {'m0_GeV': 4.177490455927, 'mu0_GeV': 4.177490455927, 'mu1_GeV': 10.0, 'alpha0': 0.223, 'nf': 5},
        },
        'required_outputs':['mass_target_GeV','alpha_target','loop_order','threshold_schedule','covariance','validation_id','no_target_reuse'],
        'forbidden_inputs':FORBIDDEN_KEYS,
        'validator':'RunDec adapter validation harness v75'
    }
    return p

def validate_response(data, allow_synthetic=False):
    failures=[]
    for f in REQUIRED_TOP:
        if f not in data: failures.append('missing_'+f)
    if data.get('schema')!='APF_RunDec_Adapter_Response_v1': failures.append('bad_schema')
    if set(data.get('results',{}).keys()) != {'c','b'}: failures.append('missing_c_b_results')
    if data.get('no_target_reuse') is not True: failures.append('missing_no_target_reuse_true')
    raw=json.dumps(data).lower()
    for k in FORBIDDEN_KEYS:
        if k in raw: failures.append('forbidden_key_'+k)
    if data.get('protocol_self_test_only') is True and not allow_synthetic:
        failures.append('synthetic_protocol_output_not_physics_promotable')
    if data.get('physics_promotable') is False and not allow_synthetic:
        failures.append('physics_promotable_false')
    if failures:
        return {'status':'ADAPTER_RESPONSE_REJECTED','failures':failures,'response':data}
    return {'status':'ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW','response':data}

def run_cmd(cmd, synthetic=False):
    try:
        proc=subprocess.run(shlex.split(cmd), input=json.dumps(payload()), text=True, capture_output=True, timeout=60)
    except Exception as e:
        return {'status':'ADAPTER_INVOCATION_FAIL_CLOSED','reason':'invocation failed','error':repr(e)}
    if proc.returncode != 0:
        return {'status':'ADAPTER_INVOCATION_FAIL_CLOSED','reason':'nonzero exit','stderr':proc.stderr[-2000:]}
    try:
        data=json.loads(proc.stdout)
    except Exception as e:
        return {'status':'ADAPTER_INVOCATION_FAIL_CLOSED','reason':'non-json stdout','stdout':proc.stdout[:1000],'error':repr(e)}
    return validate_response(data, allow_synthetic=synthetic)

def real_adapter_check():
    cmd=os.environ.get('RUNDEC_CMD')
    if not cmd:
        return {'status':'NO_REAL_RUNDEC_ADAPTER_PRESENT','reason':'RUNDEC_CMD not set'}
    return run_cmd(cmd, synthetic=False)

def synthetic_self_test():
    # Inline synthetic response to avoid any recursive process ambiguity in fail-closed environments.
    req=payload()
    results={}
    for k,v in req.get('cases',{}).items():
        results[k]={'mass_target_GeV':v['m0_GeV']*0.999,'alpha_target':v.get('alpha0',0.0)*0.999,
                    'start_scale_GeV':v['mu0_GeV'],'target_scale_GeV':v['mu1_GeV'],'nf':v['nf']}
    data={'schema':'APF_RunDec_Adapter_Response_v1','results':results,'loop_order':0,
          'threshold_schedule':'synthetic-none','matching_convention':'synthetic-protocol-self-test-only',
          'covariance':'synthetic-none','validation_id':'SYNTHETIC_PROTOCOL_SELF_TEST_DO_NOT_USE_FOR_PHYSICS',
          'no_target_reuse':True,'protocol_self_test_only':True,'physics_promotable':False}
    return validate_response(data, allow_synthetic=True)

def full_gate():
    real=real_adapter_check()
    synth=synthetic_self_test()
    physics = (real.get('status')=='ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW')
    return {
        'status':'RUNDEC_ADAPTER_VALIDATION_HARNESS_CLOSED' if synth.get('status')=='ADAPTER_RESPONSE_ACCEPTED_FOR_REVIEW' else 'RUNDEC_ADAPTER_VALIDATION_HARNESS_FAIL',
        'physics_adapter_status':'REAL_RUNDEC_ADAPTER_AVAILABLE_REQUIRES_REVIEW' if physics else 'FULL_RUNDEC_EVALUATOR_FAIL_CLOSED',
        'real_adapter':real,
        'synthetic_protocol_self_test':synth,
        'nonclaim':['full RunDec evaluator','full multi-loop QCD final','physical final masses']
    }

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'full'
    if mode=='payload': out=payload()
    elif mode=='synthetic': out=synthetic_self_test()
    elif mode=='real': out=real_adapter_check()
    elif mode=='full': out=full_gate()
    else: out={'status':'ERROR','reason':'mode must be payload, synthetic, real, or full'}
    print(json.dumps(out, indent=2, sort_keys=True))
