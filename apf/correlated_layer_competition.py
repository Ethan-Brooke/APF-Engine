"""APF correlated-layer codomain competition scaffold.

Toy structural selector for material-indexed superconductivity competition.
No material-specific phase diagram, no numeric Tc, no ab initio chemistry.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, Iterable, List, Optional

REQUIRED_CODOMAINS = (
    "R_N",
    "R_SC",
    "R_AFM",
    "R_CDW",
    "R_stripe",
    "R_pseudogap",
    "R_vortex",
)

@dataclass(frozen=True)
class CodomainCandidate:
    codomain_id: str
    enforcement_cost_C: float
    defect_pressure_Pi: float
    admissible: bool = True
    evidence_gate: bool = True

    def score(self) -> float:
        vals = [self.enforcement_cost_C, self.defect_pressure_Pi]
        if any(not isfinite(v) or v < 0 for v in vals):
            raise ValueError("cost and pressure must be finite nonnegative values")
        if not self.admissible or not self.evidence_gate:
            return float("inf")
        return self.enforcement_cost_C + self.defect_pressure_Pi

@dataclass(frozen=True)
class CompetitionInstance:
    material_id: str
    control_label: str
    candidates: Dict[str, CodomainCandidate]
    history_codomain: Optional[str] = None
    barriers: Dict[str, float] = field(default_factory=dict)

    def missing_codomain_ids(self) -> List[str]:
        return [c for c in REQUIRED_CODOMAINS if c not in self.candidates]

    def validate(self) -> None:
        missing = self.missing_codomain_ids()
        if missing:
            raise ValueError(f"missing codomains: {missing}")
        for key, candidate in self.candidates.items():
            if key != candidate.codomain_id:
                raise ValueError(f"candidate key/id mismatch: {key} != {candidate.codomain_id}")
            candidate.score()

@dataclass(frozen=True)
class CompetitionResult:
    selected_codomain: str
    instantaneous_winner: str
    score_table: Dict[str, float]
    transition_fired: bool
    classification: str
    exports: Dict[str, int]


def select_correlated_layer_codomain(instance: CompetitionInstance) -> CompetitionResult:
    instance.validate()
    scores = {cid: cand.score() for cid, cand in instance.candidates.items()}
    winner = min(scores, key=lambda k: scores[k])
    selected = winner
    transition_fired = True

    if instance.history_codomain and instance.history_codomain in scores and winner != instance.history_codomain:
        old = instance.history_codomain
        barrier = instance.barriers.get(f"{old}->{winner}", 0.0)
        improvement = scores[old] - scores[winner]
        if improvement <= barrier:
            selected = old
            transition_fired = False

    if selected == "R_SC":
        classification = "SC_CODOMAIN_SELECTED_STRUCTURAL_TOY"
    elif selected == "R_vortex":
        classification = "VORTEX_OR_MIXED_CODOMAIN_SELECTED_STRUCTURAL_TOY"
    else:
        classification = "COMPETING_CODOMAIN_SELECTED_STRUCTURAL_TOY"

    return CompetitionResult(
        selected_codomain=selected,
        instantaneous_winner=winner,
        score_table=scores,
        transition_fired=transition_fired,
        classification=classification,
        exports={
            "SC_correlated_layer_competition": 1,
            "SC_codomain_selected_structural_toy": int(selected == "R_SC"),
            "SC_material_prediction": 0,
            "SC_numeric_Tc": 0,
            "SC_material_specific_phase_diagram": 0,
        },
    )


def load_competition_dict(data: dict) -> CompetitionInstance:
    candidates = {k: CodomainCandidate(codomain_id=k, **v) for k, v in data["candidates"].items()}
    return CompetitionInstance(
        material_id=data["material_id"],
        control_label=data.get("control_label", "undeclared_control"),
        candidates=candidates,
        history_codomain=data.get("history_codomain"),
        barriers=dict(data.get("barriers", {})),
    )
