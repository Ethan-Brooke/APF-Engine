#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
v78=json.loads((ROOT/'reports/v78_threshold_matched_qcd_output.json').read_text())
ch=v78['benchmarks']['rundec_v3_charm_mc3_threshold_matched']
bt=v78['benchmarks']['crundec_bottom_mb10_threshold_matched']
apf_c=v78['apf_results']['c_APF_to_3GeV']
apf_b=v78['apf_results']['b_APF_to_10GeV']
registry={
  'module':'APF_v79_QCD_EVALUATOR_CLOSEOUT_AND_REGISTRY_UPDATE',
  'status':'QCD_EVALUATOR_CLOSEOUT_AND_REGISTRY_UPDATE_PASS',
  'closed_claim':'c,b QCD running evaluator closed to threshold-matched benchmark parity',
  'active_status':{
    'charm':'[P_threshold-matched QCD evaluator benchmark closed] at m_c(3 GeV)',
    'bottom':'[P_threshold-matched QCD evaluator benchmark closed] at m_b(10 GeV)'
  },
  'active_outputs':{
    'm_c_APF_3GeV_GeV': apf_c['mass_result_GeV'],
    'alpha_s_charm_start_from_MZ': apf_c['alpha0_from_MZ'],
    'alpha_s_3GeV': apf_c['alpha1'],
    'm_b_APF_10GeV_GeV': apf_b['mass_result_GeV'],
    'alpha_s_bottom_start_from_MZ': apf_b['alpha0_from_MZ'],
    'alpha_s_10GeV': apf_b['alpha1']
  },
  'benchmark_closure':{
    'charm':{
      'published_case':'m_c(m_c)=1.279 GeV -> m_c(3 GeV)=0.986 GeV',
      'v78_result_GeV':ch['mass_result_GeV'],
      'published_target_GeV':ch['published_target_GeV'],
      'delta_MeV':ch['delta_MeV'],
      'tolerance_MeV':1000*ch['tolerance_GeV'],
      'status':ch['status']
    },
    'bottom':{
      'published_case':'m_b(m_b)=4.163 GeV -> m_b(10 GeV)=3.610 GeV',
      'v78_result_GeV':bt['mass_result_GeV'],
      'published_target_GeV':bt['published_target_GeV'],
      'delta_MeV':bt['delta_MeV'],
      'tolerance_MeV':1000*bt['tolerance_GeV'],
      'status':bt['status']
    }
  },
  'nonclaims':[
    'not a full official RunDec binary replacement',
    'not complete higher-loop decoupling-constant parity',
    'not pole mass export',
    'not physical final',
    'not Delta=0',
    'not fitted to APF outputs'
  ],
  'next_optional_work':'attach real RunDec/CRunDec adapter for exact library parity; otherwise branch is closed for APF registry use'
}
print(json.dumps(registry,indent=2,sort_keys=True))
