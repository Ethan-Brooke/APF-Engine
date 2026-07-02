"""EW longitudinal-scattering unitarity eigenscreens, admitted as INSTRUMENT.

Standard electroweak unitarity structure (Lee-Quigg-Thacker 1977), admitted as
INSTRUMENT. Nothing in APF forces these bounds; grade [P_structural]
(instrument). No numerical m_h is evaluated against the bounds here -- the
source packs deliberately fence that, and this module preserves the fence.

This module absorbs, as exact rational/symbolic computations, the symbolic
content of the five-pack sibling-AI Interface Engine chain (held, not banked;
"IE_INTEGRATOR_HANDOFF_PACKS_HELD_NOT_BANKED"):

  1. APF_INTERFACE_ENGINE_GOLDSTONE_EQUIVALENCE_BOUNDARY_v1
  2. APF_INTERFACE_ENGINE_EW_SCATTERING_UNITARITY_SYMBOLIC_GATE_v1
  3. APF_INTERFACE_ENGINE_EW_TREE_AMPLITUDE_CUSTODIAL_CHANNEL_BASIS_v1
  4. APF_INTERFACE_ENGINE_EW_PARTIAL_WAVE_ANALYTIC_SCREEN_v1
  5. APF_INTERFACE_ENGINE_EW_COUPLED_CHANNEL_EIGENSCREEN_SYMBOLIC_GATE_v1

The four layers carried here:

  (a) The Goldstone-equivalence boundary as a DECLARED contract, not a derived
      theorem:  M(V_L) = C_V * M(pi) + O(M_V/E)  with tree-canonical C_V = 1,
      validity domain E >> M_V.  The O(M_V/E) fence is explicit; the photon has
      no Goldstone partner (U(1)_em unbroken); loop-level C_V is NOT evaluated.

  (b) The custodial channel basis: the tree master amplitude
        A_tree(s) = s/v^2 - s^2/(v^2*(s - m_h^2)) = -m_h^2*s/(v^2*(s - m_h^2)),
      the invariant-tensor decomposition
        M_abcd = d_ab d_cd A(s,t,u) + d_ac d_bd A(t,s,u) + d_ad d_bc A(u,t,s),
      the isospin channels T_0 = 3A(s)+A(t)+A(u), T_1 = A(t)-A(u),
      T_2 = A(t)+A(u), and the E^2/v^2 growth-cancellation identity: the
      radial-Higgs exchange -s^2/(v^2(s-m_h^2)) cancels the +s/v^2 growth
      exactly (Coeff_{s/v^2} = 0); the residual is m_h^2-proportional.

  (c) The coupled-channel S-wave matrix on the normalized LQT basis
      { |W+_L W-_L>, |Z_L Z_L>/sqrt(2), |h h>/sqrt(2), |Z_L h> }, core entries
      exact in Q[sqrt(2)] in units of -m_h^2/(8*pi*v^2); spectrum {3/2 (x1),
      1/2 (x3)}; eigen-unitarity screen |Re a_0|_max <= 1/2 giving
        m_h^2/v^2 <= (8/3)*pi.

  (d) The partial-wave analytic screens a_0^0, a_1^1, a_0^2 (finite-m_h log
      closed forms kept at the declared-string level, verbatim from the pack
      ledger), their exact high-energy limits, and the strongest
      single-channel screen  m_h^2/v^2 <= (16/5)*pi.

Everything numeric-exact here is Fraction arithmetic (Q and Q[sqrt(2)]); pi is
kept symbolic throughout -- bounds are expressed as Fraction multiples of pi.
No PDG values, no numeric m_h or v anywhere. The finite-m_h log closed forms
are carried as verbatim declared strings only (they are transcendental in s);
the exact content checked is their high-energy limits, which are rational
multiples of m_h^2/(pi*v^2).

Deliberately NOT merged with the native OS-W modules: this is an admitted
instrument, not a native derivation, and it has no banked logical inputs --
dependencies lists are empty by design.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Tuple

F = Fraction

# ---------------------------------------------------------------------------
# Pack provenance (held, not banked; see module docstring)
# ---------------------------------------------------------------------------

PACK_PROVENANCE: Tuple[str, ...] = (
    "APF_INTERFACE_ENGINE_GOLDSTONE_EQUIVALENCE_BOUNDARY_v1 (verifier 229/229 PASS)",
    "APF_INTERFACE_ENGINE_EW_SCATTERING_UNITARITY_SYMBOLIC_GATE_v1 (verifier 333/333 PASS)",
    "APF_INTERFACE_ENGINE_EW_TREE_AMPLITUDE_CUSTODIAL_CHANNEL_BASIS_v1 (verifier 407/407 PASS)",
    "APF_INTERFACE_ENGINE_EW_PARTIAL_WAVE_ANALYTIC_SCREEN_v1 (verifier 393/393 PASS)",
    "APF_INTERFACE_ENGINE_EW_COUPLED_CHANNEL_EIGENSCREEN_SYMBOLIC_GATE_v1 (verifier 521/521 PASS)",
)

# ---------------------------------------------------------------------------
# (a) The Goldstone-equivalence boundary: a DECLARED contract
# ---------------------------------------------------------------------------
# M(V_L^a + X) = C_a M(pi^a + X) + O(M_a/E).  This is a structural statement
# with a validity domain, not a derived theorem; the pack exports it as a
# calculational high-energy map and this module preserves that reading.

GOLDSTONE_EQUIVALENCE_CONTRACT: Dict = {
    "statement": "M(V_L) = C_V * M(pi) + O(M_V/E)",
    "status": "DECLARED_CONTRACT",            # not a derived theorem
    "validity_domain": "E >> M_V",
    "suppression_fence": "O(M_V/E)",          # the explicit residual fence
    "tree_canonical_C_V": F(1),               # exact; loop C_V NOT evaluated
    "loop_factors_evaluated": False,
    "boundary_fields": {
        # massive longitudinal target -> would-be Goldstone coordinate
        "W+_L": "phi+",
        "W-_L": "phi-",
        "Z_L": "chi0",
    },
    "photon_goldstone_partner": None,          # U(1)_em unbroken
    "radial_higgs_role": "spectator_only",     # h is not a Goldstone
    "goldstones_are_asymptotic_particles": False,
}

# The tree diagram-family coverage the scattering gate requires before the
# E^2 cancellation may be certified (the radial-Higgs row is load-bearing).
TREE_FAMILY_ROWS: Tuple[str, ...] = (
    "VVVV_gauge_contact",
    "VVV_gauge_exchange",
    "Goldstone_contact_derivative",
    "scalar_quartic",
    "radial_Higgs_exchange",
)

# ---------------------------------------------------------------------------
# Exact 2-variable polynomial arithmetic over Q:  keys (i, j) = s^i * m^j
# (m stands for m_h^2 throughout; the overall 1/v^2 is carried as a unit).
# ---------------------------------------------------------------------------

Poly2 = Dict[Tuple[int, int], Fraction]


def _p_add(a: Poly2, b: Poly2) -> Poly2:
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, F(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def _p_mul(a: Poly2, b: Poly2) -> Poly2:
    out: Poly2 = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, F(0)) + v1 * v2
            if out[k] == 0:
                del out[k]
    return out


def _p_neg(a: Poly2) -> Poly2:
    return {k: -v for k, v in a.items()}


# Building blocks: s = s^1, m = m_h^2.
_S: Poly2 = {(1, 0): F(1)}
_M: Poly2 = {(0, 1): F(1)}
_S_MINUS_M: Poly2 = {(1, 0): F(1), (0, 1): F(-1)}


def master_amplitude_identity_holds() -> bool:
    """A_tree(s) = s/v^2 - s^2/(v^2 (s-m)) == -m s/(v^2 (s-m)), exactly.

    Cross-multiplied polynomial identity over Q[s, m]:
        s*(s - m) - s^2  ==  -m*s.
    """
    lhs = _p_add(_p_mul(_S, _S_MINUS_M), _p_neg(_p_mul(_S, _S)))
    rhs = _p_mul(_p_neg(_M), _S)
    return lhs == rhs


def e2_cancellation_holds() -> Tuple[bool, Fraction]:
    """The E^2/v^2 growth-cancellation identity, exactly.

    The radial-Higgs exchange term divides as
        -s^2 = (-s - m)*(s - m) + (-m^2),
    i.e. quotient -s - m (coefficient of s is -1) and remainder -m^2.  The
    gauge/derivative growth term contributes +1 * s/v^2.  The identity is the
    exact division statement; the returned Fraction is the total s/v^2
    coefficient  (+1) + (-1) = 0.
    """
    quotient: Poly2 = {(1, 0): F(-1), (0, 1): F(-1)}     # -s - m
    remainder: Poly2 = {(0, 2): F(-1)}                   # -m^2
    lhs = _p_neg(_p_mul(_S, _S))                         # -s^2
    rhs = _p_add(_p_mul(quotient, _S_MINUS_M), remainder)
    division_ok = lhs == rhs
    growth_coeff = F(1)                                  # +s/v^2 row (MA1)
    higgs_coeff = quotient.get((1, 0), F(0))             # -1 from -s^2/(s-m)
    return division_ok, growth_coeff + higgs_coeff


# High-energy limit of the master amplitude, in units of m_h^2/v^2:
# A(q >> m_h^2) -> -1  (i.e. -m_h^2/v^2), read off exactly from
# A = -m*s / (v^2*(s-m)): numerator and denominator are both degree 1 in s,
# with leading s-coefficients -m and +1.
A_INFINITY = F(-1)   # in units of m_h^2/v^2

# ---------------------------------------------------------------------------
# (b) Custodial channel basis
# ---------------------------------------------------------------------------

CUSTODIAL_TENSOR_DECOMPOSITION = (
    "M_abcd(s,t,u) = delta_ab delta_cd A(s,t,u) + delta_ac delta_bd A(t,s,u)"
    " + delta_ad delta_bc A(u,t,s)"
)

# Isospin channel amplitudes as integer combinations (cA_s, cA_t, cA_u) of
# A(s,t,u), A(t,s,u), A(u,t,s):
ISOSPIN_CHANNELS: Dict[str, Tuple[int, int, int]] = {
    "T0": (3, 1, 1),   # I = 0 singlet
    "T1": (0, 1, -1),  # I = 1 antisymmetric triplet
    "T2": (0, 1, 1),   # I = 2 symmetric traceless fiveplet
}

# Charge-basis longitudinal processes -> custodial content (from the pack's
# CHARGE_PROCESS_LEDGER; the photon row is excluded_no_goldstone_partner).
CHARGE_PROCESS_MAP: Dict[str, Tuple[str, ...]] = {
    "W+_L W-_L -> Z_L Z_L": ("I=0", "I=2"),
    "W+_L W-_L -> W+_L W-_L": ("I=0", "I=1", "I=2"),
    "W+_L Z_L -> W+_L Z_L": ("I=1", "I=2"),
    "W-_L Z_L -> W-_L Z_L": ("I=1", "I=2"),
    "Z_L Z_L -> Z_L Z_L": ("I=0", "I=2"),
    "W+_L W+_L -> W+_L W+_L": ("I=2",),
}


def isospin_high_energy_constants() -> Dict[str, Fraction]:
    """T_I in the E >> m_h limit, in units of m_h^2/v^2 (each A -> -1)."""
    return {
        name: (ca + ct + cu) * A_INFINITY
        for name, (ca, ct, cu) in ISOSPIN_CHANNELS.items()
    }

# ---------------------------------------------------------------------------
# Exact arithmetic in Q[sqrt(2)]:  x = (a, b)  means  a + b*sqrt(2)
# ---------------------------------------------------------------------------

Q2 = Tuple[Fraction, Fraction]

Q2_ZERO: Q2 = (F(0), F(0))
Q2_ONE: Q2 = (F(1), F(0))


def _q2(a, b=0) -> Q2:
    return (F(a), F(b))


def _q2_add(x: Q2, y: Q2) -> Q2:
    return (x[0] + y[0], x[1] + y[1])


def _q2_sub(x: Q2, y: Q2) -> Q2:
    return (x[0] - y[0], x[1] - y[1])


def _q2_mul(x: Q2, y: Q2) -> Q2:
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def _q2_scale(x: Q2, c: Fraction) -> Q2:
    return (x[0] * c, x[1] * c)


def _q2_float(x: Q2) -> float:
    return float(x[0]) + float(x[1]) * (2.0 ** 0.5)


# ---------------------------------------------------------------------------
# (c) The coupled-channel S-wave matrix (LQT basis)
# ---------------------------------------------------------------------------
# Normalized basis: |W+_L W-_L>, |Z_L Z_L>/sqrt(2), |h h>/sqrt(2), |Z_L h>.
# Core matrix in units of  -m_h^2/(8*pi*v^2);  1/sqrt(8) = (sqrt(2))/4.

COUPLED_CHANNEL_BASIS: Tuple[str, ...] = (
    "|W+_L W-_L>", "|Z_L Z_L>/sqrt(2)", "|h h>/sqrt(2)", "|Z_L h>",
)

_S8: Q2 = _q2(0, F(1, 4))   # 1/sqrt(8) = sqrt(2)/4, exact in Q[sqrt(2)]

A0_CORE_MATRIX: Tuple[Tuple[Q2, ...], ...] = (
    (_q2(1), _S8, _S8, Q2_ZERO),
    (_S8, _q2(F(3, 4)), _q2(F(1, 4)), Q2_ZERO),
    (_S8, _q2(F(1, 4)), _q2(F(3, 4)), Q2_ZERO),
    (Q2_ZERO, Q2_ZERO, Q2_ZERO, _q2(F(1, 2))),
)

A0_MATRIX_PREFACTOR = "-m_h^2/(8*pi*v^2)"   # symbolic unit of the core matrix

# Exact spectrum of the core matrix: 3/2 (multiplicity 1), 1/2 (multiplicity 3)
CORE_EIGENVALUES: Tuple[Tuple[Fraction, int], ...] = ((F(3, 2), 1), (F(1, 2), 3))

# Eigenvector witnesses (unnormalized; components in Q[sqrt(2)]) with the
# pack's normalizations recorded: EV0/EV1 divide by 2, EV2 by sqrt(2).
EIGENVECTOR_WITNESSES: Tuple[Tuple[str, Tuple[Q2, ...], Fraction], ...] = (
    ("EV0 (sqrt(2),1,1,0)/2", (_q2(0, 1), Q2_ONE, Q2_ONE, Q2_ZERO), F(3, 2)),
    ("EV1 (-sqrt(2),1,1,0)/2", (_q2(0, -1), Q2_ONE, Q2_ONE, Q2_ZERO), F(1, 2)),
    ("EV2 (0,1,-1,0)/sqrt(2)", (Q2_ZERO, Q2_ONE, _q2(-1), Q2_ZERO), F(1, 2)),
    ("EV3 (0,0,0,1)", (Q2_ZERO, Q2_ZERO, Q2_ZERO, Q2_ONE), F(1, 2)),
)


def _q2_matvec(M: Tuple[Tuple[Q2, ...], ...], v: Tuple[Q2, ...]) -> Tuple[Q2, ...]:
    return tuple(
        _q2_add(_q2_add(_q2_mul(row[0], v[0]), _q2_mul(row[1], v[1])),
                _q2_add(_q2_mul(row[2], v[2]), _q2_mul(row[3], v[3])))
        for row in M
    )


def _q2_det4(M: Tuple[Tuple[Q2, ...], ...]) -> Q2:
    """Exact 4x4 determinant in Q[sqrt(2)] by Laplace expansion."""
    def det2(a, b, c, d):
        return _q2_sub(_q2_mul(a, d), _q2_mul(b, c))

    def det3(rows):
        (a, b, c), (d, e, f), (g, h, i) = rows
        t1 = _q2_mul(a, det2(e, f, h, i))
        t2 = _q2_mul(b, det2(d, f, g, i))
        t3 = _q2_mul(c, det2(d, e, g, h))
        return _q2_add(_q2_sub(t1, t2), t3)

    total = Q2_ZERO
    sign = 1
    for col in range(4):
        minor = tuple(
            tuple(M[r][c] for c in range(4) if c != col) for r in range(1, 4)
        )
        term = _q2_mul(M[0][col], det3(minor))
        total = _q2_add(total, term) if sign > 0 else _q2_sub(total, term)
        sign = -sign
    return total


# ---------------------------------------------------------------------------
# Symbolic unitarity thresholds: Fraction multiples of pi (pi stays symbolic)
# ---------------------------------------------------------------------------
# A screen with partial-wave magnitude  c * (m_h^2/(pi*v^2))  and condition
# |a| <= 1/2 yields  m_h^2/v^2 <= (1/(2c)) * pi.

def screen_threshold(coeff: Fraction) -> Fraction:
    """|a| = coeff * m_h^2/(pi*v^2) <= 1/2  =>  m_h^2/v^2 <= (1/(2*coeff))*pi."""
    return 1 / (2 * coeff)


# Eigenscreen: |lambda_max| = (3/2) * m_h^2/(8*pi*v^2) = (3/16) * m_h^2/(pi*v^2)
EIGENSCREEN_COEFF = F(3, 16)
BOUND_COUPLED_PI = F(8, 3)      # m_h^2/v^2 <= (8/3)*pi

# Single-channel a_0^0: 5/32;  fiveplet a_0^2: 1/16
A00_COEFF = F(5, 32)
A02_COEFF = F(1, 16)
BOUND_SINGLE_PI = F(16, 5)      # m_h^2/v^2 <= (16/5)*pi (strongest single-channel)
BOUND_FIVEPLET_PI = F(8)        # m_h^2/v^2 <= 8*pi
# Degenerate coupled-channel subspace screen: (1/2)*(1/8) = 1/16 -> 8*pi too.

# ---------------------------------------------------------------------------
# (d) Partial-wave analytic screens: declared closed forms (verbatim from the
# pack's ANALYTIC_PARTIAL_WAVE_LEDGER) + exact high-energy limits.
# The log terms are transcendental in s; they stay at the declared-string
# level, cleanly separated from the exact Fraction bounds below.
# ---------------------------------------------------------------------------

PARTIAL_WAVE_CLOSED_FORMS: Dict[str, str] = {
    "a_0^0": "a_0^0=-(m_h^2/(32*pi*v^2))*(3*s/(s-m_h^2)+2-2*(m_h^2/s)*log(1+s/m_h^2))",
    "a_1^1": "a_1^1=(m_h^4/(16*pi*s*v^2))*((1+2*m_h^2/s)*log(1+s/m_h^2)-2)",
    "a_0^2": "a_0^2=-(m_h^2/(16*pi*v^2))*(1-(m_h^2/s)*log(1+s/m_h^2))",
}

# Exact high-energy limits in units of m_h^2/(pi*v^2):
PARTIAL_WAVE_HIGH_ENERGY_LIMITS: Dict[str, Fraction] = {
    "a_0^0": F(-5, 32),
    "a_1^1": F(0),
    "a_0^2": F(-1, 16),
}

MANDELSTAM_KINEMATICS = {
    "t": "-(s/2)*(1-cos(theta))",
    "u": "-(s/2)*(1+cos(theta))",
    "constraint": "s+t+u=0",
    "domain_guard": "s away from the Higgs pole s = m_h^2",
}


def partial_wave_limits_from_channels() -> Dict[str, Fraction]:
    """Derive the high-energy partial-wave limits exactly from the channel
    constants:  a_0^I = T_I/(32*pi) for J=0 (the J=0 projection of a constant
    is T/(32*pi)); the J=1 projection of a constant vanishes."""
    T = isospin_high_energy_constants()
    return {
        "a_0^0": T["T0"] / 32,   # in units of m_h^2/(pi*v^2)
        "a_1^1": F(0),           # odd Legendre moment of a constant
        "a_0^2": T["T2"] / 32,
    }


# ---------------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------------

def check_T_goldstone_equivalence_boundary_declared() -> Dict:
    """The Goldstone-equivalence boundary as a DECLARED contract with fences.

    Certifies that the contract carries: (i) the boundary statement
    M(V_L) = C_V*M(pi) + O(M_V/E) with tree-canonical C_V = 1 exact; (ii) the
    explicit O(M_V/E) suppression fence and the E >> M_V validity domain;
    (iii) all three massive longitudinal targets mapped to their would-be
    Goldstone coordinates and the photon explicitly excluded (no Goldstone
    partner, U(1)_em unbroken); (iv) the DECLARED_CONTRACT status -- this is a
    structural statement with a validity domain, NOT a derived theorem, and
    loop-level equivalence factors are NOT evaluated; (v) the scattering
    gate's five-row tree-family coverage (the radial-Higgs row load-bearing)
    is present as the declared prerequisite of the E^2 cancellation.
    Instrument grade; admitted, not forced by A1.
    """
    c = GOLDSTONE_EQUIVALENCE_CONTRACT
    failures: List[str] = []
    if c["status"] != "DECLARED_CONTRACT":
        failures.append("boundary not marked as a declared contract")
    if c["tree_canonical_C_V"] != F(1):
        failures.append("tree-canonical C_V != 1")
    if c["loop_factors_evaluated"]:
        failures.append("loop factors must NOT be evaluated (pack fence)")
    if c["suppression_fence"] != "O(M_V/E)":
        failures.append("O(M_V/E) fence missing")
    if c["validity_domain"] != "E >> M_V":
        failures.append("validity domain E >> M_V missing")
    want_fields = {"W+_L": "phi+", "W-_L": "phi-", "Z_L": "chi0"}
    if c["boundary_fields"] != want_fields:
        failures.append("boundary fields wrong: %r" % (c["boundary_fields"],))
    if c["photon_goldstone_partner"] is not None:
        failures.append("photon must have no Goldstone partner")
    if c["goldstones_are_asymptotic_particles"]:
        failures.append("Goldstones must stay non-asymptotic auxiliaries")
    if len(TREE_FAMILY_ROWS) != 5 or "radial_Higgs_exchange" not in TREE_FAMILY_ROWS:
        failures.append("five-row tree-family coverage (incl. radial Higgs) missing")
    return {
        "name": (
            "T_goldstone_equivalence_boundary_declared: M(V_L) = C_V*M(pi) + "
            "O(M_V/E), C_V = 1 tree-canonical, as a DECLARED contract with "
            "explicit validity domain and suppression fence (Lee-Quigg-Thacker "
            "instrument chain) [P_structural]"
        ),
        "passed": not failures,
        "epistemic": "P_structural_instrument",
        "dependencies": [],
        "failures": failures,
        "key_result": (
            "The Goldstone-equivalence boundary M(V_L) = C_V*M(pi) + O(M_V/E) "
            "is carried as a DECLARED calculational contract (validity domain "
            "E >> M_V, C_V = 1 exact at the tree-canonical boundary, loop "
            "factors not evaluated), with W+_L/W-_L/Z_L mapped to "
            "phi+/phi-/chi0, the photon excluded (U(1)_em unbroken), and the "
            "five-row tree-family coverage (radial-Higgs row load-bearing) as "
            "the declared prerequisite of the E^2 cancellation. Admitted "
            "instrument; nothing in APF forces this structure."
        ),
    }


def check_T_ew_custodial_amplitude_basis() -> Dict:
    """The custodial channel basis and the exact E^2 growth cancellation.

    Exact Q[s, m_h^2] polynomial identities: (i) the master amplitude
    A_tree(s) = s/v^2 - s^2/(v^2(s-m_h^2)) equals -m_h^2 s/(v^2(s-m_h^2))
    (cross-multiplied identity s(s-m) - s^2 = -m s); (ii) the E^2/v^2
    growth-cancellation: the radial-Higgs exchange -s^2/(s-m) divides exactly
    as (-s-m)(s-m) - m^2, so its s/v^2 coefficient is -1 and cancels the +1
    gauge/derivative growth term -- Coeff_{s/v^2} = 0, residual
    m_h^2-proportional; (iii) the T0/T1/T2 isospin decomposition with exact
    high-energy constants (-5, 0, -2) in units of m_h^2/v^2; (iv) the
    charge-process -> isospin map covers the six longitudinal processes and
    stays inside {I=0, I=1, I=2}. Instrument grade.
    """
    failures: List[str] = []
    if not master_amplitude_identity_holds():
        failures.append("master amplitude identity s/v^2 - s^2/(v^2(s-m)) != -ms/(v^2(s-m))")
    div_ok, coeff = e2_cancellation_holds()
    if not div_ok:
        failures.append("polynomial division -s^2 = (-s-m)(s-m) - m^2 failed")
    if coeff != 0:
        failures.append("E^2 growth coefficient did not cancel: %s" % coeff)
    T = isospin_high_energy_constants()
    if T != {"T0": F(-5), "T1": F(0), "T2": F(-2)}:
        failures.append("isospin high-energy constants wrong: %r" % (T,))
    if ISOSPIN_CHANNELS != {"T0": (3, 1, 1), "T1": (0, 1, -1), "T2": (0, 1, 1)}:
        failures.append("T0/T1/T2 crossing combinations wrong")
    if len(CHARGE_PROCESS_MAP) != 6:
        failures.append("charge-process map must cover six processes")
    allowed = {"I=0", "I=1", "I=2"}
    for proc, chans in CHARGE_PROCESS_MAP.items():
        if not set(chans) <= allowed:
            failures.append("process %s cites channel outside I=0,1,2" % proc)
    if CHARGE_PROCESS_MAP.get("W+_L W+_L -> W+_L W+_L") != ("I=2",):
        failures.append("like-sign channel must isolate the fiveplet sector")
    return {
        "name": (
            "T_ew_custodial_amplitude_basis: custodial T0/T1/T2 channel basis "
            "over the master amplitude A_tree(s) = -m_h^2 s/(v^2(s-m_h^2)), "
            "with the exact E^2/v^2 growth-cancellation identity "
            "(Coeff_{s/v^2} = 0; residual m_h^2-proportional) [P_structural]"
        ),
        "passed": not failures,
        "epistemic": "P_structural_instrument",
        "dependencies": [],
        "failures": failures,
        "key_result": (
            "Exact polynomial identities over Q[s, m_h^2]: the tree master "
            "amplitude s/v^2 - s^2/(v^2(s-m_h^2)) = -m_h^2 s/(v^2(s-m_h^2)); "
            "the radial-Higgs exchange divides as -s^2 = (-s-m)(s-m) - m^2, "
            "so the GOLDSTONE-PICTURE contact/derivative +s/v^2 growth "
            "cancels exactly (Coeff_{s/v^2} = +1 - 1 = 0) and the residual "
            "is m_h^2-proportional (A -> -m_h^2/v^2 at high energy). The "
            "gauge-diagram E^4/E^2 cancellations are NOT certified here -- "
            "they sit behind the DECLARED equivalence boundary (check 1). "
            "Isospin "
            "channels T0 = 3A(s)+A(t)+A(u), T1 = A(t)-A(u), T2 = A(t)+A(u) "
            "have exact high-energy constants (-5, 0, -2)*m_h^2/v^2, and the "
            "six charge-basis longitudinal processes map into {I=0,1,2} with "
            "the like-sign channel isolating I=2. Admitted LQT instrument; "
            "no numerical amplitude exported."
        ),
    }


def check_T_ew_coupled_channel_eigenscreen_lqt() -> Dict:
    """The coupled-channel S-wave eigenscreen: m_h^2/v^2 <= (8/3)*pi, exact.

    On the normalized LQT basis {W+W-, ZZ/sqrt2, hh/sqrt2, Zh} the core
    S-wave matrix (units -m_h^2/(8 pi v^2)) has entries in Q[sqrt(2)].
    Exact verifications: (i) symmetry; (ii) all four pack eigenvector
    witnesses satisfy M v = lambda v exactly in Q[sqrt(2)] with unit norm;
    (iii) mutual orthogonality; (iv) trace = 3 = 3/2 + 3*(1/2) and
    det = 3/16 = (3/2)*(1/2)^3 pin the full spectrum {3/2, 1/2 x3};
    (v) |lambda_max| = (3/2)/(8 pi) = 3/(16 pi) * m_h^2/v^2 <= 1/2 gives the
    exact threshold m_h^2/v^2 <= (8/3)*pi, stricter than the single-channel
    16*pi/5 by the exact ratio 5/6; (vi) a float brute-force witness (power
    iteration + residuals) agrees with the exact spectrum to 1e-9. No
    numerical m_h is evaluated against the bound. Instrument grade.
    """
    failures: List[str] = []
    M = A0_CORE_MATRIX
    # (i) symmetry
    for i in range(4):
        for j in range(4):
            if M[i][j] != M[j][i]:
                failures.append("core matrix not symmetric at (%d,%d)" % (i, j))
    # (ii) exact eigenvector witnesses + unit norm of the pack normalizations
    norms = (F(1, 4), F(1, 4), F(1, 2), F(1))   # 1/2^2, 1/2^2, (1/sqrt2)^2, 1
    for (label, vec, lam), nrm in zip(EIGENVECTOR_WITNESSES, norms):
        got = _q2_matvec(M, vec)
        want = tuple(_q2_scale(x, lam) for x in vec)
        if got != want:
            failures.append("eigen equation fails exactly for %s" % label)
        n2 = Q2_ZERO
        for x in vec:
            n2 = _q2_add(n2, _q2_mul(x, x))
        if _q2_scale(n2, nrm) != Q2_ONE:
            failures.append("pack normalization not unit for %s" % label)
    # (iii) mutual orthogonality (exact)
    vecs = [w[1] for w in EIGENVECTOR_WITNESSES]
    for i in range(4):
        for j in range(i + 1, 4):
            dot = Q2_ZERO
            for a, b in zip(vecs[i], vecs[j]):
                dot = _q2_add(dot, _q2_mul(a, b))
            if dot != Q2_ZERO:
                failures.append("witnesses %d,%d not orthogonal" % (i, j))
    # (iv) trace + determinant pin the spectrum
    trace = Q2_ZERO
    for i in range(4):
        trace = _q2_add(trace, M[i][i])
    if trace != (F(3), F(0)):
        failures.append("trace != 3: %r" % (trace,))
    spec_sum = sum(lam * mult for lam, mult in CORE_EIGENVALUES)
    if spec_sum != F(3):
        failures.append("eigenvalue sum != trace")
    det = _q2_det4(M)
    spec_prod = F(1)
    for lam, mult in CORE_EIGENVALUES:
        spec_prod *= lam ** mult
    if det != (spec_prod, F(0)) or spec_prod != F(3, 16):
        failures.append("det %r != eigenvalue product %s" % (det, spec_prod))
    # (v) the eigenscreen threshold, exact Fraction multiple of pi
    lam_max = max(lam for lam, _ in CORE_EIGENVALUES)
    if lam_max != F(3, 2):
        failures.append("largest core eigenvalue != 3/2")
    coeff = lam_max / 8                      # (3/2) * 1/(8 pi) = 3/(16 pi)
    if coeff != EIGENSCREEN_COEFF:
        failures.append("eigenscreen coefficient != 3/16")
    if screen_threshold(coeff) != BOUND_COUPLED_PI or BOUND_COUPLED_PI != F(8, 3):
        failures.append("coupled-channel threshold != (8/3)*pi")
    if BOUND_COUPLED_PI / BOUND_SINGLE_PI != F(5, 6):
        failures.append("new/previous ceiling ratio != 5/6")
    if screen_threshold(min(l for l, _ in CORE_EIGENVALUES) / 8) != F(8):
        failures.append("degenerate-subspace screen != 8*pi")
    # (vi) float brute-force witness: power iteration + residuals
    Mf = [[_q2_float(M[i][j]) for j in range(4)] for i in range(4)]
    v = [1.0, 1.0, 1.0, 1.0]
    lam_f = 0.0
    for _ in range(200):
        w = [sum(Mf[i][j] * v[j] for j in range(4)) for i in range(4)]
        nrm = sum(x * x for x in w) ** 0.5
        v = [x / nrm for x in w]
        lam_f = sum(v[i] * sum(Mf[i][j] * v[j] for j in range(4)) for i in range(4))
    if abs(lam_f - 1.5) > 1e-9:
        failures.append("power-iteration dominant eigenvalue %.12f != 3/2" % lam_f)
    for label, vec, lam in EIGENVECTOR_WITNESSES:
        vf = [_q2_float(x) for x in vec]
        res = max(
            abs(sum(Mf[i][j] * vf[j] for j in range(4)) - float(lam) * vf[i])
            for i in range(4)
        )
        if res > 1e-12:
            failures.append("float residual %g too large for %s" % (res, label))
    return {
        "name": (
            "T_ew_coupled_channel_eigenscreen_lqt: coupled-channel S-wave "
            "eigenscreen on {W+W-, ZZ/sqrt2, hh/sqrt2, Zh}; exact Q[sqrt(2)] "
            "spectrum {3/2, 1/2 x3} => |Re a_0|max <= 1/2 gives m_h^2/v^2 <= "
            "(8/3)*pi (no numerical m_h evaluated) [P_structural]"
        ),
        "passed": not failures,
        "epistemic": "P_structural_instrument",
        "dependencies": [],
        "failures": failures,
        "key_result": (
            "The LQT coupled-channel S-wave core matrix (units "
            "-m_h^2/(8*pi*v^2)) on the normalized basis {|W+_L W-_L>, "
            "|Z_L Z_L>/sqrt2, |h h>/sqrt2, |Z_L h>} is verified exactly in "
            "Q[sqrt(2)]: the four pack eigenvector witnesses satisfy "
            "M v = lambda v exactly, are orthonormal under the pack "
            "normalizations, and trace = 3 with det = 3/16 pin the spectrum "
            "{3/2 (x1), 1/2 (x3)}. The eigen-unitarity screen "
            "|lambda_max| = 3 m_h^2/(16 pi v^2) <= 1/2 yields the exact "
            "symbolic threshold m_h^2/v^2 <= (8/3)*pi -- stricter than the "
            "single-channel 16*pi/5 by the exact ratio 5/6; the degenerate "
            "subspace gives 8*pi. A float power-iteration/residual witness "
            "cross-checks the exact spectrum. Admitted instrument; pi stays "
            "symbolic and no numerical Higgs mass is compared to the bound."
        ),
    }


def check_T_ew_partial_wave_screens() -> Dict:
    """The partial-wave analytic screens; strongest single-channel 16*pi/5.

    The finite-m_h closed forms for a_0^0, a_1^1, a_0^2 are carried verbatim
    from the pack ledger as declared strings (their log terms are
    transcendental in s and stay fenced from the exact layer). The exact
    layer: the high-energy limits derive from the custodial channel
    constants -- a_0^0 -> -5/32, a_1^1 -> 0, a_0^2 -> -1/16 in units of
    m_h^2/(pi*v^2) -- and |Re a| <= 1/2 yields the exact thresholds
    m_h^2/v^2 <= (16/5)*pi (strongest single-channel, from a_0^0) and 8*pi
    (fiveplet), with the coupled eigenscreen (8/3)*pi strictly strongest
    overall. The Higgs pole s = m_h^2 is guarded out of the domain.
    Instrument grade.
    """
    failures: List[str] = []
    derived = partial_wave_limits_from_channels()
    if derived != PARTIAL_WAVE_HIGH_ENERGY_LIMITS:
        failures.append("derived high-energy limits %r != declared %r"
                        % (derived, PARTIAL_WAVE_HIGH_ENERGY_LIMITS))
    if abs(PARTIAL_WAVE_HIGH_ENERGY_LIMITS["a_0^0"]) != A00_COEFF:
        failures.append("|a_0^0| coefficient != 5/32")
    if abs(PARTIAL_WAVE_HIGH_ENERGY_LIMITS["a_0^2"]) != A02_COEFF:
        failures.append("|a_0^2| coefficient != 1/16")
    if PARTIAL_WAVE_HIGH_ENERGY_LIMITS["a_1^1"] != 0:
        failures.append("a_1^1 high-energy limit != 0")
    if screen_threshold(A00_COEFF) != BOUND_SINGLE_PI or BOUND_SINGLE_PI != F(16, 5):
        failures.append("a_0^0 screen threshold != (16/5)*pi")
    if screen_threshold(A02_COEFF) != BOUND_FIVEPLET_PI or BOUND_FIVEPLET_PI != F(8):
        failures.append("a_0^2 screen threshold != 8*pi")
    if not (BOUND_COUPLED_PI < BOUND_SINGLE_PI < BOUND_FIVEPLET_PI):
        failures.append("screen ordering (8/3) < (16/5) < 8 violated")
    for key in ("a_0^0", "a_1^1", "a_0^2"):
        cf = PARTIAL_WAVE_CLOSED_FORMS.get(key, "")
        if "log(1+s/m_h^2)" not in cf:
            failures.append("closed form for %s missing its declared log term" % key)
        if "pi" not in cf:
            failures.append("closed form for %s missing symbolic pi" % key)
    if MANDELSTAM_KINEMATICS["constraint"] != "s+t+u=0":
        failures.append("massless-Goldstone Mandelstam constraint missing")
    if "pole" not in MANDELSTAM_KINEMATICS["domain_guard"]:
        failures.append("Higgs-pole domain guard missing")
    return {
        "name": (
            "T_ew_partial_wave_screens: analytic partial-wave screens a_0^0, "
            "a_1^1, a_0^2 with exact high-energy limits (-5/32, 0, -1/16) in "
            "units m_h^2/(pi*v^2); strongest single-channel screen m_h^2/v^2 "
            "<= (16/5)*pi (log closed forms fenced as declared strings) "
            "[P_structural]"
        ),
        "passed": not failures,
        "epistemic": "P_structural_instrument",
        "dependencies": [],
        "failures": failures,
        "key_result": (
            "The three custodial partial-wave screens are carried at two "
            "cleanly separated levels: the finite-m_h log closed forms as "
            "verbatim declared strings (transcendental in s; never "
            "float-evaluated), and the exact layer where the high-energy "
            "limits derive from the channel constants T0 -> -5, T1 -> 0, "
            "T2 -> -2 (units m_h^2/v^2): a_0^0 -> -5m_h^2/(32 pi v^2), "
            "a_1^1 -> 0, a_0^2 -> -m_h^2/(16 pi v^2). |Re a| <= 1/2 gives "
            "the exact symbolic thresholds (16/5)*pi (strongest "
            "single-channel) and 8*pi (fiveplet), with the exact ordering "
            "(8/3)*pi < (16/5)*pi < 8*pi against the coupled eigenscreen. "
            "The Higgs pole s = m_h^2 is guarded out. Admitted instrument; "
            "no numerical Higgs-mass bound exported."
        ),
    }


_CHECKS = {
    "T_goldstone_equivalence_boundary_declared": check_T_goldstone_equivalence_boundary_declared,
    "T_ew_custodial_amplitude_basis": check_T_ew_custodial_amplitude_basis,
    "T_ew_coupled_channel_eigenscreen_lqt": check_T_ew_coupled_channel_eigenscreen_lqt,
    "T_ew_partial_wave_screens": check_T_ew_partial_wave_screens,
}


def register(registry):
    registry.update(_CHECKS)


# ---------------------------------------------------------------------------
# IE onboarding declarations. CODOMAIN payloads were inspected first
# (_compile_codomain_input): they require a regime + network_state pair for
# adjudicate_codomain_competition -- a regime-competition contract that does
# not fit this instrument content. So these are claim_text CLAIM inputs
# (structural probes) describing the banked disposition. expect_export was
# pinned by OBSERVATION: both claims were run through
# interface_atlas.summarize_input before landing and returned
# solver_status=SOLVED_LOCAL_HELD_FOR_REPAIR, export_global_P=False,
# packet_status=OPEN_EVIDENCE_REQUIRED -- the honest verdict for an admitted
# instrument that exports no global section.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "ew_eigenscreen:coupled_channel_disposition",
        "expect_export": False,   # OBSERVED: SOLVED_LOCAL_HELD_FOR_REPAIR
        "axis": "ROUTE",
        "claim_text": (
            "structural probe: the Lee-Quigg-Thacker coupled-channel S-wave "
            "eigenscreen is admitted as an instrument; the exported object is "
            "the exact symbolic threshold m_h^2/v^2 <= (8/3)*pi from the "
            "largest eigenvalue 3/2 of the rational core matrix; no numerical "
            "Higgs mass is evaluated against the bound."
        ),
        "note": (
            "provenance: APF_INTERFACE_ENGINE_EW_COUPLED_CHANNEL_EIGENSCREEN_"
            "SYMBOLIC_GATE_v1 + EW_PARTIAL_WAVE_ANALYTIC_SCREEN_v1 (held, not "
            "banked); observed engine verdict SOLVED_LOCAL_HELD_FOR_REPAIR / "
            "export_global_P=False"
        ),
    },
    {
        "input_id": "ew_eigenscreen:goldstone_boundary_disposition",
        "expect_export": False,   # OBSERVED: SOLVED_LOCAL_HELD_FOR_REPAIR
        "axis": "ROUTE",
        "claim_text": (
            "structural probe: the Goldstone equivalence boundary "
            "M(V_L) = C_V*M(pi) + O(M_V/E) with tree-canonical C_V = 1 is a "
            "declared calculational contract with validity domain E >> M_V, "
            "not a derived theorem; the photon has no Goldstone partner and "
            "loop-level factors are not evaluated."
        ),
        "note": (
            "provenance: APF_INTERFACE_ENGINE_GOLDSTONE_EQUIVALENCE_BOUNDARY_"
            "v1 + EW_SCATTERING_UNITARITY_SYMBOLIC_GATE_v1 + EW_TREE_"
            "AMPLITUDE_CUSTODIAL_CHANNEL_BASIS_v1 (held, not banked); "
            "observed engine verdict SOLVED_LOCAL_HELD_FOR_REPAIR / "
            "export_global_P=False"
        ),
    },
)


if __name__ == "__main__":
    ok = True
    for name, fn in _CHECKS.items():
        r = fn()
        ok = ok and r["passed"]
        print(("PASS" if r["passed"] else "FAIL"), name)
        for f in r["failures"]:
            print("   -", f)
    print("module status:", "PASS" if ok else "FAIL")
