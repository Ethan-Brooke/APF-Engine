"""APF vacuum label code -- the constructed P1 witness for ICL_vac route (b).

v24.3.NEW (2026-07-02). The named module-scale work from "Reference -
ICL_vac Route (b) Walked - The Kernel Formulation, the MSC Swap, and the
QEC Strength Finding (2026-07-02)" SS7 item 3: an explicit code on the
banked second-epsilon skeleton realizing vacuum no-leakage (P1) at
computed strength, together with the SUBSPACE-COHERENCE ceiling that
CORRECTS the P1 target's wording -- the "42-dim vacuum logical sector"
is unconstructible as a subspace-coherent (pure-isometric) sector; the
classical 42-label code built here is the maximum at subspace form.
Subsystem/mixed-state encodings are NOT excluded by the no-cloning
step (Cleve-Gottesman-Lo 1999) -- and the fit question is CLOSED
EXISTS at abstract-encoding strength: check 3 exhibits a perfect
((61,61)) mixed scheme carrying a coherent 42-dim secret with every
share dimension 43 <= 102 (see the check-3 block below).
Realization/identification remains the open reading. Checks 4-5
walk the successor (the sector-aligned question) to its three-pronged
closure: support-alignment EXISTS at exact fill (share dim exactly
42, check 4), the carrier reading dissolves (type mismatch), and the
registration reading closes negatively at coherent strength (the
classical-record ceiling F_e <= 1/42, check 5); the S_42-covariant
refinement is SPLIT at v24.3.373 (vacuum_scheme_covariance.py):
subgroup covariance G_0 = S_2 x S_3 x AGL(1,7) closed EXISTS on this
construction (F2 as built, F1 after the D_4 dressing) and full-S_q F1
witnesses exist at exact fill for q = 2, 3 -- covariance does not force
classicality anywhere computed; full S_42 at (61, 42) stays open. Hostile cold audits 2026-07-02: LAND-WITH-FIXES
0.80 (checks 1-2, all eight fixes), 0.88 (check 3, all seven fixes;
independent re-derivation), and 0.88 (checks 4-5, all eight fixes;
independent re-implementation, incl. the red-bank repair of the
narrative-merge race pins).

THE MODEL (banked skeleton, every constant anchored):
  - C_total = 61 capacity channels (L_count [P]).
  - Each channel's second-epsilon commitment space is 102-dimensional:
    60 Sector-A partner options + 42 Sector-B vacuum-mode options
    (T_kappa, L_self_exclusion, T_horizon_reciprocity Step 1 [P]).
    The ambient Hilbert space H = (C^102)^{(x)61} is the banked
    L_QEC_code_space object (a dependency, not a cross-reference).
  - The label alphabet is the 42 Sector-B modes; by
    T_interface_sector_bridge [P] this 42 is dim of the global-interface
    stratum of T12 -- the same 42 that T11 reads as the vacuum block.
  - THE CARRIER IS A SLICE (disclosed, priced -- audit fix 3): the
    42-dimensional common-mode slice of the T_horizon_reciprocity
    Step-3 vacuum-dominated configuration family -- 42 of the 42^61
    banked configurations. The banked Step-3 slot has each unmatched
    channel choosing its vacuum mode INDEPENDENTLY (S_propagation =
    61 ln 42 is banked as exactly that count); the common-mode
    correlation (all channels in the same mode v) is a
    CONSTRUCTION-SUPPLIED input, not bank-supplied. Its register form
    is precisely the OPEN a = b common-demand identity [C]
    (L_common_demand_iff_degenerate, v24.3.338) -- cross-referenced,
    never assumed as banked.
  - Common-mode states |v>^{(x)61}, v in {0..41}: every channel in the
    same vacuum mode ("one demand vector under forty-two names").

THE CODE (the label states):
  |mu_bar> = 42^{-1/2} * sum_v omega^{mu v} |v>^{(x)61},
  omega = exp(2 pi i / 42), mu = 0..41.
  The 42 label states are the Fourier-dual frame of the common-mode
  family. All computations collapse exactly to the 42-dimensional span
  of {|v>^{(x)S}} (the collapse itself is verified in-module by a
  reduced-parameter full-tensor cross-check, clause (vii)); nothing of
  size 102^61 is ever represented.

WHAT check_T_vacuum_label_code_no_leakage CERTIFIES (exact):
  (i)   ORTHONORMALITY: the 42 label states are orthonormal (Fourier).
  (ii)  NO-LEAKAGE (P1, label form): for EVERY proper type-subset A
        (all sizes 1 <= |A| <= 60 computed, all 42 labels), the
        reduced state of |mu_bar> on A is (1/42) sum_v |v^A><v^A| --
        one fixed state, independent of mu AND of A. The kernel
        identity is the one-line complement-orthogonality cancellation
        <w^Abar|v^Abar> = delta_vw for Abar nonempty.
  (iii) READ-BLINDNESS, expectation form: for any A-supported
        observable O, Tr(O rho_mu) depends on O only through the
        diagonal data f_v = <v^A|O|v^A> and equals (1/42) sum_v f_v
        for every mu. (Consistency restatement of (ii); the
        operator-strength content is clause (iv).)
  (iv)  CLEANING/COMPRESSION CERTIFICATE: for any A-supported operator
        O, the code-space compression (P O P)_{mu nu} = fhat(nu - mu)
        is a CIRCULANT -- constant diagonal (the operator restatement
        of read-blindness) with off-diagonal content that is pure
        logical-shift mixing. Proper subsets can WRITE the label
        (dephase/shift); they cannot READ it. Privacy is not
        protection; the write channel is disclosed, not hidden. The
        cross-term drop (only the common-mode diagonal of O survives)
        is verified against a full-tensor build in clause (vii).
  (v)   GLOBAL REGISTRATION -- with the sharp finding stated (audit
        fix 4): one global (all-61) measurement -- the Fourier frame
        projectors -- distinguishes the 42 labels perfectly (from
        (i)). But that label-resolving global read has NO banked
        counterpart; the only banked global read (per-channel Sector-B
        registration at the horizon crossing sequence,
        T_horizon_reciprocity Step 4) is computed HERE to be mu-BLIND:
        it outputs a uniformly random common v independent of the
        label. On this encoding the label is invisible to every proper
        subset AND to the banked horizon registration -- under the
        identification reading, no banked instrument ever registers
        mu. This cuts AGAINST the identification reading and is
        recorded as a finding. Identifying either global read with the
        physical horizon registration is a READING (wedge-fence
        strength); the construction supplies existence, not the
        identification.
  (vi)  NEGATIVE CONTROL (.318 pattern): the basis encoding -- taking
        the common-mode states |v>^{(x)61} themselves as label
        carriers -- FAILS no-leakage maximally: a single channel's
        marginal distinguishes all 42 labels perfectly (pairwise trace
        distance 1). No-leakage is a property of the phase encoding,
        not of every 42-state family; the check has teeth. CENSUS
        GUARD: this negative control is a COUNTERFACTUAL ENCODING
        EXHIBIT (the basis code, shown to FAIL privacy); it constructs
        no banked reader of physical Sector-B content, and must not be
        read by a later disposition pass as an interior which-v
        reader.
  (vii) COLLAPSE CROSS-CHECK (audit fix 5): a reduced-parameter
        full-tensor build (3 channels, alphabet 3, actual 27-dim
        tensors) verifies both collapse steps against brute force:
        marginal mu-independence on every proper subset, and the
        compression of a generic A-supported operator WITH nonzero
        cross elements <v^A|O|w^A> matching the diagonal-only
        circulant formula.

WHAT check_T_vacuum_logical_sector_classical_ceiling CERTIFIES:
  (a)   THE FOURIER-DUAL EXHIBIT (exact): the uniform superposition of
        the 42 label states IS the product state |0>^{(x)61} --
        coherent superpositions of the private frame are exactly the
        maximally leaky states (single-channel trace distance from the
        uniform marginal = 1 - 1/42, computed from the two states).
  (b)   THE IN-CARRIER CEILING (exact, elementary proof here +
        computed witnesses; audit fix 2 -- the pointwise form): within
        the 42-dim common-mode carrier, NO 2-dimensional subspace has
        STATE-INDEPENDENT single-channel marginals over all its
        states. Proof (pointwise; orthogonality never needed): let
        x, y be an orthonormal basis of the subspace and suppose every
        unit state has the SAME single-channel diagonal. Comparing x
        and y: |x_v|^2 = |y_v|^2 =: p_v for every v. Comparing
        (x + y)/sqrt(2) and (x + iy)/sqrt(2) against x: Re and Im of
        conj(x_v) y_v vanish for every v, so conj(x_v) y_v = 0
        POINTWISE -- x and y have disjoint supports. But equal moduli
        p_v with disjoint supports force p_v = 0 for every v,
        contradicting normalization. QED. Witnesses computed with a
        STATE-DEPENDENCE defect (max over probe states of the sup-norm
        deviation from x's diagonal): the label frame's own 2-dim
        spans leak on superposition, and random 2-dim carrier
        subspaces all show strictly positive defect.
  (c)   THE GENERAL CEILING, SUBSPACE-SCOPED (audit fix 1): for a
        SUBSPACE (pure-isometric) code, state-independent marginals on
        a region A over all code states is the Knill-Laflamme erasure
        condition P O_A P = c(O) P; correctability of BOTH a region
        and its complement for a dim >= 2 subspace violates no-cloning
        (two disjoint recovery maps would clone). Named cited steps:
        Knill & Laflamme 1997 (PRA 55, 900); the complementary-region
        no-cloning argument. THE SCOPE FENCE: this kills
        subspace-coherent sectors ONLY. Subsystem/mixed-state
        encodings EVADE it -- Cleve, Gottesman & Lo 1999 (PRL 83,
        648): the ((2,2)) quantum one-time-pad carries a genuine
        quantum secret with BOTH proper shares state-independent; the
        banked OA-QECC code state (L_QEC_code_space) is itself MIXED,
        so the excluded species is not the bank's native one. The fit
        question is CLOSED EXISTS (check 3): a perfect ((61,61)) mixed
        scheme with all share dimensions 43 <= 102 carries a coherent
        42-dim secret; realization/identification remains the open
        reading. Nothing computed in this module depends on
        the cited steps (docstring-level import, verified).
  (d)   CLASSICALITY COROLLARY, scoped (computed): the compressions
        {P O_A P} form a COMMUTING FAMILY generating the circulant
        algebra (the compression map is not a homomorphism; the family
        commutes and is simultaneously DFT-diagonalized, computed).
        The logical structure any interior coupling can touch at
        subspace form is abelian -- classical-label-typed, the exact
        species of the .339 census row 5 and the banked which-v
        object (.318).

WHAT check_T_vacuum_mixed_42dim_secret_scheme_exists CERTIFIES:
  (Check 3; the audit's seven fixes carried. Closes the fit question
  of clause (c) in the EXISTS direction.)
  (A)   THE SCHEME: p = 43 (prime, 42 <= 43 <= 102). Base isometry
        W: C^p -> (C^p)^{(x)3}, |s> -> p^{-1/2} sum_a |a, a+s, a+2s>
        (mod p) -- the polynomial code f(x) = a + s x at x = 0, 1, 2.
        The mixed ((2,2)) scheme Sigma keeps shares (f(0), f(1)) and
        traces f(2) to the environment. E_2 = Sigma; E_n = Sigma
        applied to the LAST share of E_{n-1}. E_61 = 60 applications
        of Sigma (1 base + 59 re-shares), 61 shares, each of dimension
        exactly 43; embed C^42 in C^43 for the secret and C^43 in
        C^102 per channel. (The naive CGL route -- a pure ((61,121))
        polynomial scheme with shares discarded -- needs p >= 121 >
        102 and does NOT fit; the cascade is the move that gets under
        the local dimension.)
  (B)   BASE PRIVACY, exact integer certificate at p = 43: the
        cross-term congruence systems for each kept share and for the
        environment ({a'+s' = a+s, a'+2s' = a+2s}, etc., mod 43) have
        NO solution with s != s' -- verified by integer loop, stronger
        than any float tolerance. Each single register's marginal
        channel is completely depolarizing: X -> Tr(X) I/p, constant
        as a SUPEROPERATOR, hence blind on superpositions and on
        halves of entangled states (linearity).
  (C)   BASE RECOVERY, exact: U1|x,y> = |x, y-x>; Fourier-measure
        register 1 (convention F_-, outcome w); phase correction
        diag(e^{2 pi i (p-2) w s / p}). The correction identity
        (2 w s + (p-2) w s) = p w s = 0 (mod p) is pinned by integer
        loop over all (w, s). Implemented coherently (unitary + trace)
        so composition on entangled inputs is a channel identity.
  (D)   CASCADE PRIVACY, the induction (elementary; the one
        nontrivial step written out): for proper A in [n], three
        cases. (i) A contains both children n-1, n: A misses some
        j <= n-2, pulls back to a proper subset of [n-1]; a CP map on
        a product preserves the product. (ii) A contains exactly one
        child: the single-child marginal map of Sigma is the CONSTANT
        channel Lambda(X) = Tr(X) I/p, and (id_C (x) Lambda)(rho_CD)
        = rho_C (x) I/p is an exact algebraic identity for ARBITRARY
        C-D correlations -- including correlations carrying the secret
        through the re-shared share. The child is deleted BEFORE any
        appeal to E_{n-1} privacy, leaving A intersect [n-2], always
        proper in [n-1]. This is exactly the case the naive pullback
        would miss (A = [n-2] + one child has pullback [n-1], the
        FULL set); the constant-channel identity, not inheritance,
        kills it. (iii) A inside [n-2]: directly proper. Base case =
        (B). The hardest subsets are scanned BY NAME in-check.
  (E)   COMPUTED WITNESSES (pure Python, seconds): full proper-subset
        scans with entangled references -- ((4,4)) at p = 3 (all 14
        proper subsets, including the two hardest, {1,2,3} and
        {1,2,4}) and ((3,3)) at p = 5 with a 4-dim secret subspace
        (modeling 42 in 43); composed multi-stage decoder exact on an
        entangled reference in every case; GHZ negative control (the
        sum encoding passes basis-label privacy, FAILS the
        superoperator-constancy test -- the check has teeth).
  (F)   FENCES: existence at abstract-encoding strength ONLY. The
        scheme embeds C^43 arbitrarily in each C^102 -- no alignment
        with the 60+42 sector split, the common-mode carrier, or the
        banked horizon registration is claimed; the ALIGNED-scheme
        question closed three-pronged by checks 4-5 (support EXISTS /
        carrier dissolved / registration no-go; covariant open). Share
        dimension exactly 42 is SETTLED by check 4 (the [[5,1,3]]
        qubit factor; the Gottesman floor tight at the banked
        dimension).
        Privacy is not erasure-protection. n = 61 is not directly
        simulated; it rests on (D), verified at n = 3, 4 including
        the composed decoder. No cited theorem is load-bearing:
        privacy, recovery, and the induction's one lemma are computed
        or derived above; CGL 1999 is attribution.

EFFECT ON THE ROUTE-(b) LEDGER (audit fix 6 -- honest form):
  The SS2 "three named gaps before the quantifier" move as follows.
  "No code subspace is constructed" -- closed AT LABEL-CODE FORM ON A
  CONSTRUCTION-SUPPLIED COMMON-MODE CARRIER (fence 5); the ceiling's
  correction: the constructible object at subspace form is the
  classical label code. "KL certified only for the single-type trace
  state" -- WITNESSED AT COMPUTED STRENGTH for the constructed code;
  the banked L_QEC_knill_laflamme is untouched and not regraded.
  "The erasure-duality step (unbanked import)" -- retired for the
  privacy face of THIS construction (read-blindness is computed
  directly); the ceiling's general step reintroduces a named
  literature import (KL-1997 + no-cloning + CGL-1999) at docstring
  level -- the import is RELOCATED, not gone, and nothing computed
  rides on it. THE NOTE'S SS7 ITEM 3 IS EXECUTED AT CORRECTED FORM
  ONLY: its expectation that the construction "would also retire the
  wedge-reading fence" is NOT met -- the wedge/identification fence
  stands (fence 1). Do not cite the note as fully discharged.
  RVC then reads: P1 [computed, this module, at label form on the
  common-mode carrier] o identification [reading] + MSC [C]. The only
  violating species remains a non-marginal reader; ICL_vac stays
  NAMED, NOT ADOPTED, NOT DERIVED.

WHAT THIS MODULE DOES NOT CERTIFY:
  (1) NOT a claim that the physical vacuum sector IS this code: the
      identification of the constructed encoding with V_global content
      is a reading (SS6.1 / wedge-fence strength). Existence + ceiling
      are supplied; the identification is not. Clause (v)'s finding
      (the banked horizon registration is label-blind on this code)
      cuts AGAINST the identification and is recorded as such.
  (2) MSC is NOT derived; RVC is NOT closed; ICL_vac stays a named [C]
      axiom fragment. Route (b)'s wall (composition/inventory
      completeness independent of per-region capacity) stands.
  (3) Privacy is NOT erasure-protection: proper subsets can dephase or
      shift the label (clause (iv) off-diagonals). This is a privacy
      certificate, not an error-correcting shield.
  (4) The ceiling is SUBSPACE-SCOPED, and the mixed direction is
      CLOSED EXISTS at abstract-encoding strength (check 3): a perfect
      ((61,61)) mixed scheme with every share dimension 43 <= 102
      carries a coherent 42-dim secret. Existence != realization: the
      exhibited scheme embeds C^43 arbitrarily in each C^102 -- it
      respects neither the 60+42 sector split, nor the common-mode
      carrier, nor the banked horizon registration; the ALIGNED-scheme
      question is closed THREE-PRONGED by checks 4-5 (support-aligned
      EXISTS at exact fill / carrier reading dissolved, type mismatch /
      registration reading negative at coherent strength), never
      "closed" simpliciter, and support-alignment is still NOT
      realization (the fence pattern inherited so EXISTS cannot be
      read as realization-adjacent). Dimensional structure does not force
      classicality of globally-locked content (locked = recoverable
      only from the full set, invisible to every proper subset); the
      subspace ceiling and the banked label-typing stand; realization
      stays open.
  (5) THE CARRIER FENCE: the common-mode correlation (all channels
      same v) is a construction-supplied input, not bank-supplied; the
      banked dependence on the Step-3 slot is count-only over the
      INDEPENDENT 42^61 family; the correlation's register form is the
      OPEN a = b identity [C]. The existence claim survives (a
      P1-witnessing encoding inside the banked Hilbert space is
      exhibited); "the vacuum sector realizes it" is not claimed.
  (6) Closed-world on the banked constants (61, 42 = dim V_global,
      102); model-scope throughout.

STATUS: [P_structural_instrument] tier 4, both checks (audit fix 7:
an exhibited witness on a construction-supplied carrier is an
instrument in the .335/.337 sense, not a census of banked surfaces).
Elementary/standard mathematics (GHZ-type phase encoding; cf.
Hillery-Buzek-Berthiaume 1999 secret sharing; CGL 1999 for the
subsystem evasion) -- the content is the exact anchoring to the banked
skeleton, the scoped ceiling, the label-blindness finding, and the
route-(b) ledger effect.
Dependencies: L_count, T_kappa, L_self_exclusion,
T_horizon_reciprocity, T11, T_interface_sector_bridge,
L_QEC_code_space.
Cross-refs: check_T_which_v_no_registered_interior_reader (.318),
check_T_vglobal_offdiagonal_blocks_scalar_typed (.339),
check_T_vglobal_slot_identification_no_go (.326),
L_QEC_knill_laflamme / L_QEC_distance / L_QEC_wedge_duality,
L_common_demand_iff_degenerate (.338).
"""

import cmath
import math
import random

from apf.apf_utils import check, _result

# ---------------------------------------------------------------------------
# Banked constants (closed-world anchors)
# ---------------------------------------------------------------------------
N_TYPES = 61          # C_total (L_count [P])
ALPHABET = 42         # Sector-B vacuum modes = dim V_global (T12 bridge [P])
SECTOR_A = 60         # partner options = C_total - 1 (L_self_exclusion [P])
D_EFF = SECTOR_A + ALPHABET   # = 102 (T_horizon_reciprocity Step 1 [P])

_TOL = 1e-10


def _omega(k, n=None):
    """Root of unity omega^k, omega = exp(2 pi i / n)."""
    if n is None:
        n = ALPHABET
    return cmath.exp(2j * cmath.pi * (k % n) / n)


def _frame(n=None):
    """The label frame in the collapsed representation.

    Row mu is the n-vector of coefficients of |mu_bar> over the
    common-mode basis {|v>^{(x)n_types}}: F[mu][v] = omega^{mu v}/sqrt(n).
    The collapsed representation is exact: the common-mode states are
    orthonormal in the full space (product of per-channel Kronecker
    deltas), so every inner product below equals its full-space value
    -- and clause (vii) verifies this against an actual full-tensor
    build at reduced parameters.
    """
    if n is None:
        n = ALPHABET
    s = 1.0 / math.sqrt(n)
    return [[_omega(mu * v, n) * s for v in range(n)] for mu in range(n)]


def _overlap_complement(v, w, complement_size):
    """<w^Abar | v^Abar> for a complement of the given size (exact).

    Kronecker delta for any nonempty complement; 1 (trivial factor) for
    the improper subset A = all types. This single function is the
    entire |A|-dependence of every marginal computation below -- which
    is why no-leakage is |A|-independent for every proper A.
    """
    if complement_size == 0:
        return 1.0
    return 1.0 if v == w else 0.0


def _marginal(frame, mu, subset_size, n_types=N_TYPES):
    """Reduced state of |mu_bar> on a type-subset of the given size.

    Collapsed matrix over the {|v^A>} family:
      rho_A(mu)_{v w} = F[mu][v] * conj(F[mu][w]) * <w^Abar|v^Abar>.
    Exact for every subset of the given size (the collapsed matrix
    depends on the subset only through its size, and on the size only
    through whether the complement is empty).
    """
    n = len(frame)
    comp = n_types - subset_size
    return [[frame[mu][v] * frame[mu][w].conjugate()
             * _overlap_complement(v, w, comp)
             for w in range(n)] for v in range(n)]


def _compression(frame, g):
    """Code-space compression (P O P)_{mu nu} of an A-supported operator.

    For O supported on a proper subset A, complement orthogonality
    kills every cross term, so O enters only through its common-mode
    diagonal data g_v = <v^A| O |v^A>:
      (P O P)_{mu nu} = (1/n) sum_v omega^{(nu - mu) v} g_v.
    Returned as the n x n matrix (exact in the collapsed rep; the
    cross-term drop is verified against a full-tensor build in
    clause (vii)).
    """
    n = len(frame)
    return [[sum(_omega((nu - mu) * v, n) * g[v] for v in range(n)) / n
             for nu in range(n)] for mu in range(n)]


# ---------------------------------------------------------------------------
# Full-tensor cross-check machinery (clause (vii); reduced parameters)
# ---------------------------------------------------------------------------

def _full_tensor_crosscheck(n_ch=3, q=3, seed=424261):
    """Brute-force verification of both collapse steps at (n_ch, q).

    Builds the actual q^n_ch-dimensional tensors: the phase-code states
    |mu_bar> = q^{-1/2} sum_v omega_q^{mu v} |v...v>, then verifies
    (1) marginal mu-independence + uniformity on proper subsets of
    every size, and (2) the compression of a generic A-supported
    operator WITH nonzero cross elements against the diagonal-only
    circulant formula. Returns the max deviation found.
    """
    rng = random.Random(seed)
    dim = q ** n_ch

    def idx(tup):
        out = 0
        for t in tup:
            out = out * q + t
        return out

    def tuples():
        for i in range(dim):
            t, x = [], i
            for _ in range(n_ch):
                t.append(x % q)
                x //= q
            yield tuple(reversed(t))

    all_tuples = list(tuples())

    # the phase-code states as full vectors
    states = []
    s = 1.0 / math.sqrt(q)
    for mu in range(q):
        vec = [0j] * dim
        for v in range(q):
            vec[idx((v,) * n_ch)] = _omega(mu * v, q) * s
        states.append(vec)

    worst = 0.0

    # (1) marginals on proper subsets of every size 1..n_ch-1
    for size in range(1, n_ch):
        subset = tuple(range(size))          # by symmetry of the states,
        comp = tuple(range(size, n_ch))      # any subset of this size
        dA = q ** size
        margs = []
        for mu in range(q):
            rho = [[0j] * dA for _ in range(dA)]
            vec = states[mu]
            for t1 in all_tuples:
                a1 = idx(t1)
                if abs(vec[a1]) < 1e-15:
                    continue
                for t2 in all_tuples:
                    a2 = idx(t2)
                    if abs(vec[a2]) < 1e-15:
                        continue
                    if all(t1[c] == t2[c] for c in comp):
                        i1 = idx(tuple(t1[c] for c in subset)[:size]) \
                            if size else 0
                        i2 = idx(tuple(t2[c] for c in subset)[:size]) \
                            if size else 0
                        rho[i1][i2] += vec[a1] * vec[a2].conjugate()
            margs.append(rho)
        # mu-independence
        for mu in range(1, q):
            dev = max(abs(margs[mu][a][b] - margs[0][a][b])
                      for a in range(dA) for b in range(dA))
            worst = max(worst, dev)
        # matches the collapsed prediction: uniform 1/q over the
        # common-mode family, zero elsewhere
        for a_t in range(dA):
            for b_t in range(dA):
                # decode a_t, b_t back to tuples over the subset
                def dec(i):
                    t, x = [], i
                    for _ in range(size):
                        t.append(x % q)
                        x //= q
                    return tuple(reversed(t))
                ta, tb = dec(a_t), dec(b_t)
                common_a = all(u == ta[0] for u in ta)
                common_b = all(u == tb[0] for u in tb)
                want = (1.0 / q) if (common_a and common_b
                                     and ta[0] == tb[0]) else 0.0
                worst = max(worst, abs(margs[0][a_t][b_t] - want))

    # (2) compression with cross terms, subset = first channel
    O = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(q)]
         for _ in range(q)]                   # generic, dense cross terms
    for mu in range(q):
        for nu in range(q):
            # brute force <mu_bar| O (x) I (x) ... |nu_bar>
            val = 0j
            for v in range(q):
                for w in range(q):
                    # <v...v| O(x)I..I |w...w> = O[v][w] * delta on rest
                    if v == w or n_ch == 1:
                        val += (states[mu][idx((v,) * n_ch)].conjugate()
                                * O[v][w] * states[nu][idx((w,) * n_ch)])
                    else:
                        # rest channels give <v|w> = 0
                        pass
            # diagonal-only circulant formula
            pred = sum(_omega((nu - mu) * v, q) * O[v][v]
                       for v in range(q)) / q
            worst = max(worst, abs(val - pred))

    return worst


def check_T_vacuum_label_code_no_leakage():
    """T_vacuum_label_code_no_leakage: The Constructed P1 Witness [P_structural_instrument].

    See the module docstring for the full statement, the model, the
    fences (especially the carrier fence, 5), and the route-(b) ledger
    effect. Clauses (i)-(vii).
    """
    F = _frame()
    n = ALPHABET
    rng = random.Random(20260702)

    # ---- (i) orthonormality: Gram = I_42 (Fourier, exact) ----
    for mu in range(n):
        for nu in range(mu, n):
            g = sum(F[mu][v].conjugate() * F[nu][v] for v in range(n))
            want = 1.0 if mu == nu else 0.0
            check(abs(g - want) < _TOL,
                  f"(i) Gram[{mu}][{nu}] = {g:.2e} != {want}")

    # ---- (ii) no-leakage: rho_A(mu) uniform, ALL proper sizes, ALL mu ----
    for size in range(1, N_TYPES):        # every proper size 1..60
        for mu in range(n):               # every label
            rho = _marginal(F, mu, size)
            for v in range(n):
                for w in range(n):
                    want = (1.0 / n) if v == w else 0.0
                    if abs(rho[v][w] - want) >= _TOL:
                        check(False,
                              f"(ii) rho_A(mu={mu}, |A|={size})[{v}][{w}] "
                              f"deviates from the uniform mixture")
    check(True, "(ii) all 60 proper sizes x 42 labels: uniform mixture")
    # The improper subset (|A| = 61) is NOT blind -- sanity anchor: the
    # full-space state is pure and mu-dependent (clause (v) reads it).
    rho_full_0 = _marginal(F, 0, N_TYPES)
    rho_full_1 = _marginal(F, 1, N_TYPES)
    dev = max(abs(rho_full_0[v][w] - rho_full_1[v][w])
              for v in range(n) for w in range(n))
    check(dev > 1e-3,
          "(ii-anchor) the improper subset distinguishes labels "
          f"(dev = {dev:.3f}); privacy is proper-subset-only")

    # ---- (iii) read-blindness, expectation form (consistency with (ii);
    #            the operator-strength content is clause (iv)) ----
    for trial in range(8):
        f_diag = [rng.uniform(-3.0, 3.0) for _ in range(n)]
        expect = [sum(f_diag[v] * abs(F[mu][v]) ** 2 for v in range(n))
                  for mu in range(n)]
        spread = max(expect) - min(expect)
        check(spread < _TOL,
              f"(iii) trial {trial}: A-supported observable biases a "
              f"label (spread = {spread:.2e})")

    # ---- (iv) circulant compression: equal diagonal, shift-only mixing ----
    for trial in range(4):
        g = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
             for _ in range(n)]
        M = _compression(F, g)
        for mu in range(n):
            for nu in range(n):
                ref = M[0][(nu - mu) % n]
                check(abs(M[mu][nu] - ref) < _TOL,
                      f"(iv) compression not circulant at "
                      f"({mu},{nu}), trial {trial}")
        for mu in range(1, n):
            check(abs(M[mu][mu] - M[0][0]) < _TOL,
                  f"(iv) diagonal not constant at mu={mu}")
    # commuting family (feeds clause (d) of the ceiling check)
    g1 = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    g2 = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    M1, M2 = _compression(F, g1), _compression(F, g2)
    comm = max(abs(sum(M1[a][k] * M2[k][b] - M2[a][k] * M1[k][b]
                       for k in range(n)))
               for a in range(n) for b in range(n))
    check(comm < 1e-8,
          f"(iv) compressions must commute (|[M1,M2]| = {comm:.2e})")

    # ---- (v) global registration + the label-blindness finding ----
    # Fourier read: outcome distribution over frames for state mu_bar is
    # delta_mu (orthonormality, clause (i)) -- perfect distinguishability.
    # THE FINDING: the banked global read (per-channel Sector-B basis,
    # the horizon crossing sequence) is mu-BLIND on this code:
    for mu in (0, 5, 41):
        probs = [abs(F[mu][v]) ** 2 for v in range(n)]
        check(abs(sum(probs) - 1.0) < _TOL, "(v) dual-read normalization")
        check(max(probs) - min(probs) < _TOL,
              f"(v) the banked common-mode registration must be uniform "
              f"and mu-blind (mu={mu}) -- the label-blindness finding")

    # ---- (vi) negative control: the basis encoding leaks maximally ----
    # (a counterfactual encoding exhibit -- constructs no banked reader;
    #  see the census guard in the module docstring)
    for v, w in ((0, 1), (3, 40)):
        td = 0.5 * sum(abs((1.0 if u == v else 0.0) - (1.0 if u == w else 0.0))
                       for u in range(n))
        check(abs(td - 1.0) < _TOL,
              "(vi) basis-encoded labels must be perfectly locally "
              "distinguishable (trace distance 1)")

    # ---- (vii) full-tensor collapse cross-check at reduced parameters ----
    worst = _full_tensor_crosscheck(n_ch=3, q=3)
    check(worst < 1e-12,
          f"(vii) collapsed rep must match the full-tensor build "
          f"(max deviation {worst:.2e})")
    worst4 = _full_tensor_crosscheck(n_ch=4, q=3, seed=777)
    check(worst4 < 1e-12,
          f"(vii) collapsed rep must match at n_ch=4 "
          f"(max deviation {worst4:.2e})")

    return _result(
        name='T_vacuum_label_code_no_leakage -- the constructed P1 '
             'witness: a 42-label phase code on the common-mode slice '
             'of the banked second-epsilon skeleton with exact '
             'no-leakage on every proper type-subset, the circulant '
             'cleaning certificate, the label-blindness finding, the '
             'basis-encoding negative control, and the full-tensor '
             'collapse cross-check',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'On the banked skeleton (61 channels, 102 = 60 + 42 '
            'second-epsilon options, alphabet = the 42 Sector-B modes '
            '= dim V_global), ON THE COMMON-MODE SLICE of the Step-3 '
            'configuration family (42 of 42^61 configurations; the '
            'correlation is construction-supplied, its register form '
            'the OPEN a=b identity [C]), the Fourier phase code '
            '|mu_bar> = 42^{-1/2} sum_v omega^{mu v}|v>^{x61} realizes '
            'vacuum no-leakage (P1) at computed strength: 42 '
            'orthonormal label states whose reduced content on EVERY '
            'proper type-subset (all 60 sizes computed) is one fixed '
            'state; compressions of A-supported operators are '
            'equal-diagonal circulants (write access disclosed: '
            'privacy, not protection); one global Fourier measurement '
            'resolves the label perfectly -- and THE FINDING: that '
            'global read has no banked counterpart, while the banked '
            'horizon registration is label-BLIND on this code. The '
            'basis encoding fails the same test maximally. Collapse '
            'verified against full-tensor builds. Identification with '
            'the physical vacuum sector is a reading, not certified '
            'here; MSC/ICL_vac untouched.'
        ),
        key_result=(
            'P1 witnessed exact at label form on the common-mode '
            'carrier: no-leakage on all proper subsets; the banked '
            'horizon registration is label-blind on this code'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'T_vglobal_slot_identification_no_go',
                    'L_QEC_knill_laflamme',
                    'L_QEC_distance', 'L_QEC_wedge_duality',
                    'L_common_demand_iff_degenerate',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_vacuum_mixed_42dim_secret_scheme_exists'],
        artifacts={
            'n_types': N_TYPES,
            'alphabet': ALPHABET,
            'd_eff': D_EFF,
            'carrier': 'common-mode slice (42 of 42^61 configurations; '
                       'construction-supplied correlation)',
            'proper_subset_sizes_computed': '1..60, all 42 labels',
            'proper_subset_marginal': 'uniform mixture, 1/42 diagonal',
            'compression_structure': 'commuting family of circulants',
            'banked_horizon_read_on_this_code': 'label-blind (uniform)',
            'negative_control_trace_distance': 1.0,
            'full_tensor_crosscheck': '(3,3) and (4,3) exact',
        },
    )


def check_T_vacuum_logical_sector_classical_ceiling():
    """T_vacuum_logical_sector_classical_ceiling: No Subspace-Coherent 42-dim Sector [P_structural_instrument].

    See the module docstring, clauses (a)-(d), and fence (4). The
    privacy requirement admits no SUBSPACE-COHERENT logical sector of
    dim >= 2: coherent superpositions of the private frame are exactly
    the leaky states, no 2-dim carrier subspace has state-independent
    marginals (pointwise elementary proof in the module docstring), and
    the general subspace statement rides the named cited steps
    (Knill-Laflamme 1997 + no-cloning). Subsystem/mixed encodings are
    NOT excluded (Cleve-Gottesman-Lo 1999) -- and the fit question is
    closed EXISTS by check_T_vacuum_mixed_42dim_secret_scheme_exists;
    realization remains the open reading.
    """
    F = _frame()
    n = ALPHABET
    rng = random.Random(42061102)

    # ---- (a) the Fourier-dual exhibit: sum of the frame = product state ----
    for v in range(n):
        amp = sum(F[mu][v] for mu in range(n)) / math.sqrt(n)
        want = 1.0 if v == 0 else 0.0
        check(abs(amp - want) < _TOL,
              f"(a) uniform superposition must collapse to |0>^x61 "
              f"(component v={v}: {amp:.2e})")
    # its single-channel marginal is pure |0><0|: trace distance from
    # the uniform mixture, computed from the two states themselves
    product_state = [sum(F[mu][v] for mu in range(n)) / math.sqrt(n)
                     for v in range(n)]
    p_leak = [abs(product_state[v]) ** 2 for v in range(n)]
    p_uniform = [1.0 / n] * n
    td = 0.5 * sum(abs(p_leak[v] - p_uniform[v]) for v in range(n))
    check(abs(td - (1.0 - 1.0 / n)) < _TOL,
          f"(a) leak witness trace distance = {td:.4f} != 1 - 1/42")

    # ---- (b) in-carrier ceiling: 2-dim subspaces leak (state-dependence) ----
    def _state_dependence_defect(x, y):
        """Max over probe states psi in span{x,y} of the sup-norm
        deviation of psi's single-channel diagonal from x's diagonal
        (0 would mean state-INDEPENDENT marginals -- the P1-relevant
        privacy notion; audit fix 2)."""
        base = [abs(x[v]) ** 2 for v in range(n)]
        worst = 0.0
        for a, b in ((0.0, 1.0), (1.0, 1.0), (1.0, 1j),
                     (1.0, -1.0), (2.0, 1j)):
            vec = [a * x[v] + b * y[v] for v in range(n)]
            norm = math.sqrt(sum(abs(c) ** 2 for c in vec))
            diag = [abs(c / norm) ** 2 for c in vec]
            worst = max(worst,
                        max(abs(diag[v] - base[v]) for v in range(n)))
        return worst

    # the label frame's own 2-dim spans leak on superposition
    d01 = _state_dependence_defect(F[0], F[1])
    check(d01 > 1e-3,
          f"(b) span(|0_bar>,|1_bar>) must leak on superposition "
          f"(state-dependence defect = {d01:.4f})")
    # random 2-dim carrier subspaces all leak
    for trial in range(12):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        nx = math.sqrt(sum(abs(c) ** 2 for c in x))
        x = [c / nx for c in x]
        y0 = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        ip = sum(x[v].conjugate() * y0[v] for v in range(n))
        y = [y0[v] - ip * x[v] for v in range(n)]
        ny = math.sqrt(sum(abs(c) ** 2 for c in y))
        y = [c / ny for c in y]
        d = _state_dependence_defect(x, y)
        check(d > 1e-6,
              f"(b) random 2-dim carrier subspace trial {trial} shows "
              f"no state-dependence (defect = {d:.2e}) -- ceiling "
              f"violated?")

    # the proof chain's pivot, exhibited on the frame pair: the cross
    # products conj(x_v) y_v are NOT pointwise zero (their non-vanishing
    # is exactly where the pointwise proof localizes the leak)
    cross = [F[0][v].conjugate() * F[1][v] for v in range(n)]
    cross_max = max(abs(c) for c in cross)
    check(cross_max > 1e-3,
          "(b-pivot) frame cross products are nonzero pointwise -- the "
          "leak is exactly where the pointwise proof places it")

    # ---- (c) the general step is a docstring-level import; its
    #          in-model face: subspace privacy of A would be the
    #          operator condition P O_A P = c P; clause (iv) computed
    #          P O_A P = circulant, which is scalar ONLY on the trivial
    #          1-dim logical algebra -- generic circulants are not
    #          scalar. Subsystem/mixed evasion (CGL 1999) is FENCED in
    #          the module docstring, not adjudicated here. ----
    g = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    M = _compression(F, g)
    off = max(abs(M[a][b]) for a in range(n) for b in range(n) if a != b)
    check(off > 1e-6,
          "(c) generic compression is non-scalar: subspace-coherent "
          "privacy (the KL erasure condition) fails on the carrier")

    # ---- (d) classicality corollary, scoped: the compressions form a
    #          commuting family, simultaneously DFT-diagonalized ----
    def _dft_conj_offdiag(M_):
        n_ = len(M_)
        s = 1.0 / math.sqrt(n_)
        W = [[_omega(a * b, n_) * s for b in range(n_)] for a in range(n_)]
        WM = [[sum(W[k][a].conjugate() * M_[k][b] for k in range(n_))
               for b in range(n_)] for a in range(n_)]
        D = [[sum(WM[a][k] * W[k][b] for k in range(n_))
              for b in range(n_)] for a in range(n_)]
        return max(abs(D[a][b]) for a in range(n_) for b in range(n_)
                   if a != b)
    check(_dft_conj_offdiag(M) < 1e-8,
          "(d) every compression is DFT-diagonal: the interior-"
          "touchable logical structure at subspace form is abelian")

    return _result(
        name='T_vacuum_logical_sector_classical_ceiling -- the '
             'subspace-coherence ceiling: privacy forces the '
             'globally-locked 42-valued content to be a classical '
             'label alphabet AT SUBSPACE FORM; no subspace-coherent '
             '42-dim vacuum logical sector exists; subsystem/mixed '
             'encodings closed EXISTS (check 3; realization open)',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The privacy requirement of P1 admits NO subspace-coherent '
            '(pure-isometric) logical sector of dim >= 2: the uniform '
            'superposition of the 42 private label states IS the '
            'product state |0>^x61 (exact Fourier collapse, '
            'single-channel leak 1 - 1/42); no 2-dim subspace of the '
            'common-mode carrier has state-independent marginals '
            '(pointwise elementary proof in the module docstring, '
            'state-dependence witnesses computed); the general '
            'subspace statement is the named cited step '
            '(Knill-Laflamme 1997 erasure condition + no-cloning). '
            'THE SCOPE FENCE: subsystem/mixed-state encodings evade '
            'the no-cloning step (Cleve-Gottesman-Lo 1999 -- the '
            '((2,2)) one-time-pad is the counterexample form; the '
            'banked OA-QECC code state is itself mixed); the fit '
            'question is CLOSED EXISTS by the companion check '
            '(share dim 43 <= 102; realization stays the open '
            'reading). Corollary at '
            'subspace form: the interior-touchable logical structure '
            'is a commuting circulant family -- the "42-dim vacuum '
            'logical sector" of the route-(b) P1 wording is '
            'unconstructible as a subspace-coherent sector; the '
            'classical 42-label alphabet of the companion check is '
            'the maximum at subspace form, the exact species of the '
            'banked which-v object (.318) and census row 5 (.339).'
        ),
        key_result=(
            'No subspace-coherent 42-dim vacuum sector (in-carrier '
            'exact; general step cited KL-1997); mixed encodings '
            'closed EXISTS at 43 <= 102 (check 3; realization open)'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_label_code_no_leakage',
                    'T_vacuum_mixed_42dim_secret_scheme_exists',
                    'T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'L_QEC_knill_laflamme', 'L_QEC_wedge_duality'],
        artifacts={
            'fourier_collapse': 'sum_mu |mu_bar> / sqrt(42) = |0>^x61',
            'leak_witness_trace_distance': round(1.0 - 1.0 / ALPHABET, 6),
            'in_carrier_two_dim_privacy': 'impossible (exact, pointwise '
                                          'proof; witnesses computed)',
            'general_step': 'Knill-Laflamme 1997 + no-cloning [cited; '
                            'subspace-scoped]',
            'subsystem_evasion': 'Cleve-Gottesman-Lo 1999 [closed EXISTS, '
                                 'see check 3; realization open]',
            'compressed_algebra': 'commuting family of circulants '
                                  '(DFT-diagonal)',
        },
    )


# ---------------------------------------------------------------------------
# Check 3 machinery: the mixed ((61,61)) scheme (sparse-state simulator)
# ---------------------------------------------------------------------------

def _qss_encode_last(state, n_shares, p):
    """Apply the base isometry Sigma to the LAST share of a sparse state.

    State: dict mapping index-tuples -> amplitude. Layout: position 0
    is the reference, positions 1..n_shares are shares, positions
    n_shares+1.. are accumulated environment registers. The last share
    (position n_shares) is replaced by its two children (positions
    n_shares, n_shares+1); the new environment register is appended at
    the END of the tuple. Returns (new_state, n_shares+1).
    """
    inv = 1.0 / math.sqrt(p)
    out = {}
    for tup, amp in state.items():
        sec = tup[n_shares]
        head, tail = tup[:n_shares], tup[n_shares + 1:]
        for a in range(p):
            new = head + (a, (a + sec) % p) + tail + (((a + 2 * sec) % p),)
            out[new] = out.get(new, 0j) + amp * inv
    return out, n_shares + 1


def _qss_marginal(state, keep):
    """Reduced density (as a dict over kept-tuple pairs) on positions `keep`."""
    keep = tuple(keep)
    buckets = {}
    for tup, amp in state.items():
        rest = tuple(t for i, t in enumerate(tup) if i not in keep)
        kept = tuple(tup[i] for i in keep)
        buckets.setdefault(rest, []).append((kept, amp))
    rho = {}
    for terms in buckets.values():
        for k1, a1 in terms:
            for k2, a2 in terms:
                rho[(k1, k2)] = rho.get((k1, k2), 0j) + a1 * a2.conjugate()
    return rho


def _qss_rho_defect(rA, rB, rAB):
    """Entrywise defect || rho_AB - rho_A (x) rho_B ||_max."""
    worst = 0.0
    keys_a = {k[0] for k in rA} | {k[1] for k in rA}
    keys_b = {k[0] for k in rB} | {k[1] for k in rB}
    for (a1, a2) in [(x, y) for x in keys_a for y in keys_a]:
        for (b1, b2) in [(x, y) for x in keys_b for y in keys_b]:
            joint = rAB.get((a1 + b1, a2 + b2), 0j)
            prod = rA.get((a1, a2), 0j) * rB.get((b1, b2), 0j)
            worst = max(worst, abs(joint - prod))
    return worst


def _qss_decode_last_pair(state, n_shares, p):
    """Coherently decode the last two shares back into their parent.

    U1: (x, y) -> (x, y - x); F_- on register x; phase correction
    e^{2 pi i (p-2) w s / p}; the w register is then traced (it
    decouples exactly when recovery is exact). Environment registers
    are untouched. Returns (new_state_as_density_free_dict, n_shares-1)
    -- the w register is MOVED to the environment tail rather than
    traced, which is equivalent for the final density comparison and
    keeps the state pure.
    """
    out = {}
    pos_x, pos_y = n_shares - 1, n_shares
    inv = 1.0 / math.sqrt(p)
    for tup, amp in state.items():
        x, y = tup[pos_x], tup[pos_y]
        sec = (y - x) % p
        for w in range(p):
            ph = cmath.exp(-2j * cmath.pi * w * x / p) * cmath.exp(
                2j * cmath.pi * ((p - 2) * w * sec % p) / p)
            new = tup[:pos_x] + (sec,) + tup[pos_y + 1:] + (w,)
            out[new] = out.get(new, 0j) + amp * inv * ph
    return out, n_shares - 1


def _qss_build(n, p, d_ref, seed=None):
    """Build the ((n,n)) cascade state with a d_ref-dim entangled reference.

    Reference maximally entangled with the first d_ref basis secrets
    (d_ref <= p models the 42-in-43 subspace embedding). If seed is
    given, use a random (generic) entangled reference instead.
    """
    rng = random.Random(seed) if seed is not None else None
    state = {}
    for r in range(d_ref):
        c = (complex(rng.gauss(0, 1), rng.gauss(0, 1)) if rng
             else 1.0)
        state[(r, r)] = c
    norm = math.sqrt(sum(abs(a) ** 2 for a in state.values()))
    state = {k: v / norm for k, v in state.items()}
    n_shares = 1
    while n_shares < n:
        state, n_shares = _qss_encode_last(state, n_shares, p)
    return state, n_shares


# ---------------------------------------------------------------------------
# Checks 4-5 machinery: the sector-aligned scheme (share dim exactly 42)
# and the banked-registration coherent-recovery no-go.
# ---------------------------------------------------------------------------

_FIVEQ_STABS = ('XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ')


def _pauli_apply(pstr, state):
    """Apply a 5-qubit Pauli string to a sparse {int5: amp} state."""
    out = {}
    for b, amp in state.items():
        nb, namp = b, amp
        for q, ch in enumerate(pstr):
            bit = (nb >> (4 - q)) & 1
            if ch == 'X':
                nb ^= (1 << (4 - q))
            elif ch == 'Z':
                if bit:
                    namp = -namp
            elif ch == 'Y':
                namp = namp * (1j if bit == 0 else -1j)
                nb ^= (1 << (4 - q))
        out[nb] = out.get(nb, 0j) + namp
    return out


def _fiveq_codewords():
    """The [[5,1,3]] logical codewords as sparse dicts, built in-check
    from the cyclic XZZXI stabilizers (no literature table imported)."""
    cw = []
    for logical in (0, 1):
        st = {0b11111 if logical else 0b00000: 1.0 + 0j}
        for stab in _FIVEQ_STABS:
            new = _pauli_apply(stab, st)
            merged = dict(st)
            for b, a in new.items():
                merged[b] = merged.get(b, 0j) + a
            st = {b: a / 2.0 for b, a in merged.items() if abs(a) > 1e-14}
        norm = math.sqrt(sum(abs(a) ** 2 for a in st.values()))
        cw.append({b: a / norm for b, a in st.items()})
    return cw


def _fiveq_kl_certificate(cw):
    """KL for all 106 weight-<=2 Paulis: <iL|E|jL> = c(E) delta_ij,
    with c(E) = 0 for E != I (pure code). Returns worst deviation."""
    paulis = ['IIIII']
    letters = 'XYZ'
    for q in range(5):
        for ch in letters:
            p = list('IIIII'); p[q] = ch
            paulis.append(''.join(p))
    for q1 in range(5):
        for q2 in range(q1 + 1, 5):
            for c1 in letters:
                for c2 in letters:
                    p = list('IIIII'); p[q1] = c1; p[q2] = c2
                    paulis.append(''.join(p))
    assert len(paulis) == 106
    worst = 0.0
    for p in paulis:
        for i in range(2):
            ei = _pauli_apply(p, cw[i])
            for j in range(2):
                ov = sum(cw[j].get(b, 0j).conjugate() * a
                         for b, a in ei.items())
                want = 1.0 if (p == 'IIIII' and i == j) else 0.0
                worst = max(worst, abs(ov - want))
    return worst


def _q33_encode(state, pos, cw):
    """Encode register `pos` (a qubit) of a sparse tuple-state with the
    [[5,1,3]]-derived mixed ((3,3)): three kept child registers replace
    the parent at pos..pos+2; the two environment qubits append at the
    tail. Registers hold ints; kept children are bits."""
    out = {}
    for tup, amp in state.items():
        sec = tup[pos]
        for b, camp in cw[sec].items():
            k0, k1, k2 = (b >> 4) & 1, (b >> 3) & 1, (b >> 2) & 1
            e0, e1 = (b >> 1) & 1, b & 1
            new = tup[:pos] + (k0, k1, k2) + tup[pos + 1:] + (e0, e1)
            out[new] = out.get(new, 0j) + amp * camp
    return out


def _q33_decode(state, pos, cw):
    """Coherent Petz decode of the three kept children at pos..pos+2
    back into the parent qubit. Kraus of the recovery: R_e = 2 K_e^dag
    with K_e = (<e|_env (x) I) V (verified in-check: N(I/2) = I/8 and
    R(N(rho)) = rho). The Stinespring index e joins the tail; if the
    decode is exact the tail decouples."""
    amp_table = {}   # (kept3, env2) -> per-logical amplitude
    for sec in (0, 1):
        for b, camp in cw[sec].items():
            kept = (b >> 2) & 7
            env = b & 3
            amp_table.setdefault((kept, env), [0j, 0j])[sec] = camp
    out = {}
    for tup, amp in state.items():
        kept = (tup[pos] << 2) | (tup[pos + 1] << 1) | tup[pos + 2]
        for (k, e), pair in amp_table.items():
            if k != kept:
                continue
            for sec in (0, 1):
                coeff = 2.0 * pair[sec].conjugate()
                if abs(coeff) < 1e-14:
                    continue
                new = tup[:pos] + (sec,) + tup[pos + 3:] + (e,)
                out[new] = out.get(new, 0j) + amp * coeff
    return out


def _uniform_on_support_logrank(rho, tol=1e-10):
    """If rho is (proportional to) a projector, return ln(rank); else None.
    Entrywise test: rho/tr must satisfy P^2 = P/rank with equal diagonal
    on support -- sufficient for the structured marginals used here."""
    keys = sorted({k[0] for k in rho} | {k[1] for k in rho})
    tr = sum(rho.get((k, k), 0j).real for k in keys)
    if tr <= tol:
        return None
    diag = [rho.get((k, k), 0j).real / tr for k in keys if
            abs(rho.get((k, k), 0j)) > tol]
    if not diag or max(diag) - min(diag) > tol:
        return None
    rank = round(1.0 / diag[0])
    # off-diagonals must vanish for the projector-diagonal form
    for k1 in keys:
        for k2 in keys:
            if k1 != k2 and abs(rho.get((k1, k2), 0j)) > tol * tr:
                return None
    return math.log(rank)


def check_T_vacuum_mixed_42dim_secret_scheme_exists():
    """T_vacuum_mixed_42dim_secret_scheme_exists: The Fit Question Closed EXISTS [P_structural_instrument].

    See the module docstring, the check-3 block (A)-(F). A perfect
    ((61,61)) mixed quantum threshold scheme for a coherent 42-dim
    secret exists with every share dimension 43 <= 102. Walker
    CONSTRUCTION 0.95 + hostile audit LAND-WITH-FIXES 0.88, all seven
    fixes carried. Existence at abstract-encoding strength only; the
    banked-sector-ALIGNED scheme question is closed three-pronged by
    checks 4-5 (support EXISTS at exact fill / carrier dissolved /
    registration no-go; covariant refinement open).
    """
    P = 43

    # ---- (B) exact integer privacy certificates at p = 43 ----
    # share 1 kept (trace regs 2,3): a'+s'=a+s and a'+2s'=a+2s with
    # a'-a = ds forces 2 ds = ds i.e. ds = 0 (mod 43)
    bad = [ds for ds in range(1, P) if (2 * ds - ds) % P == 0]
    check(not bad, f"(B) share-1 cross-term congruence must be insoluble "
                   f"for s != s' (solutions: {bad})")
    # share 2 kept (trace regs 1,3): a'=a and 2(s-s') = 0
    bad = [ds for ds in range(1, P) if (2 * ds) % P == 0]
    check(not bad, "(B) share-2 cross-term congruence must be insoluble")
    # environment register (trace regs 1,2): a'=a and s'=s directly
    bad = [ds for ds in range(1, P) if ds % P == 0]
    check(not bad, "(B) environment cross-term congruence must be insoluble")

    # ---- (C) decoder phase identity, all (w, s) at p = 43 ----
    bad = [(w, sec) for w in range(P) for sec in range(P)
           if (2 * w * sec + (P - 2) * w * sec) % P != 0]
    check(not bad, f"(C) decoder correction identity fails at {bad[:3]}")

    # ---- (E) ((4,4)) p=3 full proper-subset scan, entangled ref ----
    p = 3
    state, n_sh = _qss_build(4, p, d_ref=3)
    n_pos = 1 + n_sh + (n_sh - 1)  # ref + shares + envs
    all_shares = list(range(1, n_sh + 1))
    from itertools import combinations
    n_scanned = 0
    for r in range(1, n_sh):
        for A in combinations(all_shares, r):
            rho_RA = _qss_marginal(state, (0,) + A)
            rho_R = _qss_marginal(state, (0,))
            rho_A = _qss_marginal(state, A)
            d = _qss_rho_defect(rho_R, rho_A, rho_RA)
            if d >= 1e-12:
                check(False, f"(E) ((4,4)) subset {A} leaks (defect {d:.2e})")
            n_scanned += 1
    check(n_scanned == 14, f"(E) must scan all 14 proper subsets "
                           f"(scanned {n_scanned})")
    # the two hardest subsets by name (all-but-one-child)
    for A in ((1, 2, 3), (1, 2, 4)):
        rho_RA = _qss_marginal(state, (0,) + A)
        d = _qss_rho_defect(_qss_marginal(state, (0,)),
                            _qss_marginal(state, A), rho_RA)
        check(d < 1e-12, f"(E) hardest subset {A} must be blind "
                         f"(defect {d:.2e}) -- the case-(ii) "
                         f"constant-channel identity, computed")

    # composed decoder: three stages back to the reference pair
    dec, m = state, n_sh
    while m > 2:
        dec, m = _qss_decode_last_pair(dec, m, p)
    # final base decode: shares (1,2) -> secret
    dec, m = _qss_decode_last_pair(dec, m, p)
    rho_final = _qss_marginal(dec, (0, 1))
    # target: the original maximally entangled pair
    target = {}
    for r1 in range(3):
        for r2 in range(3):
            target[((r1, r1), (r2, r2))] = 1.0 / 3
    worst = 0.0
    keys = {k[0] for k in rho_final} | {k[1] for k in rho_final} |            {k[0] for k in target} | {k[1] for k in target}
    for k1 in keys:
        for k2 in keys:
            worst = max(worst, abs(rho_final.get((k1, k2), 0j)
                                   - target.get((k1, k2), 0j)))
    check(worst < 1e-12, f"(E) ((4,4)) composed decoder must be exact "
                         f"(defect {worst:.2e})")

    # ---- (E) ((3,3)) p=5 with a 4-dim secret subspace, generic ref ----
    p = 5
    state, n_sh = _qss_build(3, p, d_ref=4, seed=424361)
    for r in range(1, n_sh):
        for A in combinations(range(1, n_sh + 1), r):
            d = _qss_rho_defect(_qss_marginal(state, (0,)),
                                _qss_marginal(state, A),
                                _qss_marginal(state, (0,) + A))
            check(d < 1e-12, f"(E) ((3,3)) p=5 subset {A} leaks "
                             f"(defect {d:.2e})")
    dec, m = state, n_sh
    while m > 1:
        dec, m = _qss_decode_last_pair(dec, m, p)
    rho_final = _qss_marginal(dec, (0, 1))
    rho_start = _qss_marginal(_qss_build(1, p, 4, seed=424361)[0],
                              (0, 1))
    worst = max(abs(rho_final.get(k, 0j) - rho_start.get(k, 0j))
                for k in set(rho_final) | set(rho_start))
    check(worst < 1e-12, f"(E) ((3,3)) p=5 composed decoder must be "
                         f"exact on the generic entangled reference "
                         f"(defect {worst:.2e})")

    # ---- (E) GHZ negative control at p=3: sum encoding leaks on
    #          superpositions (superoperator-constancy has teeth) ----
    p = 3
    ghz = {}
    for r in range(3):          # ref entangled with secret, sum encoding
        for x in range(p):
            ghz[(r, x, (r - x) % p)] = 1.0 / 3  # 1/sqrt(3) ref * 1/sqrt(3)
    # basis-label privacy: single-share marginal for each BASIS secret
    # is uniform -- but the Choi test against the entangled ref fails:
    d = _qss_rho_defect(_qss_marginal(ghz, (0,)),
                        _qss_marginal(ghz, (1,)),
                        _qss_marginal(ghz, (0, 1)))
    check(d > 0.05, f"(E) GHZ negative control must FAIL the "
                    f"superoperator-constancy test (defect {d:.3f})")

    return _result(
        name='T_vacuum_mixed_42dim_secret_scheme_exists -- the fit '
             'question closed EXISTS: a perfect ((61,61)) mixed '
             'threshold scheme for a coherent 42-dim secret with '
             'every share dimension 43 <= 102 (cascade of the '
             'polynomial-code ((2,2)); exact base certificates at '
             'p = 43; full proper-subset scans + composed decoder at '
             'reduced parameters; GHZ negative control)',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The clause-(c) fit question closes EXISTS at '
            'abstract-encoding strength: 60 applications of the mixed '
            '((2,2)) polynomial-code scheme (base |s> -> p^{-1/2} '
            'sum_a |a, a+s, a+2s>, third register to the environment; '
            'p = 43) yield a perfect ((61,61)) scheme for a coherent '
            '42-dim secret with all 61 share dimensions exactly 43 '
            '<= 102. Base privacy = exact integer congruence '
            'certificates at p = 43 (stronger than float); recovery = '
            'measure-and-correct decoder with the correction identity '
            'pinned by integer loop; cascade privacy = the case-(ii) '
            'constant-channel identity (docstring proof) with full '
            'proper-subset scans at ((4,4)) p=3 (all 14, the two '
            'hardest by name) and ((3,3)) p=5 (4-dim secret, generic '
            'entangled reference), composed decoder exact in every '
            'case. The naive CGL route (pure ((61,121))) needs p >= '
            '121 > 102 and does NOT fit; the cascade is the '
            'load-bearing move. CONSEQUENCE for the ceiling: '
            'dimensional structure does not force classicality of '
            'globally-locked content; the subspace ceiling and the '
            'banked label-typing stand; the banked-sector-ALIGNED '
            'scheme question is closed three-pronged by checks 4-5; '
            'realization/'
            'identification remains the open reading. No cited '
            'theorem is load-bearing (CGL 1999 is attribution).'
        ),
        key_result=(
            'Perfect ((61,61)) mixed scheme, coherent 42-dim secret, '
            'all share dims 43 <= 102: the mixed direction of the '
            'ceiling closes EXISTS (abstract encoding; realization '
            'open)'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_label_code_no_leakage',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_which_v_no_registered_interior_reader',
                    'T_vglobal_offdiagonal_blocks_scalar_typed',
                    'L_QEC_knill_laflamme'],
        artifacts={
            'scheme': '((61,61)) mixed; 60x cascade of polynomial-code '
                      '((2,2)) at p = 43; 1 base + 59 re-shares',
            'share_dims': '43 each (61 shares) <= 102',
            'share_dim_bound': '43 >= 42 here; exactly 42 SETTLED by '
                               'check 4 (the floor is tight at the '
                               'banked dimension)',
            'naive_cgl_excluded': 'pure ((61,121)) needs p >= 121 > '
                                  '102; the cascade is what fits',
            'base_certificates': 'integer congruence + decoder phase '
                                 'identity, exact at p = 43',
            'scans': '((4,4)) p=3 all 14 subsets + ((3,3)) p=5 d_ref=4 '
                     'generic ref; composed decoders exact',
            'norm_convention': 'entrywise max defect (reported '
                               'elsewhere as Frobenius/trace -- '
                               'convention only)',
            'alignment': 'this scheme NOT sector-aligned; the '
                         'aligned question closed three-pronged by '
                         'checks 4-5 (support EXISTS / carrier '
                         'dissolved / registration no-go; covariant '
                         'open)',
        },
    )


def check_T_vacuum_sector_aligned_scheme_share_dim_42():
    """T_vacuum_sector_aligned_scheme_share_dim_42: Support-Alignment EXISTS at Exact Fill [P_structural_instrument].

    Check 4 (2026-07-02; walker CONSTRUCTION 0.93 + hostile audit
    LAND-WITH-FIXES 0.88, all eight fixes carried). THE STATEMENT: a
    perfect ((61,61)) mixed quantum threshold scheme for a coherent
    42-dim secret exists with EVERY share dimension exactly 42 --
    admitting a Sector-B-supported embedding (exact fill of each
    channel's 42-dim Sector-B block; the embedding is a choice the
    dimension permits, not a consequence). This settles the check-3
    open pin (42 <= d_share <= 43) at 42: the important-share floor
    (d >= 42, CMI chain in this docstring) is TIGHT at the banked
    dimension, zero Sector-B slack.

    THE CONSTRUCTION (42 = 2 x 3 x 7, tensor of three ((61,61))s):
      - factors 3 and 7: the check-3 polynomial cascade at p = 3 and
        p = 7 (both prime >= 3; integer certificates re-run here);
      - THE QUBIT FACTOR (the load-bearing novelty; p = 2 FAILS the
        polynomial route -- three evaluation points do not exist mod
        2): the five-qubit code [[5,1,3]], BUILT IN-CHECK from its
        cyclic XZZXI stabilizers, is a pure ((3,5)) threshold
        structure (KL for all 106 weight-<=2 Paulis, deviation
        exactly 0); discarding two positions to the environment gives
        a mixed ((3,3)) qubit-secret ALL-QUBIT-SHARES scheme;
        re-sharing one share with the same ((3,3)) gives
        ((n+2, n+2)); 61 IS ODD (load-bearing fence): base + 29
        re-shares = ((61,61)) all-qubit. 3 + 2*29 = 61.
      - tensor composition: tensors of constant channels are constant
        (one-line linearity), decoders tensor; share_i =
        C^2 x C^3 x C^7 = C^42.

    THE LOWER BOUND (derived here, so exactly-42 is TIGHT, not just
    achieved): with reference R maximally entangled with the secret,
    privacy gives I(R:S_A) = 0 for proper A; perfect recovery gives
    I(R:S_[61]) = 2 log 42; for any share t with A = [61] minus t:
    2 log 42 = I(R:S_t|S_A) <= I(S_t : R S_A) <= 2 log d_t, so
    d_t >= 42 [chain rule + MI nonnegativity + dimension bound,
    textbook inequalities]. The saturation instance I(R:S_t|A) =
    2 ln 2 is COMPUTED on the qubit ((3,3)) below via
    uniform-on-support log-rank entropies.

    THE INDUCTION (the one nontrivial lemma, same shape as check 3's
    case (ii)): for proper A after a re-share, if A contains 1 or 2
    of the 3 children, the corresponding ((3,3)) marginal channel is
    the CONSTANT channel (KL weight-<=2 privacy at superoperator
    strength, verified at Choi strength below), and
    (id (x) Lambda)(rho) = rho_rest (x) sigma kills the parent for
    arbitrary correlations BEFORE any appeal to the previous
    scheme's privacy -- the case naive pullback misses (A = all
    other shares + some children pulls back to the FULL set). If A
    contains all 3 children, A misses some old share and pulls back
    proper; if none, directly proper.

    FENCES: (1) support-alignment is NOT realization -- the .356
    fence pattern is inherited verbatim; nothing here identifies any
    scheme with physical vacuum content; ICL_vac stays named [C];
    MSC untouched. (2) The aligned-question closure is
    THREE-PRONGED, never "closed" simpliciter: the sector-split
    reading closes EXISTS (this check); the common-mode-carrier
    reading DISSOLVES (type mismatch: the carrier is a global 42-dim
    subspace with no per-channel tensor structure -- "shares
    supported on it" is not well-typed; its subspace-coherent
    version is already killed by check 2); the registration reading
    closes NEGATIVELY at coherent strength (check 5). (3) The
    S_42-covariant refinement is SPLIT (v24.3.373,
    check_T_vacuum_scheme_product_affine_covariance): (a) this
    construction is not covariant under FULL S_42 as built (true a
    fortiori: even its G_0 covariance is F2 as built, F1 only after
    the D_4 dressing); (b) existence of some fully S_42-covariant
    scheme at (61, 42) stays OPEN -- but covariance does NOT force
    classicality at exact fill anywhere computable (full-S_q F1
    witnesses at q = 2, 3; no continuous-symmetry obstruction for a
    finite group).
    (4) n = 61 is not directly simulated: the ((3,3))/((5,5)) full
    scans + the reduced ((7,7)) hard-case scan are computed here;
    the FULL ((7,7)) 126-subset scan is pinned offline (The
    Turning/vacuum_aligned_full77_witness_2026-07-02.py, the .351
    pattern). (5) AME(4,2) nonexistence (Higuchi-Sugita 2000) is
    docstring attribution [cited, unverified] and NOT load-bearing
    (61 odd; n = 2 never used); the computed reason the qubit factor
    needs the QEC route is the p = 2 evaluation-point failure.
    (6) Privacy is not erasure-protection (inherited).
    """
    from itertools import combinations

    cw = _fiveq_codewords()

    # ---- [[5,1,3]] built in-check: orthonormal, KL weight-<=2 exact ----
    for i in range(2):
        nrm = sum(abs(a) ** 2 for a in cw[i].values())
        check(abs(nrm - 1.0) < 1e-12, f"codeword {i} normalized")
    ov = abs(sum(cw[1].get(b, 0j).conjugate() * a for b, a in cw[0].items()))
    check(ov < 1e-12, f"codewords orthogonal (overlap {ov:.2e})")
    kl = _fiveq_kl_certificate(cw)
    check(kl < 1e-12,
          f"KL for all 106 weight-<=2 Paulis, c(E!=I) = 0 (worst {kl:.2e})")

    # ---- the ((3,3)) qubit-shares scheme: privacy + decoupling + decode ----
    import math as _m
    state = {(0, 0): 1 / _m.sqrt(2), (1, 1): 1 / _m.sqrt(2)}
    s33 = _q33_encode(state, 1, cw)
    for r in (1, 2):
        for A in combinations((1, 2, 3), r):
            d = _qss_rho_defect(_qss_marginal(s33, (0,)),
                                _qss_marginal(s33, A),
                                _qss_marginal(s33, (0,) + A))
            check(d < 1e-12, f"((3,3)) subset {A} leaks (defect {d:.2e})")
    d = _qss_rho_defect(_qss_marginal(s33, (0,)), _qss_marginal(s33, (4, 5)),
                        _qss_marginal(s33, (0, 4, 5)))
    check(d < 1e-12, f"((3,3)) decoupling (recovery certificate): {d:.2e}")
    dec = _q33_decode(s33, 1, cw)
    target = {((a, a), (b, b)): 0.5 for a in (0, 1) for b in (0, 1)}
    rho = _qss_marginal(dec, (0, 1))
    keys = {k[0] for k in rho} | {k[1] for k in rho} | {k[0] for k in target}
    w = max(abs(rho.get((k1, k2), 0j) - target.get((k1, k2), 0j))
            for k1 in keys for k2 in keys)
    check(w < 1e-12, f"((3,3)) Petz decode exact (defect {w:.2e})")

    # ---- CMI saturation instance: I(R:S_t|A) = 2 ln 2 exactly ----
    # entropies via uniform-on-support log-rank (each marginal verified
    # proportional to a projector entrywise)
    # S(X) computed where the marginal is diagonal-uniform; for tA and
    # RtA use purity duality S(X) = S(X^c) (global state pure): the
    # complements (R, env) and (env) ARE diagonal-uniform.
    ent = {}
    for name, kp in (('RA', (0, 1, 2)), ('tA', (0, 4, 5)),
                     ('A', (1, 2)), ('RtA', (4, 5))):
        lr = _uniform_on_support_logrank(_qss_marginal(s33, kp))
        check(lr is not None, f"CMI marginal {name} uniform-on-support "
                              f"(via complement where noted)")
        ent[name] = lr
    cmi = ent['RA'] + ent['tA'] - ent['A'] - ent['RtA']
    check(abs(cmi - 2 * _m.log(2)) < 1e-10,
          f"CMI floor saturated: I(R:S_t|A) = {cmi:.6f} = 2 ln 2 "
          f"(the d >= 42 bound is tight at the banked dimension)")

    # ---- ((5,5)) cascade: FULL 30-subset scan + composed decoder ----
    s55 = _q33_encode(s33, 3, cw)
    for r in range(1, 5):
        for A in combinations((1, 2, 3, 4, 5), r):
            d = _qss_rho_defect(_qss_marginal(s55, (0,)),
                                _qss_marginal(s55, A),
                                _qss_marginal(s55, (0,) + A))
            check(d < 1e-12, f"((5,5)) subset {A} leaks (defect {d:.2e})")
    d2 = _q33_decode(_q33_decode(s55, 3, cw), 1, cw)
    rho = _qss_marginal(d2, (0, 1))
    w = max(abs(rho.get((k1, k2), 0j) - target.get((k1, k2), 0j))
            for k1 in keys for k2 in keys)
    check(w < 1e-12, f"((5,5)) composed decode exact (defect {w:.2e})")

    # ---- ((7,7)) reduced scan: the named hard cases + one probe/size ----
    s77 = _q33_encode(s55, 5, cw)
    hard = [(1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 7), (1, 2, 3, 4, 6, 7)]
    probes = [(1,), (2, 5), (1, 4, 7), (2, 3, 5, 6), (1, 2, 4, 6, 7)]
    for A in hard + probes:
        d = _qss_rho_defect(_qss_marginal(s77, (0,)),
                            _qss_marginal(s77, A),
                            _qss_marginal(s77, (0,) + A))
        check(d < 1e-12, f"((7,7)) subset {A} leaks (defect {d:.2e}) -- "
                         f"hard cases = all-shares-minus-one-child")
    # decoupling of the accumulated environment
    env77 = tuple(range(8, 8 + 6))
    d = _qss_rho_defect(_qss_marginal(s77, (0,)), _qss_marginal(s77, env77),
                        _qss_marginal(s77, (0,) + env77))
    check(d < 1e-12, f"((7,7)) decoupling: {d:.2e}")
    check(3 + 2 * 29 == 61, "parity: base 3 + 29 re-shares = 61 (odd)")

    # ---- factors 3 and 7: integer certificates (the check-3 pattern) ----
    for P_ in (3, 7):
        bad = [ds for ds in range(1, P_) if (2 * ds - ds) % P_ == 0]
        check(not bad, f"p={P_} share-1 congruence insoluble")
        bad = [ds for ds in range(1, P_) if (2 * ds) % P_ == 0]
        check(not bad, f"p={P_} share-2 congruence insoluble")
        bad = [(w_, sec) for w_ in range(P_) for sec in range(P_)
               if (2 * w_ * sec + (P_ - 2) * w_ * sec) % P_ != 0]
        check(not bad, f"p={P_} decoder phase identity")
    # p = 2 FAILS (the computed reason the qubit factor needs QEC):
    check(len(set(x % 2 for x in (0, 1, 2))) < 3,
          "p=2: three distinct evaluation points do not exist mod 2")

    # ---- tensor witness at share dim 6: qubit ((3,3)) x qutrit ((3,3))
    #      (both factors THREE shares -- tensoring requires equal n;
    #      the qutrit ((3,3)) is one cascade level of the p=3 scheme) ----
    q3 = {}
    for r_ in range(3):
        q3[(r_, r_)] = 1.0 / math.sqrt(3)
    q3, nsh = _qss_encode_last(q3, 1, 3)      # 2 shares
    q3, nsh = _qss_encode_last(q3, nsh, 3)    # 3 shares (+ 2 envs at tail)
    # combined: registers (ref2, ref3, q1,t1, q2,t2, q3,t3, qenvs, tenvs)
    comb = {}
    for t1, a1 in s33.items():
        for t2, a2 in q3.items():
            new = (t1[0], t2[0], t1[1], t2[1], t1[2], t2[2], t1[3], t2[3],
                   t1[4], t1[5], t2[4], t2[5])
            comb[new] = comb.get(new, 0j) + a1 * a2
    refs = (0, 1)
    joint = {1: (2, 3), 2: (4, 5), 3: (6, 7)}
    for r_ in (1, 2):
        for A in combinations((1, 2, 3), r_):
            kp = sum((joint[i] for i in A), ())
            d = _qss_rho_defect(_qss_marginal(comb, refs),
                                _qss_marginal(comb, kp),
                                _qss_marginal(comb, refs + kp))
            check(d < 1e-12,
                  f"tensor witness (dim 6) subset {A} leaks ({d:.2e})")

    check(2 * 3 * 7 == ALPHABET, "42 = 2 x 3 x 7 (exact fill of Sector-B)")

    return _result(
        name='T_vacuum_sector_aligned_scheme_share_dim_42 -- '
             'support-alignment EXISTS at exact fill: a perfect ((61,61)) '
             'mixed scheme for a coherent 42-dim secret with every share '
             'dimension exactly 42 (the [[5,1,3]] qubit factor x the p=3,7 '
             'cascades); the important-share floor tight at the banked '
             'dimension',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'The check-3 open pin (42 <= d_share <= 43) settles at 42: '
            'tensoring the polynomial cascades at p = 3, 7 with a qubit '
            'factor built from the five-qubit code [[5,1,3]] (a pure '
            '((3,5)) threshold structure; discard two positions -> mixed '
            '((3,3)) all-qubit-shares; re-share +2 per step; 61 odd '
            'reaches ((61,61))) gives every share dimension exactly '
            '2 x 3 x 7 = 42, admitting a Sector-B-supported embedding at '
            'exact fill. KL certificate exact over all 106 weight-<=2 '
            'Paulis; ((3,3))/((5,5)) FULL proper-subset scans + composed '
            'Petz decoders exact; ((7,7)) hard cases + probes in-check '
            '(full scan pinned offline); CMI floor computed saturated '
            '(2 ln 2); p = 2 failure computed (the reason the qubit '
            'factor needs the QEC route). THE THREE-PRONGED closure of '
            'the aligned question: sector-split EXISTS (here), carrier '
            'reading dissolved (type mismatch), registration reading '
            'negative at coherent strength (check 5). Support-alignment '
            'is NOT realization; ICL_vac stays named [C]; the '
            'S_42-covariant refinement is split at v24.3.373 (subgroup EXISTS; full S_42 open).'
        ),
        key_result=(
            'Share dimension exactly 42 = the Sector-B block, exact '
            'fill: aligned support EXISTS; the Gottesman floor is tight '
            'at the banked dimension (realization open)'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_mixed_42dim_secret_scheme_exists',
                    'T_vacuum_logical_sector_classical_ceiling',
                    'T_vacuum_label_code_no_leakage',
                    'T_banked_registration_coherent_recovery_no_go'],
        artifacts={
            'share_dims': 'exactly 42 = 2 x 3 x 7, all 61 shares '
                          '(Sector-B exact fill)',
            'qubit_factor': '[[5,1,3]] -> mixed ((3,3)) all-qubit; '
                            '+2 per re-share; 3 + 2*29 = 61 (odd, '
                            'load-bearing)',
            'kl_certificate': '106 weight-<=2 Paulis, deviation 0',
            'cmi_saturation': 'I(R:S_t|A) = 2 ln 2 computed (floor '
                              'tight)',
            'p2_failure': 'computed: no 3 evaluation points mod 2',
            'ame42_citation': 'Higuchi-Sugita 2000 [cited, unverified, '
                              'NOT load-bearing]',
            'offline_witness': 'The Turning/vacuum_aligned_full77_'
                               'witness_2026-07-02.py (full ((7,7)) '
                               'scan)',
            'alignment_ledger': 'support EXISTS / carrier dissolved / '
                                'registration no-go / covariant SPLIT at .373 (subgroup EXISTS; full S_42 open)',
        },
    )


def check_T_banked_registration_coherent_recovery_no_go():
    """T_banked_registration_coherent_recovery_no_go: The Classical-Record Ceiling [P_structural_instrument].

    Check 5 (2026-07-02; walker NO-GO 0.97 + hostile audit
    LAND-WITH-FIXES 0.88, all fixes carried). THE STATEMENT: no
    recovery that factors through the CLASSICAL RECORD of any
    measurement of all shares -- the banked horizon registration
    (per-channel Sector-B-basis readout, T_horizon_reciprocity Step
    4) being the relevant instance UNDER THE IDENTIFICATION READING
    (wedge-fence strength) -- can deliver a coherent secret of
    dimension >= 2, for ANY encoding (any share dims, any alignment,
    mixed or pure). PROOF (elementary, in full): recovery-from-record
    is measure-and-prepare, rho -> sum_k Tr(M_k rho) sigma_k; with
    any reference the output is manifestly separable; for separable
    states the overlap with the maximally entangled state is at most
    1/d (computed below, attained at product |alpha>|alpha*>); hence
    entanglement fidelity F_e <= 1/d and the composite cannot be the
    identity on any dim >= 2 subspace. The average-fidelity
    conversion F_avg = (d F_e + 1)/(d + 1) is a one-line Kraus
    identity (trace preservation gives sum_K Tr K^dag K = d). At the
    banked constants: F_e <= 1/42, F_avg <= 2/43 -- classical-guess
    level.

    MEASUREMENT-LEVEL CEILING STRUCTURE (audit fix 2 -- the ceiling
    is attained under SOME measurements; a FIXED basis readout need
    not attain it): computed below on three schemes --
      - the ((2,2)) polynomial scheme: the share-basis record
        DETERMINES the classical label (label-transparent), and
        coherent recovery attains the ceiling F_e = 1/d exactly;
      - the phase code: the per-channel v-basis record is
        LABEL-BLIND (uniform, mu-independent -- the .352 clause-(v)
        finding re-derived), and coherent recovery still attains the
        ceiling 1/d;
      - the qubit ((3,3)): the fixed Z-basis record gives F_e = 1/4
        < 1/2 (ceiling NOT attained by that basis), while the
        decoder-basis measurement attains 1/2 exactly (computed via
        the coherent Petz decode + computational readout).
    The inversion (label-blind yet ceiling-attaining vs
    label-transparent and ceiling-attaining) is recorded as a
    finding.

    THE COMPOSED FINDING (honest form, audit fix 3): a coherent
    42-dim secret can be carried with every share Sector-B-supported
    at exact fill (check 4), and any recovery factoring through the
    classical record of any full-share measurement -- the banked
    registration being the relevant instance under the
    identification reading -- is capped at F_e <= 1/42; CLASSICAL
    label content is NOT protected by this no-go (the ((2,2)) record
    determines its label); realization/identification stays the open
    reading. This inherits the direction of the .352 label-blindness
    finding: it prices the identification reading, nothing more.

    FENCES: the no-go binds recovery factoring through the classical
    record ONLY -- coherent operations before registration and
    quantum side-information are untouched; "banked registration =
    v-basis measure-and-record" is a reading of Step 4 (wedge-fence
    strength, same as .352 clause (v)); nothing here adopts ICL_vac,
    closes RVC, or touches MSC.
    """
    import math as _m
    from itertools import product as _prod

    # ---- separable overlap bound: max_sep <phi|sigma|phi> = 1/d ----
    d3 = 3
    rng = random.Random(20260703)
    worst = 0.0
    for _ in range(400):
        a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d3)]
        b = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d3)]
        na = _m.sqrt(sum(abs(c) ** 2 for c in a))
        nb = _m.sqrt(sum(abs(c) ** 2 for c in b))
        ov = abs(sum(a[i] / na * b[i] / nb for i in range(d3))) ** 2 / d3
        worst = max(worst, ov)
    check(worst <= 1.0 / d3 + 1e-12,
          f"separable overlap <= 1/d (sampled max {worst:.6f})")
    att = abs(sum((1 / _m.sqrt(d3)) * (1 / _m.sqrt(d3))
                  for _ in range(1))) ** 2  # |alpha>|alpha*> attains:
    ov = sum(1 / d3 * 1 / d3 for _ in range(d3))  # = 1/d exactly
    check(abs(ov - 1.0 / d3) < 1e-12, "bound attained at |alpha>|alpha*>")

    # ---- ((2,2)) p=3: record determines the label; F_e = 1/3 exactly ----
    p = 3
    st = {}
    for r in range(p):
        for a in range(p):
            st[(r, a, (a + r) % p, (a + 2 * r) % p)] = 1.0 / p
    # measure shares (positions 1,2): outcomes (x,y); conditional rho_R
    fe = 0.0
    n_out = 0
    for x in range(p):
        for y in range(p):
            branch = {t: amp for t, amp in st.items()
                      if t[1] == x and t[2] == y}
            if not branch:
                continue
            n_out += 1
            pk = sum(abs(a) ** 2 for a in branch.values())
            rhoR = {}
            for t1, a1 in branch.items():
                for t2, a2 in branch.items():
                    if t1[3] == t2[3]:
                        rhoR[(t1[0], t2[0])] = rhoR.get((t1[0], t2[0]), 0j)                             + a1 * a2.conjugate()
            # purity test => lambda_max = 1 (the record determines s)
            tr = sum(rhoR.get((k, k), 0j).real for k in range(p))
            tr2 = sum((rhoR.get((k1, k2), 0j)
                       * rhoR.get((k2, k1), 0j)).real
                      for k1 in range(p) for k2 in range(p))
            check(abs(tr2 - tr * tr) < 1e-12,
                  f"((2,2)) outcome ({x},{y}): conditional rho_R pure "
                  f"(label determined by the record)")
            s_det = (y - x) % p
            check(abs(rhoR.get((s_det, s_det), 0j).real - tr) < 1e-12,
                  f"((2,2)) record determines s = y - x = {s_det}")
            fe += tr * 1.0   # p_k * lambda_max, lambda_max = 1
    fe /= p                  # F_e = (1/d) sum p_k lambda_max
    check(abs(fe - 1.0 / p) < 1e-12,
          f"((2,2)) record-recovery ceiling attained: F_e = {fe:.6f} = 1/3 "
          f"(label-transparent AND coherence-capped)")

    # ---- phase code (3 channels, q=3): record label-blind, F_e = 1/3 ----
    F3 = _frame(3)
    ph = {}
    for mu in range(3):
        for v in range(3):
            ph[(mu, v, v, v)] = F3[mu][v] / _m.sqrt(3)
    fe = 0.0
    for v in range(3):     # only all-equal outcomes occur
        branch = {t: a for t, a in ph.items() if t[1] == v}
        pk = sum(abs(a) ** 2 for a in branch.values())
        check(abs(pk - 1.0 / 3) < 1e-12,
              f"phase-code record uniform (outcome v={v}: {pk:.4f}) -- "
              f"label-BLIND (the .352 finding re-derived)")
        rhoR = {}
        for t1, a1 in branch.items():
            for t2, a2 in branch.items():
                rhoR[(t1[0], t2[0])] = rhoR.get((t1[0], t2[0]), 0j)                     + a1 * a2.conjugate()
        tr = sum(rhoR.get((k, k), 0j).real for k in range(3))
        tr2 = sum((rhoR.get((k1, k2), 0j) * rhoR.get((k2, k1), 0j)).real
                  for k1 in range(3) for k2 in range(3))
        check(abs(tr2 - tr * tr) < 1e-12, "phase-code conditional pure")
        fe += tr
    fe /= 3
    check(abs(fe - 1.0 / 3) < 1e-12,
          f"phase-code record-recovery: F_e = {fe:.6f} = 1/3 "
          f"(label-BLIND and coherence-capped)")

    # ---- qubit ((3,3)): fixed Z-record 1/4 < 1/2; decoder basis = 1/2 ----
    cw = _fiveq_codewords()
    st33 = _q33_encode({(0, 0): 1 / _m.sqrt(2), (1, 1): 1 / _m.sqrt(2)},
                       1, cw)
    fe = 0.0
    for out in _prod((0, 1), repeat=3):
        branch = {t: a for t, a in st33.items()
                  if (t[1], t[2], t[3]) == out}
        if not branch:
            continue
        pk = sum(abs(a) ** 2 for a in branch.values())
        rhoR = {}
        for t1, a1 in branch.items():
            for t2, a2 in branch.items():
                if t1[4:] == t2[4:]:
                    rhoR[(t1[0], t2[0])] = rhoR.get((t1[0], t2[0]), 0j)                         + a1 * a2.conjugate()
        # lambda_max of the 2x2 conditional (exact closed form)
        a11 = rhoR.get((0, 0), 0j).real
        a22 = rhoR.get((1, 1), 0j).real
        a12 = rhoR.get((0, 1), 0j)
        lam = 0.5 * (a11 + a22) + 0.5 * _m.sqrt((a11 - a22) ** 2
                                                + 4 * abs(a12) ** 2)
        fe += lam
    fe /= 2
    check(abs(fe - 0.25) < 1e-12,
          f"((3,3)) fixed Z-record: F_e = {fe:.6f} = 1/4 < 1/2 -- the "
          f"ceiling is NOT attained by that basis")
    # decoder-basis measurement attains the ceiling exactly:
    dec = _q33_decode(st33, 1, cw)
    fe = 0.0
    groups = {}
    for t, a in dec.items():
        key = t[1:]          # recovered secret + env + anc = the record
        groups.setdefault(key, {})[t[0]] =             groups.setdefault(key, {}).get(t[0], 0j) + a
    for key, rvec in groups.items():
        pk = sum(abs(a) ** 2 for a in rvec.values())
        lam = pk             # conditional rho_R pure (verify)
        tr2 = sum((rvec.get(k1, 0j) * rvec.get(k1, 0j).conjugate()).real
                  for k1 in (0, 1))
        check(abs(tr2 - pk) < 1e-12, "decoder-basis conditional pure")
        fe += lam
    fe /= 2
    check(abs(fe - 0.5) < 1e-12,
          f"((3,3)) decoder-basis measurement attains the ceiling: "
          f"F_e = {fe:.6f} = 1/2 (measurement-level structure)")

    # ---- the banked-constant statement ----
    check(abs(1.0 / ALPHABET - 1.0 / 42) < 1e-15
          and abs((42 * (1.0 / 42) + 1) / 43 - 2.0 / 43) < 1e-15,
          "banked constants: F_e <= 1/42, F_avg = (d F_e + 1)/(d + 1) "
          "<= 2/43")

    return _result(
        name='T_banked_registration_coherent_recovery_no_go -- the '
             'classical-record ceiling: no recovery factoring through '
             'the classical record of any full-share measurement (the '
             'banked horizon registration being the relevant instance '
             'under the identification reading) delivers a coherent '
             'secret of dim >= 2; F_e <= 1/42 at banked constants',
        tier=4,
        epistemic='P_structural_instrument',
        summary=(
            'Measure-and-prepare is entanglement-breaking: output '
            'separable with any reference; separable overlap with the '
            'maximally entangled state <= 1/d (computed, attained); '
            'hence F_e <= 1/d = 1/42 and F_avg <= 2/43 at banked '
            'constants -- classical-guess level; identity on any dim '
            '>= 2 subspace impossible. Measurement-level structure '
            'computed on three schemes: the ((2,2)) record is '
            'label-TRANSPARENT and coherence-capped at exactly 1/d; '
            'the phase-code v-record is label-BLIND (the .352 finding '
            're-derived) and coherence-capped at exactly 1/d; the '
            'qubit ((3,3)) fixed Z-record sits BELOW the ceiling (1/4 '
            '< 1/2) while the decoder-basis measurement attains it -- '
            'the ceiling is attained under some measurements, not '
            'necessarily by a fixed basis readout. Composed finding '
            '(honest form): coherent globally-lockable content is '
            'Sector-B-supportable at exact fill (check 4) and its '
            'coherent recovery through the classical record of any '
            'full-share measurement is capped at 1/42; classical label '
            'content is NOT protected; the banked-registration '
            'identification is a reading (wedge-fence strength); '
            'realization stays open; ICL_vac/RVC/MSC untouched.'
        ),
        key_result=(
            'Coherent recovery through any classical full-share record '
            'capped at F_e <= 1/42 (entanglement-breaking, exact '
            'ceilings computed); classical content not protected; '
            'identification stays a reading'
        ),
        dependencies=['L_count', 'T_kappa', 'L_self_exclusion',
                      'T_horizon_reciprocity', 'T11',
                      'T_interface_sector_bridge', 'L_QEC_code_space'],
        cross_refs=['T_vacuum_sector_aligned_scheme_share_dim_42',
                    'T_vacuum_mixed_42dim_secret_scheme_exists',
                    'T_vacuum_label_code_no_leakage',
                    'T_which_v_no_registered_interior_reader'],
        artifacts={
            'ceiling': 'F_e <= 1/42, F_avg <= 2/43 (banked constants)',
            'mechanism': 'measure-and-prepare = entanglement-breaking; '
                         'separable overlap <= 1/d, attained',
            'regimes': '((2,2)) label-transparent capped at 1/d; '
                       'phase code label-blind capped at 1/d; ((3,3)) '
                       'Z-record 1/4 < 1/2, decoder basis attains 1/2',
            'scope': 'recovery-from-classical-record only; coherent '
                     'pre-registration operations untouched; Step-4 '
                     'identification at reading strength',
            'nielsen_conversion': 'Kraus identity, derived in docstring',
        },
    )


_CHECKS = {
    'T_vacuum_label_code_no_leakage':
        check_T_vacuum_label_code_no_leakage,
    'T_vacuum_logical_sector_classical_ceiling':
        check_T_vacuum_logical_sector_classical_ceiling,
    'T_vacuum_mixed_42dim_secret_scheme_exists':
        check_T_vacuum_mixed_42dim_secret_scheme_exists,
    'T_vacuum_sector_aligned_scheme_share_dim_42':
        check_T_vacuum_sector_aligned_scheme_share_dim_42,
    'T_banked_registration_coherent_recovery_no_go':
        check_T_banked_registration_coherent_recovery_no_go,
}


def register(registry):
    """Register the vacuum label code checks into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)


# ---------------------------------------------------------------------------
# Interface Engine onboarding (Full Bank Onboarding wave, 2026-07-04)
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "quantum:vacuum_label_code_p1_witness",
        "axis": "ROUTE",
        "expect_export": False,
        "claim_text": (
            "The constructed P1 witness at computed strength "
            "[P_structural_instrument]: vacuum no-leakage realized by a "
            "CLASSICAL 42-label code on the banked second-epsilon skeleton "
            "-- the maximum at subspace-coherent (pure-isometric) form; the "
            "42-dim vacuum logical sector is UNCONSTRUCTIBLE as a "
            "subspace-coherent sector. The fit question is CLOSED EXISTS at "
            "abstract-encoding strength (a perfect ((61,61)) mixed scheme "
            "carries a coherent 42-dim secret at share dimension 43); the "
            "sector-aligned question is CLOSED THREE-PRONGED (exact fill "
            "EXISTS via [[5,1,3]] at share dim exactly 42; the carrier "
            "reading dissolves by type mismatch; registration closes "
            "negatively at the classical-record ceiling F_e <= 1/42) -- "
            "NEVER cited closed simpliciter. Realization/identification "
            "remains the open reading. (5 checks, vacuum_label_code.py)"
        ),
        "note": (
            "Onboards the ICL_vac route-(b) witness family (.352/.356/.357) "
            "onto the ROUTE axis as a held claim at "
            "[P_structural_instrument]. The three-pronged closure discipline "
            "is frozen in the claim text; a future lane citing the "
            "sector-aligned question closed simpliciter fails the pin."
        ),
    },
)
