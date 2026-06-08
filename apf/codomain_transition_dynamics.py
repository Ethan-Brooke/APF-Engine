"""
APF Interface Engine codomain transition dynamics.

Structural-only phase landscape evaluator.
"""

from __future__ import annotations
from dataclasses import dataclass, field, replace
from math import isfinite
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class CodomainCandidate:
    name: str
    enforcement_cost: float
    defect_penalty: float = 0.0
    admissible: bool = True
    susceptibility: float = 0.0
    role: str = ""

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name required")
        for v in [self.enforcement_cost, self.defect_penalty, self.susceptibility]:
            if not isfinite(v):
                raise ValueError("finite numeric values required")
        if self.enforcement_cost < 0 or self.defect_penalty < 0:
            raise ValueError("cost and penalty nonnegative required")

    def score(self, perturbation_lambda: float = 0.0) -> float:
        self.validate()
        if not self.admissible:
            return float("inf")
        return self.enforcement_cost + self.defect_penalty + self.susceptibility * perturbation_lambda


@dataclass(frozen=True)
class CodomainTransition:
    source: str
    target: str
    barrier: float = 0.0
    allowed: bool = True

    def validate(self) -> None:
        if not self.source or not self.target:
            raise ValueError("source and target required")
        if self.barrier < 0 or not isfinite(self.barrier):
            raise ValueError("barrier finite nonnegative required")


@dataclass(frozen=True)
class CodomainLandscape:
    candidates: Dict[str, CodomainCandidate]
    transitions: List[CodomainTransition] = field(default_factory=list)

    def validate(self) -> None:
        if not self.candidates:
            raise ValueError("candidates required")
        for c in self.candidates.values():
            c.validate()
        for t in self.transitions:
            t.validate()
            if t.source not in self.candidates or t.target not in self.candidates:
                raise ValueError("transition references missing candidate")

    def scores(self, perturbation_lambda: float = 0.0) -> Dict[str, float]:
        self.validate()
        return {k: c.score(perturbation_lambda) for k, c in self.candidates.items()}

    def select(self, perturbation_lambda: float = 0.0) -> "LandscapeSelection":
        scores = self.scores(perturbation_lambda)
        selected = min(scores, key=scores.get)
        ordered = sorted(scores.items(), key=lambda kv: kv[1])
        runner = ordered[1] if len(ordered) > 1 else (None, float("inf"))
        return LandscapeSelection(
            perturbation_lambda=perturbation_lambda,
            selected=selected,
            selected_score=scores[selected],
            runner_up=runner[0],
            runner_up_score=runner[1],
            margin_to_runner_up=runner[1] - scores[selected],
            scores=scores,
        )

    def transition_barrier(self, source: str, target: str) -> float:
        for t in self.transitions:
            if t.source == source and t.target == target and t.allowed:
                return t.barrier
        return float("inf")

    def sweep(self, values: List[float]) -> List["LandscapeSelection"]:
        return [self.select(v) for v in values]

    def phase_boundaries(self, values: List[float]) -> List[Tuple[float, str, str]]:
        selections = self.sweep(values)
        boundaries = []
        for prev, cur in zip(selections, selections[1:]):
            if prev.selected != cur.selected:
                boundaries.append((cur.perturbation_lambda, prev.selected, cur.selected))
        return boundaries


@dataclass(frozen=True)
class LandscapeSelection:
    perturbation_lambda: float
    selected: str
    selected_score: float
    runner_up: str | None
    runner_up_score: float
    margin_to_runner_up: float
    scores: Dict[str, float]

    def pairwise_delta(self, a: str, b: str) -> float:
        return self.scores[a] - self.scores[b]


def load_landscape(data: dict) -> CodomainLandscape:
    candidates = {c["name"]: CodomainCandidate(**c) for c in data["candidates"]}
    transitions = [CodomainTransition(**t) for t in data.get("transitions", [])]
    return CodomainLandscape(candidates=candidates, transitions=transitions)
