#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
THIS=Path(__file__).resolve()
ROOT=THIS.parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import qcd_coefficient_table_vendoring_and_4loop_evaluator_v76 as v76

MZ=91.1876
AS_MZ_EXAMPLE=0.1189
# Benchmark-style heavy thresholds chosen from the examples themselves; these are external RunDec/CRunDec test ledgers, not APF-fitted values.
MB_BENCH=4.163
MC_BENCH=1.279

BENCHMARKS={
  'rundec_v3_charm_mc3_threshold_matched': {
    'source':'Herren-Steinhauser RunDec/CRunDec v3 useful example',
    'description':'RunDec v3 example ledger: alpha_s^(5)(MZ)=0.1189-style benchmark context; m_c(m_c)=1.279 GeV -> m_c(3 GeV)=0.986 GeV.',
    'm0_GeV':1.279, 'mu0_GeV':1.279, 'mu1_GeV':3.0, 'nf_mass':4,
    'published_target_GeV':0.986, 'tolerance_GeV':0.001,
    'alpha_source':'alpha_s^(5)(MZ)=0.1189 propagated through fixed thresholds MZ -> mb -> mc; continuous alpha_s at thresholds; no APF-output tuning.'
  },
  'crundec_bottom_mb10_threshold_matched': {
    'source':'Schmidt-Steinhauser CRunDec useful example',
    'description':'CRunDec example: m_b(10 GeV)=3.610 GeV maps to m_b(m_b)=4.163 GeV using alpha_s^(5)(MZ)=0.1189; forward audit m_b(m_b)->10 GeV.',
    'm0_GeV':4.163, 'mu0_GeV':4.163, 'mu1_GeV':10.0, 'nf_mass':5,
    'published_target_GeV':3.610, 'tolerance_GeV':0.001,
    'alpha_source':'alpha_s^(5)(MZ)=0.1189 propagated MZ -> mb with nf=5; no APF-output tuning.'
  }
}

APF_CASES={
  'c_APF_to_3GeV': {'m0_GeV':1.272334177712, 'mu0_GeV':1.272334177712, 'mu1_GeV':3.0, 'nf_mass':4},
  'b_APF_to_10GeV': {'m0_GeV':4.177490455927, 'mu0_GeV':4.177490455927, 'mu1_GeV':10.0, 'nf_mass':5}
}

def alpha_from_MZ_to(mu:float, loops:int=4, as_mz:float=AS_MZ_EXAMPLE, mb:float=MB_BENCH):
    """Run alpha_s from MZ to mu with a continuous threshold at mb.

    This is a RunDec-compatible benchmark scaffold, not complete RunDec parity: higher-loop decoupling constants are not applied.
    """
    if mu >= mb:
        return v76.run_alpha(as_mz, MZ, mu, 5, loops=loops)
    a_mb = v76.run_alpha(as_mz, MZ, mb, 5, loops=loops)
    return v76.run_alpha(a_mb, mb, mu, 4, loops=loops)

def mass_run_threshold_matched(m0, mu0, mu1, nf_mass, loops=4):
    # Get alpha at the actual starting mass scale from a source external to APF outputs.
    a0=alpha_from_MZ_to(mu0, loops=loops)
    m1,a1,ratio=v76.mass_run(m0,a0,mu0,mu1,nf_mass,loops=loops)
    return m1,a0,a1,ratio

def evaluate():
    rows=[]; details={}
    for name,b in BENCHMARKS.items():
        m,a0,a1,ratio=mass_run_threshold_matched(b['m0_GeV'],b['mu0_GeV'],b['mu1_GeV'],b['nf_mass'],loops=4)
        delta=m-b['published_target_GeV']
        status='BENCHMARK_PASS' if abs(delta)<=b['tolerance_GeV'] else 'BENCHMARK_FAIL'
        row={
          'benchmark':name,'status':status,'m0_GeV':b['m0_GeV'],'mu0_GeV':b['mu0_GeV'],'mu1_GeV':b['mu1_GeV'],
          'nf_mass':b['nf_mass'],'alpha0_from_MZ':a0,'alpha1':a1,'mass_result_GeV':m,'published_target_GeV':b['published_target_GeV'],
          'delta_GeV':delta,'delta_MeV':1000*delta,'tolerance_GeV':b['tolerance_GeV'],'mass_ratio':ratio,
          'interpretation':'threshold-matched alpha_s(MZ) scaffold passes this published benchmark; full RunDec parity still requires validated higher-loop decoupling constants or adapter.'
        }
        rows.append(row); details[name]={**b,**row}
    apf={}
    for name,c in APF_CASES.items():
        m,a0,a1,ratio=mass_run_threshold_matched(c['m0_GeV'],c['mu0_GeV'],c['mu1_GeV'],c['nf_mass'],loops=4)
        apf[name]={**c,'alpha0_from_MZ':a0,'alpha1':a1,'mass_result_GeV':m,'mass_ratio':ratio}
    overall='THRESHOLD_MATCHED_QCD_BENCHMARK_CLOSURE_PASS' if all(r['status']=='BENCHMARK_PASS' for r in rows) else 'THRESHOLD_MATCHED_QCD_BENCHMARK_CLOSURE_FAIL'
    return {
      'status':overall,
      'alpha_s_MZ_input':AS_MZ_EXAMPLE,
      'MZ_GeV':MZ,
      'threshold_protocol':'continuous alpha_s at mb benchmark threshold; nf=5 above mb, nf=4 below mb; no higher-loop decoupling constants applied',
      'benchmarks':details,
      'apf_results':apf,
      'closed_claim':'selected RunDec/CRunDec benchmark parity closes for alpha_s(MZ)-driven threshold-matched scaffold',
      'remaining_boundary':'full RunDec parity still requires adapter or vendored zeta_g/zeta_m higher-loop decoupling/matching implementation',
      'non_claims':['not complete RunDec parity','not full decoupling constants','not physical final','not fitted to APF outputs']
    }

if __name__=='__main__':
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
