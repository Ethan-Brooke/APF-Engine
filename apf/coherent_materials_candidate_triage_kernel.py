"""CMAL candidate triage kernel (architecture-only).

Ranks candidates by expected claim-admissibility gain per burden. It is not a
material predictor and not autonomous lab execution.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
try:
    from .coherent_materials_receipt_contract_validator import DEMO_RECEIPTS, validate_receipt
except Exception:
    from coherent_materials_receipt_contract_validator import DEMO_RECEIPTS, validate_receipt

VALUE = {'SC_MATERIAL_ADMISSIBILITY':5.0,'RARE_EARTH_QUANTUM_MEMORY':4.0,'TOPOLOGICAL_MATERIAL_STUB':0.0,'THERMOELECTRIC_STUB':0.0,'ION_CONDUCTOR_STUB':0.0}
ACTION = {'SC_RECEIPT_BUNDLE_VALIDATED':'RUN_RECEIPT_UPDATE_PROMOTION','RESISTIVE_ONLY_NO_MEISSNER':'MEASURE_MEISSNER_RESPONSE','CLAIM_QUARANTINED':'QUARANTINE_AND_REPRODUCE','RARE_EARTH_QM_RECEIPT_BUNDLE_VALIDATED':'OPTIMIZE_AFC_EFFICIENCY','RARE_EARTH_QM_RECEIPT_PARTIAL':'COMPLETE_QM_COHERENCE_RECEIPTS','ROUTE_TO_DIFFERENT_CODOMAIN':'REROUTE_TO_DECLARED_CODOMAIN','PRESSURE_CONDITIONED_SC_RECEIPT':'SEPARATE_PRESSURE_CONDITION_FROM_AMBIENT_USABILITY','AMBIENT_CLAIM_FROM_PRESSURE_CONDITIONED_RECEIPT':'QUARANTINE_AMBIENT_OVERCLAIM','UPDATE_PHASE_BOUNDARY_MAP':'UPDATE_PHASE_BOUNDARY_MAP','STUB_RECOGNIZED_NOT_EXPORTED':'DEFINE_RECEIPT_CARD_BEFORE_USE','MISSING_CONTRACT_FIELDS':'REPAIR_RECEIPT_CONTRACT','UNKNOWN_OR_UNEXPORTED_CODOMAIN':'REJECT_OR_DEFINE_CODOMAIN'}
PRIORITY = {'QUARANTINE_PRIORITY':0,'EVIDENCE_COMPLETION_PRIORITY':1,'PHASE_BOUNDARY_QUEUE':2,'ADMISSIBLE_CODOMAIN_QUEUE':3,'BURDEN_SEPARATION_QUEUE':4,'REROUTE_QUEUE':5,'CONTRACT_REPAIR_QUEUE':6,'LOW_PRIORITY_OR_STUB_QUEUE':7}

@dataclass(frozen=True)
class TriageResult:
    candidate_id: str; target_codomain: str; queue_bucket: str; next_action: str
    triage_score: float; expected_admissibility_gain: float; burden_cost: float
    validation_status: str; validation_route: str; promote_discovery_claim: bool
    preserved_nonclaims: tuple[str,...]; reasons: tuple[str,...]
    def to_dict(self) -> dict[str, Any]: return {k:getattr(self,k) for k in self.__dataclass_fields__}

def _burden(r: Mapping[str, Any], route: str) -> float:
    base = {'SC_RECEIPT_BUNDLE_VALIDATED':2.0,'RESISTIVE_ONLY_NO_MEISSNER':3.0,'CLAIM_QUARANTINED':7.5,'RARE_EARTH_QM_RECEIPT_BUNDLE_VALIDATED':2.5,'RARE_EARTH_QM_RECEIPT_PARTIAL':3.5,'ROUTE_TO_DIFFERENT_CODOMAIN':4.0,'PRESSURE_CONDITIONED_SC_RECEIPT':5.5,'AMBIENT_CLAIM_FROM_PRESSURE_CONDITIONED_RECEIPT':8.0,'UPDATE_PHASE_BOUNDARY_MAP':4.5,'STUB_RECOGNIZED_NOT_EXPORTED':6.0}.get(route,5.0)
    if r.get('replication_status') in {'NONE','UNREPLICATED'}: base += 1.0
    cv = r.get('control_vector') if isinstance(r.get('control_vector'), Mapping) else {}
    try: p=float(cv.get('pressure_GPa',0) or 0)
    except Exception: p=0.0
    if p>50: base += 1.5
    return base

def triage_candidate(r: Mapping[str, Any]) -> TriageResult:
    v = validate_receipt(r)
    target = str(r.get('target_codomain',''))
    val = VALUE.get(target, 1.0)
    if v.status == 'QUARANTINED': gain = 1.0; bucket='QUARANTINE_PRIORITY'
    elif v.route == 'RESISTIVE_ONLY_NO_MEISSNER': gain=3.5; bucket='EVIDENCE_COMPLETION_PRIORITY'
    elif v.route == 'UPDATE_PHASE_BOUNDARY_MAP': gain=3.0; bucket='PHASE_BOUNDARY_QUEUE'
    elif v.route == 'PRESSURE_CONDITIONED_SC_RECEIPT': gain=3.2; bucket='BURDEN_SEPARATION_QUEUE'
    elif v.reroute_target: gain=2.0; bucket='REROUTE_QUEUE'
    elif v.promotable: gain=val; bucket='ADMISSIBLE_CODOMAIN_QUEUE'
    elif v.status == 'REPAIRABLE': gain=1.2; bucket='CONTRACT_REPAIR_QUEUE'
    else: gain=max(0.3, val-1.5); bucket='LOW_PRIORITY_OR_STUB_QUEUE'
    burden = _burden(r, v.route)
    overclaim = 3.0 if v.status == 'QUARANTINED' else 0.0
    score = round(gain + val - burden - overclaim, 3)
    preserved = tuple(dict.fromkeys(tuple(r.get('nonclaim_guard') or ()) + ('not_Tc_prediction','not_new_material_prediction','not_autonomous_lab_execution')))
    return TriageResult(str(r.get('material_id') or r.get('receipt_id')), target, bucket, ACTION.get(v.route,'REQUEST_REVIEW'), score, round(gain,3), round(burden,3), v.status, v.route, False, preserved, v.reasons)

def triage_queue(receipts: Sequence[Mapping[str, Any]]) -> list[TriageResult]:
    return sorted([triage_candidate(x) for x in receipts], key=lambda x:(PRIORITY.get(x.queue_bucket,99), -x.expected_admissibility_gain, -x.triage_score))

def demo_triage_queue() -> list[TriageResult]: return triage_queue(list(DEMO_RECEIPTS.values()))
