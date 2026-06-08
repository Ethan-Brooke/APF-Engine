#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, pathlib, csv
ROOT=pathlib.Path(__file__).resolve().parents[1]
# ensure v78 still passes
v78check=subprocess.run([sys.executable, str(ROOT/'scripts/check_threshold_matched_qcd_evaluator_benchmark_closure_v78.py')], capture_output=True, text=True)
proc=subprocess.run([sys.executable, str(ROOT/'scripts/qcd_evaluator_closeout_registry_update_v79.py')], capture_output=True, text=True, check=True)
out=json.loads(proc.stdout)
checks=[]
checks.append(('v78_inherited_pass', v78check.returncode==0 and 'PASS' in v78check.stdout))
checks.append(('overall_status', out['status']=='QCD_EVALUATOR_CLOSEOUT_AND_REGISTRY_UPDATE_PASS'))
checks.append(('closed_claim_exists', 'threshold-matched benchmark parity' in out['closed_claim']))
checks.append(('charm_benchmark_pass', out['benchmark_closure']['charm']['status']=='BENCHMARK_PASS'))
checks.append(('bottom_benchmark_pass', out['benchmark_closure']['bottom']['status']=='BENCHMARK_PASS'))
checks.append(('charm_sub_MeV', abs(out['benchmark_closure']['charm']['delta_MeV'])<1.0))
checks.append(('bottom_sub_MeV', abs(out['benchmark_closure']['bottom']['delta_MeV'])<1.0))
checks.append(('active_charm_value_locked', abs(out['active_outputs']['m_c_APF_3GeV_GeV']-0.979226596181)<1e-9))
checks.append(('active_bottom_value_locked', abs(out['active_outputs']['m_b_APF_10GeV_GeV']-3.625054969391)<1e-9))
checks.append(('no_physical_final', 'not physical final' in out['nonclaims']))
checks.append(('no_rundec_binary_replacement', 'not a full official RunDec binary replacement' in out['nonclaims']))
checks.append(('no_fit', 'not fitted to APF outputs' in out['nonclaims']))
(ROOT/'reports/v79_qcd_evaluator_closeout_registry.json').write_text(json.dumps(out,indent=2,sort_keys=True))
with (ROOT/'tables/v79_qcd_evaluator_registry.csv').open('w', newline='') as f:
    fieldnames=['sector','status','active_output','alpha_s_start','alpha_s_target','nonclaim_boundary']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
    w.writerow({'sector':'charm','status':out['active_status']['charm'],'active_output':out['active_outputs']['m_c_APF_3GeV_GeV'],'alpha_s_start':out['active_outputs']['alpha_s_charm_start_from_MZ'],'alpha_s_target':out['active_outputs']['alpha_s_3GeV'],'nonclaim_boundary':'not full RunDec binary replacement; not physical final'})
    w.writerow({'sector':'bottom','status':out['active_status']['bottom'],'active_output':out['active_outputs']['m_b_APF_10GeV_GeV'],'alpha_s_start':out['active_outputs']['alpha_s_bottom_start_from_MZ'],'alpha_s_target':out['active_outputs']['alpha_s_10GeV'],'nonclaim_boundary':'not full RunDec binary replacement; not physical final'})
failed=[n for n,ok in checks if not ok]
report='QCD_EVALUATOR_CLOSEOUT_AND_REGISTRY_UPDATE_PASS\nTotal checks: %d/%d\n' % (len(checks)-len(failed), len(checks))
if failed: report+='FAILED: '+','.join(failed)+'\n'
(ROOT/'reports/v79_verifier_report.txt').write_text(report)
print(report)
sys.exit(1 if failed else 0)
