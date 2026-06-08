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
required=['paper/BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_v51.tex','tables/heavy_quark_route_registry_v51.csv','tables/heavy_quark_external_ledger_audit_v51.csv','tables/shared_heavy_qcd_ledger_schema_v51.csv','tables/shared_heavy_qcd_export_gates_v51.csv','tables/shared_heavy_qcd_forbidden_inputs_v51.csv','tables/shared_heavy_qcd_residual_channels_v51.csv','tables/trace_to_scheme_case_table_v51.csv','reports/bottom_top_charm_shared_qcd_covariance_ledger_summary_v51.md','reports/bottom_top_charm_shared_qcd_covariance_ledger_v51_data.json','README_v51.md']
for rel in required: check('exists_'+rel.replace('/','_'),(ROOT/rel).exists())
tex=text('paper/BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_v51.tex'); summary=text('reports/bottom_top_charm_shared_qcd_covariance_ledger_summary_v51.md'); readme=text('README_v51.md'); j=data('reports/bottom_top_charm_shared_qcd_covariance_ledger_v51_data.json')
registry={r['sector']:r for r in rows('tables/heavy_quark_route_registry_v51.csv')}; audit={r['sector']:r for r in rows('tables/heavy_quark_external_ledger_audit_v51.csv')}; schema={r['ledger_item']:r for r in rows('tables/shared_heavy_qcd_ledger_schema_v51.csv')}; gates={r['gate']:r for r in rows('tables/shared_heavy_qcd_export_gates_v51.csv')}; forbidden={r['forbidden_input']:r for r in rows('tables/shared_heavy_qcd_forbidden_inputs_v51.csv')}; chans={r['channel']:r for r in rows('tables/shared_heavy_qcd_residual_channels_v51.csv')}; case={r['sector']:r for r in rows('tables/trace_to_scheme_case_table_v51.csv')}
mc_pred=1.272334177712253; mc_ref=1.2730; mc_unc=0.0046; mb_trace=4.177490455927; mb_ref=4.183; mb_unc=0.007; mt_trace=168.1690557938; R=85.8572226983853
mc_abs=mc_pred-mc_ref; mc_rel=100*mc_abs/mc_ref; mc_sig=mc_abs/mc_unc; mb_abs=mb_trace-mb_ref; mb_rel=100*mb_abs/mb_ref; mb_sig=mb_abs/mb_unc
for nd in ['Shared heavy-quark QCD ledger admissibility','m_c^{\\overline{\\rm MS}}(m_c)','m_b^{\\overline{\\rm MS}}(m_b)','m_t^{\\rm MSR}(R_\\star)','MSR-conversion ledger','does not claim']:
    check('tex_contains_'+nd[:30].replace(' ','_').replace('\\','bs'), nd in tex)
for nd in ['BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_PASS','Same-codomain MSbar audits','Top boundary','Not claimed','APF_LIGHT_QUARK_TRACE_TO_MSBAR_2GEV_CHIRAL_LATTICE_TRANSPORT_MAP']:
    check('summary_contains_'+nd[:35].replace(' ','_'), nd in summary)
check('readme_stamp','BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_PASS' in readme); check('json_status',j['status']=='BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_PASS'); check('json_pkg',j['package']=='APF_v51_BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER')
for sec in ['charm','bottom','top']:
    check('registry_'+sec, sec in registry); check('audit_'+sec, sec in audit); check('json_route_'+sec, sec in j['heavy_routes'])
check('charm_status',registry['charm']['v51_status']=='P_export_candidate_MSBAR_self_scale_QCD_ledger_v51'); check('bottom_status',registry['bottom']['v51_status']=='P_export_candidate_MSBAR_self_scale_QCD_ledger_v51'); check('top_status',registry['top']['v51_status']=='P_export_candidate_MSR_Rstar_QCD_ledger_v51')
check('charm_audit_status',audit['charm']['audit_status']=='inside_same_codomain_uncertainty'); check('bottom_audit_status',audit['bottom']['audit_status']=='inside_same_codomain_uncertainty'); check('top_audit_status',audit['top']['audit_status']=='no_same_codomain_audit_until_conversion_ledger')
for key,val in [('charm APF_value_GeV',mc_pred),('charm external_value_GeV',mc_ref),('charm external_uncertainty_GeV',mc_unc),('charm absolute_residual_GeV',mc_abs),('charm relative_residual_percent',mc_rel),('charm sigma_units',mc_sig),('bottom APF_value_GeV',mb_trace),('bottom external_value_GeV',mb_ref),('bottom external_uncertainty_GeV',mb_unc),('bottom absolute_residual_GeV',mb_abs),('bottom relative_residual_percent',mb_rel),('bottom sigma_units',mb_sig)]:
    s,field=key.split(' ',1); check('audit_num_'+s+'_'+field, abs(float(audit[s][field])-val)<1e-12)
check('json_charm_num',abs(j['heavy_routes']['charm']['APF_value_GeV']-mc_pred)<1e-15 and abs(j['heavy_routes']['charm']['sigma_units']-mc_sig)<1e-15); check('json_bottom_num',abs(j['heavy_routes']['bottom']['APF_value_GeV']-mb_trace)<1e-15 and abs(j['heavy_routes']['bottom']['sigma_units']-mb_sig)<1e-15); check('json_top_num',abs(j['heavy_routes']['top']['APF_trace_GeV']-mt_trace)<1e-12 and abs(j['heavy_routes']['top']['R_star_GeV']-R)<1e-12)
for item in ['scheme_family','scale_mu','alpha_s_reference','beta_function_order','mass_anomalous_dimension_order','threshold_matching','scheme_conversion','covariance_matrix','forbidden_target_reuse']:
    check('schema_'+item,item in schema); check('schema_guard_'+item, schema[item]['no_smuggling_guard']!='')
for gate in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE_PROTOCOL','G5_NO_SMUGGLING_AUDIT','G6_RESIDUAL_CHANNELS']:
    check('gate_'+gate,gate in gates); check('gate_status_'+gate,gates[gate]['v51_status']!=''); check('gate_guard_'+gate,gates[gate]['boundary_or_guard']!='')
for forb in ['PDG charm mass to choose sqrt(7/2)','PDG bottom mass to edit mb_TRACE','direct top mass to choose R_star','pole/MC top mass as same-codomain audit','alpha_s tuned to minimize c,b,t residuals','thresholds chosen independently per residual','loop order selected after seeing residuals','scheme conversion coefficients adjusted by hand']:
    check('forbidden_'+forb.replace(' ','_').replace(',',''),forb in forbidden); check('forbidden_status_'+forb.replace(' ','_').replace(',',''), forbidden[forb]['v51_audit'] in ['not_used','blocked'])
for ch,st in [('same_codomain_MSbar_c','closed_for_export_candidate'),('same_codomain_MSbar_b','closed_for_export_candidate'),('top_MSR_Rstar','closed_for_export_candidate'),('top_conversion','boundary'),('alpha_s_threshold_covariance','typed_required'),('physical_final','not_claimed')]:
    check('channel_'+ch,ch in chans); check('channel_status_'+ch,chans[ch]['status']==st)
for sec in ['EW/W','bottom','charged leptons','top','charm','light quarks']:
    check('case_'+sec.replace('/','_').replace(' ','_'),sec in case)
check('case_bottom_v51',case['bottom']['physical_export_status']=='P_export_candidate_MSBAR_self_scale_QCD_ledger_v51'); check('case_top_v51',case['top']['physical_export_status']=='P_export_candidate_MSR_Rstar_QCD_ledger_v51'); check('case_charm_v51',case['charm']['physical_export_status']=='P_export_candidate_MSBAR_self_scale_QCD_ledger_v51'); check('case_leptons_preserved','P_QED_branch_complete' in case['charged leptons']['physical_export_status']); check('case_light_open','LIGHT_QUARK' in case['light quarks']['first_failed_gate_or_boundary'])
for nc in ['P_physical_final','zero_residual','top_pole_or_MC_mass','full_QCD_covariance_final','light_quark_chiral_lattice_closure']:
    check('not_claimed_'+nc,nc in j['not_claimed'])
for req in ['alpha_s_reference_and_covariance','beta_function_order','mass_anomalous_dimension_order','threshold_matching','scheme_conversion_coefficients','joint_covariance_matrix','residual_assignment_protocol']:
    check('json_req_'+req, req in j['shared_ledger_required_for_physical_final'])
for s in ['check_charm_trace_to_msbar_normalization_transport_v50.py','check_charged_lepton_qed_closure_boundary_v49.py','check_top_msr_scale_selection_v37.py']:
    check('inherited_'+s,(ROOT/'scripts'/s).exists())
passed=sum(ok for _,ok in checks); total=len(checks)
for name,ok in checks: print(('PASS' if ok else 'FAIL'),name)
print(f'Total checks: {passed}/{total}')
if passed!=total or total!=j.get('checks_total'):
    raise SystemExit(1)
print('BOTTOM_TOP_CHARM_SHARED_QCD_COVARIANCE_LEDGER_PASS')
