#!/usr/bin/env python3
import csv, json, math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)

def read_csv(name):
    with (ROOT/'tables'/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))
# Files exist
for rel in [
 'paper/LIGHT_QUARK_CHIRAL_LATTICE_TRANSPORT_GATE_v52.tex',
 'tables/light_quark_source_inventory_v52.csv',
 'tables/light_quark_pdg2025_codomain_ledger_v52.csv',
 'tables/light_quark_identity_transport_knockout_v52.csv',
 'tables/light_quark_chiral_lattice_transport_schema_v52.csv',
 'tables/light_quark_export_gates_v52.csv',
 'tables/light_quark_forbidden_inputs_v52.csv',
 'tables/light_quark_residual_channels_v52.csv',
 'tables/trace_to_scheme_case_table_v52.csv',
 'reports/light_quark_chiral_lattice_transport_gate_v52_data.json',
 'reports/light_quark_chiral_lattice_transport_gate_summary_v52.md'
]: check('exists_'+rel.replace('/','_'), (ROOT/rel).exists())
tex=(ROOT/'paper/LIGHT_QUARK_CHIRAL_LATTICE_TRANSPORT_GATE_v52.tex').read_text(encoding='utf-8')
for s in ['Light-Quark Chiral--Lattice Transport Gate','U_{\\chi{\\rm lat}}','T_u','No-smuggling','not claim']:
    check('tex_contains_'+re.sub('[^A-Za-z0-9]+','_',s), s in tex)
# Source inventory
src=read_csv('light_quark_source_inventory_v52.csv')
check('source_rows_ge_6', len(src)>=6)
status={r['source_object']:r['status'] for r in src}
check('source_Td_banked', status.get('T_d^APF[1]')=='banked_v41_down_family_trace')
check('source_Ts_banked', status.get('T_d^APF[2]')=='banked_v41_down_family_trace')
check('source_Tu_not_banked', status.get('T_u^APF[1]')=='not_banked_v52')
for r in src:
    if r['source_object'] in ('T_d^APF[1]','T_d^APF[2]'):
        check('source_trace_not_physical_'+r['source_object'], 'not a physical' in r['meaning'])
# PDG ledger
pdg=read_csv('light_quark_pdg2025_codomain_ledger_v52.csv')
check('pdg_has_three', {r['quark'] for r in pdg}=={'u','d','s'})
vals={r['quark']:float(r['PDG2025_MSbar_2GeV_MeV']) for r in pdg}
unc={r['quark']:float(r['uncertainty_MeV_90CL']) for r in pdg}
check('pdg_u_value', abs(vals['u']-2.16)<1e-12)
check('pdg_d_value', abs(vals['d']-4.70)<1e-12)
check('pdg_s_value', abs(vals['s']-93.5)<1e-12)
check('pdg_unc_positive', all(v>0 for v in unc.values()))
check('pdg_external_only', all('not used' in r['v52_use'] for r in pdg))
# Identity knockout math
kn=read_csv('light_quark_identity_transport_knockout_v52.csv')
kr={r['component']:r for r in kn}
check('u_blocked_by_missing_source', 'blocked' in kr['u']['diagnostic_status'])
Td=0.003870916422334*1000
Ts=0.087143281633652*1000
drel=100*(Td-4.70)/4.70
srel=100*(Ts-93.5)/93.5
check('d_identity_trace_value', abs(float(kr['d']['APF_trace_identity_MeV'])-Td)<1e-12)
check('s_identity_trace_value', abs(float(kr['s']['APF_trace_identity_MeV'])-Ts)<1e-12)
check('d_residual_math', abs(float(kr['d']['relative_residual_percent'])-drel)<1e-12)
check('s_residual_math', abs(float(kr['s']['relative_residual_percent'])-srel)<1e-12)
check('identity_knockout_nontrivial_d', abs(drel)>10)
check('identity_knockout_nontrivial_s', abs(srel)>5)
check('identity_transport_fails_labels', all(('fails' in kr[q]['diagnostic_status'] or 'blocked' in kr[q]['diagnostic_status']) for q in ['u','d','s']))
# Schema and gates
schema=read_csv('light_quark_chiral_lattice_transport_schema_v52.csv')
items={r['ledger_item']:r for r in schema}
for item in ['codomain','source_vector','chiral_lattice_map','lattice_scale_setting','chiral_fit','EM_isospin','renormalization_matching','covariance','no_target_inversion']:
    check('schema_has_'+item, item in items)
check('schema_codomain_closed', items['codomain']['v52_status']=='closed_v52')
check('schema_source_partial', items['source_vector']['v52_status']=='partial')
check('schema_map_typed', items['chiral_lattice_map']['v52_status']=='typed_v52')
check('schema_external_requirements', sum(1 for r in schema if r['v52_status']=='external_required')>=5)
check('schema_no_target_closed', items['no_target_inversion']['v52_status']=='closed_v52')
gates=read_csv('light_quark_export_gates_v52.csv')
g={r['gate']:r for r in gates}
for gate in ['G1_CODOMAIN_DECLARED','G2_TRANSPORT_MAP','G3_CONSTANTS_LEDGER','G4_COVARIANCE_PROTOCOL','G5_NO_SMUGGLING_AUDIT','G6_RESIDUAL_CHANNELS']:
    check('gate_has_'+gate, gate in g)
check('gate_G1_pass', g['G1_CODOMAIN_DECLARED']['v52_status']=='pass')
check('gate_G2_schema_not_evaluator', 'schema' in g['G2_TRANSPORT_MAP']['v52_status'])
check('gate_G5_pass', g['G5_NO_SMUGGLING_AUDIT']['v52_status']=='pass')
check('gate_no_export_due_boundaries', 'required' in g['G2_TRANSPORT_MAP']['remaining_boundary'])
# Forbidden inputs
forb=read_csv('light_quark_forbidden_inputs_v52.csv')
check('forbidden_count_8', len(forb)>=8)
check('forbidden_all_blocked', all(r['v52_audit']=='blocked' for r in forb))
for needle in ['PDG m_u','least-squares','lattice scale','chiral ansatz','heavy-quark']:
    check('forbidden_mentions_'+needle.replace(' ','_'), any(needle in r['forbidden_input'] for r in forb))
# Residual channels
channels=read_csv('light_quark_residual_channels_v52.csv')
ch={r['channel']:r for r in channels}
for key in ['source_T_u','source_T_d_T_s','identity_transport','chiral_lattice_transport','EM_isospin_corrections','MSbar_2GeV_matching','covariance','physical_export']:
    check('channel_has_'+key, key in ch)
check('channel_Tu_open', ch['source_T_u']['status']=='open')
check('channel_identity_knockout', ch['identity_transport']['status']=='knockout')
check('channel_export_not_claimed', ch['physical_export']['status']=='not_claimed')
# Case table update
case=read_csv('trace_to_scheme_case_table_v52.csv')
light=[r for r in case if r['sector']=='light quarks'][0]
check('case_light_status_v52', light['physical_export_status']=='P_light_quark_transport_gate_typed_not_exported_v52')
check('case_light_not_exported', 'not exported' in light['physical_export_status'] or 'not_exported' in light['physical_export_status'])
check('case_light_boundary_Tu', 'T_u' in light['first_failed_gate_or_boundary'])
# Inherited heavy and QED statuses untouched
for sector in ['EW/W','bottom','charged leptons','top','charm']:
    check('case_preserves_'+sector.replace('/','_').replace(' ','_'), any(r['sector']==sector for r in case))
check('charm_still_export_candidate', any(r['sector']=='charm' and 'P_export_candidate' in r['physical_export_status'] for r in case))
check('top_still_MSR', any(r['sector']=='top' and 'MSR' in r['codomain'] for r in case))
# Data json
data=json.loads((ROOT/'reports/light_quark_chiral_lattice_transport_gate_v52_data.json').read_text(encoding='utf-8'))
check('json_stamp', data['stamp']=='LIGHT_QUARK_CHIRAL_LATTICE_TRANSPORT_GATE_PASS')
check('json_no_export_claim', 'P_export_candidate_uds' in data['not_claimed'])
check('json_next_theorem_named', data['next_theorem']=='APF_LIGHT_QUARK_UP_TRACE_SOURCE_AND_CHIRAL_LATTICE_EVALUATOR_LEDGER')
# Verify no target-smuggling phrase omitted
for term in ['blocked','not used','not_claimed','T_u']:
    check('audit_text_'+term, term in (ROOT/'reports/light_quark_chiral_lattice_transport_gate_summary_v52.md').read_text(encoding='utf-8') or term in tex)
# Update JSON check total
passed=sum(1 for _,ok in checks if ok); total=len(checks)
data['checks_total']=total; data['checks_passed']=passed
(ROOT/'reports/light_quark_chiral_lattice_transport_gate_v52_data.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(f"\nTotal checks: {passed}/{total}")
if passed!=total:
    raise SystemExit(1)
print('LIGHT_QUARK_CHIRAL_LATTICE_TRANSPORT_GATE_PASS')
