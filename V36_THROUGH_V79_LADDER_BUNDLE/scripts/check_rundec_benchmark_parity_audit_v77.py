#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, pathlib, csv
ROOT=pathlib.Path(__file__).resolve().parents[1]
proc=subprocess.run([sys.executable, str(ROOT/'scripts/rundec_benchmark_parity_audit_v77.py')], text=True, capture_output=True, check=True)
out=json.loads(proc.stdout)
checks=[]
checks.append(('status_blocked_pending_adapter', out['status']=='RUNDEC_BENCHMARK_PARITY_BLOCKED_PENDING_ADAPTER'))
checks.append(('has_charm_benchmark', 'rundec_v3_charm_mc3' in out['benchmarks']))
checks.append(('has_bottom_benchmark', 'crundec_bottom_mb10_reverse' in out['benchmarks']))
checks.append(('charm_fixed_nf_fails', out['benchmarks']['rundec_v3_charm_mc3']['status']=='PARITY_FAIL_FIXED_NF_SUBSET'))
checks.append(('bottom_fixed_nf_fails', out['benchmarks']['crundec_bottom_mb10_reverse']['status']=='PARITY_FAIL_FIXED_NF_SUBSET'))
checks.append(('implied_alpha_not_output_fitted_charm', 0.39 < out['benchmarks']['rundec_v3_charm_mc3']['implied_alpha0_for_parity'] < 0.41))
checks.append(('implied_alpha_not_output_fitted_bottom', 0.22 < out['benchmarks']['crundec_bottom_mb10_reverse']['implied_alpha0_for_parity'] < 0.235))
checks.append(('nonclaim_physical_final', 'not physical final' in out['non_claims']))
# write reports/tables
(ROOT/'reports/v77_benchmark_parity_output.json').write_text(json.dumps(out, indent=2, sort_keys=True))
with (ROOT/'tables/v77_benchmark_parity_audit.csv').open('w', newline='') as f:
    fieldnames=['benchmark','status','m0_GeV','mu0_GeV','mu1_GeV','nf','alpha0_test','fixed_nf_result_GeV','published_target_GeV','delta_GeV','tolerance_GeV','implied_alpha0_for_parity','implied_alpha1','interpretation']
    w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
    for b in out['benchmarks'].values():
        w.writerow({k:b[k] for k in fieldnames})
failed=[name for name,ok in checks if not ok]
report='RUNDEC_BENCHMARK_PARITY_AUDIT_PASS\nTotal checks: %d/%d\n' % (len(checks)-len(failed), len(checks))
if failed:
    report+='FAILED: '+','.join(failed)+'\n'
(ROOT/'reports/v77_verifier_report.txt').write_text(report)
print(report)
sys.exit(1 if failed else 0)
