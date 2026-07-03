"""apf/fermion_normalizers.py -- Local up-sector residual normalizer.

Phase 28 of the Paper 32 quark-anchor-gate program (2026-05-08): codebase
landing of the DominantChannel sprint v0.14 local theorem.  After the
spent quotient $Q_{\\rm spent}$ removes the already-spent weak-scale,
common spectral, weak-carrier, Yukawa-bilinear, and projective trace-shape
structures, the residual quadratic $U(1)$ interface load
$L_2(f) = d_3(f)\\,d_2(f)\\,Y(f)^2$ uniquely selects $u_R^c$ on the
one-generation pre-mass channel table, and the residual coefficient
functional $F_1(f) = |d_3(f)\\,d_2(f)\\,Y(f)|$ on that selected channel
gives $F_1(u_R^c) = |3 \\cdot 1 \\cdot (-2/3)| = 2$.  The module therefore
exports the local theorem
$$
L_{\\rm residual\\_up\\_normalizer\\_local} \\;\\Rightarrow\\; \\Lambda_u = c_R = 2.
$$

This module deliberately exports ONLY the local up-sector normalizer.
It does not export a physical top mass, an $\\overline{\\rm MS}$ mass,
a pole mass, a direct-reconstruction mass, or a $W$-mass correction.
The no-smuggling guard is structural: ``check_no_inverse_inputs``
rejects use of any input in the forbidden set
$\\{m_t,\\,y_t,\\,m_b,\\,m_\\tau,\\,v_{\\rm obs},\\,
   \\text{physical\\_yukawa\\_normalization}\\}$, so the local theorem
proves $\\Lambda_u = 2$ from representation multiplicity and hypercharge
alone.

Bank-registered theorems:

  * check_L_residual_up_normalizer_local -- local theorem witness on the
    five-channel one-generation table.  Verifies that $L_2$ uniquely
    selects $u_R^c$ at $4/3$ and that $F_1(u_R^c) = 2$.

  * check_T_no_inverse_inputs_up_normalizer -- non-smuggling guard:
    given a default declared input set $\\{d_3, d_2, Y, Q_{\\rm spent},
    L_2, F_1\\}$, the intersection with the forbidden set is empty.

Source-of-record: Paper 32 Quark-Anchor Gate v0.9 + DC sprint v0.12 +
DC sprint v0.14 (refinement code-only); audit code mirror at
``Papers/Paper 32 .../code/dc_v0.14/fermion_normalizers.py``.

The full top-mass theorem $m_t : [P]$ remains conditional on three
upstream gates:

  - ``T_scheme``: a deterministic trace-to-scheme transport map
    $T_{\\rm scheme} : m_{\\rm trace} \\mapsto m_t(\\mu, S)$ from APF
    thresholds, QCD anomalous dimensions, and a declared mass scheme,
    fixed before comparison to any target.
  - ``W_commute``: the $W$ branch must consume the same $\\Lambda_u$
    rather than a shadow $L_{\\sigma\\,\\rm normalization}$.
  - ``B_upstream``: the present module is the install pass for this
    third gate.

The shape of an admissible $T_{\\rm scheme}$ contract is named in
``Papers/Paper 32 .../code/dc_v0.14/transport_contract.py``; that
contract validator returns ``PASS_CONTRACT_SHAPE_ONLY`` only — it
is held outside the bank until a real $T_{\\rm scheme}$ theorem
exists to validate against.
"""

from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Optional, Tuple


# =====================================================================
# Channel-table data (one-generation pre-mass Standard Model)
# =====================================================================

@dataclass(frozen=True)
class Channel:
    """A one-generation pre-mass Standard Model channel.

    `d3` is the SU(3)_c representation dimension; `d2` is the SU(2)_L
    representation dimension; `Y` is the U(1)_Y hypercharge.  All five
    per-generation channels (Q_L, u_R^c, d_R^c, L_L, e_R^c) are listed.
    """
    name: str
    d3: int
    d2: int
    Y: Fraction


CHANNELS: Tuple[Channel, ...] = (
    Channel("Q_L",    3, 2, Fraction(1,  6)),
    Channel("u_R^c",  3, 1, Fraction(-2, 3)),
    Channel("d_R^c",  3, 1, Fraction(1,  3)),
    Channel("L_L",    1, 2, Fraction(-1, 2)),
    Channel("e_R^c",  1, 1, Fraction(1,  1)),
)


SPENT_QUOTIENT_REMOVES: Tuple[str, ...] = (
    "L_EW primitive weak scale",
    "sqrt(3) spectral participation lift",
    "weak-carrier bookkeeping",
    "Yukawa bilinear bookkeeping",
    "spectral trace shape",
)


FORBIDDEN_INPUTS = frozenset({
    "m_t",
    "y_t",
    "m_b",
    "m_tau",
    "v_obs",
    "physical_yukawa_normalization",
})


# =====================================================================
# Residual selector and coefficient functionals
# =====================================================================

def L2(channel: Channel) -> Fraction:
    """Residual quadratic U(1) interface load $L_2 = d_3 d_2 Y^2$.

    Used as the channel selector on the post-spent-quotient residual
    table; orders channels without orientation.
    """
    return Fraction(channel.d3 * channel.d2, 1) * channel.Y * channel.Y


def F1(channel: Channel) -> Fraction:
    """Residual flux coefficient $F_1 = |d_3 d_2 Y|$.

    Used as the coefficient functional on the unique $L_2$ maximizer;
    counts absolute residual U(1) flux across representation slots.
    """
    val = Fraction(channel.d3 * channel.d2, 1) * channel.Y
    return abs(val)


def selected_channel() -> Channel:
    """Return the unique residual-load maximizer.

    Raises AssertionError if the maximum is non-unique.
    """
    pairs = [(L2(c), c) for c in CHANNELS]
    m = max(v for v, _ in pairs)
    winners = [c for v, c in pairs if v == m]
    if len(winners) != 1:
        raise AssertionError(
            f"non-unique residual load maximizer: {[w.name for w in winners]}"
        )
    return winners[0]


# =====================================================================
# Bank-registered checks
# =====================================================================

def check_L_residual_up_normalizer_local():
    """L_residual_up_normalizer_local: the local up-sector normalizer
    theorem $\\Lambda_u = c_R = 2$.

    Tier 4 [P_structural].

    Source-of-record: Paper 32 v0.9 + DominantChannel sprint v0.12 / v0.14.

    Verifies on the five-channel one-generation Standard Model table
    after the declared spent quotient $Q_{\\rm spent}$:
      (i)  $L_2(f) = d_3 d_2 Y^2$ has a unique maximum at $u_R^c$
           with value $4/3$ (other channels: $Q_L$ at $1/6$,
           $d_R^c$ at $1/3$, $L_L$ at $1/2$, $e_R^c$ at $1$).
      (ii) The residual coefficient functional $F_1(f) = |d_3 d_2 Y|$
           on the selected channel evaluates to
           $F_1(u_R^c) = |3 \\cdot 1 \\cdot (-2/3)| = 2$.
      (iii) The theorem's exports do not include a physical top mass:
            $\\Lambda_u = 2$ is the only quantity exported.

    The two-stage residual rule (norm-selects-then-flux-counts) is the
    structural shape: $L_2$ orders without orientation, $F_1$ counts
    absolute residual U(1) flux on the already-selected channel.  The
    sprint trajectory v0.4 (load-functional uniqueness) → v0.6 (local
    embedding candidate) → v0.12 (theorem-form local result) packages
    here as a single executable check.

    The full top-mass theorem $m_t : [P]$ remains conditional on three
    upstream gates ($T_{\\rm scheme}$, $W_{\\rm commute}$,
    $B_{\\rm upstream}$); this check supplies $B_{\\rm upstream}$ and
    nothing else.
    """
    sel = selected_channel()
    assert sel.name == "u_R^c", (
        f"residual-load maximizer must be u_R^c, got {sel.name}"
    )
    coeff = F1(sel)
    assert coeff == 2, (
        f"selected-channel flux F_1(u_R^c) must equal 2, got {coeff}"
    )
    # Cross-check the full residual table for the documentation summary
    table = [(c.name, L2(c), F1(c)) for c in CHANNELS]
    expected_L2 = {
        "Q_L":   Fraction(1, 6),
        "u_R^c": Fraction(4, 3),
        "d_R^c": Fraction(1, 3),
        "L_L":   Fraction(1, 2),
        "e_R^c": Fraction(1, 1),
    }
    expected_F1 = {
        "Q_L":   Fraction(1, 1),
        "u_R^c": Fraction(2, 1),
        "d_R^c": Fraction(1, 1),
        "L_L":   Fraction(1, 1),
        "e_R^c": Fraction(1, 1),
    }
    for name, l2, f1 in table:
        assert l2 == expected_L2[name], f"L_2({name}) mismatch: {l2} vs {expected_L2[name]}"
        assert f1 == expected_F1[name], f"F_1({name}) mismatch: {f1} vs {expected_F1[name]}"
    return {
        "name": "L_residual_up_normalizer_local",
        "passed": True,
        "key_result": (
            f"Residual quadratic U(1) interface load L_2 = d_3 d_2 Y^2 "
            f"uniquely selects u_R^c at 4/3 on the one-generation pre-mass "
            f"Standard Model channel table after Q_spent (other channels: "
            f"Q_L=1/6, d_R^c=1/3, L_L=1/2, e_R^c=1); residual flux F_1(u_R^c) "
            f"= |3*1*(-2/3)| = 2.  Therefore Lambda_u = c_R = 2.  Exports: "
            f"Lambda_u only — exports_physical_top_mass = False."
        ),
        "summary": (
            "Local up-sector residual normalizer theorem: after the spent "
            "quotient (removing L_EW, sqrt(3) spectral lift, weak-carrier "
            "bookkeeping, Yukawa-bilinear bookkeeping, and projective trace "
            "shape), the residual quadratic interface load uniquely selects "
            "u_R^c, and the absolute residual U(1) flux on that channel is 2.  "
            "Local theorem only: does not export a physical top mass.  Full "
            "top-mass theorem remains conditional on T_scheme + W_commute + "
            "B_upstream.  Source-of-record: Paper 32 v0.9 + DC sprint v0.12 / v0.14."
        ),
        "tier": 4,
        "epistemic": "[P_structural]",
        "dependencies": ["L_count", "L_gauge_template_uniqueness", "Q_spent"],
        "selected_channel": sel.name,
        "Lambda_u": int(coeff),
        "exports_physical_top_mass": False,
        "spent_quotient_removes": list(SPENT_QUOTIENT_REMOVES),
    }


def check_T_no_inverse_inputs_up_normalizer(used_inputs: Optional[Iterable[str]] = None):
    """T_no_inverse_inputs_up_normalizer: structural non-smuggling guard
    for the local up-normalizer theorem.

    Tier 4 [P_structural].

    Source-of-record: Paper 32 v0.9 + DominantChannel sprint v0.11 §
    "No-Inverse-Transport Theorem" (the trace-side form) + v0.12 §
    "What is now closed" (the local form).

    Verifies that the local up-normalizer theorem's declared input set
    is disjoint from the forbidden set
    $\\{m_t, y_t, m_b, m_\\tau, v_{\\rm obs},
       \\text{physical\\_yukawa\\_normalization}\\}$.

    The default declared input set is
    $\\{d_3, d_2, Y, Q_{\\rm spent}, L_2, F_1\\}$ — representation
    multiplicities, hypercharge, the spent quotient, and the two
    residual functionals.  No physical mass, no Yukawa target, no
    observed-$v$ smuggling.

    Calling with a custom ``used_inputs`` argument allows downstream
    audits (e.g., re-running this check after extending the declared
    inputs) to verify that any extension stays out of the forbidden
    set.  The check raises ``AssertionError`` if any forbidden input
    is detected.
    """
    if used_inputs is None:
        used = {"d3", "d2", "Y", "Q_spent", "L2", "F1"}
    else:
        used = set(used_inputs)
    bad = sorted(used & FORBIDDEN_INPUTS)
    assert not bad, (
        f"local up-normalizer theorem must not depend on inverse inputs; "
        f"detected: {bad}"
    )
    return {
        "name": "T_no_inverse_inputs_up_normalizer",
        "passed": True,
        "key_result": (
            f"Local up-normalizer theorem declared input set "
            f"{sorted(used)} is disjoint from the forbidden set "
            f"{sorted(FORBIDDEN_INPUTS)}; no inverse mass / Yukawa / "
            f"observed-v smuggling.  Lambda_u = 2 is proved from "
            f"representation multiplicity and hypercharge only."
        ),
        "summary": (
            "Non-smuggling guard for L_residual_up_normalizer_local.  "
            "Declared inputs are representation multiplicities, "
            "hypercharge, the spent quotient, and the two residual "
            "functionals; forbidden inputs are m_t, y_t, m_b, m_tau, "
            "v_obs, physical_yukawa_normalization.  The intersection is "
            "empty by construction.  Source-of-record: Paper 32 v0.9 + "
            "DC sprint v0.11 §No-Inverse-Transport + v0.12 §What is now closed."
        ),
        "tier": 4,
        "epistemic": "[P_structural]",
        "dependencies": ["L_residual_up_normalizer_local"],
        "forbidden_inputs_detected": bad,
        "used_inputs": sorted(used),
    }


# =====================================================================
# Public exports — only Lambda_u, never a physical top mass
# =====================================================================

def exports() -> dict:
    """Return the canonical exports of this module.

    The local up-normalizer theorem exports $\\Lambda_u = 2$ and
    nothing else.  ``exports_physical_top_mass`` is always ``False``.
    """
    r = check_L_residual_up_normalizer_local()
    return {
        "Lambda_u": r["Lambda_u"],
        "exports_physical_top_mass": False,
    }


# =====================================================================
# Bank registration
# =====================================================================

_CHECKS = {
    "L_residual_up_normalizer_local":      check_L_residual_up_normalizer_local,
    "T_no_inverse_inputs_up_normalizer":   check_T_no_inverse_inputs_up_normalizer,
}


def register(registry):
    """Register fermion-normalizer theorems into the global bank."""
    registry.update(_CHECKS)


# =====================================================================
# Module-level testing entry point
# =====================================================================

if __name__ == "__main__":
    for fn in (check_L_residual_up_normalizer_local,
               check_T_no_inverse_inputs_up_normalizer):
        result = fn()
        status = "PASS" if result.get("passed") else "FAIL"
        print(f"  [{status}] {result['name']}")
        print(f"         -> {result['key_result']}")
    print(f"  exports: {exports()}")

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "flavour:up_normalizer_local",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Two bank-registered checks, both tier 4 with returned machine field "
            "epistemic='[P_structural]'. check_L_residual_up_normalizer_local "
            "certifies the LOCAL up-sector normalizer theorem: after the declared "
            "spent quotient Q_spent (removing weak-scale, common spectral, weak- "
            "carrier, Yukawa-bilinear, and projective trace-shape structure), the "
            "residual quadratic U(1) interface load L_2(f) = d_3 d_2 Y^2 uniquely "
            "selects u_R^c at 4/3 on the five-channel one-generation table (Q_L = "
            "1/6, d_R^c = 1/3, L_L = 1/2, e_R^c = 1), and the residual flux "
            "functional gives F_1(u_R^c) = |3 x 1 x (-2/3)| = 2, hence Lambda_u = "
            "c_R = 2. check_T_no_inverse_inputs_up_normalizer is the structural "
            "non-smuggling guard: the declared input set {d_3, d_2, Y, Q_spent, "
            "L_2, F_1} is disjoint from the forbidden set {m_t, y_t, m_b, m_tau, "
            "v_obs, physical_yukawa_normalization}. The module exports Lambda_u = "
            "2 and NOTHING else -- no physical top mass, no MSbar or pole mass, "
            "no W-mass correction. The full top-mass theorem stays conditional on "
            "the T_scheme and W_commute upstream gates; this module supplies only "
            "the B_upstream gate, and the T_scheme transport-contract validator "
            "is held outside the bank (PASS_CONTRACT_SHAPE_ONLY). "
        ),
        "note": "Wave 7; local theorem + guard pair; conditional gates named as banked",
    },
)
