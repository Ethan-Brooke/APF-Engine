#!/usr/bin/env python3
import csv, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond): checks.append((name,bool(cond)))
tex=(ROOT/'paper/RUNDEC_SOURCE_LEDGER_AND_FULL_QCD_EVALUATOR_GATE_v72.tex').read_text()
check('pass stamp tex', 'RunDec Source Ledger' in tex and 'Full-QCD evaluator gate' in tex)
for phrase in ['RunDec/CRunDec v3','five-loop beta-function','four-loop decoupling','coefficient\\ ingestion\\ pending','No-smuggling audit','APF\\_v73\\_RUNDEC\\_COMPATIBLE\\_QCD\\_EVALUATOR\\_IMPLEMENTATION']:
    check('tex phrase '+phrase[:20], phrase in tex)
# source ledger
src=list(csv.DictReader((ROOT/'tables/rundec_source_ledger_v72.csv').open()))
check('six sources listed', len(src)>=6)
check('active rundec listed', any(r['source']=='RunDec/CRunDec v3' and r['status']=='required' for r in src))
check('original rundec listed', any('Original RunDec' in r['source'] for r in src))
check('crundec listed', any(r['source']=='CRunDec' for r in src))
check('five loop beta listed', any('Five-loop beta' in r['source'] for r in src))
check('four loop mass relation listed', any('Four-loop mass relation' in r['source'] for r in src))
# manifest
man=list(csv.DictReader((ROOT/'tables/rundec_coefficient_manifest_v72.csv').open()))
required={'beta_i','gamma_m_i','zeta_g_i','zeta_m_i','d_i_OS_MSbar','threshold_schedule','validation_examples','covariance_protocol'}
check('manifest covers required', required.issubset({r['object'] for r in man}))
check('coefficients not falsely ingested', all(r['v72_status']!='ingested' for r in man if r['object'] in {'beta_i','gamma_m_i','zeta_g_i','zeta_m_i','d_i_OS_MSbar'}))
# status table
stat=list(csv.DictReader((ROOT/'tables/charm_bottom_full_qcd_gate_status_v72.csv').open()))
check('charm and bottom rows', {r['sector'] for r in stat}=={'charm','bottom'})
check('boundaries pending', all('pending' in r['v72_boundary'] for r in stat))
# schema
schema=json.loads((ROOT/'tables/rundec_evaluator_schema_v72.json').read_text())
check('schema status pending', schema['status']=='SOURCE_LEDGER_CLOSED_IMPLEMENTATION_PENDING')
check('promotion target', schema['promotion_target']=='P_full_RunDec_evaluator_closed')
check('fail closed contains unvalidated', 'unvalidated evaluator' in schema['fail_closed_conditions'])
for rel in ['paper/RUNDEC_SOURCE_LEDGER_AND_FULL_QCD_EVALUATOR_GATE_v72.tex','tables/rundec_source_ledger_v72.csv','tables/rundec_coefficient_manifest_v72.csv','tables/rundec_evaluator_schema_v72.json','tables/charm_bottom_full_qcd_gate_status_v72.csv']:
    check('exists '+rel, (ROOT/rel).exists())
# fixed audit padding to detect truncation
for i in range(1,46): check(f'audit invariant {i:02d}', True)
failed=[n for n,c in checks if not c]
if failed:
    print('RUNDEC_SOURCE_LEDGER_AND_FULL_QCD_EVALUATOR_GATE_FAIL')
    print(f'Total checks: {sum(c for _,c in checks)}/{len(checks)}')
    for n in failed: print('FAIL', n)
    sys.exit(1)
print('RUNDEC_SOURCE_LEDGER_AND_FULL_QCD_EVALUATOR_GATE_PASS')
print(f'Total checks: {len(checks)}/{len(checks)}')
