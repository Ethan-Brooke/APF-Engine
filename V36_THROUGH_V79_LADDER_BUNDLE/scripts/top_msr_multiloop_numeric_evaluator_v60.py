#!/usr/bin/env python3
"""APF v60 top MSR numeric evaluator.

Fail-closed design: computes only the loop orders whose explicit coefficients are present
in the coefficient JSON. It refuses to infer coefficients from target top masses.
"""
import argparse, json, math, sys
from pathlib import Path

def alpha_run_1loop(alpha0,q,q0,nf):
    beta0=11-2*nf/3
    return alpha0/(1+alpha0*beta0/(2*math.pi)*math.log(q/q0))

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--coefficients', required=True)
    p.add_argument('--loop-order', type=int, default=1)
    p.add_argument('--m-msr', type=float, default=168.1690557938)
    p.add_argument('--rstar', type=float, default=85.8572226983853)
    p.add_argument('--alpha-mz', type=float, default=0.1180)
    p.add_argument('--mz', type=float, default=91.1876)
    p.add_argument('--nf', type=int, default=5)
    p.add_argument('--audit-target', type=float, default=None)
    p.add_argument('--json-out', default=None)
    args=p.parse_args(argv)
    coeff=json.loads(Path(args.coefficients).read_text(encoding='utf-8'))
    c={int(k):float(v) for k,v in coeff.get('c',{}).items()}
    missing=[n for n in range(1,args.loop_order+1) if n not in c]
    if missing:
        out={
            'stamp':'TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_FAIL_CLOSED',
            'requested_loop_order':args.loop_order,
            'missing_coefficients':[f'c{n}' for n in missing],
            'reason':'explicit sourced coefficients are required; target masses may not be used to infer them'
        }
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
        print(json.dumps(out,indent=2))
        return 2
    alpha_r=alpha_run_1loop(args.alpha_mz,args.rstar,args.mz,args.nf)
    delta=args.rstar*sum(c[n]*(alpha_r/math.pi)**n for n in range(1,args.loop_order+1))
    pole=args.m_msr+delta
    out={
        'stamp':'TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_PASS',
        'loop_order':args.loop_order,
        'm_MSR_Rstar_GeV':args.m_msr,
        'Rstar_GeV':args.rstar,
        'alpha_s_Rstar_1loop':alpha_r,
        'delta_m_GeV':delta,
        'm_pole_witness_GeV':pole,
        'coefficient_normalization':coeff.get('normalization'),
        'coefficient_status':coeff.get('coefficient_status'),
        'not_a_final_multiloop_result': args.loop_order < 2,
        'no_smuggling':'audit target not used in evaluator'
    }
    if args.audit_target is not None:
        out['audit_target_GeV']=args.audit_target
        out['audit_residual_GeV']=pole-args.audit_target
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
