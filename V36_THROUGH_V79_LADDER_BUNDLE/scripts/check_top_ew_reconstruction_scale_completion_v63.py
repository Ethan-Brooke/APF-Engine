#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/top_ew_reconstruction_scale_completion_v63_data.json'
cmd=[sys.executable, str(ROOT/'scripts/top_ew_reconstruction_scale_completion_v63.py'), '--root', str(ROOT), '--json-out', str(OUT)]
res=subprocess.run(cmd,capture_output=True,text=True)
checks=[]
def check(name, cond): checks.append((name, bool(cond)))
if res.returncode!=0:
    print(res.stdout); print(res.stderr,file=sys.stderr); sys.exit(res.returncode)
data=json.loads(OUT.read_text())
scale=data['scale_theorem']; comp=data['direct_completion']; stat=data['status']; gates=data['gates']
check('v63 stamp', data['stamp']=='TOP_EW_RECONSTRUCTION_SCALE_COMPLETION_PASS')
check('inherits v62 pass', data['inherited_v62_stamp']=='TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS')
check('scale theorem closed stamp', scale['stamp']=='APF_EW_RECONSTRUCTION_SCALE_THEOREM_CLOSED')
check('R formula is MW over 2pi', scale['R_rec_formula']=='M_W_TRACE/(2*pi)')
check('lambda equals one over 2pi', abs(scale['lambda_error'])<1e-15)
check('R_EW numeric', abs(scale['R_rec_GeV']-12.79003569131931)<1e-10)
check('no target in scale theorem', scale['uses_target_mass'] is False and scale['uses_pdg_direct_mass'] is False)
check('no pole in scale theorem', scale['uses_pole_mass'] is False)
check('codomain direct MSR', comp['codomain']=='direct_reconstruction_MSR_at_R_EW')
check('completion value numeric', abs(comp['m_MSR_R_EW_GeV']-172.56475441070756)<1e-9)
check('residual is 4.754 MeV', abs(comp['residual_MeV']-4.754410707562329)<1e-6)
check('inside one sigma audit', comp['inside_one_sigma'] is True)
check('inside 100 MeV', comp['inside_100MeV'] is True)
check('z is tiny', abs(comp['z'])<0.02)
check('pole branch quarantined', abs(data['v61_pole_quarantine']['z_vs_direct'])>3.0)
check('forbidden target fit exists', 'R_fit_GeV' in data['forbidden_target_fit_diagnostic'])
check('R_EW not target fit', abs(data['forbidden_target_fit_diagnostic']['R_fit_minus_R_EW_GeV'])>0.01)
check('G1 present', 'MSR' in gates['G1_codomain_declared'])
check('G2 present', 'R_EW' in gates['G2_transport_supplied'] and 'R*' in gates['G2_transport_supplied'])
check('G3 present', 'four-loop' in gates['G3_constants_ledger'])
check('G4 present', 'covariance' in gates['G4_covariance_protocol'] or 'envelope' in gates['G4_covariance_protocol'])
check('G5 present', 'target-independent' in gates['G5_no_smuggling'])
check('G6 present', '4.754' in gates['G6_residual_channels'])
check('closed symbol direct MSR completion', 'P_direct-MSR-completion' in stat['closed_symbol'])
check('no physical final claim', 'physical_final' in stat['not_claimed'])
check('no MC equality claim', 'MC_equality' in stat['not_claimed'])
check('no exact pole claim', 'exact_pole' in stat['not_claimed'])
check('delta not zero not claimed', 'Delta_t=0' in stat['not_claimed'])
check('registry row top', data['registry_row']['sector']=='top')
check('registry blocks pole route', 'pole/MC' in data['registry_row']['blocked_route'])
check('candidate screen preserved', len(data['candidate_scale_screen'])>=4)
failed=[c for c in checks if not c[1]]
for name,ok in checks:
    print(('PASS' if ok else 'FAIL'), name)
if failed:
    print(f'TOP_EW_RECONSTRUCTION_SCALE_COMPLETION_FAIL {len(checks)-len(failed)}/{len(checks)}')
    sys.exit(1)
print(f'Total checks: {len(checks)}/{len(checks)}')
print('TOP_EW_RECONSTRUCTION_SCALE_COMPLETION_PASS')
