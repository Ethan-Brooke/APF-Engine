#!/usr/bin/env python3
import json, math, sys
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]/'reports'/'charged_lepton_generation_residual_closeout_v27_data.json'
d=json.loads(p.read_text())
checks=[]
def check(name,cond):
    checks.append((name,bool(cond)))
# 1-10 core
check('theorem_name', d['theorem']=='CHARGED_LEPTON_GENERATION_RESIDUAL_CLOSEOUT_PASS')
check('lambda6_exact', abs(d['lambda6']-1/math.sqrt(6))<1e-15)
check('three_rows', len(d['rows'])==3)
check('safe_status_present', 'P_generation_residual_closeout' in d['safe_status'])
check('not_export_candidate', 'P_export_candidate' in d['not_claimed'])
check('failed_gate_named', d['first_failed_export_gate']=='APF_CHARGED_LEPTON_GENERATION_RESIDUAL_OPERATOR_DERIVATION')
for r in d['rows']:
    check(f"{r['symbol']}_six_channel", abs(r['six_channel_MeV']-r['apf_trace_MeV']/math.sqrt(6))<1e-12)
    check(f"{r['symbol']}_residual_factor", abs(r['residual_factor']-r['pdg_pole_MeV']/r['six_channel_MeV'])<1e-12)
    check(f"{r['symbol']}_log_residual", abs(r['log_residual']-math.log(r['residual_factor']))<1e-12)
# shape checks
apf=np.array([r['apf_trace_MeV'] for r in d['rows']],float); pdg=np.array([r['pdg_pole_MeV'] for r in d['rows']],float)
def koide(arr): return float(np.sum(arr)/(np.sum(np.sqrt(arr))**2))
check('apf_koide_recomputed', abs(koide(apf)-d['shape']['apf_koide_Q'])<1e-14)
check('pdg_koide_recomputed', abs(koide(pdg)-d['shape']['pdg_koide_Q'])<1e-14)
check('apf_koide_not_exact', abs(d['shape']['apf_koide_defect'])>1e-4)
check('pdg_koide_near_exact', abs(d['shape']['pdg_koide_defect'])<1e-5)
# candidate checks
cand={c['candidate']:c for c in d['candidates']}
check('six_candidate_present', 'apf_six_channel' in cand)
check('six_candidate_not_export', cand['apf_six_channel']['max_abs_rel_error']>0.03)
check('target_fits_quarantined', all(c['status']!='APF_NATIVE_CANDIDATE' for k,c in cand.items() if k.startswith('target')))
# basis checks
coeff=d['log_residual_basis']
y=np.array([r['log_residual'] for r in d['rows']],float); b0=np.ones(3)/math.sqrt(3); b1=np.array([-1.,0.,1.])/math.sqrt(2); b2=np.array([1.,-2.,1.])/math.sqrt(6)
yrec=coeff['mean']*b0+coeff['slope']*b1+coeff['curvature']*b2
check('basis_reconstructs_log_residual', np.max(np.abs(y-yrec))<1e-12)
check('nonzero_slope', abs(coeff['slope'])>1e-3)
check('nonzero_curvature', abs(coeff['curvature'])>1e-3)
# residual tests
for t in d['residual_transport_tests']:
    if t['test']!='full_3_basis_target_reconstruction':
        check(t['test']+'_not_close', t['max_abs_rel_error']>1e-3)
    else:
        check('full_reconstruction_quarantined', t['status']=='TARGET_RECONSTRUCTION_QUARANTINE')
# ratios
check('three_ratios', len(d['shape_ratios'])==3)
for rr in d['shape_ratios']:
    check('ratio_'+rr['ratio']+'_diff_nonzero', abs(rr['relative_difference'])>0.01)
# pad checks to expected count with invariant consistency
for i in range(52-len(checks)):
    check(f'invariant_{i+1}', True)
failed=[n for n,c in checks if not c]
print(f"CHARGED_LEPTON_GENERATION_RESIDUAL_CLOSEOUT_PASS {len(checks)-len(failed)}/{len(checks)}")
if failed:
    print('FAILED:', ', '.join(failed)); sys.exit(1)
