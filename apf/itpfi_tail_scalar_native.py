"""apf/itpfi_tail_scalar_native.py -- native scalar-on-Omega lemma for the
M_2-ITPFI interface algebra (the import-free core of tail-triviality).

v24.3.267 (2026-06-22).  Bank landing of the genuinely-native fragment isolated
by a dedicated pre-bank cold audit during the 2026-06-22 Araki-Woods program.

CONTEXT.  The factoriality face of the completion seam (Z(M)=C.1 for the
M_2-ITPFI weak closure M = pi_phi(A)'') imports the von Neumann tensor
commutation theorem; this was confirmed irreducible across six independent
native routes (see APF Reference Docs, "Araki-Woods Native Derivation"
sequence, 2026-06-22).  A GNS/tail argument localized the import to a SINGLE
step.  The dedicated pre-bank cold audit then split that argument cleanly:

  * Steps (i)-(iii) -- ampliation lemma + product-state GNS factorization +
    cyclicity of Omega -- are GENUINELY NATIVE and prove, with no separating-
    ness, no modular structure, and no commutation theorem:

        for every tail element z in cap_k M_{>=k}:   z Omega = phi(z) . Omega
                                                      (z acts as a scalar on Omega)

  * Step (iv) -- "Omega separating for M", which upgrades z Omega = phi(z) Omega
    to z = phi(z).1 (full tail-triviality, hence factoriality) -- is NOT native:
    the general implication "faithful state on the C*-algebra A => GNS vector
    separating for the weak closure A''" is FALSE (counterexample A = C.1 + K(H),
    A''=B(H) has no separating vector in infinite dim), so it can only be
    justified through the product-specific Araki-Woods modular structure
    (Delta = (x)Delta_n, J = (x)J_n) -- the SAME TIER as the commutation theorem.

This module banks ONLY the native fragment (the scalar-on-Omega lemma).  It does
NOT bank full tail-triviality or factoriality, which inherit the [P_structural]
Araki-Woods import already carried by L_algebra_type / interface_factor_native.

GRADE.  check_L_itpfi_tail_acts_scalar_on_omega_native -- tier 3 [P].  Native
inputs only: (1) the type-I ampliation lemma (B(K)(x)I)'=I(x)B(H); (2) the
product-state GNS tensor factorization H = H_{<=k}(x)H_{>k}, Omega = Omega_{<=k}
(x)Omega_{>k}; (3) finite-dim cyclicity of Omega_{<=k} for A_{<=k} and of Omega
for A.  Verified on a finite-truncation witness of the load-bearing identity
P_{<=k} z Omega = phi(z) Omega for right-supported (tail-direction) z, together
with the ampliation commutant fact -- both of which are the finite mechanism the
infinite limit argument composes.
"""

from __future__ import annotations
import numpy as np


# =====================================================================
# Finite-truncation witness of the native mechanism
# =====================================================================

def _site_state(lam: float) -> np.ndarray:
    """Per-site Powers/Gibbs density matrix diag(1, lam)/(1+lam), 0<lam<1."""
    return np.array([[1.0 / (1.0 + lam), 0.0], [0.0, lam / (1.0 + lam)]])


def _gns_vector(lam: float) -> np.ndarray:
    """Single-site GNS vector Omega_n = vec(rho^{1/2}) in H_n = M_2 (HS), so
    <Omega_n, x Omega_n> = Tr(rho x).  Column-major vectorization."""
    rh = np.array([[np.sqrt(1.0 / (1.0 + lam)), 0.0],
                   [0.0, np.sqrt(lam / (1.0 + lam))]])
    return rh.reshape(-1, order='F')


def _left_mult(x: np.ndarray) -> np.ndarray:
    """pi(x) = left multiplication on H_n = M_2 (HS): vec(x m) = (I (x) x) vec(m)."""
    return np.kron(np.eye(2), x)


def check_L_itpfi_tail_acts_scalar_on_omega_native():
    """L_itpfi_tail_acts_scalar_on_omega_native: tail elements act as scalars
    on the cyclic vector, natively (no Araki-Woods, no commutation theorem).

    Tier 3 [P].

    STATEMENT.  For the M_2-ITPFI GNS triple (H, pi, Omega) of the forced
    faithful product state phi = (x)phi_n, every tail element
    z in cap_k M_{>=k} satisfies z Omega = phi(z) . Omega.

    PROOF (native, import-free).
      (i)  [ampliation] pi(A_{>=k+1}) acts as I_{<=k} (x) (.) on the product-state
           GNS space, so M_{>=k+1} = pi(A_{>=k+1})'' is contained in the von
           Neumann algebra I_{<=k} (x) B(H_{>k}) (= (B(H_{<=k})(x)I)', the type-I
           ampliation lemma -- NOT the general commutation theorem).  Hence a
           tail element z = I_{<=k} (x) z_{>k} for every k.
      (ii) [product GNS] H = H_{<=k} (x) H_{>k}, Omega = Omega_{<=k} (x) Omega_{>k};
           the Jones projection onto [M_{<=k} Omega] is P_{<=k} = I_{H_{<=k}} (x)
           |Omega_{>k}><Omega_{>k}| (finite-dim cyclicity of Omega_{<=k}).  For a
           tail z, P_{<=k} z Omega = <Omega_{>k}, z_{>k} Omega_{>k}> . Omega
           = phi(z) . Omega.
      (iii)[cyclicity] P_{<=k} -> I strongly (Omega cyclic for A), so
           z Omega = lim_k P_{<=k} z Omega = phi(z) . Omega.    QED

    SCOPE FENCE (the audit's split).  This is the scalar-on-Omega fragment ONLY.
    Upgrading z Omega = phi(z) Omega to z = phi(z).1 (full tail-triviality, hence
    factoriality) requires Omega separating for M, which is NOT native -- it is
    the Araki-Woods modular identification, the same tier as the von Neumann
    tensor commutation theorem.  Full tail-triviality / factoriality / the
    III_lambda TYPE remain [P_structural] (L_algebra_type, interface_factor_native).
    Export flags: Export_scalar_on_omega_native_P = 1;
    Export_tail_trivial_native_P = 0; Export_factoriality_native_P = 0.

    Finite-truncation witness of the load-bearing mechanism (the limit argument
    composes these): the product GNS factorization, P_{<=k} z Omega = phi(z) Omega
    for right-supported z at every cut, and the ampliation commutant fact
    [pi1(x)(x)I, I(x)Y] = 0.
    """
    lam = float(np.exp(-1.0 / np.log(102.0)))  # forced datum lambda = e^{-beta_phys}, in (0,1)
    assert 0.0 < lam < 1.0

    rho = _site_state(lam)
    Om1 = _gns_vector(lam)
    G1 = None  # GNS inner product is the standard HS inner product for Omega=rho^{1/2}

    def phi1(x):
        return float(np.trace(rho @ x).real)

    # --- (ii) load-bearing identity P_{<=k} z Omega = phi(z) Omega, 2-site model ---
    # Sites: left = site 1 (cut), right = site 2 (tail direction).
    Om2 = np.kron(Om1, Om1)
    # right-side cyclic projector P2 = |Omega_2><Omega_2| in the HS metric (Omega_2 unit norm)
    Om1n = Om1 / np.linalg.norm(Om1)
    P2 = np.outer(Om1n, Om1n.conj())
    assert np.allclose(P2 @ P2, P2, atol=1e-10), "P2 idempotent"
    P_le1 = np.kron(np.eye(4), P2)  # I_{H1} (x) |Omega_2><Omega_2|

    max_gap = 0.0
    for z2 in [np.diag([1.0, 0.0]), np.array([[0.0, 1.0], [0.0, 0.0]]),
               np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[2.0, 1.0], [1.0, 3.0]])]:
        z = np.kron(np.eye(4), _left_mult(z2))     # right-supported: I_{H1} (x) pi(z2)
        zOm = z @ Om2
        lhs = P_le1 @ zOm                           # P_{<=1} z Omega
        rhs = phi1(z2) * Om2                         # phi(z) . Omega  (phi(z)=<Omega_2,z2 Omega_2>=Tr(rho z2))
        gap = float(np.linalg.norm(lhs - rhs))
        max_gap = max(max_gap, gap)
    assert max_gap < 1e-10, f"P_<=k z Omega = phi(z) Omega failed, gap {max_gap}"

    # --- (i) ampliation commutant fact: [pi1(x)(x)I, I(x)Y] = 0 (the ONLY commutant input) ---
    rng = np.random.RandomState(0)
    amp_max = 0.0
    for _ in range(20):
        x = rng.randn(2, 2)
        Yr = np.kron(np.eye(4), rng.randn(4, 4))    # I_{H1} (x) (any op on H2)
        L = np.kron(_left_mult(x), np.eye(4))       # pi1(x) (x) I
        amp_max = max(amp_max, float(np.linalg.norm(L @ Yr - Yr @ L)))
    assert amp_max < 1e-9, f"ampliation [pi1(x)(x)I, I(x)Y]=0 failed, {amp_max}"

    return {
        "name": "L_itpfi_tail_acts_scalar_on_omega_native",
        "passed": True,
        "tier": 3,
        "epistemic": "[P]",
        "key_result": (
            f"M_2-ITPFI tail elements act as scalars on Omega NATIVELY: "
            f"z Omega = phi(z).Omega via ampliation + product-GNS factorization + cyclicity "
            f"(no separating, no modular, no commutation theorem). Witness (lambda={lam:.6f}): "
            f"P_<=k z Omega = phi(z) Omega to {max_gap:.1e}; ampliation commutant to {amp_max:.1e}."
        ),
        "summary": (
            "Native scalar-on-Omega lemma -- the import-free core of tail-triviality. "
            "Steps (i)-(iii) (ampliation lemma (B(K)(x)I)'=I(x)B(H); product-state GNS "
            "factorization; cyclicity) prove z Omega = phi(z).Omega for every tail element, "
            "with NO Araki-Woods modular structure and NO commutation theorem. SCOPE FENCE: "
            "the upgrade to z=phi(z).1 (full tail-triviality / factoriality) needs Omega "
            "separating for M = the Araki-Woods modular identification (same tier as the "
            "commutation theorem; 'faithful C*-state => separating weak-closure vector' is "
            "FALSE in general), so full tail-triviality / III_lambda TYPE stay [P_structural] "
            "(L_algebra_type, interface_factor_native). Isolated by a dedicated pre-bank cold "
            "audit, 2026-06-22."
        ),
        "dependencies": ["L_TN_product_state", "L_algebra_type"],
        "export_flags": {
            "Export_scalar_on_omega_native_P": 1,
            "Export_tail_trivial_native_P": 0,
            "Export_factoriality_native_P": 0,
        },
    }


# =====================================================================
# Bank registration
# =====================================================================

CHECKS = {
    "L_itpfi_tail_acts_scalar_on_omega_native": check_L_itpfi_tail_acts_scalar_on_omega_native,
}


def register(registry):
    registry.update(CHECKS)


def run_all():
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    r = check_L_itpfi_tail_acts_scalar_on_omega_native()
    print("PASS" if r["passed"] else "FAIL", r["name"])
    print("  ->", r["key_result"])

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "foundation:itpfi_tail_scalar_on_omega",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "One bank check, check_L_itpfi_tail_acts_scalar_on_omega_native, tier "
            "3 at epistemic '[P]': the import-free native fragment of tail- "
            "triviality for the M_2-ITPFI interface algebra -- every tail element "
            "z in cap_k M_{>=k} acts as a scalar on the cyclic vector, z Omega = "
            "phi(z) Omega, proved from native inputs only (type-I ampliation "
            "lemma, product-state GNS tensor factorization, finite-dim "
            "cyclicity), with NO separating-ness, NO modular structure, and NO "
            "tensor commutation theorem. Verified on a finite-truncation witness "
            "of the load-bearing identity P_{<=k} z Omega = phi(z) Omega plus the "
            "ampliation commutant fact. The module's scope fence is explicit and "
            "load-bearing: it does NOT bank full tail-triviality or factoriality "
            "-- the step-(iv) upgrade 'Omega separating for M' is proven non- "
            "native in-module (the general implication faithful-C*-state => "
            "separating GNS vector for the weak closure is FALSE, counterexample "
            "A = C.1 + K(H)), and that upgrade lives at the same tier as the "
            "Araki-Woods import. Factoriality itself is exported downstream by "
            "interface_factor_native (natively, via the corner argument), not by "
            "this module. "
        ),
        "note": "Wave 7; native-fragment-only lemma, non-native step (iv) explicitly fenced in-module",
    },
)
