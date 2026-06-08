"""
APF IE codomain hysteresis and metastability scaffold.

A current codomain persists unless the gain from switching to the instantaneous
minimum exceeds the transition barrier from current -> target.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, List


@dataclass(frozen=True)
class CodomainCandidate:
    name: str
    enforcement_cost: float
    defect_penalty: float = 0.0
    susceptibility: float = 0.0
    admissible: bool = True

    def score(self, lam: float) -> float:
        for x in (self.enforcement_cost, self.defect_penalty, self.susceptibility):
            if not isfinite(x):
                raise ValueError("finite numeric values required")
        if not self.admissible:
            return float("inf")
        return self.enforcement_cost + self.defect_penalty + self.susceptibility * lam


@dataclass(frozen=True)
class CodomainTransition:
    source: str
    target: str
    barrier: float
    allowed: bool = True

    def validate(self) -> None:
        if self.barrier < 0 or not isfinite(self.barrier):
            raise ValueError("barrier must be finite nonnegative")


@dataclass(frozen=True)
class HysteresisStep:
    lam: float
    previous: str
    instantaneous_target: str
    selected: str
    gain: float
    barrier: float
    status: str
    scores: Dict[str, float]


@dataclass(frozen=True)
class HysteresisLandscape:
    candidates: Dict[str, CodomainCandidate]
    transitions: List[CodomainTransition] = field(default_factory=list)

    def scores(self, lam: float) -> Dict[str, float]:
        return {k: v.score(lam) for k, v in self.candidates.items()}

    def barrier(self, source: str, target: str) -> float:
        if source == target:
            return 0.0
        for t in self.transitions:
            t.validate()
            if t.source == source and t.target == target and t.allowed:
                return t.barrier
        return float("inf")

    def step(self, current: str, lam: float) -> HysteresisStep:
        scores = self.scores(lam)
        target = min(scores, key=scores.get)
        if current not in self.candidates:
            current = target
        gain = scores[current] - scores[target]
        barrier = self.barrier(current, target)
        fires = target != current and gain > barrier
        selected = target if fires else current
        status = "TRANSITION_FIRED" if fires else ("METASTABLE_HELD" if target != current else "AT_MINIMUM")
        return HysteresisStep(lam, current, target, selected, gain, barrier, status, scores)

    def path(self, initial: str, lambdas: List[float]) -> List[HysteresisStep]:
        current = initial
        out = []
        for lam in lambdas:
            st = self.step(current, lam)
            out.append(st)
            current = st.selected
        return out


def load_hysteresis_landscape(data: dict) -> HysteresisLandscape:
    candidates = {c["name"]: CodomainCandidate(**c) for c in data["candidates"]}
    transitions = [CodomainTransition(**t) for t in data.get("transitions", [])]
    return HysteresisLandscape(candidates=candidates, transitions=transitions)
