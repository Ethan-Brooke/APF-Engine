#!/usr/bin/env python3
from __future__ import annotations
import json, math, os, subprocess, sys, shlex
CL90_TO_SIGMA = 0.6079568319117692
CASES = {
  'c': {'m0': 1.272334177712, 'alpha0': 0.38, 'sigma_m0_90': 0.0046, 'sigma_alpha0': 0.03, 'mu0': 1.272334177712, 'mu1': 3.0, 'nf': 4},
  'b': {'m0': 4.177490455927, 'alpha0': 0.223, 'sigma_m0_90': 0.007, 'sigma_alpha0': 0.008, 'mu0': 4.177490455927, 'mu1': 10.0, 'nf': 5},
}
EXPECTED_LO = {
  'c': {'alpha1_LO': 0.2653070677084119, 'mass_target_LO_GeV': 1.07079047780338},
  'b': {'alpha1_LO': 0.18020045008307345, 'mass_target_LO_GeV': 3.7379116829092527},
}
def beta0(nf:int)->float: return 11.0 - 2.0*nf/3.0
def alpha_run_lo(alpha0:float, mu0:float, mu1:float, nf:int)->float:
    return alpha0/(1.0 + alpha0*beta0(nf)/(2.0*math.pi)*math.log(mu1/mu0))
def mass_run_lo(m0:float, alpha0:float, mu0:float, mu1:float, nf:int):
    a1=alpha_run_lo(alpha0,mu0,mu1,nf); exp=4.0/beta0(nf)
    return m0*(a1/alpha0)**exp, a1, exp
def derivs(m0,alpha0,mu0,mu1,nf):
    y,_,_=mass_run_lo(m0,alpha0,mu0,mu1,nf); dm=max(abs(m0)*1e-6,1e-12); da=max(abs(alpha0)*1e-6,1e-12)
    yp,_,_=mass_run_lo(m0+dm,alpha0,mu0,mu1,nf); d_dm=(yp-y)/dm
    yp,_,_=mass_run_lo(m0,alpha0+da,mu0,mu1,nf); d_da=(yp-y)/da
    return d_dm,d_da
def evaluate_lo():
    out={}
    for q,inp in CASES.items():
        m,a,exp=mass_run_lo(inp['m0'],inp['alpha0'],inp['mu0'],inp['mu1'],inp['nf'])
        d_dm,d_da=derivs(inp['m0'],inp['alpha0'],inp['mu0'],inp['mu1'],inp['nf'])
        sigma_m=inp['sigma_m0_90']*CL90_TO_SIGMA
        sigma=math.sqrt((d_dm*sigma_m)**2+(d_da*inp['sigma_alpha0'])**2)
        out[q]={'m0_GeV':inp['m0'],'mu0_GeV':inp['mu0'],'mu1_GeV':inp['mu1'],'nf':inp['nf'],'alpha0':inp['alpha0'],'alpha1_LO':a,'mass_target_LO_GeV':m,'mass_target_LO_sigma_GeV':sigma,'mass_exponent':exp}
    return {'status':'APF_V73_LO_SCAFFOLD_CLOSED','engine':'internal_LO_scaffold','results':out}
def self_test_lo():
    result=evaluate_lo()['results']; checks=[]
    for q in ['c','b']:
        checks.append((q+'_mass', abs(result[q]['mass_target_LO_GeV']-EXPECTED_LO[q]['mass_target_LO_GeV'])<1e-12))
        checks.append((q+'_alpha', abs(result[q]['alpha1_LO']-EXPECTED_LO[q]['alpha1_LO'])<1e-12))
    return {'status':'PASS' if all(c for _,c in checks) else 'FAIL', 'checks':dict(checks)}
def call_rundec_adapter():
    cmd=os.environ.get('RUNDEC_CMD')
    if not cmd:
        return {'status':'FAIL_CLOSED','reason':'RUNDEC_CMD not set','required_interface':'command reads JSON from stdin and returns JSON with c,b mass_target_GeV plus validation metadata'}
    payload={'module':'APF_v73','cases':CASES,'requested_loop_order':'declared_by_adapter','required_outputs':['mass_target_GeV','alpha_target','loop_order','threshold_schedule','validation_id']}
    try:
        proc=subprocess.run(shlex.split(cmd), input=json.dumps(payload), text=True, capture_output=True, timeout=30)
    except Exception as e:
        return {'status':'FAIL_CLOSED','reason':'adapter invocation failed','error':repr(e)}
    if proc.returncode!=0:
        return {'status':'FAIL_CLOSED','reason':'adapter nonzero exit','stderr':proc.stderr[-2000:]}
    try:
        data=json.loads(proc.stdout)
    except Exception as e:
        return {'status':'FAIL_CLOSED','reason':'adapter did not return JSON','stdout':proc.stdout[:1000],'error':repr(e)}
    if not {'c','b'}.issubset(set(data.get('results',{}).keys())):
        return {'status':'FAIL_CLOSED','reason':'adapter missing c/b results','adapter_output':data}
    if 'validation_id' not in data:
        return {'status':'FAIL_CLOSED','reason':'adapter missing validation_id','adapter_output':data}
    return {'status':'RUNDEC_COMPATIBLE_ADAPTER_RETURNED','adapter_output':data}
def evaluate_full():
    adapter=call_rundec_adapter()
    if adapter.get('status')!='RUNDEC_COMPATIBLE_ADAPTER_RETURNED':
        return {'status':'FULL_QCD_EVALUATOR_FAIL_CLOSED','reason':'RunDec-compatible validated adapter unavailable','adapter':adapter,'lo_scaffold':evaluate_lo()}
    return {'status':'FULL_QCD_EVALUATOR_EXTERNAL_ADAPTER_AVAILABLE_REQUIRES_REVIEW','adapter':adapter,'lo_scaffold':evaluate_lo()}
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'lo'
    if mode=='lo': out=evaluate_lo()
    elif mode=='test': out=self_test_lo()
    elif mode=='adapter': out=call_rundec_adapter()
    elif mode=='full': out=evaluate_full()
    else: out={'status':'ERROR','reason':'mode must be lo, test, adapter, or full'}
    print(json.dumps(out, indent=2, sort_keys=True))
