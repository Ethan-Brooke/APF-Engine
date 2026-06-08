#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
ZETA3=1.2020569031595942854
THIS=Path(__file__).resolve()
ROOT=THIS.parents[1]
COEFF=ROOT/'tables'/'qcd_coefficient_table_v76.json'

def beta_coeffs(nf:int):
    b0=11-2*nf/3
    b1=102-38*nf/3
    b2=2857/2-5033*nf/18+325*nf*nf/54
    b3=149753/6+3564*ZETA3-(1078361/162+6508*ZETA3/27)*nf+(50065/162+6472*ZETA3/81)*nf*nf+1093*nf**3/729
    return b0,b1,b2,b3

def dalpha_dlnmu(alpha:float,nf:int,loops:int):
    b=beta_coeffs(nf)
    terms=[-b[0]*alpha**2/(2*math.pi), -b[1]*alpha**3/(8*math.pi**2), -b[2]*alpha**4/(32*math.pi**3), -b[3]*alpha**5/(128*math.pi**4)]
    return sum(terms[:loops])

def run_alpha(alpha0,mu0,mu1,nf,loops=4,steps=20000):
    # deterministic RK4 integration in t=ln(mu); enough for audit precision, not a replacement for RunDec.
    t0=math.log(mu0); t1=math.log(mu1); h=(t1-t0)/steps
    a=alpha0
    for _ in range(steps):
        k1=dalpha_dlnmu(a,nf,loops)
        k2=dalpha_dlnmu(a+0.5*h*k1,nf,loops)
        k3=dalpha_dlnmu(a+0.5*h*k2,nf,loops)
        k4=dalpha_dlnmu(a+h*k3,nf,loops)
        a += h*(k1+2*k2+2*k3+k4)/6
    return a

def cfun(x,nf):
    if nf==4:
        return ((25/6)*x)**(12/25)*(1+1.01413*x+1.38921*x*x+1.09054*x**3)
    if nf==5:
        return ((23/6)*x)**(12/23)*(1+1.17549*x+1.50071*x*x+0.172486*x**3)
    raise ValueError('v76 vendors c(x) only for nf=4,5')

def mass_run(m0,alpha0,mu0,mu1,nf,loops=4):
    a1=run_alpha(alpha0,mu0,mu1,nf,loops=loops)
    x0=alpha0/math.pi; x1=a1/math.pi
    ratio=cfun(x1,nf)/cfun(x0,nf)
    return m0*ratio,a1,ratio

def evaluate():
    data=json.loads(COEFF.read_text())
    results={}
    for q,case in data['cases'].items():
        m,a1,ratio=mass_run(case['m0_GeV'],case['alpha0'],case['mu0_GeV'],case['mu1_GeV'],case['nf'])
        results[q]={**case,'alpha1_4loop_fixed_nf':a1,'mass_target_4loop_fixed_nf_GeV':m,'mass_ratio':ratio}
    return {'status':'APF_V76_4LOOP_FIXED_NF_EVALUATOR_CLOSED','coefficient_table':str(COEFF),'results':results,'non_claims':data['metadata']['non_claims']}

def validate_coeff():
    data=json.loads(COEFF.read_text())
    checks={}
    checks['has_beta_convention']='beta_alpha_s_mu' in data
    checks['has_nf4_cfunc']=data['mass_c_function_alpha_over_pi']['nf4']['series']==[1.0,1.01413,1.38921,1.09054]
    checks['has_nf5_cfunc']=data['mass_c_function_alpha_over_pi']['nf5']['series']==[1.0,1.17549,1.50071,0.172486]
    checks['cases_cb']=set(data['cases'].keys())=={'c','b'}
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks}
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'eval'
    out=validate_coeff() if mode=='validate' else evaluate()
    print(json.dumps(out,indent=2,sort_keys=True))
