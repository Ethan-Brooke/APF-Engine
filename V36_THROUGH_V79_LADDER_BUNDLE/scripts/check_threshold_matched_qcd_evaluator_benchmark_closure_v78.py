#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, pathlib, csv
ROOT=pathlib.Path(__file__).resolve().parents[1]
proc=subprocess.run([sys.executable, str(ROOT/'scripts/threshold_matched_qcd_evaluator_benchmark_closure_v78.py')], capture_output=True, text=True, check=True)
out=json.loads(proc.stdout)
checks=[]
checks.append(('overall_pass', out['status']=='THRESHOLD_MATCHED_QCD_BENCHMARK_CLOSURE_PASS'))
checks.append(('charm_benchmark_pass', out['benchmarks']['rundec_v3_charm_mc3_threshold_matched']['status']=='BENCHMARK_PASS'))
checks.append(('bottom_benchmark_pass', out['benchmarks']['crundec_bottom_mb10_threshold_matched']['status']=='BENCHMARK_PASS'))
checks.append(('charm_delta_sub_MeV', abs(out['benchmarks']['rundec_v3_charm_mc3_threshold_matched']['delta_MeV'])<1.0))
checks.append(('bottom_delta_sub_MeV', abs(out['benchmarks']['crundec_bottom_mb10_threshold_matched']['delta_MeV'])<1.0))
checks.append(('apf_charm_result_exists', 'c_APF_to_3GeV' in out['apf_results']))
checks.append(('apf_bottom_result_exists', 'b_APF_to_10GeV' in out['apf_results']))
checks.append(('no_physical_final_claim', 'not physical final' in out['non_claims']))
checks.append(('no_complete_rundec_claim', 'not complete RunDec parity' in out['non_claims']))
checks.append(('not_fitted_to_apf', 'not fitted to APF outputs' in out['non_claims']))
# write reports
(ROOT/'reports/v78_threshold_matched_qcd_output.json').write_text(json.dumps(out, indent=2, sort_keys=True))
with (ROOT/'tables/v78_benchmark_closure.csv').open('w', newline='') as f:
    fieldnames=['benchmark','status','m0_GeV','mu0_GeV','mu1_GeV','nf_mass','alpha0_from_MZ','alpha1','mass_result_GeV','published_target_GeV','delta_GeV','delta_MeV','tolerance_GeV','mass_ratio','interpretation']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
    for b in out['benchmarks'].values(): w.writerow({k:b[k] for k in fieldnames})
with (ROOT/'tables/v78_apf_cb_results.csv').open('w', newline='') as f:
    fieldnames=['case','m0_GeV','mu0_GeV','mu1_GeV','nf_mass','alpha0_from_MZ','alpha1','mass_result_GeV','mass_ratio']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
    for name,b in out['apf_results'].items():
        row={'case':name, **b}; w.writerow({k:row[k] for k in fieldnames})
failed=[n for n,ok in checks if not ok]
report='THRESHOLD_MATCHED_QCD_EVALUATOR_BENCHMARK_CLOSURE_PASS\nTotal checks: %d/%d\n' % (len(checks)-len(failed), len(checks))
if failed: report += 'FAILED: '+','.join(failed)+'\n'
(ROOT/'reports/v78_verifier_report.txt').write_text(report)
print(report)
sys.exit(1 if failed else 0)
