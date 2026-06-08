#!/usr/bin/env python3
import math, json, sys
ALPHA_INV = 137.035999177
ALPHA = 1.0 / ALPHA_INV
A = ALPHA / math.pi
POLE_V43_MEV = {'e': 0.511002635789, 'mu': 105.658243985342, 'tau': 1776.916832008411}
CODATA2022_POLE_MEV = {'e': 0.51099895069, 'mu': 105.6583755, 'tau': 1776.86}

def evaluate(loop_order=1):
    if loop_order != 1:
        return {'status':'FAIL_CLOSED','reason':'full QED running requires sourced L>=2 coefficient/threshold ledger','missing':['gamma_m_QED_L>=2','beta_QED_L>=2','threshold_matching','scheme_covariance']}
    out={}
    for k,m in POLE_V43_MEV.items():
        out[k]={
            'pole_v43_MeV':m,
            'msbar_LO_selfscale_MeV': m/(1.0+A),
            'codata_pole_MeV': CODATA2022_POLE_MEV[k],
            'pole_residual_percent': (m-CODATA2022_POLE_MEV[k])/CODATA2022_POLE_MEV[k]*100.0,
        }
    return {'status':'QED_LO_SELF_SCALE_EVALUATOR_CLOSED','alpha_inverse':ALPHA_INV,'alpha_over_pi':A,'results':out}

if __name__ == '__main__':
    loop=1
    if len(sys.argv)>1:
        loop=int(sys.argv[1])
    print(json.dumps(evaluate(loop), indent=2, sort_keys=True))
