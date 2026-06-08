"""APF Interaction Pattern Schema (architecture-only).

Bank-discoverable schema for the Pattern object of the Interface Engine family's
Pattern Adjudication reading (Reference - Interfaces as Discrete Pattern Selection
on the (61 x 102) Interaction Sea, v0.3). Installed architecture-only per the
Integrator Response v1.1 Q4 decision: no register(), no check_*, no BANK_REGISTRY
entry, no EXPECTED delta. Makes the Pattern object cross-tool consumable without
committing to a "Pattern Engine" the IE Charter prohibits.

A Pattern is a six-field tau-tuple over the (61 x 102) interaction sea:
  chi_tau    -- admissibility mask (which interaction slots are live)
  omega_tau  -- weights / costs on the live slots
  P_tau      -- candidate patterns under consideration
  D_tau      -- defects / competitors (what pressures the pattern)
  K_tau      -- codomain under test (the resolution being adjudicated)
  O_tau      -- obligations (the obligation-packet payload the pattern owes)

The shape matches the IE engine pipeline output contract: every engine reads a
configured slice + emits a verdict + an obligation packet. Structural typing only;
no numeric or material export.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Mapping, Optional

SCHEMA_NAME = "interaction_pattern_schema"
SCHEMA_VERSION = "v1"
SEA_SHAPE = (61, 102)
PATTERN_FIELDS = ("chi_tau", "omega_tau", "P_tau", "D_tau", "K_tau", "O_tau")
NON_CLAIMS = {"numeric_export": 0, "material_prediction": 0, "pattern_engine": 0}


@dataclass(frozen=True)
class InteractionPattern:
    """A six-field Pattern (tau-tuple) over the (61 x 102) interaction sea.

    Architecture-only schema object: structural typing, no claim-grade content.
    """
    pattern_id: str
    chi_tau: Mapping[str, bool]
    omega_tau: Mapping[str, float]
    P_tau: List[str]
    D_tau: List[str]
    K_tau: Optional[str]
    O_tau: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def validate_pattern(p: "InteractionPattern") -> Dict[str, Any]:
    """Structural validation of a Pattern. Returns a typed report; never raises
    on content. Architecture-only: checks shape/typing, never physics or numbers."""
    issues: List[str] = []
    if not p.pattern_id:
        issues.append("pattern_id empty")
    if not isinstance(p.chi_tau, Mapping):
        issues.append("chi_tau must be a mapping")
    if not isinstance(p.omega_tau, Mapping):
        issues.append("omega_tau must be a mapping")
    if not isinstance(p.P_tau, list):
        issues.append("P_tau must be a list")
    if not isinstance(p.D_tau, list):
        issues.append("D_tau must be a list")
    return {"schema": SCHEMA_NAME, "version": SCHEMA_VERSION,
            "pattern_id": p.pattern_id, "well_formed": not issues, "issues": issues}


def inspect_schema() -> Dict[str, Any]:
    """Static schema metadata for manifest / tool discovery."""
    return {
        "schema": SCHEMA_NAME,
        "version": SCHEMA_VERSION,
        "sea_shape": SEA_SHAPE,
        "fields": list(PATTERN_FIELDS),
        "architecture_only": True,
        "pattern_engine_committed": False,
        "reference": "Reference - Interfaces as Discrete Pattern Selection on the (61 x 102) Interaction Sea (v0.3)",
        "non_claims": dict(NON_CLAIMS),
    }
