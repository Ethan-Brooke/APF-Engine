#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(name,cond): checks.append((name,bool(cond)))
# files
for p in ['tables/qcd_coefficient_table_v76.json','scripts/qcd_coefficient_table_vendoring_and_4loop_evaluator_v76.py','reports/v76_4loop_fixed_nf_output.json','tables/v76_4loop_fixed_nf_results.csv','paper/QCD_COEFFICIENT_TABLE_VENDORING_AND_4LOOP_EVALUATOR_v76.tex']:
    ck('exists_'+p,(ROOT/p).exists())
coeff=json.loads((ROOT/'tables/qcd_coefficient_table_v76.json').read_text())
ck('coeff_nf4_series', coeff['mass_c_function_alpha_over_pi']['nf4']['series']==[1.0,1.01413,1.38921,1.09054])
ck('coeff_nf5_series', coeff['mass_c_function_alpha_over_pi']['nf5']['series']==[1.0,1.17549,1.50071,0.172486])
ck('nonclaim_full_rundec', 'not full RunDec parity' in coeff['metadata']['non_claims'])
val=json.loads(subprocess.check_output([str(ROOT/'scripts/qcd_coefficient_table_vendoring_and_4loop_evaluator_v76.py'),'validate'],text=True))
ck('validation_pass', val['status']=='PASS')
out=json.loads(subprocess.check_output([str(ROOT/'scripts/qcd_coefficient_table_vendoring_and_4loop_evaluator_v76.py'),'eval'],text=True))
ck('eval_status', out['status']=='APF_V76_4LOOP_FIXED_NF_EVALUATOR_CLOSED')
ck('has_c_b', set(out['results'].keys())=={'c','b'})
ck('mc_reasonable', 0.9 < out['results']['c']['mass_target_4loop_fixed_nf_GeV'] < 1.2)
ck('mb_reasonable', 3.6 < out['results']['b']['mass_target_4loop_fixed_nf_GeV'] < 3.9)
tex=(ROOT/'paper/QCD_COEFFICIENT_TABLE_VENDORING_AND_4LOOP_EVALUATOR_v76.tex').read_text()
for token in ['P_{\\rm 4loop\\ fixed\\text{-}n_f\\ evaluator\\ closed}','not claimed','RunDec']:
    ck('tex_token_'+token, token in tex)
passed=sum(1 for _,c in checks if c)
report=f"QCD_COEFFICIENT_TABLE_VENDORING_AND_4LOOP_EVALUATOR_PASS\nTotal checks: {passed}/{len(checks)}\n" + '\n'.join(f"{'PASS' if c else 'FAIL'} {n}" for n,c in checks)
(ROOT/'reports/v76_verifier_report.txt').write_text(report)
print(report)
sys.exit(0 if passed==len(checks) else 1)
