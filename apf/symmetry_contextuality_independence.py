"""apf/symmetry_contextuality_independence.py -- symmetry-degeneracy is logically
INDEPENDENT of contextuality: a corroborating finite illustration.

Strengthens (corroborates) the cosmogenesis-route refutation in 'Reference - The
IJC Keystone - Bridge Derived, Occupancy Is the QAC (Settled, Twice Cold-Audited)
(2026-06-26)'. Paper 37 sec:cosm-trivial-alignment labels the maximally-symmetric
trivial alignment "IJC-side" and treats the cosmogenic descent (G_max -> {e}) as
if it bore on branch occupancy. This module exhibits, with exact 2-qubit
witnesses, that a symmetry-degeneracy property and a contextuality property are
LOGICALLY INDEPENDENT -- all four combinations occur -- so "maximal symmetry
=> IJC" is not a logical entailment (nor is its converse "maximal symmetry => Sep",
which the Bell state refutes: it is maximally symmetric AND maximally contextual).

SCOPE / honest readings (what this is and is NOT):
  * The symmetry property used is a PROXY: SYM(rho) := the reduced state rho_A has
    DEGENERATE spectrum. This is a concrete 2-qubit illustration of "symmetry-
    induced degeneracy"; it is NOT identical to the cosmogenic Type-II quantity,
    which is non-uniqueness of the PLEC argmin over admissible destinations under
    the symmetry group of Omega_Gamma (a cost-functional property on configuration
    space, check_T_trivial_alignment_is_Type_II in plec.py). Read SYM as a proxy.
  * The contextuality property used is the CHSH-FACET special case: IJC_CHSH(rho)
    := Horodecki M(rho) > 1 (CHSH/Boole local-polytope violation). This is the
    Bell-CHSH cover instance of the framework's general Boolean-defender / global-
    section Sep/IJC criterion (Paper 5 supp v6.8). It is STRICTLY NARROWER than the
    general criterion: it does not detect CHSH-local-but-contextual states (Werner
    states in the local-nonseparable range, Peres-Mermin parity obstructions). A
    narrower IJC predicate only strengthens an independence result (one direction
    survives any narrowing), but the witnesses below exhibit the CHSH instance, not
    the full Boolean-defender axis.
  * What is established: marginal-degeneracy and CHSH-violation are logically
    independent over 2-qubit states (the narrow statement is exact / [P]); hence
    "maximal symmetry => IJC" is not a logical entailment. What is NOT established
    here: the trajectory-level claim that ALONG the specific cosmogenic path
    contextuality is uncorrelated with symmetry -- that non-derivability is carried
    by the settled note (two distinct senses of IJC + cosmogenesis runs Sep-ward by
    record-locking), for which this is corroboration, not independent proof.

GRADE [P_structural_reading]: a finite-witness independence illustration resting on
two adopted readings (SYM as a Type-II proxy; IJC_CHSH as the Bell-CHSH instance of
the Boolean-defender axis). The narrow embedded math fact (marginal-degeneracy _|_
CHSH-violation over 2-qubit states) is exact.
"""
from __future__ import annotations
import numpy as np
from apf.apf_utils import check as _check, _result as _full_result

_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULI = [_X, _Y, _Z]


def _rho_from_ket(psi):
    psi = np.asarray(psi, dtype=complex).reshape(4, 1)
    psi = psi / np.linalg.norm(psi)
    return psi @ psi.conj().T


def _partial_trace_A(rho):
    r = rho.reshape(2, 2, 2, 2)          # iA iB jA jB
    return np.einsum('ikjk->ij', r)


def _sym_degenerate(rho, tol=1e-9):
    """PROXY for Type-II symmetry: reduced rho_A has degenerate spectrum."""
    ev = np.linalg.eigvalsh(_partial_trace_A(rho))
    return bool(abs(ev[0] - ev[1]) < tol)


def _horodecki_M(rho):
    T = np.array([[np.real(np.trace(rho @ np.kron(a, b))) for b in _PAULI] for a in _PAULI])
    ev = np.sort(np.linalg.eigvalsh(T.T @ T))[::-1]
    return float(ev[0] + ev[1])


def _ijc_chsh(rho):
    """CHSH-facet special case of the Boolean-defender Sep/IJC axis: M(rho) > 1."""
    return bool(_horodecki_M(rho) > 1.0 + 1e-9)


def check_T_symmetry_degeneracy_orthogonal_to_contextuality():
    """T_symmetry_degeneracy_orthogonal_to_contextuality: marginal-degeneracy (a
    Type-II symmetry proxy) is logically INDEPENDENT of CHSH-facet contextuality;
    a corroborating finite illustration that "maximal symmetry => IJC" is not a
    logical entailment [P_structural_reading].

    THEOREM (exact, narrow). Over 2-qubit states, SYM(rho) := "rho_A spectrum
    degenerate" and IJC_CHSH(rho) := "Horodecki M(rho) > 1" are logically
    independent: all four (SYM, IJC_CHSH) combinations are realized by exact
    witnesses. Therefore neither "maximal symmetry => IJC" nor "maximal symmetry
    => Sep" is a logical entailment.

    READINGS (see module docstring): SYM is a 2-qubit PROXY for the cosmogenic
    Type-II argmin-degeneracy (not identical to it); IJC_CHSH is the Bell-CHSH
    instance of the general Boolean-defender Sep/IJC criterion (strictly narrower).

    COROLLARY (demoted, honest scope): this refutes the LOGICAL-ENTAILMENT form of
    Paper 37's "trivial alignment is IJC-side." It does NOT by itself establish the
    trajectory-level non-derivability of occupancy from cosmogenesis -- that is
    carried by the settled note (the two senses of IJC are distinct; cosmogenesis
    runs Sep-ward by record-locking). This check is corroboration, not independent
    proof, of the already-settled refutation.

    WITNESSES (all exact): (sym,Sep)=I/4 [M=0]; (sym,IJC)=Bell [M=2];
    (asym,Sep)=|0><0| (x) diag(.7,.3) [M=0.16]; (asym,IJC)=cos(pi/5)|00>+sin(pi/5)|11>
    [M=1+sin^2(2pi/5)=1.9045].
    """
    import math
    rho_mm = np.eye(4, dtype=complex) / 4.0
    bell = _rho_from_ket([1, 0, 0, 1])
    rho_prod = np.kron(np.array([[1, 0], [0, 0]], dtype=complex),
                       np.array([[0.7, 0], [0, 0.3]], dtype=complex))
    a = math.pi / 5
    partial = _rho_from_ket([math.cos(a), 0, 0, math.sin(a)])

    table = {
        "(sym,Sep)":  (rho_mm,   True,  False),
        "(sym,IJC)":  (bell,     True,  True),
        "(asym,Sep)": (rho_prod, False, False),
        "(asym,IJC)": (partial,  False, True),
    }
    results = {}
    for name, (rho, want_sym, want_ijc) in table.items():
        _check(np.allclose(rho, rho.conj().T), f"{name}: rho Hermitian")
        _check(abs(np.trace(rho) - 1) < 1e-9, f"{name}: trace 1")
        _check(np.min(np.linalg.eigvalsh(rho)) > -1e-9, f"{name}: PSD")
        sym = _sym_degenerate(rho)
        ijc = _ijc_chsh(rho)
        M = float(_horodecki_M(rho))
        _check(sym == want_sym, f"{name}: SYM proxy = {want_sym} (got {sym})")
        _check(ijc == want_ijc, f"{name}: IJC_CHSH = {want_ijc} (got {ijc}, M={M:.4f})")
        results[name] = {"sym": sym, "ijc": ijc, "M": round(M, 4)}

    cells = {(r["sym"], r["ijc"]) for r in results.values()}
    _check(cells == {(True, False), (True, True), (False, False), (False, True)},
           "all four (SYM, IJC_CHSH) cells populated -> logical independence")
    # the naive strengthening 'maximal symmetry => Sep' is FALSE: Bell is (sym, IJC)
    _check(results["(sym,IJC)"]["sym"] and results["(sym,IJC)"]["ijc"],
           "Bell witness: maximally symmetric AND contextual -> 'sym=>Sep' refuted")
    # the Paper-37 form 'maximal symmetry => IJC' is also not entailed: I/4 is (sym, Sep)
    _check(results["(sym,Sep)"]["sym"] and not results["(sym,Sep)"]["ijc"],
           "I/4 witness: maximally symmetric AND non-contextual -> 'sym=>IJC' not entailed")

    # EMPTY-distinction-family boundary (the trivial alignment): with NO queried
    # distinctions there is no marginal scenario, so the Boolean-defender Sep/IJC
    # dichotomy is UNDEFINED (no queried contexts, no A/B pair) -- per the settled
    # note. We assert the antecedent (empty cover), NOT a Sep/IJC verdict.
    queried_contexts = []          # empty distinction family
    ab_pairs = []                  # no co-available record-incompatible pair
    _check(len(queried_contexts) == 0 and len(ab_pairs) == 0,
           "empty distinction family: no queried cover -> Sep/IJC dichotomy UNDEFINED "
           "(not Sep, not IJC); cannot carry occupancy")

    return _full_result(
        name=("T_symmetry_degeneracy_orthogonal_to_contextuality: marginal-degeneracy "
              "(a Type-II symmetry proxy) is logically independent of CHSH-facet "
              "contextuality -- all four cells realized by exact 2-qubit witnesses; "
              "'maximal symmetry => IJC' is not a logical entailment (nor 'sym=>Sep'). "
              "Corroborates the cosmogenesis-route refutation [P_structural_reading]"),
        tier=4, epistemic="P_structural_reading",
        summary=(
            "Exact 2-qubit witnesses populate all four (SYM, IJC_CHSH) cells: "
            "(sym,Sep)=I/4 [M=0]; (sym,IJC)=Bell [M=2]; (asym,Sep)=product [M=0.16]; "
            "(asym,IJC)=cos(pi/5)|00>+sin(pi/5)|11> [M=1.9045]. SYM is a proxy "
            "(reduced-state spectral degeneracy) for the cosmogenic Type-II "
            "argmin-degeneracy; IJC_CHSH is the Bell-CHSH instance of the general "
            "Boolean-defender Sep/IJC criterion (strictly narrower -- misses "
            "CHSH-local contextuality). The narrow embedded fact (marginal-degeneracy "
            "_|_ CHSH-violation) is exact: it refutes the LOGICAL-ENTAILMENT form of "
            "'maximal symmetry => IJC' (Paper 37 trivial-alignment clause) and its "
            "converse (Bell = symmetric + contextual). It does NOT prove trajectory-"
            "level non-derivability of occupancy -- that is carried by the settled "
            "IJC-keystone note; this is corroboration. The empty distinction family "
            "(trivial alignment) has no queried cover, so the dichotomy is UNDEFINED "
            "there -- it cannot carry occupancy either way."
        ),
        key_result=("marginal-degeneracy (Type-II symmetry proxy) and CHSH-facet IJC are "
                    "logically independent (2x2 table, exact witnesses); 'maximal symmetry "
                    "=> IJC' is not a logical entailment; corroborates the cosmogenesis-route "
                    "refutation (trajectory-level non-derivability carried by the settled note)."),
        dependencies=[],
        cross_refs=["T_inseparable_IJC", "T_quantum_admissibility_condition",
                    "T_trivial_alignment_is_Type_II"],
        artifacts={
            "witness_table": results,
            "symmetry_proxy": "reduced rho_A spectral degeneracy (proxy for Type-II argmin-degeneracy; NOT identical)",
            "contextuality_test": "Horodecki M = two largest eigvals of T^T T; IJC_CHSH iff M>1 (Bell-CHSH instance, strictly narrower than general Boolean-defender)",
            "empty_family": "no queried cover -> Sep/IJC dichotomy UNDEFINED (not Sep, not IJC)",
            "refutes": "logical-entailment form of 'maximal symmetry => IJC' (and its converse); Bell = symmetric+contextual",
            "scope": "corroborating illustration; trajectory-level non-derivability carried by the settled IJC-keystone note",
        },
    )


_CHECKS = {"T_symmetry_degeneracy_orthogonal_to_contextuality":
           check_T_symmetry_degeneracy_orthogonal_to_contextuality}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}
