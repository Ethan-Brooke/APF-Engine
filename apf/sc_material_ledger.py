"""APF superconductivity material ledger schema.

Structural-only validator. It verifies that a material candidate has the declared
ledger slots required before the superconducting coherent-phase selector may be
applied. It does not predict Tc, derive chemistry, or identify real materials.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, Iterable, List, Optional

REQUIRED_SLOTS = (
    "C_composition",
    "G_structure",
    "B_carrier_sector",
    "D_defects_disorder",
    "E_external_controls",
    "K_kernel_class",
    "P_competing_phases",
    "Sigma_uncertainty_provenance",
)

FORBIDDEN_INPUTS = (
    "known_superconductor_label_as_input",
    "target_Tc_as_fit_parameter",
    "post_hoc_threshold_tuning",
    "resistivity_drop_only_as_full_SC_evidence",
    "sample_identity_without_provenance",
)

@dataclass(frozen=True)
class LedgerSlot:
    name: str
    declared: bool
    value_summary: str = ""
    provenance: str = ""
    uncertainty_declared: bool = False

    def valid(self) -> bool:
        if not self.name:
            return False
        if not self.declared:
            return False
        if not self.value_summary.strip():
            return False
        if not self.provenance.strip():
            return False
        return True

@dataclass(frozen=True)
class DefectPressureLedger:
    Pi_th: float = 0.0
    Pi_dis: float = 0.0
    Pi_comp: float = 0.0
    Pi_dim: float = 0.0
    Pi_synth: float = 0.0

    def total(self) -> float:
        vals = [self.Pi_th, self.Pi_dis, self.Pi_comp, self.Pi_dim, self.Pi_synth]
        if any((not isfinite(v) or v < 0) for v in vals):
            raise ValueError("defect pressures must be finite nonnegative values")
        return sum(vals)

@dataclass(frozen=True)
class SCMaterialLedger:
    material_id: str
    slots: Dict[str, LedgerSlot]
    defect_pressures: DefectPressureLedger = field(default_factory=DefectPressureLedger)
    forbidden_inputs_present: List[str] = field(default_factory=list)

    def missing_required_slots(self) -> List[str]:
        missing = []
        for name in REQUIRED_SLOTS:
            slot = self.slots.get(name)
            if slot is None or not slot.valid():
                missing.append(name)
        return missing

    def provenance_complete(self) -> bool:
        return all(self.slots[name].provenance.strip() for name in REQUIRED_SLOTS if name in self.slots)

    def sigma_attached(self) -> bool:
        slot = self.slots.get("Sigma_uncertainty_provenance")
        return bool(slot and slot.valid() and slot.uncertainty_declared)

    def no_forbidden_inputs(self) -> bool:
        return not any(x in FORBIDDEN_INPUTS for x in self.forbidden_inputs_present)

    def ledger_complete(self) -> bool:
        return not self.missing_required_slots() and self.provenance_complete() and self.sigma_attached()

@dataclass(frozen=True)
class SCCostLedger:
    C_normal: float
    C_superconducting: float

    def validate(self) -> None:
        for name, value in (("C_normal", self.C_normal), ("C_superconducting", self.C_superconducting)):
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")

@dataclass(frozen=True)
class SCMaterialEvaluation:
    material_id: str
    ledger_complete: bool
    no_forbidden_inputs: bool
    admissibility_margin: Optional[float]
    classification: str
    missing_slots: List[str]
    exports: Dict[str, int]


def material_admissibility_margin(ledger: SCMaterialLedger, costs: SCCostLedger) -> float:
    costs.validate()
    return costs.C_normal - costs.C_superconducting - ledger.defect_pressures.total()


def evaluate_material_ledger(ledger: SCMaterialLedger, costs: SCCostLedger | None = None) -> SCMaterialEvaluation:
    missing = ledger.missing_required_slots()
    complete = ledger.ledger_complete()
    clean = ledger.no_forbidden_inputs()
    margin = material_admissibility_margin(ledger, costs) if (complete and clean and costs is not None) else None

    if not clean:
        cls = "CLAIM_QUARANTINED"
    elif not complete:
        cls = "MATERIAL_LEDGER_INSUFFICIENT"
    elif margin is None:
        cls = "MATERIAL_LEDGER_COMPLETE_NO_COST_EVALUATION"
    elif margin > 0:
        cls = "MATERIAL_LEDGER_ADMISSIBLE_FOR_SC_SELECTOR"
    else:
        cls = "MATERIAL_LEDGER_COMPLETE_MARGIN_NONPOSITIVE"

    return SCMaterialEvaluation(
        material_id=ledger.material_id,
        ledger_complete=complete,
        no_forbidden_inputs=clean,
        admissibility_margin=margin,
        classification=cls,
        missing_slots=missing,
        exports={
            "SC_material_ledger_schema": 1,
            "SC_material_ledger_complete": int(complete),
            "SC_material_selector_allowed": int(complete and clean),
            "SC_material_prediction": 0,
            "SC_numeric_Tc": 0,
            "SC_ab_initio_chemistry": 0,
        },
    )


def load_ledger_dict(data: dict) -> tuple[SCMaterialLedger, SCCostLedger | None]:
    slots = {name: LedgerSlot(name=name, **slot) for name, slot in data["slots"].items()}
    pressures = DefectPressureLedger(**data.get("defect_pressures", {}))
    ledger = SCMaterialLedger(
        material_id=data["material_id"],
        slots=slots,
        defect_pressures=pressures,
        forbidden_inputs_present=list(data.get("forbidden_inputs_present", [])),
    )
    costs = SCCostLedger(**data["costs"]) if "costs" in data else None
    return ledger, costs
