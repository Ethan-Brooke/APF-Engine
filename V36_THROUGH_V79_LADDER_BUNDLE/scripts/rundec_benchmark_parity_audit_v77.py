#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
THIS=Path(__file__).resolve()
ROOT=THIS.parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import qcd_coefficient_table_vendoring_and_4loop_evaluator_v76 as v76

BENCHMARKS={
  'rundec_v3_charm_mc3': {
    'source':'Herren-Steinhauser RunDec/CRunDec v3 useful examples',
    'description':'RunDec v3 example ledger lists m_c(m_c)=1.279 GeV and m_c(3 GeV)=0.986 GeV under full RunDec-style running/decoupling context.',
    'm0_GeV':1.279, 'mu0_GeV':1.279, 'mu1_GeV':3.0, 'nf':4,
    'published_target_GeV':0.986, 'alpha0_test':0.38,
    'tolerance_GeV':0.002
  },
  'crundec_bottom_mb10_reverse': {
    'source':'Schmidt-Steinhauser CRunDec useful example',
    'description':'CRunDec example states m_b(10 GeV)=3.610 GeV maps to m_b(m_b)=4.163 GeV with alpha_s(M_Z)=0.1189; reverse fixed-nf audit uses m_b(m_b)=4.163 to 10 GeV.',
    'm0_GeV':4.163, 'mu0_GeV':4.163, 'mu1_GeV':10.0, 'nf':5,
    'published_target_GeV':3.610, 'alpha0_test':0.223,
    'tolerance_GeV':0.002
  }
}

def solve_alpha_for_target(b):
    # Precomputed using the same v76 fixed-nf evaluator; avoids repeatedly re-running RK4 during verifier.
    if abs(b['m0_GeV']-1.279)<1e-12:
        a=0.39713785808057833
    elif abs(b['m0_GeV']-4.163)<1e-12:
        a=0.22839599569953017
    else:
        raise ValueError('unknown benchmark')
    m,a1,ratio=v76.mass_run(b['m0_GeV'],a,b['mu0_GeV'],b['mu1_GeV'],b['nf'],4)
    return a,m,a1,ratio

def run():
    rows=[]; details={}
    for name,b in BENCHMARKS.items():
        m,a1,ratio=v76.mass_run(b['m0_GeV'],b['alpha0_test'],b['mu0_GeV'],b['mu1_GeV'],b['nf'],4)
        delta=m-b['published_target_GeV']
        implied_alpha, m_imp, a1_imp, ratio_imp=solve_alpha_for_target(b)
        parity=abs(delta)<=b['tolerance_GeV']
        status='PARITY_PASS' if parity else 'PARITY_FAIL_FIXED_NF_SUBSET'
        row={
          'benchmark':name,
          'status':status,
          'm0_GeV':b['m0_GeV'],
          'mu0_GeV':b['mu0_GeV'],
          'mu1_GeV':b['mu1_GeV'],
          'nf':b['nf'],
          'alpha0_test':b['alpha0_test'],
          'fixed_nf_result_GeV':m,
          'published_target_GeV':b['published_target_GeV'],
          'delta_GeV':delta,
          'tolerance_GeV':b['tolerance_GeV'],
          'implied_alpha0_for_parity':implied_alpha,
          'implied_alpha1':a1_imp,
          'interpretation':'fixed-nf coefficient subset is useful but not full RunDec parity; full adapter must provide alpha_s(MZ) running/threshold/matching protocol.'
        }
        rows.append(row); details[name]={**b, **row}
    overall = 'RUNDEC_BENCHMARK_PARITY_BLOCKED_PENDING_ADAPTER' if any(r['status'].startswith('PARITY_FAIL') for r in rows) else 'RUNDEC_BENCHMARK_PARITY_PASS'
    return {
      'status':overall,
      'benchmarks':details,
      'claim': 'v77 validates that the v76 fixed-nf 4-loop evaluator is not full RunDec parity; a real RunDec/CRunDec adapter or full alpha_s(MZ)+threshold evaluator is required.',
      'non_claims':['not full RunDec parity','not full threshold matching','not physical final','not fitted to APF outputs']
    }

if __name__=='__main__':
    out=run()
    print(json.dumps(out, indent=2, sort_keys=True))
