#!/usr/bin/env python3
import csv, json, math, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond))); print(('PASS' if cond else 'FAIL'), name)
def rows(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def txt(path): return (ROOT/path).read_text(encoding='utf-8')
files=[
 'paper/TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION_v60.tex',
 'scripts/top_msr_multiloop_numeric_evaluator_v60.py',
 'coefficients/top_msr_coefficients_LO_only_v60.json',
 'tables/top_msr_multiloop_numeric_evaluator_results_v60.csv',
 'tables/top_msr_evaluator_closure_status_v60.csv',
 'tables/top_msr_required_coefficients_for_v61_v60.csv',
 'tables/top_msr_evaluator_fail_closed_tests_v60.csv',
 'tables/top_msr_source_reference_manifest_v60.csv',
 'tables/global_trace_to_scheme_closure_registry_v60.csv',
 'tables/trace_to_scheme_case_table_v60.csv',
 'schemas/top_msr_multiloop_numeric_evaluator_schema_v60.json',
 'reports/top_msr_multiloop_numeric_evaluator_v60_LO_output.json',
 'reports/top_msr_multiloop_numeric_evaluator_v60_L2_fail_closed_output.json',
 'reports/top_msr_multiloop_numeric_evaluator_v60_data.json',
 'reports/top_msr_multiloop_numeric_evaluator_summary_v60.md',
 'README_v60.md'
]
for f in files: check('exists_'+f.replace('/','_'), (ROOT/f).exists())
j=json.loads(txt(Path('reports/top_msr_multiloop_numeric_evaluator_v60_data.json')))
check('stamp', j['stamp']=='TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION_PASS')
check('closed_status', j['closed_status']=='P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary')
check('source_mt', abs(j['source']['m_t_MSR_Rstar_GeV']-168.1690557938)<1e-12)
check('source_rstar', abs(j['source']['Rstar_GeV']-85.8572226983853)<1e-9)
check('alpha_R_range', 0.1190<j['LO_result']['alpha_s_Rstar']<0.1191)
check('lo_pole_value', abs(j['LO_result']['top_pole_LO_witness_GeV']-172.506466595364)<1e-9)
check('lo_residual', abs(j['LO_result']['residual_vs_PDG_direct_GeV']+0.053533404636)<1e-9)
check('fail_closed_stamp', j['fail_closed_test']['stamp']=='TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_FAIL_CLOSED')
check('fail_closed_c2', 'c2' in j['fail_closed_test']['missing_coefficients'])
for s in ['P_physical_final','exact_pole_mass','MC_mass_equality','full_multiloop_numeric_conversion','zero_residual','target_fitted_coefficients']:
    check('not_claimed_'+s, s in j['not_claimed'])
# run evaluator live
cmd=['python3',str(ROOT/'scripts'/'top_msr_multiloop_numeric_evaluator_v60.py'),'--coefficients',str(ROOT/'coefficients'/'top_msr_coefficients_LO_only_v60.json'),'--loop-order','1','--audit-target','172.56']
run=subprocess.run(cmd,capture_output=True,text=True)
check('live_LO_exit0', run.returncode==0)
live=json.loads(run.stdout)
check('live_LO_stamp', live['stamp']=='TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_PASS')
check('live_LO_value', abs(live['m_pole_witness_GeV']-172.506466595364)<1e-9)
cmd2=cmd.copy(); cmd2[cmd2.index('--loop-order')+1]='2'
run2=subprocess.run(cmd2,capture_output=True,text=True)
check('live_L2_exit2', run2.returncode==2)
live2=json.loads(run2.stdout)
check('live_L2_fail_stamp', live2['stamp']=='TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_FAIL_CLOSED')
check('live_L2_missing_c2', 'c2' in live2['missing_coefficients'])
# coefficients
coeff=json.loads(txt(Path('coefficients/top_msr_coefficients_LO_only_v60.json')))
check('coeff_schema', coeff['schema']=='APF_TOP_MSR_EVALUATOR_COEFFICIENTS_v60')
check('coeff_c1_CF', abs(float(coeff['c']['1'])-4/3)<1e-12)
check('coeff_missing_L4', '4' in coeff['missing_required_for_loop_orders'])
check('coeff_forbidden', 'Do not infer' in coeff['forbidden'])
# tables
res=rows('top_msr_multiloop_numeric_evaluator_results_v60.csv')
check('results_four_rows', len(res)==4)
by={r['loop_order']:r for r in res}
check('row_LO_evaluated', by['1']['status']=='evaluated')
for L in ['2','3','4']:
    check('row_L'+L+'_fail_closed', by[L]['status']=='fail-closed')
status=rows('top_msr_evaluator_closure_status_v60.csv')
check('status_rows4', len(status)==4)
check('status_full_final_not_claimed', any(r['object']=='full physical-final top mass' and r['status']=='not claimed' for r in status))
req=rows('top_msr_required_coefficients_for_v61_v60.csv')
check('required_coeff_rows5', len(req)==5)
for fam in ['MSR-pole difference','R-evolution','QCD beta function','OS-MSbar relation','threshold decoupling']:
    check('required_family_'+re.sub('[^A-Za-z0-9]+','_',fam), any(r['family']==fam for r in req))
ft=rows('top_msr_evaluator_fail_closed_tests_v60.csv')
check('fail_tests_4', len(ft)==4)
check('fail_tests_have_fail_closed', any(r['observed']=='FAIL_CLOSED' for r in ft))
refs=rows('top_msr_source_reference_manifest_v60.csv')
for sid in ['MSR2018','RunDec3','Marquard2015/2016','PDG2025']:
    check('ref_'+sid.replace('/','_'), any(r['source_id']==sid for r in refs))
# schema and registry
schema=json.loads(txt(Path('schemas/top_msr_multiloop_numeric_evaluator_schema_v60.json')))
check('schema_name', schema['schema_name']=='APF_TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_SCHEMA_v60')
check('schema_LO_only', schema['implemented_closed_loop_orders']==[1])
check('schema_fail_closed_orders', schema['fail_closed_loop_orders_pending_coefficients']==[2,3,4])
check('schema_target_not_used', 'audit_target is never used in calculation' in schema['no_smuggling_rules'])
reg=rows('global_trace_to_scheme_closure_registry_v60.csv')
bysec={r['sector']:r for r in reg}
check('registry_top_status', bysec['top']['highest_closed_status']=='P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary')
check('registry_top_next_v61', 'v61' in bysec['top']['boundary_or_next_gate'])
case=rows('trace_to_scheme_case_table_v60.csv')
check('case_top_v60', any(r['sector']=='top' and r['v59_registry_status']=='P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary' for r in case))
tex=txt(Path('paper/TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION_v60.tex'))
for phrase in ['Top MSR Multiloop Numeric Evaluator Implementation','Fail-closed multiloop boundary','No final-top overclaim','TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_FAIL_CLOSED']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
readme=txt(Path('README_v60.md'))
check('readme_status', 'P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary' in readme)
# inherited v59 available
for f in ['scripts/check_top_msr_full_qcd_conversion_ledger_v59.py','tables/top_msr_full_qcd_conversion_ledger_v59.csv','paper/TOP_MSR_FULL_QCD_CONVERSION_LEDGER_v59.tex']:
    check('inherited_'+f.replace('/','_'), (ROOT/f).exists())
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:', failed)
    raise SystemExit(1)
print('TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION_PASS')
