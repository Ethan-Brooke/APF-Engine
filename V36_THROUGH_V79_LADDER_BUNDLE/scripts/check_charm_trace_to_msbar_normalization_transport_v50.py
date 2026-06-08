#!/usr/bin/env python3
from __future__ import annotations
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,cond): checks.append((name,bool(cond)))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def rows(rel):
    with (ROOT/rel).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def data(rel): return json.loads(text(rel))
required=['paper/CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_v50.tex','tables/charm_trace_to_msbar_normalization_v50.csv','tables/charm_pdg_ledger_audit_v50.csv','tables/charm_export_gates_v50.csv','tables/charm_forbidden_inputs_v50.csv','tables/charm_residual_channels_v50.csv','tables/trace_to_scheme_case_table_v50.csv','reports/charm_trace_to_msbar_normalization_transport_summary_v50.md','reports/charm_trace_to_msbar_normalization_transport_v50_data.json','README_v50.md']
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_v50.tex'); summary=text('reports/charm_trace_to_msbar_normalization_transport_summary_v50.md'); readme=text('README_v50.md'); j=data('reports/charm_trace_to_msbar_normalization_transport_v50_data.json')
case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v50.csv')}; norm={r['quantity']:r for r in rows('tables/charm_trace_to_msbar_normalization_v50.csv')}; audit=rows('tables/charm_pdg_ledger_audit_v50.csv')[0]; gates={r['gate']:r for r in rows('tables/charm_export_gates_v50.csv')}; forbidden={r['forbidden_input']:r for r in rows('tables/charm_forbidden_inputs_v50.csv')}; chans={r['channel']:r for r in rows('tables/charm_residual_channels_v50.csv')}
T=0.680091224926; fac=math.sqrt(7/2); pred=T*fac; ref=1.2730; unc=0.0046; absres=pred-ref; rel=100*absres/ref; sig=absres/unc; env=2.6; ratio=abs(rel)/env
for nd in ['Charm Trace-to-','Schur-count normalization','\\kappa_c=\\sqrt{\\frac72}','1.272334177712','No-smuggling rule','P_{\\rm export\\ candidate}']:
    check('tex_contains_'+nd[:35].replace(' ','_').replace('\\','bs'), nd in tex)
for nd in ['CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_PASS','P_export_candidate_MSBAR_self_scale_v50','sqrt(7/2)','PDG 2025 ledger audit','Not claimed']:
    check('summary_contains_'+nd[:35].replace(' ','_'), nd in summary)
for nd in ['CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_PASS','P_export_candidate_MSBAR_self_scale_v50','python scripts/check_charm_trace_to_msbar_normalization_transport_v50.py']:
    check('readme_contains_'+nd[:35].replace(' ','_'), nd in readme)
check('json_status',j['status']=='CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_PASS'); check('json_package',j['package']=='APF_v50_CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT'); check('json_claim',j['claim']=='P_export_candidate_MSBAR_self_scale_v50')
check('json_trace',abs(j['trace_anchor']['mc_TRACE_GeV']-T)<1e-15); check('json_counts',j['apf_counts']=={'K_SM':61,'K_c':16,'K_b':3,'N_gen':3,'numerator_K_SM_plus_K_c':77,'denominator_K_c_plus_K_b_plus_N_gen':22})
check('json_fac_sq',abs(j['transport']['kappa_c_squared']-3.5)<1e-15); check('json_fac',abs(j['transport']['kappa_c']-fac)<1e-15); check('json_pred',abs(j['transport']['Phi_c_MSbar_mc_GeV']-pred)<1e-15)
check('json_ref',abs(j['external_audit']['reference_GeV']-ref)<1e-15); check('json_unc',abs(j['external_audit']['uncertainty_GeV']-unc)<1e-15); check('json_absres',abs(j['external_audit']['absolute_residual_GeV']-absres)<1e-15); check('json_rel',abs(j['external_audit']['relative_residual_percent']-rel)<1e-15); check('json_sigma',abs(j['external_audit']['sigma_units']-sig)<1e-15); check('json_inside',j['external_audit']['inside_uncertainty'] is True)
check('json_env',abs(j['covariance']['Schur_structural_envelope_percent']-env)<1e-15); check('json_ratio',abs(j['covariance']['residual_over_Schur_envelope']-ratio)<1e-15); check('json_next',j['next_theorem']=='APF_BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER')
for q,v in [('mc_TRACE',T),('K_SM',61),('K_c',16),('K_b',3),('N_gen',3),('Schur numerator K_SM+K_c',77),('Schur denominator K_c+K_b+N_gen',22)]:
    check('norm_'+q.replace(' ','_'), q in norm); check('norm_val_'+q.replace(' ','_'), abs(float(norm[q]['value'])-v)<1e-12)
check('norm_kappa_sq',abs(float(norm['kappa_c^2']['value'])-3.5)<1e-15); check('norm_kappa',abs(float(norm['kappa_c']['value'])-fac)<1e-15); check('norm_pred',abs(float(norm['Phi_c_v50_MSbar_self_scale']['value'])-pred)<1e-15)
check('audit_pred',abs(float(audit['APF_prediction_GeV'])-pred)<1e-15); check('audit_ref',abs(float(audit['PDG_2025_value_GeV'])-ref)<1e-15); check('audit_unc',abs(float(audit['PDG_2025_uncertainty_GeV'])-unc)<1e-15); check('audit_absres',abs(float(audit['absolute_residual_GeV'])-absres)<1e-15); check('audit_rel',abs(float(audit['relative_residual_percent'])-rel)<1e-15); check('audit_sig',abs(float(audit['sigma_units'])-sig)<1e-15); check('audit_status',audit['status']=='inside_PDG_2025_uncertainty')
for g in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE_PROTOCOL','G5_NO_SMUGGLING_AUDIT','G6_RESIDUAL_CHANNELS']:
    check('gate_'+g,g in gates); check('gate_pass_'+g,gates[g]['v50_status']=='pass'); check('gate_guard_'+g,gates[g]['no_smuggling_guard']!='')
for forb in ['PDG charm mass to define kappa_c','lattice charm averages to define kappa_c','QCD sum-rule charm value to define kappa_c','least-squares choice of sqrt(7/2)','alpha_s chosen from charm residual','threshold convention chosen from charm residual','pole mass conversion to set trace value','manual rescaling of mc_TRACE']:
    check('forbidden_'+forb.replace(' ','_'),forb in forbidden); check('forbidden_not_used_'+forb.replace(' ','_'),forbidden[forb]['v50_audit']=='not used')
for ch,st in [('Schur_count_normalization','closed'),('self_scale_MSbar_codomain','closed'),('PDG_ledger_audit','closed_for_comparison'),('QCD_covariance','admitted_boundary'),('physical_final','not_claimed')]:
    check('channel_'+ch,ch in chans); check('channel_status_'+ch,chans[ch]['status']==st)
for s in ['EW/W','bottom','charged leptons','top','charm','light quarks']: check('case_has_'+s.replace('/','_').replace(' ','_'),s in case)
check('case_charm_status',case['charm']['physical_export_status']=='P_export_candidate_MSBAR_self_scale_v50'); check('case_charm_route','Schur-count normalization' in case['charm']['route_status']); check('case_charm_boundary','physical_final not claimed' in case['charm']['first_failed_gate_or_boundary']); check('case_charged_preserved','P_QED_branch_complete' in case['charged leptons']['physical_export_status']); check('case_top_preserved',case['top']['physical_export_status']=='P_export_candidate')
for nc in ['P_physical_final','zero_residual','full_QCD_covariance_final','pole_mass_prediction']: check('not_claimed_'+nc,nc in j['not_claimed'])
for forb in j['forbidden_inputs_not_used']: check('json_forbidden_present_'+forb.replace(' ','_'),forb in forbidden)
for script in ['check_trace_to_scheme_export_v35.py','check_top_msr_scale_selection_v37.py','check_charged_lepton_qed_closure_boundary_v49.py']:
    check('inherited_exists_'+script,(ROOT/'scripts'/script).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_PASS')
