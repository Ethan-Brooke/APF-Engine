"""
APF Interface Engine codomain competition selector.

Structural-only machinery.

The selected codomain is the admissible codomain with minimum total enforcement
cost plus defect penalty:

    score(R_i) = C(R_i) + Pi_i

Lower score wins. Pairwise deltas classify margins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class CodomainCandidate:
    name: str
    enforcement_cost: float
    defect_penalty: float = 0.0
    admissible: bool = True
    role: str = ""

    def validate(self) -> None:
        if not self.name:
            raise ValueError("codomain name required")
        if self.enforcement_cost < 0 or self.defect_penalty < 0:
            raise ValueError("costs and penalties must be nonnegative")
        if not isfinite(self.enforcement_cost) or not isfinite(self.defect_penalty):
            raise ValueError("costs and penalties must be finite")

    def score(self) -> float:
        self.validate()
        if not self.admissible:
            return float("inf")
        return self.enforcement_cost + self.defect_penalty


@dataclass(frozen=True)
class CodomainTransition:
    source: str
    target: str
    transition_cost: float = 0.0
    allowed: bool = True

    def validate(self) -> None:
        if not self.source or not self.target:
            raise ValueError("source and target required")
        if self.transition_cost < 0 or not isfinite(self.transition_cost):
            raise ValueError("transition cost must be finite and nonnegative")


@dataclass(frozen=True)
class CodomainCompetitionGraph:
    candidates: Dict[str, CodomainCandidate]
    transitions: List[CodomainTransition] = field(default_factory=list)

    def validate(self) -> None:
        if not self.candidates:
            raise ValueError("at least one codomain candidate required")
        for c in self.candidates.values():
            c.validate()
        for t in self.transitions:
            t.validate()
            if t.source not in self.candidates or t.target not in self.candidates:
                raise ValueError("transition references missing codomain")

    def scores(self) -> Dict[str, float]:
        self.validate()
        return {name: candidate.score() for name, candidate in self.candidates.items()}

    def select(self) -> "CodomainSelection":
        scores = self.scores()
        selected_name = min(scores, key=scores.get)
        selected_score = scores[selected_name]
        ordered = sorted(scores.items(), key=lambda kv: kv[1])
        runner_up_name, runner_up_score = ordered[1] if len(ordered) > 1 else (None, float("inf"))
        pairwise_deltas = {
            f"{a}_minus_{b}": scores[a] - scores[b]
            for a in scores
            for b in scores
            if a != b
        }
        return CodomainSelection(
            selected=selected_name,
            selected_score=selected_score,
            runner_up=runner_up_name,
            runner_up_score=runner_up_score,
            margin_to_runner_up=runner_up_score - selected_score,
            scores=scores,
            pairwise_deltas=pairwise_deltas,
        )


@dataclass(frozen=True)
class CodomainSelection:
    selected: str
    selected_score: float
    runner_up: str | None
    runner_up_score: float
    margin_to_runner_up: float
    scores: Dict[str, float]
    pairwise_deltas: Dict[str, float]

    @property
    def is_degenerate(self) -> bool:
        return self.margin_to_runner_up <= 1e-9


def load_competition_graph(data: dict) -> CodomainCompetitionGraph:
    candidates = {
        item["name"]: CodomainCandidate(**item)
        for item in data["candidates"]
    }
    transitions = [CodomainTransition(**item) for item in data.get("transitions", [])]
    return CodomainCompetitionGraph(candidates=candidates, transitions=transitions)
