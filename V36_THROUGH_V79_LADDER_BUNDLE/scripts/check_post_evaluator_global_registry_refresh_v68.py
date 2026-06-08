#!/usr/bin/env python3
import csv,json,re,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)
def read(p): return (ROOT/p).read_text(encoding='utf-8')
def js(p): return json.loads(read(p))
def rows(p):
    with (ROOT/p).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
files=['paper/POST_EVALUATOR_GLOBAL_REGISTRY_REFRESH_v68.tex','registry/post_evaluator_global_registry_v68.csv','registry/top_post_evaluator_registry_v68.csv','registry/claim_ladder_v68.csv','reports/post_evaluator_global_registry_refresh_v68_data.json','reports/post_evaluator_global_registry_refresh_summary_v68.md','README_v68.md']
for f in files: check('exists_'+f.replace('/','_'),(ROOT/f).exists())
d=js('reports/post_evaluator_global_registry_refresh_v68_data.json')
check('stamp',d['stamp']=='POST_EVALUATOR_GLOBAL_REGISTRY_REFRESH_PASS')
check('no_physical_final',d['physical_final_assigned_any_sector'] is False)
check('sector_count',d['sector_count']==6)
check('top_value_current',abs(d['top_current_value_GeV']-172.716805649486)<1e-12)
check('top_old_witness_quarantined',abs(d['top_previous_fixed_order_witness_GeV']-172.564754410708)<1e-12)
check('top_pole_blocked',abs(d['top_pole_branch_blocked_GeV']-174.016604383647)<1e-12)
reg=rows('registry/post_evaluator_global_registry_v68.csv')
check('registry_rows',len(reg)==6)
sector_names={r['sector'] for r in reg}
for s in ['W / EW','charged leptons','charm','bottom','top','light quarks']:
    check('has_'+s.replace(' ','_').replace('/','_'),s in sector_names)
top=[r for r in reg if r['sector']=='top'][0]
check('top_status_updated','R-evolution' in top['status'] and 'numeric_evaluator_closed' in top['status'])
check('top_no_pole_boundary','Pole branch blocked' in top['boundary'] and 'no MC equality' in top['boundary'])
check('old_v63_not_top_primary','172.564754410708' not in top['primary_value'])
check('v67_is_top_primary','172.716805649486' in top['primary_value'])
topreg=rows('registry/top_post_evaluator_registry_v68.csv')
check('top_registry_three_rows',len(topreg)==3)
roles={r['registry_action'] for r in topreg}
check('quarantine_old',any('quarantine' in x for x in roles))
check('promote_new',any('promote' in x for x in roles))
check('retain_blocked',any('blocked' in x for x in roles))
ladder=rows('registry/claim_ladder_v68.csv')
check('ladder_has_reserved_final',any(r['status']=='[P_physical_final]' and 'not assigned' in r['definition'] for r in ladder))
tex=read('paper/POST_EVALUATOR_GLOBAL_REGISTRY_REFRESH_v68.tex')
for phrase in ['POST\\_EVALUATOR\\_GLOBAL\\_REGISTRY\\_REFRESH\\_PASS','No-smuggling controls retained','current registry value','blocked branch','No sector is assigned']:
    check('tex_'+re.sub('[^A-Za-z0-9]+','_',phrase), phrase in tex)
# inherited v67 result should exist and be consistent
v67=js('reports/top_msr_r_evolution_numeric_evaluator_v67_data.json')
check('inherits_v67',abs(v67['m_t_MSR_REW_4loop_GeV']-d['top_current_value_GeV'])<1e-12)
# selected prior verifier if present
p=ROOT/'scripts/check_top_msr_r_evolution_numeric_evaluator_v67.py'
if p.exists():
    r=subprocess.run(['python',str(p)],capture_output=True,text=True,cwd=ROOT,timeout=60)
    check('v67_verifier_still_passes',r.returncode==0 and 'TOP_MSR_R_EVOLUTION_COEFFICIENT_INGESTION_EVALUATOR_PASS' in r.stdout)
failed=[n for n,c in checks if not c]
print(f'Total checks: {len(checks)-len(failed)}/{len(checks)}')
if failed:
    print('FAILED:',failed); sys.exit(1)
print('POST_EVALUATOR_GLOBAL_REGISTRY_REFRESH_PASS')
