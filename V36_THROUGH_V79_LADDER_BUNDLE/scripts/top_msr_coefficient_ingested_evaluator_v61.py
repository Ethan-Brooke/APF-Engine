#!/usr/bin/env python3
"""APF v61 top MSR coefficient-ingested evaluator.

Computes the MSR(R*) -> pole witness through any loop order whose sourced coefficients
are present. Audit targets are reported only after calculation and are never inputs to the series.
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

def alpha_run(alpha0, mu0, mu, nf, beta_loops=4, steps=20000):
    # Convention: a=alpha_s/(4*pi), da/d ln(mu^2)=-sum beta_i a^(i+2).
    betas=beta_coeffs(nf)[:beta_loops]
    a=alpha0/(4*math.pi)
    x0=math.log(mu0); x1=math.log(mu); h=(x1-x0)/steps
    def f(aa): return -2*sum(betas[i]*aa**(i+2) for i in range(len(betas)))
    for _ in range(steps):
        k1=f(a); k2=f(a+h*k1/2); k3=f(a+h*k2/2); k4=f(a+h*k3)
        a += h*(k1+2*k2+2*k3+k4)/6
    return a*4*math.pi

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--coefficients', required=True)
    p.add_argument('--loop-order', type=int, default=4)
    p.add_argument('--alpha-beta-loops', type=int, default=4)
    p.add_argument('--m-msr', type=float, default=168.1690557938)
    p.add_argument('--rstar', type=float, default=85.8572226983853)
    p.add_argument('--alpha-mz', type=float, default=0.1180)
    p.add_argument('--mz', type=float, default=91.1876)
    p.add_argument('--nf', type=int, default=5)
    p.add_argument('--audit-target', type=float, default=None)
    p.add_argument('--json-out', default=None)
    args=p.parse_args(argv)
    data=json.loads(Path(args.coefficients).read_text(encoding='utf-8'))
    c={int(k):float(v) for k,v in data['c'].items()}
    missing=[n for n in range(1,args.loop_order+1) if n not in c]
    if missing:
        out={'stamp':'TOP_MSR_COEFFICIENT_INGESTION_FAIL_CLOSED','missing_coefficients':[f'c{n}' for n in missing], 'reason':'sourced coefficients required'}
        if args.json_out: Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
        print(json.dumps(out,indent=2)); return 2
    alpha_r=alpha_run(args.alpha_mz,args.mz,args.rstar,args.nf,args.alpha_beta_loops)
    a=alpha_r/(4*math.pi)
    terms=[args.rstar*c[n]*(a**n) for n in range(1,args.loop_order+1)]
    pole=args.m_msr+sum(terms)
    out={'stamp':'TOP_MSR_COEFFICIENT_INGESTION_EVALUATOR_PASS','loop_order':args.loop_order,'alpha_beta_loops':args.alpha_beta_loops,'alpha_s_Rstar':alpha_r,'m_MSR_Rstar_GeV':args.m_msr,'Rstar_GeV':args.rstar,'terms_GeV':terms,'delta_m_GeV':sum(terms),'m_pole_witness_GeV':pole,'normalization':data.get('normalization'),'no_smuggling':'audit target not used in calculation'}
    if args.audit_target is not None:
        out['audit_target_GeV']=args.audit_target
        out['audit_residual_GeV']=pole-args.audit_target
    if args.json_out: Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2)); return 0
if __name__=='__main__':
    raise SystemExit(main())
