"""CMAL receipt contract validator (architecture-only).

Validates APFMaterialReceipt objects before the CMAL receipt-update loop. It is
not a live connector, not a public ingestion core, and not an APF engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

REQ = {"schema_version","receipt_id","material_id","sample_id","target_codomain","receipt_kind","measurement_method","control_vector","measured_value","uncertainty","instrument_or_protocol","provenance","replication_status","updates_required_slots","nonclaim_guard"}
CRIT = {"receipt_id","material_id","sample_id","target_codomain","receipt_kind","provenance"}
SC_PROMOTE = {"zero_resistance","meissner_or_diamagnetic_response","field_suppression","replication"}
QM_PROMOTE = {"homogeneous_linewidth","inhomogeneous_linewidth","spin_lifetime"}
QM_SLOTS = QM_PROMOTE | {"spectral_hole_burning","afc_efficiency","afc_bandwidth","afc_storage_time","synthesis_provenance","stability"}
PHASE_SLOTS = {"strain_sweep","pressure_sweep","oxygenation_sweep","history_sweep","normal_transport"}
STUBS = {"TOPOLOGICAL_MATERIAL_STUB","THERMOELECTRIC_STUB","ION_CONDUCTOR_STUB"}

def _slots(r: Mapping[str, Any]) -> set[str]:
    v = r.get('updates_required_slots') or []
    if isinstance(v, str): return {v}
    return {str(x) for x in v}

def _txt(*v: Any) -> str: return ' '.join(str(x).lower() for x in v)

def _pressure(cv: Any) -> float:
    if not isinstance(cv, Mapping): return 0.0
    raw = cv.get('pressure_GPa', 0)
    try: return float(raw or 0)
    except Exception: return 0.0

@dataclass(frozen=True)
class ReceiptValidation:
    status: str
    route: str
    promotable: bool
    target_codomain: str | None
    accepted_slots: tuple[str, ...]
    missing_slots: tuple[str, ...]
    repairs: tuple[str, ...]
    reasons: tuple[str, ...]
    reroute_target: str | None = None
    nonclaim_guard_preserved: bool = True
    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}

DEMO_RECEIPTS: dict[str, dict[str, Any]] = {
  'bulk_sc_full': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-BULK-SC','material_id':'generic_bulk_sc_control','sample_id':'s1','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'bulk_sc_bundle','measurement_method':'transport+magnetometry','control_vector':{'pressure_GPa':0,'temperature_K':'sweep'},'measured_value':{'zero_resistance':True,'meissner_or_diamagnetic_response':True,'field_suppression':True},'uncertainty':{'declared':True},'instrument_or_protocol':'four_probe+magnetometry','provenance':{'chain':'declared'},'replication_status':'REPLICATED','updates_required_slots':['zero_resistance','meissner_or_diamagnetic_response','field_suppression','replication'],'nonclaim_guard':['not_new_material_prediction','not_numeric_Tc']},
  'resistive_only': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-RESISTIVE','material_id':'partial_sc_claim','sample_id':'s2','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'resistive_transition_only','measurement_method':'transport','control_vector':{'temperature_K':'sweep'},'measured_value':{'zero_resistance':True},'uncertainty':{'declared':True},'instrument_or_protocol':'four_probe','provenance':{'chain':'partial'},'replication_status':'UNREPLICATED','updates_required_slots':['zero_resistance'],'nonclaim_guard':['resistive_only_not_SC']},
  'formula_only_rtsc': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-FORMULA','material_id':'formula_only_claim','sample_id':'none','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'formula_only_claim','measurement_method':'none','control_vector':{},'measured_value':{'claimed_room_temperature_SC':True},'uncertainty':{},'instrument_or_protocol':'none','provenance':{'chain':'missing'},'replication_status':'NONE','updates_required_slots':[],'nonclaim_guard':[]},
  'pearson_qm': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-PEARSON-QM','material_id':'Pearson_NaEu_IO3_4','sample_id':'NaEu(IO3)4_crystal','target_codomain':'RARE_EARTH_QUANTUM_MEMORY','receipt_kind':'rare_earth_qm_bundle','measurement_method':'cryogenic_spectroscopy_AFC','control_vector':{'temperature_K':1.7},'measured_value':{'homogeneous_linewidth_kHz':120,'inhomogeneous_linewidth_GHz':2.2,'spin_lifetime_s_lower_bound':1.0,'AFC_preliminary':True},'uncertainty':{'declared':True},'instrument_or_protocol':'Pearson thesis Chapter 7','provenance':{'source':'Pearson 2025 UIUC dissertation'},'replication_status':'THESIS_REPORTED','updates_required_slots':['homogeneous_linewidth','inhomogeneous_linewidth','spin_lifetime','afc_efficiency','synthesis_provenance'],'nonclaim_guard':['not_superconductivity','not_Tc']},
  'pearson_misrouted_sc': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-PEARSON-MISROUTE','material_id':'Pearson_NaEu_IO3_4','sample_id':'NaEu(IO3)4_crystal','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'rare_earth_qm_bundle','measurement_method':'cryogenic_spectroscopy','control_vector':{'temperature_K':1.7},'measured_value':{'homogeneous_linewidth_kHz':120},'uncertainty':{'declared':True},'instrument_or_protocol':'Pearson thesis Chapter 7','provenance':{'source':'Pearson 2025 UIUC dissertation'},'replication_status':'THESIS_REPORTED','updates_required_slots':['homogeneous_linewidth'],'nonclaim_guard':['not_superconductivity']},
  'hydride_pressure': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-HYDRIDE','material_id':'generic_hydride_pressure','sample_id':'s3','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'pressure_conditioned_sc_receipt','measurement_method':'diamond_anvil_transport','control_vector':{'pressure_GPa':150,'temperature_K':'sweep'},'measured_value':{'zero_resistance':True,'pressure_calibrated':True,'ambient_usability_claimed':False},'uncertainty':{'declared':True},'instrument_or_protocol':'high_pressure_transport','provenance':{'chain':'declared'},'replication_status':'TEMPLATE','updates_required_slots':['pressure_calibration','zero_resistance'],'nonclaim_guard':['pressure_conditioned_only','ambient_usability_not_promoted']},
  'hydride_ambient_smuggle': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-HYDRIDE-SMUGGLE','material_id':'generic_hydride_pressure','sample_id':'s3','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'pressure_conditioned_sc_receipt','measurement_method':'diamond_anvil_transport','control_vector':{'pressure_GPa':150},'measured_value':{'zero_resistance':True,'ambient_usability_claimed':True},'uncertainty':{'declared':True},'instrument_or_protocol':'high_pressure_transport','provenance':{'chain':'declared'},'replication_status':'TEMPLATE','updates_required_slots':['pressure_calibration','zero_resistance'],'nonclaim_guard':[]},
  'nickelate_sweep': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-NICKELATE','material_id':'generic_nickelate_template','sample_id':'s4','target_codomain':'SC_MATERIAL_ADMISSIBILITY','receipt_kind':'phase_boundary_sweep_receipt','measurement_method':'strain_pressure_oxygenation_sweep','control_vector':{'strain':'sweep','pressure_GPa':'sweep','oxygenation':'declared'},'measured_value':{'phase_boundary':'updated'},'uncertainty':{'declared':True},'instrument_or_protocol':'correlated_layer_phase_boundary_protocol','provenance':{'chain':'declared'},'replication_status':'TEMPLATE','updates_required_slots':['strain_sweep','oxygenation_sweep','normal_transport'],'nonclaim_guard':['not_formula_level_prediction','not_numeric_Tc']},
  'topological_stub': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-TOPO-STUB','material_id':'future_topological_candidate','sample_id':'stub','target_codomain':'TOPOLOGICAL_MATERIAL_STUB','receipt_kind':'band_invariant','measurement_method':'future','control_vector':{},'measured_value':{},'uncertainty':{'declared':False},'instrument_or_protocol':'future','provenance':{'source':'stub'},'replication_status':'NONE','updates_required_slots':['band_invariant'],'nonclaim_guard':['stub_only']},
  'thermoelectric_stub': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-THERMO-STUB','material_id':'future_thermo_candidate','sample_id':'stub','target_codomain':'THERMOELECTRIC_STUB','receipt_kind':'ZT','measurement_method':'future','control_vector':{},'measured_value':{},'uncertainty':{'declared':False},'instrument_or_protocol':'future','provenance':{'source':'stub'},'replication_status':'NONE','updates_required_slots':['ZT'],'nonclaim_guard':['stub_only']},
  'ion_conductor_stub': {'schema_version':'APFMaterialReceipt.v1','receipt_id':'R-ION-STUB','material_id':'future_ion_conductor','sample_id':'stub','target_codomain':'ION_CONDUCTOR_STUB','receipt_kind':'ionic_conductivity','measurement_method':'future','control_vector':{},'measured_value':{},'uncertainty':{'declared':False},'instrument_or_protocol':'future','provenance':{'source':'stub'},'replication_status':'NONE','updates_required_slots':['ionic_conductivity'],'nonclaim_guard':['stub_only']},
}

def validate_receipt(r: Mapping[str, Any]) -> ReceiptValidation:
    missing = sorted(REQ - set(r))
    rid = str(r.get('receipt_id','<missing>'))
    target = str(r.get('target_codomain',''))
    kind = str(r.get('receipt_kind',''))
    slots = _slots(r)
    measured = r.get('measured_value') if isinstance(r.get('measured_value'), Mapping) else {}
    nonclaims = tuple(r.get('nonclaim_guard') or ())
    if missing:
        crit = sorted(CRIT - set(r))
        return ReceiptValidation('REJECTED' if crit else 'REPAIRABLE','MISSING_CONTRACT_FIELDS',False,None,tuple(),tuple(missing),tuple('supply:'+x for x in missing),('missing_required_fields',),None,False)
    if kind in {'formula_only_claim','composition_only_claim','room_temperature_formula_only_sc'} or not r.get('sample_id') or r.get('formula_only'):
        return ReceiptValidation('QUARANTINED','CLAIM_QUARANTINED',False,None,tuple(),tuple(),('supply sample-specific receipts','open quarantine replication packet'),('formula_only_or_sample_absent',),None,True)
    if r.get('target_value_smuggling') or kind == 'target_value_smuggling':
        return ReceiptValidation('QUARANTINED','TARGET_VALUE_SMUGGLING',False,None,tuple(),tuple(),('remove fitted target value',),('target_value_smuggling',),None,False)
    if target in STUBS:
        return ReceiptValidation('VALID','STUB_RECOGNIZED_NOT_EXPORTED',False,target,tuple(sorted(slots)),tuple(),('define active receipt card before use',),('stub_codomain_not_exported',),None,True)
    if 'pearson' in _txt(r.get('material_id'), r.get('formula'), r.get('sample_id')) and target == 'SC_MATERIAL_ADMISSIBILITY':
        return ReceiptValidation('REJECTED','ROUTE_TO_DIFFERENT_CODOMAIN',False,'RARE_EARTH_QUANTUM_MEMORY',tuple(sorted(slots & QM_SLOTS)),tuple(),('reroute Pearson/NaEu receipt to RARE_EARTH_QUANTUM_MEMORY',),('Pearson_NaEu_is_QM_not_SC',),'RARE_EARTH_QUANTUM_MEMORY',True)
    if target == 'RARE_EARTH_QUANTUM_MEMORY':
        missing_qm = tuple(sorted(QM_PROMOTE - slots))
        route = 'RARE_EARTH_QM_RECEIPT_BUNDLE_VALIDATED' if not missing_qm else 'RARE_EARTH_QM_RECEIPT_PARTIAL'
        return ReceiptValidation('VALID',route,not missing_qm,target,tuple(sorted(slots & QM_SLOTS)),missing_qm,tuple(),('non_SC_coherent_material_receipt',),None,True)
    if target == 'SC_MATERIAL_ADMISSIBILITY':
        p = _pressure(r.get('control_vector'))
        if p > 1 and measured.get('ambient_usability_claimed') is True:
            return ReceiptValidation('QUARANTINED','AMBIENT_CLAIM_FROM_PRESSURE_CONDITIONED_RECEIPT',False,None,tuple(sorted(slots)),tuple(),('separate pressure-conditioned SC from ambient usability',),('ambient_claim_from_high_pressure_receipt',),None,True)
        if kind == 'pressure_conditioned_sc_receipt':
            return ReceiptValidation('VALID','PRESSURE_CONDITIONED_SC_RECEIPT',{'zero_resistance','pressure_calibration'}.issubset(slots),target,tuple(sorted(slots)),tuple(),tuple(),('pressure_conditioned_SC_only',),None,True)
        if kind == 'phase_boundary_sweep_receipt':
            return ReceiptValidation('VALID','UPDATE_PHASE_BOUNDARY_MAP',False,target,tuple(sorted(slots & PHASE_SLOTS)),tuple(),tuple(),('phase_boundary_update_not_formula_level_prediction',),None,True)
        if kind == 'resistive_transition_only' or ('zero_resistance' in slots and 'meissner_or_diamagnetic_response' not in slots):
            return ReceiptValidation('VALID','RESISTIVE_ONLY_NO_MEISSNER',False,target,tuple(sorted(slots)),tuple(sorted(SC_PROMOTE - slots)),('add Meissner/field/replication receipts',),('resistive_only_evidence_is_partial',),None,True)
        miss = tuple(sorted(SC_PROMOTE - slots))
        return ReceiptValidation('VALID','SC_RECEIPT_BUNDLE_VALIDATED',not miss,target,tuple(sorted(slots)),miss,tuple(),('SC_receipt_bundle_checked',),None,True)
    return ReceiptValidation('REJECTED','UNKNOWN_OR_UNEXPORTED_CODOMAIN',False,None,tuple(sorted(slots)),tuple(),('define codomain receipt card',),('unknown_codomain',),None,False)

def validate_receipt_bundle(receipts: Sequence[Mapping[str, Any]]) -> list[ReceiptValidation]:
    return [validate_receipt(x) for x in receipts]
