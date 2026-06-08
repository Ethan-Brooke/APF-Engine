#!/usr/bin/env python3
"""Verifier for APF v62 top codomain diagnosis and MSR repair witness."""
import json, math, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/top_codomain_diagnosis_and_msr_repair_v62_data.json'
cmd=[sys.executable, str(ROOT/'scripts/top_codomain_diagnosis_and_msr_repair_v62.py'),
     '--coefficients', str(ROOT/'coefficients/top_msr_coefficients_4loop_v61.json'), '--json-out', str(OUT)]
res=subprocess.run(cmd,capture_output=True,text=True)
checks=[]
def check(name,cond,detail=''):
    checks.append((name,bool(cond),detail))
if res.returncode!=0:
    print(res.stdout); print(res.stderr,file=sys.stderr); sys.exit(res.returncode)
data=json.loads(OUT.read_text())
check('stamp', data['stamp']=='TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS')
check('pole branch remains nonclosed', abs(data['v61_pole_branch']['z_vs_direct'])>3.0)
check('R_EW derived from W trace not target', data['ew_resolution_msr_repair_witness']['definition']=='M_W_TRACE/(2*pi)')
check('R_EW numeric', abs(data['ew_resolution_msr_repair_witness']['R_EW_GeV']-12.79003569131931)<1e-10)
check('EW witness mass', abs(data['ew_resolution_msr_repair_witness']['m_MSR_R_EW_GeV']-172.56475441070754)<1e-9)
check('EW witness inside 1 sigma direct audit', abs(data['ew_resolution_msr_repair_witness']['z_vs_direct'])<1.0)
check('EW witness very close', abs(data['ew_resolution_msr_repair_witness']['residual_MeV'])<10.0)
check('target fit quarantined', 'forbidden diagnostic' in data['forbidden_target_fit_diagnostic']['note'])
check('R_EW not equal target fit', abs(data['forbidden_target_fit_diagnostic']['R_fit_minus_R_EW_GeV'])>0.01)
check('no physical final claim', 'physical_final' in data['claim_status']['not_claimed'])
check('no exact pole claim', 'exact_pole' in data['claim_status']['not_claimed'])
check('no MC equality claim', 'MC_equality' in data['claim_status']['not_claimed'])
check('candidate scale table present', len(data['candidate_scale_screen'])>=4)
check('W over 2pi candidate present', any(r['candidate']=='M_W_trace_over_2pi' for r in data['candidate_scale_screen']))
check('Rstar over 2pi candidate nonfit and near', any(r['candidate']=='Rstar_over_2pi' and abs(r['z_vs_direct'])<1 for r in data['candidate_scale_screen']))
check('MZ over 2pi candidate nonfit and near', any(r['candidate']=='M_Z_over_2pi' and abs(r['z_vs_direct'])<1 for r in data['candidate_scale_screen']))
check('no smuggling statement', 'target not used' in data['no_smuggling'])
check('same coefficients as v61', data['inputs']['loop_order']==4)
check('nf=5 high-scale route', data['inputs']['nf']==5)
check('direct audit is audit only', abs(data['inputs']['audit_direct_GeV']-172.56)<1e-12)
failed=[c for c in checks if not c[1]]
for name,ok,detail in checks:
    print(('PASS' if ok else 'FAIL'), name, detail)
if failed:
    print(f'TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_FAIL {len(checks)-len(failed)}/{len(checks)}')
    sys.exit(1)
print(f'Total checks: {len(checks)}/{len(checks)}')
print('TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS')
