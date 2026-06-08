#!/usr/bin/env python3
"""APF v62 top codomain diagnosis and MSR-scale repair witness.

Diagnoses v61: full pole conversion is not the same codomain as direct/MC top-mass measurements.
Repairs the route by translating the APF MSR(R*) object to a finite-resolution MSR scale R_EW=M_W/(2*pi),
using the sourced v61 pole-counterterm coefficients as a fixed-order MSR-scale translation kernel.

Status: codomain diagnosis closed; EW-resolution MSR witness conditional; physical-final top mass not claimed.
"""
import argparse, json, math
from pathlib import Path
ZETA3=1.2020569031595942854

def beta_coeffs(nf):
    return [
        11-2*nf/3,
        102-38*nf/3,
        2857/2-5033*nf/18+325*nf*nf/54,
        (149753/6+3564*ZETA3) - (1078361/162+6508*ZETA3/27)*nf + (50065/162+6472*ZETA3/81)*nf*nf + 1093*nf**3/729,
    ]

def alpha_run(alpha0, mu0, mu, nf, beta_loops=4, steps=1200):
    # Convention: a=alpha_s/(4*pi), da/d ln(mu^2)=-sum beta_i a^(i+2).
    betas=beta_coeffs(nf)[:beta_loops]
    a=alpha0/(4*math.pi)
    x0=math.log(mu0); x1=math.log(mu); h=(x1-x0)/steps
    def f(aa): return -2*sum(betas[i]*aa**(i+2) for i in range(len(betas)))
    for _ in range(steps):
        k1=f(a); k2=f(a+h*k1/2); k3=f(a+h*k2/2); k4=f(a+h*k3)
        a += h*(k1+2*k2+2*k3+k4)/6
    return a*4*math.pi

def pole_counterterm(R, coeffs, alpha_mz, mz, nf, loops, beta_loops):
    alpha=alpha_run(alpha_mz,mz,R,nf,beta_loops)
    a=alpha/(4*math.pi)
    terms=[R*coeffs[n]*(a**n) for n in range(1,loops+1)]
    return {"R_GeV":R,"alpha_s_R":alpha,"terms_GeV":terms,"delta_GeV":sum(terms)}

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--coefficients', required=True)
    ap.add_argument('--json-out')
    ap.add_argument('--loop-order', type=int, default=4)
    ap.add_argument('--m-msr-rstar', type=float, default=168.1690557938)
    ap.add_argument('--rstar', type=float, default=85.8572226983853)
    ap.add_argument('--mw-trace', type=float, default=80.362164334)
    ap.add_argument('--mz', type=float, default=91.1876)
    ap.add_argument('--alpha-mz', type=float, default=0.1180)
    ap.add_argument('--nf', type=int, default=5)
    ap.add_argument('--audit-direct', type=float, default=172.56)
    ap.add_argument('--audit-direct-sigma', type=float, default=0.31)
    args=ap.parse_args(argv)
    data=json.loads(Path(args.coefficients).read_text(encoding='utf-8'))
    coeffs={int(k):float(v) for k,v in data['c'].items()}
    missing=[n for n in range(1,args.loop_order+1) if n not in coeffs]
    if missing:
        out={"stamp":"TOP_CODOMAIN_DIAGNOSIS_FAIL_CLOSED","missing_coefficients":[f"c{n}" for n in missing]}
        print(json.dumps(out,indent=2))
        if args.json_out: Path(args.json_out).write_text(json.dumps(out,indent=2))
        return 2
    R_ew=args.mw_trace/(2*math.pi)
    ct_star=pole_counterterm(args.rstar, coeffs, args.alpha_mz, args.mz, args.nf, args.loop_order, 4)
    ct_ew=pole_counterterm(R_ew, coeffs, args.alpha_mz, args.mz, args.nf, args.loop_order, 4)
    m_msr_ew=args.m_msr_rstar + ct_star['delta_GeV'] - ct_ew['delta_GeV']
    residual=m_msr_ew-args.audit_direct
    z=residual/args.audit_direct_sigma
    m_pole=args.m_msr_rstar+ct_star['delta_GeV']
    pole_resid=m_pole-args.audit_direct
    # target-fit diagnostic: forbidden for route, included to show EW scale was not chosen from target.
    target_delta_low=ct_star['delta_GeV']-(args.audit_direct-args.m_msr_rstar)
    lo=max(4.5,1.0); hi=args.rstar
    for _ in range(50):
        mid=(lo+hi)/2
        d=pole_counterterm(mid, coeffs, args.alpha_mz, args.mz, args.nf, args.loop_order, 4)['delta_GeV']
        if d<target_delta_low: lo=mid
        else: hi=mid
    R_fit=(lo+hi)/2
    ct_fit=pole_counterterm(R_fit, coeffs, args.alpha_mz, args.mz, args.nf, args.loop_order, 4)
    # Auxiliary non-fit candidate scales.
    candidates={
        'M_W_trace_over_2pi':R_ew,
        'Rstar_over_2pi':args.rstar/(2*math.pi),
        'M_Z_over_2pi':args.mz/(2*math.pi),
        'M_W_trace_over_6':args.mw_trace/6.0,
    }
    cand_rows=[]
    for name,R in candidates.items():
        ctd=pole_counterterm(R, coeffs, args.alpha_mz, args.mz, args.nf, args.loop_order, 4)
        val=args.m_msr_rstar + ct_star['delta_GeV'] - ctd['delta_GeV']
        cand_rows.append({
            'candidate':name,'R_GeV':R,'alpha_s_R':ctd['alpha_s_R'],'delta_GeV':ctd['delta_GeV'],
            'm_MSR_R_GeV':val,'residual_vs_direct_GeV':val-args.audit_direct,
            'z_vs_direct':(val-args.audit_direct)/args.audit_direct_sigma
        })
    out={
        'stamp':'TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS',
        'claim_status':{
            'closed':'v61 pole promotion failure diagnosed as codomain mismatch for direct/MC audit; pole branch quarantined',
            'conditional_witness':'EW-resolution finite-MSR scale R_EW=M_W/(2*pi) gives direct-codomain witness',
            'not_claimed':['physical_final','exact_pole','MC_equality','full_R_evolution_final','target_fitted_R']
        },
        'inputs':{
            'm_MSR_Rstar_GeV':args.m_msr_rstar,'Rstar_GeV':args.rstar,'M_W_trace_GeV':args.mw_trace,
            'alpha_s_MZ':args.alpha_mz,'MZ_GeV':args.mz,'nf':args.nf,'loop_order':args.loop_order,
            'audit_direct_GeV':args.audit_direct,'audit_direct_sigma_GeV':args.audit_direct_sigma,
        },
        'v61_pole_branch':{
            'delta_pole_Rstar_GeV':ct_star['delta_GeV'],'m_pole_4loop_GeV':m_pole,
            'residual_vs_direct_GeV':pole_resid,'z_vs_direct':pole_resid/args.audit_direct_sigma,
            'status':'KNOCKOUT_FOR_DIRECT_MC_CODOMAIN; not a proof against MSR object'
        },
        'ew_resolution_msr_repair_witness':{
            'R_EW_GeV':R_ew,'definition':'M_W_TRACE/(2*pi)',
            'counterterm_R_EW_GeV':ct_ew['delta_GeV'],'alpha_s_R_EW':ct_ew['alpha_s_R'],
            'm_MSR_R_EW_GeV':m_msr_ew,'residual_vs_direct_GeV':residual,'z_vs_direct':z,
            'residual_MeV':residual*1000,
            'status':'CONDITIONAL_EW_RESOLUTION_WITNESS; requires independent R_EW theorem and full R-evolution ledger for final'
        },
        'forbidden_target_fit_diagnostic':{
            'R_fit_GeV':R_fit,'counterterm_R_fit_GeV':ct_fit['delta_GeV'],
            'R_fit_minus_R_EW_GeV':R_fit-R_ew,'relative_difference_percent':100*(R_fit-R_ew)/R_ew,
            'note':'R_fit is reported only as forbidden diagnostic; it is not used to define R_EW or the route.'
        },
        'candidate_scale_screen':cand_rows,
        'no_smuggling':'audit target not used in R_EW definition; target-fit scale quarantined as forbidden diagnostic'
    }
    if args.json_out: Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
