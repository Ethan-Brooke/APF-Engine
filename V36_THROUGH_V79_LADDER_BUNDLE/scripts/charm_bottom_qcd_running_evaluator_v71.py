#!/usr/bin/env python3
import math, json, sys
INPUTS = {
  'c': {'m0': 1.272334177712, 'alpha0': 0.38, 'sigma_m0_90': 0.0046, 'sigma_alpha0': 0.03, 'mu0': 1.272334177712, 'mu1': 3.0, 'nf': 4},
  'b': {'m0': 4.177490455927, 'alpha0': 0.223, 'sigma_m0_90': 0.007, 'sigma_alpha0': 0.008, 'mu0': 4.177490455927, 'mu1': 10.0, 'nf': 5},
}
CL90_TO_SIGMA = 0.6079568319117692
def beta0(nf): return 11.0 - 2.0*nf/3.0
def alpha_run_lo(alpha0, mu0, mu1, nf):
    return alpha0/(1.0 + alpha0*beta0(nf)/(2.0*math.pi)*math.log(mu1/mu0))
def mass_run_lo(m0, alpha0, mu0, mu1, nf):
    a1=alpha_run_lo(alpha0, mu0, mu1, nf)
    exp=4.0/beta0(nf)
    return m0*(a1/alpha0)**exp, a1, exp
def derivs(m0, alpha0, mu0, mu1, nf):
    y,_,_=mass_run_lo(m0, alpha0, mu0, mu1, nf)
    dm=max(abs(m0)*1e-6,1e-12); da=max(abs(alpha0)*1e-6,1e-12)
    yp,_,_=mass_run_lo(m0+dm, alpha0, mu0, mu1, nf); d_dm=(yp-y)/dm
    yp,_,_=mass_run_lo(m0, alpha0+da, mu0, mu1, nf); d_da=(yp-y)/da
    return d_dm,d_da
def evaluate(loop_order=1):
    if loop_order != 1:
        return {'status':'FAIL_CLOSED','reason':'higher-loop QCD running requires sourced RunDec/CRunDec coefficient, decoupling, matching, and covariance ledger','missing':['beta_i_L>=2','gamma_m_i_L>=2','decoupling_zeta_i','threshold_matching','RunDec_or_equivalent_validation','joint_covariance']}
    results={}
    for q,inp in INPUTS.items():
        y,a1,exp=mass_run_lo(inp['m0'],inp['alpha0'],inp['mu0'],inp['mu1'],inp['nf'])
        d_dm,d_da=derivs(inp['m0'],inp['alpha0'],inp['mu0'],inp['mu1'],inp['nf'])
        sig_m=inp['sigma_m0_90']*CL90_TO_SIGMA
        sig=math.sqrt((d_dm*sig_m)**2 + (d_da*inp['sigma_alpha0'])**2)
        results[q]={'m0_GeV':inp['m0'],'mu0_GeV':inp['mu0'],'mu1_GeV':inp['mu1'],'nf':inp['nf'],'alpha0':inp['alpha0'],'alpha1_LO':a1,'mass_target_LO_GeV':y,'mass_target_LO_sigma_GeV':sig,'mass_exponent':exp}
    return {'status':'CHARM_BOTTOM_LO_QCD_RUNNING_EVALUATOR_CLOSED','results':results}
if __name__=='__main__':
    L=1
    if len(sys.argv)>1: L=int(sys.argv[1])
    print(json.dumps(evaluate(L), indent=2, sort_keys=True))
