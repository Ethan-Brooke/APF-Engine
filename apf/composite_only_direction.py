"""The composite-only direction of the real bipartite GPT, computed and identified.

WHAT THIS ADDS, AND WHAT IS STANDARD (read this first).

The bank knows the INTEGER.  check_T_field_selection_complex
(quantum_admissibility.py) computes Delta_R(n, m) = K_R(nm) - K_R(n) K_R(m)
and verifies Delta_R > 0 on the sixteen shapes with 2 <= n, m <= 5.  It does
not say WHICH state parameters the integer counts.  It is an unidentified
surplus.

This module identifies it:

    Sym(R^n (x) R^m)  =  [Sym(R^n) (x) Sym(R^m)]  (+)  [Lam(R^n) (x) Lam(R^m)]

so the parameters no product observable can read are EXACTLY the
antisymmetric-tensor-antisymmetric directions, and

    Delta_R(n, m)  =  dim Lam(R^n) . dim Lam(R^m)  =  [n(n-1)/2] . [m(m-1)/2].

At (n, m) = (2, 2) that is one direction, spanned by J (x) J with
J = [[0,-1],[1,0]], and the module turns the count into two DISTINCT valid
real states with identical statistics under every product measurement, on any
number of copies.

NONE OF THE UNDERLYING MATHEMATICS IS NEW AND NONE OF IT IS BILLED AS NEW.
The decomposition is the GL(n) x GL(m) branching of the symmetric square --
Fulton and Harris, Representation Theory: A First Course, GTM 129, Springer
(1991), Ex. 6.11; equivalently Cauchy's identity, Macdonald, Symmetric
Functions and Hall Polynomials, 2nd ed., Oxford (1995), I.(4.3) and its
dual (4.3').  That real quantum theory fails local tomography, with a
parameter count of exactly this shape, is standard: Wootters, "Local
accessibility of quantum states", in
Zurek (ed.), Complexity, Entropy and the Physics of Information (1990);
Hardy, "Quantum theory from five reasonable axioms", arXiv:quant-ph/0101012
(2001).  (An earlier version cited Araki, Commun. Math. Phys. 75, 1 (1980),
at three sites for that parameter count.  Araki characterizes the state space;
it does not carry the local-tomography count, and the citation is withdrawn.
Wootters and Hardy carry it and were already named.)  What is executed here is
the identification, its tie to the bank's own integer, and a witness pair.

------------------------------------------------------------------------------
THE ARITHMETIC IDENTITY IS PROVED FOR ALL n, m; THE SPAN STATEMENT IS NOT
------------------------------------------------------------------------------
Two different sentences used to be carried by one citation.  They are
separated, and the shape counts behind them are separated too.

  PROVED HERE, FOR ALL n AND m, SYMBOLICALLY.  Leg D_sym runs a three-line
  polynomial computation in the bivariate ring Q[n, m]:

      K_R(nm) - K_R(n) K_R(m)
        = nm(nm+1)/2 - [n(n+1)/2][m(m+1)/2]
        = nm[2(nm+1) - (n+1)(m+1)]/4
        = nm(n-1)(m-1)/4
        = [n(n-1)/2][m(m-1)/2].

  The three polynomials are evaluated against the BANKED K_dim_real on a
  49-point integer grid, so the symbolic object is the bank's own count and
  not a parallel definition.  The grid's size, its distinctness, the 36 of
  its points that carry a nonzero defect, and two executed rejections of
  perturbed candidates are each computed as legs.  The MAY-NOT-CITE bar on
  "Delta_R(n,m) = A_n A_m for all n, m" is therefore LIFTED for the
  arithmetic.

  NOT PROVED HERE.  Two different counts, on two different numbers of shapes.
  The CODIMENSION equality -- dim Sym(R^{nm}) minus the rank of the
  product-observable span equals the banked Delta_R -- is executed on NINE
  shapes: the six of legs A-D plus (4,4), (3,5), (5,5) at leg D'''.  The
  ORTHOGONAL-COMPLEMENT identification -- that span(Lam (x) Lam) IS the
  orthogonal complement, which needs the HS-orthogonality legs and the
  spanning legs, not a rank alone -- is executed on the SIX shapes only.  The
  step from either to ALL n, m is the branching identity, which is a NAMED
  PREMISE with a citation rather than a sentence of prose.  That bar STANDS.

------------------------------------------------------------------------------
THE WITNESS PAIR, AND WHY IT IS THIS ONE
------------------------------------------------------------------------------
An earlier draft exhibited sigma_{+1/8} and sigma_{-1/8} from the family
sigma_t = I/4 + (1/8) Z (x) Z + t J (x) J.  A blinded audit found, correctly,
that those two are related by a LOCAL REFLECTION on Alice's side alone:
with O = diag(1, -1), (O (x) I) sigma_+ (O (x) I)^T = sigma_- exactly.  A
reader is then entitled to say the hidden parameter is a local
frame-orientation sign -- gauge, not physics.  That relation is COMPUTED at
leg H here and disclosed rather than left for the next auditor.

THE WITNESS PAIR OF RECORD IS DIFFERENT.  With

    R       =  I_4/4  +  (X (x) X + Z (x) Z)/16 ,
    rho_+-  =  R  +-  (J (x) J)/32 ,

both are density matrices, and their characteristic polynomials DIFFER:

    spec(rho_+) = {13/32, 7/32, 7/32, 5/32},
    spec(rho_-) = {11/32,  9/32, 9/32, 3/32},

verified as an exact polynomial identity, not by root-finding.  Distinct
spectra rule out EVERY conjugation, orthogonal or unitary, local or global.
The gauge objection is closed rather than mitigated.

THE MECHANISM, EXECUTED, AND STATED AT ITS ACTUAL STRENGTH.  The partial
transpose does not merely preserve the pair's spectra: it maps the two states
onto each other AS MATRICES,

    PT_A(rho_+) = rho_-   and   PT_A(rho_-) = rho_+,

exactly.  (An earlier version said "charpoly(PT(rho_+)) = charpoly(rho_-)",
which is the weaker consequence of what the leg computes.)  The composite-only
direction IS the PT-odd part -- PT_A(J (x) J) = -J (x) J while PT_A(R) = R,
both computed -- and that single fact is what makes the pair invisible to
product observables and what makes both of them PPT.

------------------------------------------------------------------------------
BOTH ARE PPT.  THE FIELD MATTERS, AND IT WAS GOT WRONG BEFORE
------------------------------------------------------------------------------
Horodecki, Horodecki and Horodecki, Phys. Lett. A 223, 1 (1996), is a theorem
about a COMPLEX Hilbert space: on C^2 (x) C^2, positivity under partial
transpose is equivalent to separability.  Its FIELD hypothesis is as
load-bearing as its dimension hypothesis, and an earlier version of this
module checked only the dimension one and concluded, from PPT, that the pair
is separable and therefore "the defect is not an entanglement phenomenon".

THAT SENTENCE IS FALSE AND IS DELETED.  In the REAL product cone the pair is
NOT separable, and the refutation is one line, computed here rather than
imported.  For any real SYMMETRIC A, Tr(J A) = 0 -- the functional is linear
and vanishes on a basis of Sym(R^2), which is computed -- so for real
symmetric A and B,

    Tr[(A (x) B) . (J (x) J)]  =  Tr(J A) . Tr(J B)  =  0.

Every real-separable state is a convex combination of such products, so EVERY
real-separable state has composite coefficient exactly zero.  An explicit
three-term real product mixture is exhibited at coefficient 0.  The witness
pair sits at +1/8 and -1/8.

    AT (2,2) A NONZERO COMPOSITE-ONLY COORDINATE IMPLIES THAT THE STATE IS
    NOT SEPARABLE IN THE REAL PRODUCT CONE.

THAT IS ONE DIRECTION, AND IT IS THE ONLY ONE PROVED.  An earlier version
wrote the slogan as an identification -- "the composite-only coordinate IS
the real-entanglement coordinate" -- which asserts the converse as well: that
every real-inseparable state at (2,2) has a nonzero J (x) J coefficient.  The
converse is not computed anywhere in this module.  (An auditor's linear
program over 14,400 real product states found no counterexample to it, so it
is probably true; probably true and computed here are different things, and
only one of them may be cited.)  The bar is in MAY-NOT-CITE.

What PPT plus Horodecki buys, and all it buys, is that the pair is separable
IN THE COMPLEX EMBEDDING -- which is exactly what a 2x2 PPT test sees.

THE SHARPER POSITIVE STATEMENT THIS OPENS, also computed.  J (x) J is not a
product of two real symmetric observables (it is outside the product span,
computed at leg W).  But J (x) J = -(iJ) (x) (iJ) = -Y (x) Y with Y Hermitian.
The missing direction becomes an ordinary LOCAL PRODUCT observable exactly at
complexification, and not before.  That sits beside the leg-E(iii) result that
the complex codimension is zero: the same complexification that closes the
count is the one that turns this direction into a product observable.

------------------------------------------------------------------------------
MULTI-COPY INVISIBILITY -- NOW GENERAL IN k
------------------------------------------------------------------------------
Leg K executes, at k = 1, 2 and 3, as exact matrix identities on the
regrouped k-copy system:

    rho_+^{(x)k} - rho_-^{(x)k}  =  2 sum_{|S| odd} eps^{|S|} (x)_j T_j(S),

with eps = 1/32, T_j = J (x) J for j in S and R otherwise; the difference is
PT_A-ODD; and it is annihilated by every real symmetric collective local
effect E_A (x) E_B in a battery of SIX PAIRWISE DISTINCT PAIRS assembled from
FIVE distinct matrices -- both counts computed on the battery object that was
built -- while a GLOBAL effect separates the pair.  The pairing list that
carries the blindness leg and the nonzero global reading are computed in ONE
expression over ONE difference matrix, so the two are values of the same
object.

THE GENERAL-k SENTENCE NO LONGER RESTS ON THE THREE EXECUTED VALUES.  Once
PT_A(rho_+) = rho_- holds as a MATRIX IDENTITY -- which it does, computed --
the argument is immediate for every k:

    PT_A(rho_+^{(x)k}) = (PT_A rho_+)^{(x)k} = rho_-^{(x)k},

so D_k = rho_+^{(x)k} - rho_-^{(x)k} is PT_A-odd at every k; every real
symmetric E_A (x) E_B is PT_A-even (computed); and the transfer identity
Tr(PT_A(M) N) = Tr(M PT_A(N)) with the involution gives

    Tr(D_k E) = Tr(PT_A(D_k) PT_A(E)) = -Tr(D_k E),   hence  0,  for ALL k.

THE CHAIN IS NOT EXECUTED AS A CHAIN, AND AN EARLIER VERSION OF THIS
PARAGRAPH SAID IT WAS.  Every quantity along it -- Tr(D_k E),
Tr(PT_A(D_k) PT_A(E)), and their negatives -- is ZERO whenever the statement
is true, so a leg comparing them compares zeros and has nothing to
distinguish.  Two legs per k did exactly that; they are DELETED rather than
repaired, because a chain of equalities among vanishing quantities cannot be
made non-degenerate.  What carries the argument with something at stake is
elsewhere and stays: the difference is computed PT_A-odd at each k, a real
symmetric collective product effect is computed PT_A-even at each k, and the
transfer identity is executed at leg P on a witness list carrying a NONZERO
reading.  The only general input is that the partial transpose distributes
over the tensor product of copies -- elementary index bookkeeping, executed at
k = 1, 2, 3 on a NON-SYMMETRIC probe, and named as a premise.  The previous
restriction "nothing here may be cited as verified for all k" is lifted, and
replaced by an honest statement of what carries it: an exact matrix identity
plus two named elementary facts.  The finite verification stays as
corroboration rather than as the argument.

------------------------------------------------------------------------------
STATEMENTS
------------------------------------------------------------------------------

check_L_real_composite_only_direction_is_lambda_tensor_lambda
    tier 3, [P_math]

  LEG P   predicate witnesses -- every predicate is exercised against a FALSE
          input ON THE AXIS IT IS USED FOR.  This covers the COMPLEX
          primitives too: cmul is computed on i^2 = -1, ckron on two written-out
          literals, cflat by a rank witness that separates i from 1.  is_psd
          is given a minor of magnitude 10^-6 on the negative side, and its
          SYMMETRY precondition is exercised on [[1,2],[0,1]], whose principal
          minors are all non-negative.  hs is computed against a non-symmetric
          pair on which the transposed convention answers 1, and the two
          conventions are TIED BY VALUE on that same pair and required to
          DISAGREE.  charpoly is computed on a NON-PALINDROMIC literal, so the
          coefficient order is fixed by the literal.  p_eval's VARIABLE ORDER
          is fixed by a leg: every polynomial in play is symmetric in n and m.
          The self-comparison refusals in product_sweep,
          correlator_vectors_of_pair, _distinct and _distinct_lists are
          exercised on both sides.
  LEG A   dim Sym(R^N) computed by rank of an explicit basis, N = nm.
  LEG B   the locally generated span: rank of {A (x) B}; equals K_R(n) K_R(m).
  LEG C   the Lam (x) Lam family: symmetric, independent, HS-orthogonal to
          EVERY local generator in two independent forms, and local +
          Lam (x) Lam spans Sym(R^N).  The identification is two-way.  SIX
          shapes.  The orthogonality loop reads its two generator lists
          through _distinct_lists, which refuses a single list handed twice.
  LEG D   the codimension equals composite_defect(K_dim_real, n, m), called
          LIVE from the bank, on six shapes, and equals A_n A_m.
  LEG Dsym THE CLOSED FORM PROVED IN Q[n, m], evaluated against the banked K
          on a 49-point grid whose size, distinctness, non-degeneracy and
          separating power are themselves legs.
  LEG D'  the BEHAVIOUR of the imported symbol, on probes where the closed
          form and the defect disagree: 0 on K(N) = N, -8 on the banked
          quaternionic count.
  LEG D''' the bank value at THREE FURTHER SHAPES for which this module ships
          no literal, taking the codimension count from six shapes to nine.
          NOT a relation with two live ranks -- see the correction below.
  LEG D'' THE BANKED SIBLING, called live and found to AGREE, in magnitude
          and in sign, with its own prose and with this module.
          Provenance is asserted by OBJECT IDENTITY against the freshly
          imported bank module, and the numbers are read out of the R clause
          STRUCTURALLY, by position, not by substring.  ALL
          SIX sibling numbers are parsed -- R joint and local, C joint and
          local, H joint and local -- and every comparison is guarded on the
          parse having returned an integer, so a moved clause HEADING yields a
          record rather than a TypeError.
  LEG E   MUST-BITE CONTROLS: drop a local generator, the codimension moves;
          add J (x) J, it dies; the same machinery over C returns zero.
  LEG F   THE CORRECTION: the direction is NOT the singlet projector, and not
          up to an additive identity term either.
  LEG G   the singlet placed; the coefficient 1/4; and THE MAXIMALITY OF THAT
          COEFFICIENT, COMPUTED, by two routes.  THE MAXIMIZERS ARE A
          CONTINUUM: J (x) J has +1 eigenspace of dimension 2, computed, and a
          one-parameter family of distinct pure states inside it all attain
          the bound.  "The direction singles out the singlet" fails not by
          three counterexamples but by a two-dimensional eigenspace.
  LEG H   THE INTERVAL, closed, for sigma_t -- retained because the range of
          the composite coordinate is worth having -- TOGETHER WITH THE
          COMPUTED DISCLOSURE that the sigma endpoints are related by a local
          reflection and are therefore NOT the witness pair.
  LEG W   THE WITNESS PAIR OF RECORD, rho_+-: states, spectrally
          inequivalent by exact characteristic polynomials, zero separations
          over the 3x3 basis products and the 49-pair sweep -- both run
          through a sweep routine that RETURNS THE PAIRS IT TESTED, so the
          "forty-nine" is what ran and not a re-derivation from a module
          constant, and that REFUSES a self-comparison -- separated by
          the global J (x) J at difference exactly 1/4, both PPT hence
          separable IN THE COMPLEX EMBEDDING, NOT separable in the real
          product cone, and mapped onto each other exactly by the partial
          transpose.  The projective-measurement pair, the difference pair and
          the superseded sigma pair are each taken through _distinct.
  LEG K   MULTI-COPY, executed at k = 1, 2, 3, with the general-k argument
          above carried by the exact PT identity.  The collective effect
          battery is BUILT ONCE from two hoisted seed lists and every leg
          about it reads the object that was built, not the seed list
          re-derived as a literal.  The blindness values and the nonzero
          global value are entries of ONE list computed over ONE difference.
  LEG EV  THE SHIPPED EVIDENCE, tied by value to the computation that
          produced it, for the entries named in CERTIFIED_EVIDENCE_KEYS_*.
          Everything else in `ev` is descriptive and uncertified, and says so.

check_L_bipartite_chsh_blind_to_composite_only_direction
    tier 3, [P_math | bipartite single-source: a READING FENCE, not a premise]

  LEG P2  the sqrt-free polytope decision validated against the banked
          _in_local_polytope on 1296 rational vectors covering both verdicts,
          with the battery's SIZE and its six-value alphabet computed as legs
          rather than reported as evidence.
          THE BOX CLAUSE IS EXERCISED AT k != 1, which is the only regime
          any downstream use is in: w = (3/2, 0, 0, 0) is OUTSIDE at k = 2 and
          INSIDE at k = 4, no facet is violated at either scale, and the three
          plausible mis-scalings (v^2 > k*k, v^2 > 1, |v| > k) each get the
          wrong answer on one of the two.  The FACET clause is separately
          exercised at k = 2.
  LEG A2  the exhibit is well formed; the rescale constant Ksq is READ OFF the
          settings, not written down.
  LEG B2  the raw combination is -4 exactly, SIGN KEPT; CHSH^2 = 8.
  LEG C2  the banked facet set consulted live; THE SIGN GUARD IS EXERCISED on
          a synthetic non-negation-closed list where removing it flips a
          verdict.
  LEG D2  nonclassicality decided on the TRUE correlator vector, sqrt-free.
  LEG E2  THE BRIDGE: every CHSH correlator is an expectation of a product
          observable, so it cannot see the composite-only coordinate.
          Computed on the FUNCTIONAL and on the rho_+- STATES, the latter
          through correlator_vectors_of_pair, which refuses a pair whose two
          members are the same matrix.  The interval endpoints go through the
          same routine.

------------------------------------------------------------------------------
THE RESULT ARCHITECTURE
------------------------------------------------------------------------------
Neither check reports "green because nothing was appended to a failure list".
That architecture treats silence as evidence: strip a check of all its
assertions and it still returns green.

Instead each check builds ONE dictionary

    legs[label] = <predicate value>

and the verdict is

    passed = (set(legs) == EXPECTED_LEGS[name]) and all(legs.values())

against a frozenset of labels WRITTEN OUT AS LITERALS below.  The comparison
is set-exact.  Three further literals are read inside _enforce_leg_inventory(),
which _result() calls on the record it is about to return, and _result() is
the function every check returns through, hence on the path
verify_all.run_module executes:

  1. SET-EXACT against the frozen EXPECTED_LEGS literal, read inside the gate
     and not through whatever local variable the caller used;
  2. EXPECTED_LEG_COUNTS, the number of legs each check evaluates, compared
     against every count in play at once;
  3. EXPECTED_LEG_DIGEST, the SHA-256 of the sorted label list, computed on
     the EVALUATED labels and separately on the FROZEN set;
  4. the verdict RE-DERIVED from the returned fields and compared with the
     reported one.

run_all() computes the same four on the returned record.  verify_all.run_module
never calls run_all(); it enumerates a module's `check_*` attributes and calls
each one directly.

THE GATES RAISE RATHER THAN RETURNING passed = False, DELIBERATELY.  verify_all
grades a returned passed=False as FLAG and an exception as FAIL.  A FALSE
PREDICATE is a claim of this module turning out untrue: the record is intact,
the failing labels are in it, and it is returned as a FLAG -- and, because
verify_all prints `ret.get("summary") or ret.get("key_result")`, the record
carries a `summary` naming the failing labels, so a FLAG prints those and not
this module's key_result.  A BROKEN INVENTORY is not a result -- the record no
longer describes what ran, so no field of it should be read or quoted -- and it
is raised.

WHAT THE LEG INVENTORY IS, AND WHERE ITS FLOOR ACTUALLY SITS.  The leg
inventory is a review device, not tamper evidence.  A previous version of this
paragraph said that REMOVAL of a leg is a four-site diff -- the leg, its label
in EXPECTED_LEGS, the count literal and the digest literal.  THAT IS WRONG ON
THE BANK PATH, WHERE THREE SITES SUFFICE: delete the
`_enforce_leg_inventory(record)` call from _result(), strip the leg, and
delete its label from EXPECTED_LEGS, and both checks return passed = True.
The count and the digest literals are never consulted, because the only site
that reads them is the call that was removed.

GUTTING THE GATE BODY IS A DIFFERENT EDIT, AND WHAT IT LEAVES BEHIND IS
STATED HERE BECAUSE AN AUDITOR ASKED FOR IT.  _result() computes
`passed = (seen == expected) and all(legs.values())` against the frozen
EXPECTED_LEGS literal itself, before the gate is called at all, so a leg
stripped without its label yields passed = False -- a FLAG -- with the gate
body empty.  The gate CALL supplies the FLAG -> FAIL upgrade and the count and
digest comparisons; the set comparison that yields the FLAG is not in it.

The inventory does nothing at all against a predicate stubbed to a literal,
against a leg evaluated on the wrong object, or against an edit to _result()'s
own return statement.  Those are visible only to a reader.

The free-standing ck()/fails.append() machinery is REMOVED, not kept
alongside; there is no second path by which a leg can be recorded.  The `_leg`
helper raises on a duplicate label and raises on a verdict that is not
literally True or False.

THE EVIDENCE DICT USED TO SIT OUTSIDE ALL OF THIS.  Inflating the reported
CHSH^2 from 8 to 16 in `ev` left every leg of the previous version green, so
a number a reader would quote was uncertified while every number a leg
computed was not.  The entries named in CERTIFIED_EVIDENCE_KEYS_1 and
CERTIFIED_EVIDENCE_KEYS_2 are TIED BY VALUE to the computation that produced
them, by the EV legs at the end of each check.  EVERY OTHER ENTRY OF `ev` IS
DESCRIPTIVE AND UNCERTIFIED, and this sentence is the disclosure.

CERTIFICATION IS PER KEY, AND TWO OF THOSE KEYS ARE TABLES.  `real_shapes`
and `multicopy` are lists of rows, and a previous version tied only the
columns that some other leg happened to cross-reference -- so
ev['real_shapes'][i]['rank_local'] = 999 passed.  Which column was protected
was an accident of what else was being compared.  Every column of both tables
is now compared, as a whole row, against the values held from the loop that
produced them.  What that comparison is, stated exactly: a tie to a RETAINED
value, not to an independent recomputation -- see KNOWN LIMITS.

ONE ITEM IS STRUCK FROM THAT LIST.  A literal True written over
ev['multicopy'][i]['pt_A_odd'] stood beside rank_local = 999 in an earlier
version of this paragraph, as a second thing that passed.  It does not belong
there.  The value that column carries IS True at every row -- that is the
multi-copy parity result -- so writing True over it changes no byte of the
record.  It is an EQUIVALENT MUTANT: nothing in this module or outside it can
register a difference, and the mutation harness installs it only in the
PAIRED form that also makes the computed predicate false.

------------------------------------------------------------------------------
GRADE, PREMISES, DEPENDENCIES
------------------------------------------------------------------------------
Both checks are [P_math].  NO REGIME PREMISE IS CONSUMED ANYWHERE.

  THE [P_regime] HALF IS DELIBERATELY NOT TAKEN.  check_T_field_selection_complex
  is graded [P_regime + P_math] in its own module.  Its [P_math] half is the
  arithmetic Delta_R(n,m) = K_R(nm) - K_R(n) K_R(m); its [P_regime] half is the
  step from a positive defect to INADMISSIBILITY, which rests on
  Composite-Continuation Tomography being the selected regime.  This module
  consumes the arithmetic ONLY.  It does not say, anywhere, that the exhibited
  system is APF-inadmissible, and nothing here may be cited for that.

  MODELLING DEFINITION -- the structural premise, named FIRST because it is
  where the physics enters:
  LOCAL_PRODUCT_OBSERVABLE_MODEL -- "what a pair of local measurements can
  read" is modelled as the real span of {A (x) B : A in Sym(R^n),
  B in Sym(R^m)}.  This is the standard local-tomography span; it is a
  DEFINITION OF THE MODEL, not a theorem proved here.  It covers joint outcome
  statistics of arbitrary local measurements, since each joint outcome
  operator is a product of the two local spectral projectors, hence in the
  span; leg H exercises this on an explicit projective pair, and leg K extends
  the same modelling choice to collective effects on k copies per side.

  PSD_CONE_CONVEXITY -- the set of PSD matrices is convex.  Used at leg H to
  close the interval |t| <= 1/8 from its two endpoints.  Structural, named
  here rather than buried below the citation list.

  NAMED STANDARD IMPORTS, each load-bearing where stated:
    HOROD_1996_PPT_SEPARABLE -- M. Horodecki, P. Horodecki and R. Horodecki,
      Phys. Lett. A 223, 1 (1996): on a COMPLEX Hilbert space at 2x2 (and
      2x3), positivity under partial transpose is EQUIVALENT to separability.
      THE FIELD HYPOTHESIS IS AS LOAD-BEARING AS THE DIMENSION HYPOTHESIS.
      The dimension hypothesis is COMPUTED at leg W; the field hypothesis is
      RECORDED there, because a field hypothesis is not a computational
      predicate and calling it "checked" -- as an earlier version did, over a
      leg that conjoined a tautology with two constant lookups -- says more
      than the code does.  THE MODULE COMPUTES PPT; IT DOES NOT COMPUTE
      SEPARABILITY.  What the import licenses is separability IN THE COMPLEX
      EMBEDDING, and nothing else.
    REAL_PRODUCT_CONE_COEFFICIENT -- COMPUTED HERE, not an import: Tr(J A) = 0
      for every real symmetric A, hence the J (x) J coefficient of every
      real-separable state is zero, hence the witness pair is NOT separable in
      the real product cone.
    GL_BRANCHING_OF_THE_SYMMETRIC_SQUARE -- S^2(V (x) W) = (S^2 V (x) S^2 W)
      (+) (Lam^2 V (x) Lam^2 W) as a GL(V) x GL(W) representation.
      Fulton-Harris (1991) Ex. 6.11; equivalently Macdonald (1995),
      the Cauchy identity I.(4.3) and its dual (4.3').
      LOAD-BEARING FOR THE GENERAL-(n,m) SPAN STATEMENT AND FOR NOTHING ELSE.
      It was previously carried in prose with no citation while five more
      elementary facts were named; that asymmetry is corrected.
    SPECTRAL_THEOREM_FINITE_DIM -- used at legs G and H to pass from the
      computed facts (J (x) J)^2 = I and Tr(J (x) J) = 0 to the eigenvalue
      list (+1, +1, -1, -1).  Every positivity verdict actually REPORTED is
      computed by exact principal minors and does not rest on it.
    PSD_TRACE_PAIRING -- Tr(A B) >= 0 for PSD A, B.  The route leg G
      executes for the maximality of 1/4.
    SIMILARITY_INVARIANCE_OF_CHARPOLY -- conjugation preserves the
      characteristic polynomial.  This is what turns "the charpolys differ"
      into "no conjugation relates them" at leg W.
    PARTIAL_TRANSPOSE_TENSOR_FUNCTORIALITY -- the partial transpose of a
      tensor product of copies, on the regrouped A-side, is the tensor product
      of the per-copy partial transposes.  Executed at k = 1, 2, 3 on a
      non-symmetric probe; named because with the exact identity
      PT_A(rho_+) = rho_- it is what carries leg K to ALL k.
    CIRELSON_1980 -- 2 sqrt(2) is the quantum maximum.  B. S. Cirel'son,
      Lett. Math. Phys. 4, 93 (1980).  LOAD-BEARING FOR NO LEG; the word
      "saturates" is not used of any computed result.  CHSH 1969 and Fine
      1982 stand behind the banked polytope, which is called.
    REAL_SINGLET_CHSH_EXHIBIT_PROVENANCE -- THE EXHIBIT IS NOT ATTRIBUTED,
      because it is not attributable.  The singlet measured in two real
      planar bases at 45 degrees is the standard CHSH/Tsirelson
      configuration; it is written down in Clauser, Horne, Shimony and Holt,
      PRL 23, 880 (1969) and in Cirel'son (1980), and it predates every paper
      named below.  A previous version credited it to Gisin and Peres,
      Phys. Lett. A 162, 15 (1992); that over-credits, and is withdrawn.
      What that paper is, and it is not what an earlier version of this
      docstring said it was: N. Gisin and A. Peres, "Maximal violation of
      Bell's inequality for arbitrarily large spin", Phys. Lett. A 162, 15
      (1992) -- GISIN IS THE FIRST AUTHOR, and an earlier version of this
      module wrote the correction itself the wrong way round.  It does not
      carry a general real-representability statement.
      McKague, Mosca and Gisin cite it for the narrower fact that the optimal
      CHSH observables can be written real in the Schmidt bases; that is the
      only thing it is cited for here, and the earlier description of it is
      withdrawn along with the attribution.  Two versions ago the exhibit was
      credited to McKague, Mosca and Gisin, PRL 102, 020505 (2009); withdrawn
      earlier for the same reason.  MMG themselves (Sec. III.B) attribute the
      BIPARTITE real-representation result to a PERSONAL COMMUNICATION (2007)
      from Navascues, Acin, Pironio and Gisin -- that entry in their reference
      list is a personal communication, not a paper, and an earlier version of
      this module cited it as though it were one -- and to Pal and Vertesi,
      PRA 77, 042105 (2008); a previous version of this module named only Pal
      and Vertesi out of that list.  MMG's own contribution is the
      multipartite extension, and they remain the citation of record for the
      real-Hilbert-space SIMULATION claim, which is where they are still used.

DEPENDENCIES (live calls into the bank):
  apf.quantum_admissibility.composite_defect, K_dim_real, K_dim_complex,
      K_dim_quaternionic
  apf.third_boat_no_extension._chsh_facets, _dot, _in_local_polytope,
      CLASSICAL_CHSH_BOUND
  apf.closed_world_completeness.check_T_split_composite_gates_tomographic_locality
      -- called live at leg D'' ONLY to pin its six reported numbers.  Nothing
      downstream of leg D'' uses its numbers.

  WHAT "LIVE CALL" DOES AND DOES NOT BUY, STATED PLAINLY, AND FOR EVERY
  IMPORTED SYMBOL AND NOT ONLY FOR composite_defect.  An earlier version
  scoped this disclosure to composite_defect alone; it applies equally to
  _chsh_facets, _in_local_polytope and the K_dim_* family.  Each of those is
  a deterministic pure function or a constant list, so each can be replaced
  by a faithful local reimplementation -- a transcription table, an inlined
  formula, a written-out facet list -- with no leg of this module going red.
  A previous version claimed the composite_defect call was "certified at leg
  E(iii), where the module computes no closed form"; that was false twice
  over -- there IS a closed form at leg E(iii), namely the constant 0, and
  substituting it passes.  The claim is withdrawn and is not replaced by a
  weaker version of itself.

  THE ONE PLACE THE MODULE WAS UNDER-STATING ITSELF, NOW WITH ITS RANGE
  ATTACHED: K_dim_real is not in that list unconditionally.  Patching
  K_dim_real INSIDE the bank module is caught at leg A, because leg A compares
  K_dim_real(N) against the rank of an explicitly constructed symmetric basis
  -- two independent computations of the same integer.  THAT HOLDS ONLY AT THE
  ARGUMENTS THIS MODULE EXERCISES: N in {4, 6, 8, 9, 10, 12} at leg A, and
  N = ab with a, b <= 7 on the leg-D_sym grid, where the comparison is against
  the symbolic polynomial rather than a basis rank.  A patch that moves no
  value in that range is not caught, and neither is a faithful
  reimplementation of K_dim_real here, which returns the same integers.

  What the module does instead is raise the number of simultaneous arithmetic
  relations a transcription would have to satisfy.  Leg D' computes the
  imported symbol's BEHAVIOUR as a higher-order function of the K it is handed
  (0 on K(N) = N; -8 on the banked quaternionic count, a value no A_n A_m can
  take).  Leg D''' computes the bank value at three FURTHER shapes -- (4,4),
  (3,5), (5,5) -- for which this module ships no literal.

  A BILLING WITHDRAWN AT LEG D'''.  A previous version described that leg as
  putting the bank value into "a NON-TRIVIAL relation with TWO live ranks",

      dim Sym(R^{nm}) - rank(under-generated list)
          =  composite_defect(K_dim_real, n, m) + (rank(full) - rank(under)).

  It is not.  Substituting the two definitions, rank(under) CANCELS between
  the sides and the statement reduces to dim - rank(full) = Delta_R -- the
  ordinary codimension identity, with ONE live rank -- and PROBE_DROP is
  unconstrained by it.  The extra shapes are real content and stay; the
  description does not.  The leg now states the reduced form directly and
  keeps the under-generated form as a labelled cross-check.

------------------------------------------------------------------------------
THE BANKED SIBLING NOW AGREES WITH THIS MODULE
------------------------------------------------------------------------------
check_T_split_composite_gates_tomographic_locality (closed_world_completeness.py)
counts full observable dimensions, d_R(n) = n(n+1)/2, and compares

    joint_R = d_R(n_A n_B) = 10   against   local_R = d_R(n_A) d_R(n_B) = 9,

a SURPLUS of one.  This module compares the same joint dimension against the
rank of the span of the product observables, also 9, and computes the same
surplus of one.  The two banked numbers agree in magnitude and in sign, and
the agreement is not a coincidence of (2,2): the surplus is
dim Lambda^2(R^n) (x) Lambda^2(R^m), which is what this module proves for all
n and m, and the sibling recomputes that identity at seven shapes.

An earlier version of the sibling mixed two conventions -- full dimensions for
R and H against a trace-one dimension for C -- and applied the trace-one
composition rule to all three, reporting R as failing by a deficit of five and
H by a deficit of twenty.  Its own docstring already carried the surplus
reading.  The conventions are now consistent, and either one may be used:
subtracting one from each factor and from the joint count cancels, so the
trace-one and full-dimension conventions return the same signed mismatch at
every shape.  They may not be mixed.

Of the two legs that recorded the sibling's disagreement with its own
docstring, one is retired and one is re-pointed.  The retired one asserted the
disagreement itself, which no longer exists.  The re-pointed one asserts the
opposite -- that the sibling's prose carries the same two signs its code
computes.  It is TWO SUBSTRING TESTS.  A docstring edit leaving both
substrings intact passes it, including one that inverts the surrounding
physics prose or restores a superseded number elsewhere in the text.

THE CLAUSE LEGS HAVE A LIMIT.  They parse numbers out of the sibling's
returned key_result, which is an f-string over the sibling's own variables, so
the legs cannot distinguish a computed value from a literal.  A sibling
replaced by a stub returning the same record passes ALL THIRTY Dpp legs, not
only the six clause legs.  A sibling whose key_result is rewritten with the
integers inlined decouples the two entirely.

THE MAINTENANCE INSTRUCTION STANDS, WITH ITS DIRECTION UNCHANGED.  The clause
legs pin the sibling's six numbers by position.  If one goes red because the
sibling moved, update the leg to the sibling's new value; do not revert the
sibling.  The tripwire exists to make a silent divergence loud, not to freeze
a banked check.

LEG D'' READS THE SIBLING STRUCTURALLY.  A previous version matched the
substring "local=15" against the sibling's key_result -- and that string
occurs TWICE there, once in the R clause and once in the C clause, so moving
the sibling's R-local from 15 to 9 left this module green while its docstring
claimed the tripwire "goes red if either number moves".  That claim was false
and is withdrawn.  The leg now isolates the R clause by position, parses
joint and local out of THAT clause only, and separately parses the C clause.
Provenance is asserted on the OBJECT: the imported symbol is required to BE
`apf.closed_world_completeness.check_T_split_composite_gates_tomographic_
locality`, and its code object is required to come from a file named
closed_world_completeness.py.  __module__, __name__ and callability are
computed too, and they are not enough on their own -- a locally defined
function with both attributes reassigned and a matching __doc__ and
key_result passed all four provenance legs of the previous version, as a dict
carrying name, tier, summary and key_result had passed the field-presence
clauses of the version before that.

------------------------------------------------------------------------------
SCOPE -- BIPARTITE, SINGLE-SOURCE ONLY.  A FENCE ON THE READING, NOT A PREMISE
------------------------------------------------------------------------------
Nothing in the second check's computation consumes single-sourcedness: the
legs are exact linear algebra on a 4x4 matrix and a call into the banked
(2,2,2) polytope, and they would return the same values whatever the source
structure of the world.  What the scope fences is what the RESULT may be read
as saying.

The second check licenses nothing about whether nature's algebra is real.  In
a network with INDEPENDENT SOURCES, real and complex Hilbert-space quantum
theory predict different correlation sets -- Renou, Trillo, Weilenmann, Le,
Tavakoli, Gisin, Acin and Navascues, Nature 600, 625 (2021) -- and the real
theory has been experimentally falsified there: Li et al., PRL 128, 040402
(2022); Chen et al., PRL 128, 040403 (2022).  This module cites ONE side of
that question and surveys no rebuttal literature.  What it does record,
because it is settled and relevant, is the SCOPE of that falsification: it
targets real quantum theory without a universal superselection observable.
Real quantum theory WITH one reproduces complex quantum theory
(Stueckelberg, Helv. Phys. Acta 33, 727 (1960); McKague, Mosca and Gisin,
PRL 102, 020505 (2009)) and is not what those experiments rule out.  That is
a statement about what was tested, not a rebuttal, and it is not offered as
one.

------------------------------------------------------------------------------
MAY-NOT-CITE
------------------------------------------------------------------------------
  - "the witness pair is separable in real quantum theory" -- FALSE.  Every
    real-separable state has J (x) J coefficient zero, because Tr(J A) = 0 for
    symmetric A; the pair sits at +-1/8.  Separability holds only in the
    COMPLEX embedding, which is what PPT at 2x2 decides.
  - "the composite-only direction is not an entanglement phenomenon" -- FALSE,
    and it was asserted by an earlier version of this module.  At (2,2) a
    NONZERO composite-only coordinate implies real-inseparability, computed.
  - "at (2,2) the composite-only coordinate IS the real-entanglement
    coordinate" -- OVER-CLAIMED, and an earlier version of this module said
    it.  The proved direction is nonzero => real-inseparable.  The CONVERSE
    -- that every real-inseparable state at (2,2) carries a nonzero J (x) J
    coefficient -- is computed NOWHERE here and may not be cited.  An
    external linear program over 14,400 real product states found no
    counterexample to it; that is an absence of a counterexample in someone
    else's search, not a result of this module.
  - "Horodecki (1996) applies because the system is 2x2" -- incomplete.  The
    theorem's hypotheses are 2x2 AND a complex Hilbert space; a leg that
    checks only the dimension is checking half of them.
  - "the composite-only direction is the real singlet projector" -- COMPUTED
    FALSE at leg F, in two ways.  Also barred: "up to normalization" or "up to
    an additive identity term"; both are refuted there.
  - "the direction singles out the singlet" -- refuted at leg G by a
    TWO-DIMENSIONAL eigenspace of maximizers, not merely by three states.
  - "the exhibited system is APF-inadmissible" -- not claimed; the [P_regime]
    half of check_T_field_selection_complex is not consumed.
  - "real quantum theory is refuted / vindicated"; "quantum mechanics is real".
  - "the inference 'nonclassical correlation therefore complex algebra' is
    refuted" WITHOUT the bipartite single-source qualifier.
  - "real quantum theory is not experimentally distinguishable from complex" --
    false; it is network-falsifiable and has been falsified.
  - "this module cites both sides of the network dispute" -- it cites ONE side
    and says so.
  - "the plethysm decomposition, or the failure of local tomography in real
    quantum theory, is a finding of this module" -- both are standard.
  - "the codimension of the product-observable span equals A_n A_m for all
    n, m" -- the codimension count is executed on NINE shapes and the
    ORTHOGONAL-COMPLEMENT identification on SIX; the general span statement
    rests on the branching identity, a NAMED PREMISE this module does not
    prove.  (The ARITHMETIC identity Delta_R = A_n A_m IS proved for all n, m
    at leg D_sym; that bar is lifted and only that one.)
  - "leg D''' executes a non-trivial relation with two live ranks" -- FALSE.
    The under-generated rank cancels; the statement reduces to the ordinary
    one-rank codimension identity and leaves PROBE_DROP unconstrained.  What
    the leg buys is three further SHAPES, and that is what it may be cited
    for.
  - "the live composite_defect call is certified anywhere in this module" --
    FALSE.  See the disclosure above; the symbol is a pure function of two
    integers and any of its values can be transcribed.  The same is true of
    _chsh_facets, _in_local_polytope and K_dim_complex / K_dim_quaternionic.
  - "leg D'' goes red if ANY sibling number moves" -- this was FALSE of the
    version that used a substring test and FALSE of the version that parsed
    four of six numbers, and it is not restated here in any form.  What the
    leg does is parse all six by position and compare each against a literal.
  - "this module rules on which of the sibling's two readings is right" --
    there are no longer two.  The sibling's prose and code agree, and the
    legs pin its six numbers without ruling on them.
  - "the field hypothesis of Horodecki (1996) is CHECKED here" -- it is
    RECORDED, not checked.  A field hypothesis is not a computational
    predicate; there is nothing to evaluate that could come back False.  The
    DIMENSION hypothesis is computed.  A previous version wrote a leg that
    conjoined a tautology with two constant lookups and called it a check.
  - "the numbers in the evidence dict are certified" -- only the entries
    named in CERTIFIED_EVIDENCE_KEYS_1 and CERTIFIED_EVIDENCE_KEYS_2 are, by
    the EV legs, which tie them by value to the computation.  Every other
    entry of `ev` is DESCRIPTIVE AND UNCERTIFIED.  In the previous version
    none of them were: inflating the reported CHSH^2 from 8 to 16 left every
    leg green.
  - "the reported codimension variable is pinned to the subtraction" -- it
    is not, and it cannot be.  `codim` and the Lam (x) Lam rank are equal at
    every shape here -- that equality IS the result -- so no arithmetic
    relation among the computed numbers can tell `codim = dim - rank` from
    `codim = r_lam`.  What was done instead is that every headline leg at
    leg D recomputes the subtraction on the spot rather than reading the
    variable.  That is a weaker property than a pin and is not billed as one.
  - "the sibling's agreement CONFIRMS this module" -- it does not.  The
    sibling recomputes the same closed form; two checks agreeing on an
    identity one of them proves is concordance, not independent
    corroboration.
  - "Cirel'son's bound is derived" / "the exhibit saturates" -- maximality is
    a named import and is used by no leg.
  - "the real-singlet CHSH exhibit is due to McKague, Mosca and Gisin", or
    to Gisin and Peres -- BOTH withdrawn.  The exhibit is the standard
    CHSH/Tsirelson configuration and predates all of them; it carries no
    attribution here beyond CHSH (1969) and Cirel'son (1980).
  - "Gisin and Peres (1992) carry the general real-representability
    statement" -- WITHDRAWN, and it was asserted by an earlier version of
    this module.  Phys. Lett. A 162, 15 (1992) is "Maximal violation of
    Bell's inequality for arbitrarily large spin"; MMG cite it for the
    narrower fact that the optimal CHSH observables can be written real in
    the Schmidt bases.
  - "Navascues, Acin, Pironio and Gisin (2007) is a paper" -- it is a
    PERSONAL COMMUNICATION in MMG's reference list, and an earlier version of
    this module cited it as though it were a publication.
  - "the composite-only parameter is unobservable" -- it is unreadable by
    real PRODUCT observables in the modelled sense; legs W and K exhibit a
    global observable that reads it, and after complexification it is itself
    a product observable, -Y (x) Y.
  - "rho_+ and rho_- are computed separable" -- PPT is computed; separability
    IN THE COMPLEX EMBEDDING is Horodecki (1996) at 2x2, a named import; and
    in the real product cone they are NOT separable.
  - "sigma_{+1/8} and sigma_{-1/8} differ by a genuinely non-local parameter"
    -- they are related by the local reflection diag(1,-1) (x) I, COMPUTED at
    leg H.  They are the interval endpoints, not the witness pair.
  - "check_T_split_composite_gates_tomographic_locality runs a parallel
    count" -- FALSE, and leg D'' computes why.
  - "the 49-pair product sweep gives coverage beyond a basis" -- it does not;
    dim Sym(R^2) = 3, so at most three of the seven probes per side can be
    independent and nothing outside span{I, Z, X} is reachable.  The extra
    probes are duplicates inside the same span.
  - "the transfer chain at leg K is executed link by link" -- FALSE, and an
    earlier version of this module asserted it in three places.  Every
    quantity in that chain is zero when the statement holds; the two legs per
    k that compared them are withdrawn.  What may be cited is the computed
    PT_A-parity of the difference and of the collective product effects, and
    the transfer identity at leg P.
  - "removal of a leg is a four-site diff" -- FALSE on the bank path, where
    three sites suffice once the gate CALL is one of them.  See THE RESULT
    ARCHITECTURE.
  - "the leg inventory makes a leg strip visible" -- half true and stated
    exactly above: the FLAG comes from _result()'s own comparison against
    EXPECTED_LEGS, not from the gate; the gate supplies the FLAG -> FAIL
    upgrade and the count / digest comparisons.
  - "Phys. Lett. A 162, 15 (1992) is by Peres and Gisin" -- the authors are
    N. GISIN and A. PERES, in that order, and an earlier version of this
    module wrote the correction itself the wrong way round at three sites
    while getting the withdrawal right at four.
  - "the composite-only direction is proved to be outside the product span
    twice" -- it is computed ONCE, at leg W; the second leg was the same
    expression under a second name and is deleted.
  - "the branch / QAC is derived" -- standing corpus bar, untouched.

------------------------------------------------------------------------------
WHAT THIS MODULE DOES NOT SETTLE -- OCCUPANCY (added 2026-08-01, count-neutral)
------------------------------------------------------------------------------
Everything above is about the SPACE.  The direction is identified, its
dimension is proved for all (n,m), and at (2,2) it is exhibited.  NOTHING HERE
SAYS ANY STATE OCCUPIES IT, and no leg computes anything about a coefficient.

A reader arriving at "there is a direction no local observation can reach" is
one step from "therefore the world is complex," and that step is not available.
An unreachable coordinate is exactly the kind of thing a theory may simply
never populate.  v24.3.464 (`apf/composite_orientation_occupancy.py`) computes
what the real theory actually does with the coefficient: the zero-coefficient
sector is nonempty, convex, and carried into itself by every local orthogonal
conjugation, so nothing in the real theory moves it off zero; and the
reachability of the coordinate is field-dependent, so the occupancy question
has no field-neutral form at all.  On that module's reading -- recorded in its
docstring and in none of its legs -- the question is QAC genre: per-interface,
read off the world, not derived.

TWO CONSEQUENCES FOR CITATION.  The bridge packet's Theorems D and E take
ACTUAL COMPOSITE ORIENTATION-PAIR DISTINCTION as their first premise; that
premise is not supplied here and is not supplied there.  And the two modules
NORMALIZE DIFFERENTLY: the witness pair is reported at +-1/8 here, using the
raw pairing, and at +-1/32 in v24.3.464, which divides by <J(x)J, J(x)J> = 4.
Both are correct.  Any comparison across the two must divide.

Survey of record: `APF Reference Docs/Reference - AUDIT-FIRST SURVEY -
Composite Orientation Occupancy (2026-08-01).md`.

------------------------------------------------------------------------------
KNOWN LIMITS
------------------------------------------------------------------------------
Named here rather than left to be found.  None of these is repaired by
anything in this file.

  - A predicate replaced by a literal True keeps its label, and `_leg`
    accepts it because it is a bool.
  - `_leg` itself recording True for every label.
  - An edit to a check's own return statement.
  - A COORDINATED EDIT INSIDE _result().  `passed` and `fail_reasons` are
    computed in the same function from the same `legs` dictionary, and
    _enforce_leg_inventory() re-derives the verdict FROM THOSE TWO RETURNED
    FIELDS.  An edit that sets both together -- `passed = True` with
    `fail_reasons = ()` -- leaves the re-derivation agreeing with itself.  The
    re-derivation compares the reported `passed` against one recomputed
    from `fail_reasons` and the two inventory-difference lists; a record in
    which all four have been edited together agrees with itself.
  - REMOVAL OF THE GATE CALL.  See THE RESULT ARCHITECTURE above: on the bank
    path a leg can be removed in THREE sites, not four, once the
    `_enforce_leg_inventory(record)` call in _result() is one of them.
  - VACUITY AT A QUANTIFIER SITE.  `all(P(x) for x in xs)` is True when `xs`
    is empty, so a comprehension re-pointed at `[]` records True with nothing
    evaluated, and the leg inventory cannot see the difference: the label is
    still there and the count is unchanged.  `all_of(n, ...)` is written at
    61 call sites; it materializes what the
    quantifier consumed and returns True only for exactly n items each
    literally True, and that return value is computed on FALSE inputs at
    P/all_of_rejects_an_empty_quantifier,
    P/all_of_rejects_a_short_quantifier and
    P/all_of_rejects_a_truthy_non_bool.  BARE `all(...)` HAS NOT BEEN
    ELIMINATED, and a previous version of this bullet said that it had.  The
    surviving occurrences, all of them, are:
      * `all(legs.values())` in _result(), which is the check's own verdict
        and not a leg, over a dictionary that is already built;
      * the range-quantifier inside `is_symmetric`, whose range is read off
        the matrix handed in;
      * the range-quantifier inside the zero-matrix branch of
        `is_scalar_multiple`, whose range is read off the matrix handed in.
        THAT BRANCH IS REACHED, and the consequence is a vacuous positive
        control: `is_scalar_multiple(zeros(2), zeros(2))` at
        P/scal_accepts_zero_over_zero is the only call in this module that
        gets to it -- every other call either has a non-zero `b` or returns
        earlier -- so emptying that range returns True with no entry of `a`
        compared, and the leg that is supposed to exercise the branch stays
        green.  An earlier version of this bullet named the site and not the
        consequence;
      * two inside the `wrong = [...]` comprehension that computes the three
        P2/box_variant/*/is_wrong_at_some_tested_scale legs.  An earlier
        version of this bullet said "each of the two is compared against the
        other over `w`", which reads as mutual protection and is not one:
        emptying the VARIANT quantifier ALONE leaves
        `all(variant(x, k_) for x in [])` True at both tested scales, while
        the true clause is False at k = 2 and True at k = 4, so the two
        disagree at k = 2, `wrong` is non-empty, and all three legs stay
        green WITH THE VARIANT FUNCTION NEVER CALLED.  That is a ONE-SITE
        vacuity, not a two-site one.  Those three legs read `wrong != []` --
        a non-emptiness assertion about the list the two quantifiers build,
        and not a universal over `w`.
    A GUARD WRITTEN BESIDE THE QUANTIFIER WOULD NOT HAVE
    CLOSED IT, and the obvious form is the one that fails: `len(xs) == 9 and
    all(P(x) for x in xs)` still passes when the comprehension itself is
    edited to `for x in []`, because `len(xs)` is a different site.  WHAT
    all_of LEAVES OPEN, and it is not small:
      (a) at 56 of the 61 call sites `n` is a written-out literal, so a
          TWO-site edit that empties the comprehension AND moves `n` to 0
          passes.  At the other five `n` is DERIVED from the same objects
          the comprehension ranges over -- `all_of(len(Sn) * len(Sm), ...)`,
          `all_of(len(An) * len(Am), ...)` twice, `all_of(len(lam) *
          len(loc), ...)` and `all_of(len(Hn) * len(Hm), ...)` -- and at
          those five, emptying the source is a ONE-site edit, because the
          count moves with it.  A previous version of this bullet said `n`
          was a written-out literal at the call, without qualification;
      (b) nothing notices a comprehension re-pointed at a DIFFERENT iterable
          of the same length -- the count is a cardinality, not an identity;
      (c) two legs compare TWO quantifiers over ONE iterable --
          P2/the_true_box_clause_agrees_with_itself_at_k_1 and
          P2/every_box_variant_agrees_with_the_true_clause_at_k_1 -- and an
          agreement between two quantifiers survives emptying the thing they
          both range over.  The cardinality of the shared iterable is
          asserted separately at both legs; that is a different site again,
          and it is all there is;
      (d) `any(...)` is not wrapped.  It does not need the same treatment --
          `any(... for x in [])` is False, so emptying turns those legs red --
          but it is not covered by anything written here either.
  - A leg evaluated on the wrong object.  The comparison sites are routed
    through helpers that take BOTH members as arguments and raise on an equal
    pair -- product_sweep, correlator_vectors_of_pair, _distinct,
    _distinct_lists, _difference_of_distinct, _charpolys_of_distinct,
    _joint_tables_of_distinct -- so re-pointing an argument AT THE OTHER
    MEMBER OF THE PAIR raises.  IT DOES NOT RAISE ON ANY OTHER RE-POINTING:
    `product_sweep(RHO_PLUS, tau(F(0)), PROBES)` returns normally, because the
    helpers test equality of the two arguments and nothing else.  A previous
    version of this bullet said "re-pointing an ARGUMENT raises", which claims
    the whole class.  Nothing stops a leg BODY from naming one of two
    already-computed variables twice, and nothing stops a comparison being
    written at a site with no helper on its path.
  - THE EVIDENCE TIE IS A TIE TO A RETAINED VALUE, NOT TO AN INDEPENDENT
    RECOMPUTATION.  The EV legs compare each shipped entry against a value
    held from the computation that produced it (and, where it is cheap,
    against a recomputation).  An edit at the site where BOTH are produced
    moves both.  What the EV legs see is an evidence dictionary edited AFTER
    the computation; they do not see a wrong computation reported faithfully.
  - THE `correlator_vector` SLOT-ORDER CONVENTION IS UNPINNED.  The four
    entries are (Z,B0), (Z,B1), (X,B0), (X,B1), and on the exhibit used here
    slots 1 and 2 carry the same value (-1), so no leg of this module can see
    a transposition of those two slots.  The consequence is limited -- the
    polytope decision is invariant under permuting the four correlators, and
    `raw_chsh` picks out the fourth slot, which is the one that differs -- but
    the convention is carried by the function definition and by nothing that
    is computed.
  - Deriving EXPECTED_LEG_COUNTS or EXPECTED_LEG_DIGEST from EXPECTED_LEGS.
    Both are one-line edits -- `{k: len(v) for k, v in EXPECTED_LEGS.items()}`
    and the same over `_leg_digest` -- and after either, the corresponding
    gate compares a quantity with itself.  The module forbids deriving
    EXPECTED_LEGS from `legs` and said nothing about the cheaper edit one
    level up; this entry is that omission closed.  The three literals are
    written out by hand and recomputed by hand when a leg is added.
  - RECORD FIELDS THAT NO LEG READS, AND A REGISTRY KEY.  `_result()` ships
    `dependencies`, `premises`, `negative_controls` and `cross_refs` straight
    through from the argument list at the bottom of each check, and the
    module's registry dictionary `_CHECKS` keys each callable by a theorem
    name written out there.  Emptying any of those four lists, falsifying an
    entry inside one, or keying `_CHECKS` to a theorem name this module does
    not prove, changes what the bank stores and what a reader quotes, and
    every leg of both checks returns the same verdict on both execution
    paths.  They are declaration lines with nothing computed from them.  NO
    LEG IS ADDED FOR THEM HERE; this bullet is the disclosure and not a
    repair.
  - A faithful local reimplementation of any imported bank symbol.  The
    exception noted above is NARROWER THAN IT WAS STATED: K_dim_real patched
    inside the bank module is caught at leg A only for the ARGUMENTS THIS
    MODULE ACTUALLY EXERCISES -- N in {4, 6, 8, 9, 10, 12}, where leg A
    compares K_dim_real(N) against the rank of a constructed symmetric basis,
    and N = ab for a, b <= 7, where the leg-D_sym grid compares K_dim_real
    against the symbolic polynomial.  A patch at any argument outside those,
    or one that leaves every exercised value fixed, is invisible here.
  - THE PPT LEGS DO NOT TEST THE SIDE THEY NAME.  `W/rho_plus_is_ppt` and its
    neighbours pass `'B'` to partial_transpose.  On a symmetric matrix
    PT_A and PT_B agree, so the argument is inert at those sites and the same
    legs would return the same verdicts with `'A'`.  What distinguishes the
    two sides is computed at leg P, on a NON-symmetric argument, and nowhere
    else.
  - Float tolerances strictly below 1e-6.  The is_psd witness has a binding
    principal minor of exactly -10^-6; a tolerance of 1e-9 returns the same
    two answers on it and on its positive-minor counterpart.

A mutation harness, MUT_composite_only_direction_v10.py, ships alongside.  It
installs edits on copies of this file and reports, per edit and per execution
path, whether any check went red.  It is a record of what those particular
edits did.  No coverage claim is made for it here.

PROVENANCE.  The rho_+- witness pair, the PPT fence, and the multi-copy parity
argument are due to an external research packet,
APF_COMPOSITE_ONLY_DIRECTION_RECIPROCITY_BRIDGE v0.1 (2026-07-31), whose
mathematics was reproduced independently in a separate computer algebra
system before adoption.  The identification of the partial transpose as the
mechanism, the real-cone refutation of the separability reading, and every
apparatus decision below, are this module's.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

import hashlib
from fractions import Fraction as F
from itertools import combinations, product
from typing import Dict, FrozenSet, List, Sequence, Tuple

import apf.closed_world_completeness as _cwc
from apf.closed_world_completeness import (
    check_T_split_composite_gates_tomographic_locality as
    _sibling_tomographic_locality)
from apf.quantum_admissibility import (K_dim_complex, K_dim_quaternionic,
                                       K_dim_real, composite_defect)
from apf.third_boat_no_extension import (CLASSICAL_CHSH_BOUND, _chsh_facets,
                                         _dot, _in_local_polytope)

MODULE_TIER = 3
PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

Mat = Tuple[Tuple[F, ...], ...]
CMat = Tuple[Tuple[Tuple[F, F], ...], ...]


def _identity_count(N: int) -> int:
    """K(N) = N.  A synthetic parameter count with Delta identically zero,
    used at leg D' to compute what the imported composite_defect returns for
    the K it is handed."""
    return N


# ==========================================================================
# THE RESULT ARCHITECTURE.  One dictionary of labelled predicate values, and
# a frozen literal inventory.  See the docstring section of the same name.
# ==========================================================================


EXPECTED_LEGS: Dict[str, FrozenSet[str]] = {
    # Frozen at authoring time by enumerating the labels ONE run
    # produced, then written here as literals.  It is not derived
    # from `legs` at runtime.  The comparison performed in
    # _enforce_leg_inventory() is set-exact; _result() calls that
    # function, and run_all() computes the same four quantities
    # again on the returned record.
    'check_L_real_composite_only_direction_is_lambda_tensor_lambda':
        frozenset({
            'P/kron_ZX_literal',
            'P/kron_XZ_literal',
            'P/kron_order_distinct',
            'P/mm_noncommuting_pair',
            'P/mm_ZX_value',
            'P/trace_offdiagonal_ignored',
            'P/trace_product_agrees_with_trace_of_product',
            'P/trace_product_rejects_entrywise',
            'P/hs_X_with_itself_is_2',
            'P/hs_I_and_JJ_orthogonal',
            'P/hs_is_entrywise_and_not_transposed',
            'P/hs_transposed_convention_would_have_returned_one',
            'P/hs_differs_from_the_transposed_convention_on_that_pair',
            'P/the_hs_witness_pair_is_not_symmetric',
            'P/hs_and_the_transposed_convention_agree_on_a_symmetric_pair',
            'P/sym_accepts_JJ',
            'P/sym_rejects_J',
            'P/sym_rejects_4x4_single_offdiagonal',
            'P/transpose_is_not_identity',
            'P/transpose_of_J_is_minus_J',
            'P/scal_accepts_3JJ',
            'P/scal_accepts_JJ_over_3JJ',
            'P/scal_rejects_diagonal_trap',
            'P/scal_rejects_nonzero_over_zero',
            'P/scal_accepts_zero_over_zero',
            'P/psd_accepts_identity',
            'P/psd_rejects_negative_diagonal',
            'P/psd_rejects_leading_minor_trap',
            'P/psd_rejects_offdiagonal_2x2',
            'P/psd_rejects_offdiagonal_4x4',
            'P/psd_rejects_JJ',
            'P/psd_rejects_tiny_negative_minor',
            'P/psd_tiny_witness_minor_is_minus_one_millionth',
            'P/psd_accepts_tiny_positive_minor',
            'P/psd_rejects_a_non_symmetric_matrix_with_non_negative_minors',
            'P/psd_symmetry_witness_really_has_non_negative_minors',
            'P/psd_symmetry_witness_is_not_symmetric',
            'P/det_2x2_value',
            'P/det_singular_is_zero',
            'P/det_offdiagonal_sign',
            'P/det_3x3_diagonal',
            'P/rank_of_rank_one_set',
            'P/rank_of_sym4_basis_is_10',
            'P/span_accepts_identity_in_local',
            'P/span_rejects_JJ_in_local',
            'P/orth_summed_squares_zero_for_JJ',
            'P/orth_summed_squares_nonzero_for_contaminated',
            'P/rank_increment_zero_for_member',
            'P/rank_increment_one_for_JJ',
            'P/corr_argument_order_values',
            'P/corr_argument_order_differs',
            'P/kernel_basis_of_zero_matrix_is_full',
            'P/kernel_basis_of_identity_is_empty',
            'P/kernel_basis_vectors_are_annihilated',
            'P/charpoly_of_a_non_palindromic_diagonal_2x2',
            'P/charpoly_coefficient_order_is_not_reversible',
            'P/charpoly_matches_roots_for_diagonal',
            'P/charpoly_rejects_wrong_roots',
            'P/charpoly_sees_offdiagonal',
            'P/charpoly_invariant_under_conjugation',
            'P/pt_A_is_an_involution',
            'P/pt_B_is_an_involution',
            'P/pt_A_differs_from_full_transpose',
            'P/pt_A_differs_from_pt_B',
            'P/pt_A_on_a_product_transposes_only_A',
            'P/pt_trace_transfer_identity',
            'P/the_pt_transfer_witness_list_has_three_members',
            'P/the_pt_transfer_witnesses_are_pairwise_distinct',
            'P/the_pt_transfer_witness_list_is_not_vacuous',
            'P/trace_transfer_also_holds_for_the_full_transpose',
            'P/the_full_transpose_witness_list_is_not_vacuous',
            'P/trace_transfer_fails_for_a_non_self_adjoint_map',
            'P/regroup_is_identity_at_k_1',
            'P/regroup_is_a_permutation_at_k_2',
            'P/regroup_moves_something_at_k_2',
            'P/refuses_helper_reports_false_when_nothing_raises',
            'P/refuses_helper_reports_true_on_an_assertion',
            'P/product_sweep_refuses_the_identical_object',
            'P/product_sweep_refuses_an_equal_but_distinct_object',
            'P/the_self_comparison_exhibit_routine_returns_the_empty_list',
            'P/product_sweep_accepts_a_genuinely_distinct_pair',
            'P/product_sweep_reports_every_ordered_pair_it_tested',
            'P/product_sweep_tested_list_tracks_the_probe_list_it_was_handed',
            'P/correlator_vectors_of_pair_refuses_the_identical_object',
            'P/correlator_vectors_of_pair_refuses_an_equal_but_distinct_object',
            'P/correlator_vectors_of_pair_accepts_a_distinct_pair',
            'P/the_distinct_helper_refuses_an_equal_pair',
            'P/the_distinct_helper_accepts_a_distinct_pair',
            'P/the_distinct_lists_helper_refuses_one_list_handed_twice',
            'P/the_distinct_lists_helper_accepts_two_different_lists',
            'P/cmul_i_squared_is_minus_one',
            'P/cmul_i_squared_is_not_plus_one',
            'P/cmul_general_product',
            'P/cmul_is_commutative_witness',
            'P/cmul_rejects_componentwise',
            'P/ckron_YY_literal',
            'P/ckron_ZY_literal',
            'P/ckron_order_distinct',
            'P/ckron_YY_is_minus_JJ_realified',
            'P/ckron_YY_has_no_imaginary_part',
            'P/cflat_separates_real_from_imaginary',
            'P/cmat_rank_i_and_one_are_independent',
            'P/cmat_rank_of_herm2_is_4',
            'P/cmat_rank_of_a_repeated_generator_is_1',
            'P/cdagger_fixes_hermitian_generators',
            'P/cdagger_moves_a_non_hermitian_matrix',
            'P/cdagger_conjugates_the_imaginary_part',
            'P/all_of_rejects_an_empty_quantifier',
            'P/all_of_rejects_a_short_quantifier',
            'P/all_of_rejects_a_truthy_non_bool',
            'P/all_of_accepts_exactly_n_trues',
            'P/the_module_certifies_no_physical_premises',
            'P/the_module_declares_no_bank_modification',
            'P/the_module_exports_nothing',
            'P/the_module_tier_is_three',
            'P/the_grade_is_p_math_and_not_a_bare_p',
            'A/2x2/dim_sym_matches_basis_and_bank',
            'B/2x2/local_rank_is_KR_product',
            'B/2x2/local_generators_symmetric',
            'C/2x2/lam_generators_symmetric',
            'C/2x2/lam_rank_is_An_times_Am',
            'C/2x2/lam_hs_orthogonal_to_every_local',
            'C/2x2/the_orthogonality_loop_reads_two_distinct_lists',
            'C/2x2/cross_pair_count_is_nonvacuous',
            'C/2x2/summed_squares_certificate_is_zero',
            'C/2x2/each_lam_generator_raises_rank_by_one',
            'C/2x2/union_spans_sym',
            'D/2x2/codim_equals_banked_defect',
            'D/2x2/codim_equals_closed_form',
            'D/2x2/codim_equals_lam_rank',
            'D/2x2/the_reported_codimension_is_that_subtraction',
            'D/2x2/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/2x2/under_generating_the_span_moves_the_subtraction',
            'A/2x3/dim_sym_matches_basis_and_bank',
            'B/2x3/local_rank_is_KR_product',
            'B/2x3/local_generators_symmetric',
            'C/2x3/lam_generators_symmetric',
            'C/2x3/lam_rank_is_An_times_Am',
            'C/2x3/lam_hs_orthogonal_to_every_local',
            'C/2x3/the_orthogonality_loop_reads_two_distinct_lists',
            'C/2x3/cross_pair_count_is_nonvacuous',
            'C/2x3/summed_squares_certificate_is_zero',
            'C/2x3/each_lam_generator_raises_rank_by_one',
            'C/2x3/union_spans_sym',
            'D/2x3/codim_equals_banked_defect',
            'D/2x3/codim_equals_closed_form',
            'D/2x3/codim_equals_lam_rank',
            'D/2x3/the_reported_codimension_is_that_subtraction',
            'D/2x3/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/2x3/under_generating_the_span_moves_the_subtraction',
            'A/3x3/dim_sym_matches_basis_and_bank',
            'B/3x3/local_rank_is_KR_product',
            'B/3x3/local_generators_symmetric',
            'C/3x3/lam_generators_symmetric',
            'C/3x3/lam_rank_is_An_times_Am',
            'C/3x3/lam_hs_orthogonal_to_every_local',
            'C/3x3/the_orthogonality_loop_reads_two_distinct_lists',
            'C/3x3/cross_pair_count_is_nonvacuous',
            'C/3x3/summed_squares_certificate_is_zero',
            'C/3x3/each_lam_generator_raises_rank_by_one',
            'C/3x3/union_spans_sym',
            'D/3x3/codim_equals_banked_defect',
            'D/3x3/codim_equals_closed_form',
            'D/3x3/codim_equals_lam_rank',
            'D/3x3/the_reported_codimension_is_that_subtraction',
            'D/3x3/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/3x3/under_generating_the_span_moves_the_subtraction',
            'A/2x4/dim_sym_matches_basis_and_bank',
            'B/2x4/local_rank_is_KR_product',
            'B/2x4/local_generators_symmetric',
            'C/2x4/lam_generators_symmetric',
            'C/2x4/lam_rank_is_An_times_Am',
            'C/2x4/lam_hs_orthogonal_to_every_local',
            'C/2x4/the_orthogonality_loop_reads_two_distinct_lists',
            'C/2x4/cross_pair_count_is_nonvacuous',
            'C/2x4/summed_squares_certificate_is_zero',
            'C/2x4/each_lam_generator_raises_rank_by_one',
            'C/2x4/union_spans_sym',
            'D/2x4/codim_equals_banked_defect',
            'D/2x4/codim_equals_closed_form',
            'D/2x4/codim_equals_lam_rank',
            'D/2x4/the_reported_codimension_is_that_subtraction',
            'D/2x4/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/2x4/under_generating_the_span_moves_the_subtraction',
            'A/2x5/dim_sym_matches_basis_and_bank',
            'B/2x5/local_rank_is_KR_product',
            'B/2x5/local_generators_symmetric',
            'C/2x5/lam_generators_symmetric',
            'C/2x5/lam_rank_is_An_times_Am',
            'C/2x5/lam_hs_orthogonal_to_every_local',
            'C/2x5/the_orthogonality_loop_reads_two_distinct_lists',
            'C/2x5/cross_pair_count_is_nonvacuous',
            'C/2x5/summed_squares_certificate_is_zero',
            'C/2x5/each_lam_generator_raises_rank_by_one',
            'C/2x5/union_spans_sym',
            'D/2x5/codim_equals_banked_defect',
            'D/2x5/codim_equals_closed_form',
            'D/2x5/codim_equals_lam_rank',
            'D/2x5/the_reported_codimension_is_that_subtraction',
            'D/2x5/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/2x5/under_generating_the_span_moves_the_subtraction',
            'A/3x4/dim_sym_matches_basis_and_bank',
            'B/3x4/local_rank_is_KR_product',
            'B/3x4/local_generators_symmetric',
            'C/3x4/lam_generators_symmetric',
            'C/3x4/lam_rank_is_An_times_Am',
            'C/3x4/lam_hs_orthogonal_to_every_local',
            'C/3x4/the_orthogonality_loop_reads_two_distinct_lists',
            'C/3x4/cross_pair_count_is_nonvacuous',
            'C/3x4/summed_squares_certificate_is_zero',
            'C/3x4/each_lam_generator_raises_rank_by_one',
            'C/3x4/union_spans_sym',
            'D/3x4/codim_equals_banked_defect',
            'D/3x4/codim_equals_closed_form',
            'D/3x4/codim_equals_lam_rank',
            'D/3x4/the_reported_codimension_is_that_subtraction',
            'D/3x4/the_two_ranks_are_not_equal_so_the_subtraction_bites',
            'D/3x4/under_generating_the_span_moves_the_subtraction',
            'D/codimension_is_not_constant_across_shapes',
            'Dsym/polynomial_identity_defect_equals_closed_form',
            'Dsym/identity_is_not_vacuous_polynomials_are_nonzero',
            'Dsym/the_grid_is_forty_nine_points',
            'Dsym/the_grid_points_are_pairwise_distinct',
            'Dsym/the_grid_has_thirty_six_points_with_a_nonzero_defect',
            'Dsym/the_grid_contains_points_where_the_closed_form_is_nonzero',
            'Dsym/the_grid_rejects_a_perturbed_joint_polynomial',
            'Dsym/the_grid_rejects_a_perturbed_closed_form',
            'Dsym/joint_polynomial_matches_banked_K_on_grid',
            'Dsym/local_polynomial_matches_banked_K_on_grid',
            'Dsym/defect_polynomial_matches_banked_defect_on_grid',
            'Dsym/closed_polynomial_matches_An_Am_on_grid',
            'Dsym/engine_multiplication_witness',
            'Dsym/engine_addition_cancels_to_the_empty_polynomial',
            'Dsym/engine_rejects_a_false_identity',
            'Dsym/engine_distinguishes_the_two_variables',
            'Dsym/engine_evaluation_agrees_with_hand_arithmetic',
            'Dsym/engine_evaluation_reads_the_first_variable_as_n',
            'Dsym/engine_evaluation_is_not_symmetric_in_its_arguments',
            'Dsym/engine_evaluation_of_a_mixed_monomial_is_order_sensitive',
            'Dp/composite_defect_computes_K_nm_minus_K_n_K_m',
            'Dp/identity_count_defect_is_zero',
            'Dp/quaternionic_defect_matches_its_own_formula',
            'Dp/quaternionic_defect_is_minus_eight',
            'Dp/quaternionic_defect_is_negative',
            'Dp/quaternionic_defect_differs_from_closed_form',
            'Dp/the_two_probes_disagree_with_each_other',
            'Dppp/the_declared_drop_is_the_frozen_value',
            'Dppp/4x4/full_codimension_equals_the_bank_value',
            'Dppp/4x4/full_codimension_equals_the_closed_form',
            'Dppp/4x4/the_declared_drop_is_positive',
            'Dppp/4x4/the_under_generated_list_is_shorter_by_the_drop',
            'Dppp/4x4/under_generation_lost_rank',
            'Dppp/4x4/under_generated_reading_is_consistent',
            'Dppp/4x4/value_is_neither_zero_nor_the_closed_form',
            'Dppp/4x4/value_is_not_the_banked_defect_either',
            'Dppp/3x5/full_codimension_equals_the_bank_value',
            'Dppp/3x5/full_codimension_equals_the_closed_form',
            'Dppp/3x5/the_declared_drop_is_positive',
            'Dppp/3x5/the_under_generated_list_is_shorter_by_the_drop',
            'Dppp/3x5/under_generation_lost_rank',
            'Dppp/3x5/under_generated_reading_is_consistent',
            'Dppp/3x5/value_is_neither_zero_nor_the_closed_form',
            'Dppp/3x5/value_is_not_the_banked_defect_either',
            'Dppp/5x5/full_codimension_equals_the_bank_value',
            'Dppp/5x5/full_codimension_equals_the_closed_form',
            'Dppp/5x5/the_declared_drop_is_positive',
            'Dppp/5x5/the_under_generated_list_is_shorter_by_the_drop',
            'Dppp/5x5/under_generation_lost_rank',
            'Dppp/5x5/under_generated_reading_is_consistent',
            'Dppp/5x5/value_is_neither_zero_nor_the_closed_form',
            'Dppp/5x5/value_is_not_the_banked_defect_either',
            'Dppp/probe_values_are_pairwise_distinct',
            'Dppp/probe_shapes_are_disjoint_from_the_tested_shapes',
            'Dppp/probe_values_avoid_every_tested_codimension',
            'Dpp/sibling_symbol_is_a_function',
            'Dpp/sibling_symbol_module_provenance',
            'Dpp/sibling_symbol_name_provenance',
            'Dpp/sibling_symbol_is_the_object_the_bank_module_exports',
            'Dpp/sibling_passes',
            'Dpp/sibling_record_name',
            'Dpp/sibling_record_tier_and_summary',
            'Dpp/R_clause_is_present',
            'Dpp/C_clause_is_present',
            'Dpp/H_clause_is_present',
            'Dpp/the_three_clauses_are_distinct_sites',
            'Dpp/R_clause_joint_is_10',
            'Dpp/R_clause_local_is_9',
            'Dpp/C_clause_joint_is_16',
            'Dpp/C_clause_local_is_16',
            'Dpp/H_clause_joint_is_28',
            'Dpp/H_clause_local_is_36',
            'Dpp/the_six_parsed_sibling_numbers_are_all_present',
            'Dpp/the_C_clause_reports_joint_equal_to_local',
            'Dpp/the_R_clause_reports_a_surplus',
            'Dpp/the_H_clause_reports_a_deficit',
            'Dpp/the_R_and_H_clauses_have_opposite_signs',
            'Dpp/parser_detects_a_move_in_the_R_clause_alone',
            'Dpp/the_simulated_move_actually_changed_the_string',
            'Dpp/parser_detects_a_move_in_the_C_clause_alone',
            'Dpp/naive_substring_test_is_demonstrably_insufficient',
            'Dpp/structural_parser_reads_the_demo_C_clause_independently',
            'Dpp/reconstructed_sibling_joint_matches_the_parsed_value',
            'Dpp/reconstructed_sibling_local_matches_the_parsed_value',
            'Dpp/the_sibling_prose_carries_the_signs_its_code_computes',
            'Dpp/local_counts_agree',
            'Dpp/joint_dimensions_agree',
            'Dpp/this_module_signed_mismatch_is_plus_one',
            'Dpp/the_two_mismatches_agree',
            'E/under_generation_moves_the_codimension',
            'E/under_generation_codimension_is_2',
            'E/enlargement_sends_the_codimension_to_zero',
            'E3/2x2/dim_herm_matches_banked_KC',
            'E3/2x2/complex_codimension_and_banked_defect_both_zero',
            'E3/2x2/complex_local_rank_is_the_product_of_local_dimensions',
            'E3/2x2/every_complex_local_generator_is_hermitian',
            'E3/2x3/dim_herm_matches_banked_KC',
            'E3/2x3/complex_codimension_and_banked_defect_both_zero',
            'E3/2x3/complex_local_rank_is_the_product_of_local_dimensions',
            'E3/2x3/every_complex_local_generator_is_hermitian',
            'E3/3x3/dim_herm_matches_banked_KC',
            'E3/3x3/complex_codimension_and_banked_defect_both_zero',
            'E3/3x3/complex_local_rank_is_the_product_of_local_dimensions',
            'E3/3x3/every_complex_local_generator_is_hermitian',
            'F/the_exhibited_direction_is_the_lam_tensor_lam_generator',
            'F/JJ_is_not_a_multiple_of_the_singlet_projector',
            'F/the_singlet_projector_is_not_a_multiple_of_JJ',
            'F/identity_and_JJ_are_independent',
            'F/singlet_is_outside_span_of_identity_and_JJ',
            'F/JJ_equals_two_psi_plus_phi_minus_identity',
            'G/singlet_decomposition_is_an_identity',
            'G/local_summand_is_in_the_product_span',
            'G/local_summand_is_not_psd',
            'G/singlet_is_a_state',
            'G/JJ_hs_norm_squared_is_4',
            'G/singlet_composite_coefficient_is_one_quarter',
            'G/singlet_trace_against_JJ_is_one',
            'G/phi_plus_co_attains_the_value_one',
            'G/JJ_squared_is_the_identity',
            'G/JJ_is_traceless',
            'G/identity_minus_JJ_is_psd',
            'G/identity_plus_JJ_is_psd',
            'G/identity_minus_twice_JJ_is_not_psd',
            'G/half_identity_minus_JJ_is_not_psd',
            'G/battery_labels_match_the_frozen_list',
            'G/battery/psi-/is_a_density_matrix',
            'G/battery/psi-/value_is_at_most_one',
            'G/battery/psi-/coefficient_is_at_most_one_quarter',
            'G/battery/phi+/is_a_density_matrix',
            'G/battery/phi+/value_is_at_most_one',
            'G/battery/phi+/coefficient_is_at_most_one_quarter',
            'G/battery/I/4/is_a_density_matrix',
            'G/battery/I/4/value_is_at_most_one',
            'G/battery/I/4/coefficient_is_at_most_one_quarter',
            'G/battery/|00><00|/is_a_density_matrix',
            'G/battery/|00><00|/value_is_at_most_one',
            'G/battery/|00><00|/coefficient_is_at_most_one_quarter',
            'G/battery/sigma_+1/8/is_a_density_matrix',
            'G/battery/sigma_+1/8/value_is_at_most_one',
            'G/battery/sigma_+1/8/coefficient_is_at_most_one_quarter',
            'G/battery/sigma_-1/8/is_a_density_matrix',
            'G/battery/sigma_-1/8/value_is_at_most_one',
            'G/battery/sigma_-1/8/coefficient_is_at_most_one_quarter',
            'G/battery/(psi-+phi+)/2/is_a_density_matrix',
            'G/battery/(psi-+phi+)/2/value_is_at_most_one',
            'G/battery/(psi-+phi+)/2/coefficient_is_at_most_one_quarter',
            'G/battery/rho_+/is_a_density_matrix',
            'G/battery/rho_+/value_is_at_most_one',
            'G/battery/rho_+/coefficient_is_at_most_one_quarter',
            'G/battery/rho_-/is_a_density_matrix',
            'G/battery/rho_-/value_is_at_most_one',
            'G/battery/rho_-/coefficient_is_at_most_one_quarter',
            'G/battery_bound_attained_by_at_least_three_members',
            'G/battery_has_a_member_strictly_below_the_bound',
            'G/battery_has_a_member_on_the_negative_side',
            'G/battery_maximum_coefficient_is_the_singlet_value',
            'G/eigen/plus_one_eigenspace_has_dimension_2',
            'G/eigen/eigenspace_basis_is_independent',
            'G/eigen/eigenspace_vectors_are_genuine_eigenvectors',
            'G/eigen/minus_one_eigenspace_also_has_dimension_2',
            'G/eigen/family_members_are_states',
            'G/eigen/family_members_all_attain_the_bound',
            'G/eigen/family_members_are_pairwise_distinct',
            'G/eigen/family_is_larger_than_the_three_exhibited_states',
            'G/eigen/family_contains_states_outside_the_exhibited_three',
            'G/eigen/an_off_eigenspace_state_falls_strictly_short',
            'G/eigen/the_bound_is_not_attained_by_every_state',
            'H/factorization/0/product_trace_factorizes',
            'H/factorization/1/product_trace_factorizes',
            'H/factorization/2/product_trace_factorizes',
            'H/factorization_battery_is_not_vacuous',
            'H/trace_of_J_against_every_symmetric_probe_vanishes',
            'H/trace_of_J_against_a_nonsymmetric_matrix_does_not_vanish',
            'H/probe_list_spans_sym_R2',
            'H/every_probe_is_symmetric',
            'H/probe_list_is_longer_than_a_basis',
            'H/probe_list_is_linearly_dependent',
            'H/basis_of_sym_R2_has_rank_three',
            'H/nine_basis_products_span_the_whole_product_space',
            'H/sigma_endpoints_are_distinct',
            'H/sigma+/has_trace_one',
            'H/sigma+/is_symmetric',
            'H/sigma+/is_psd',
            'H/sigma-/has_trace_one',
            'H/sigma-/is_symmetric',
            'H/sigma-/is_psd',
            'H/gauge/reflection_is_orthogonal',
            'H/gauge/reflection_is_a_product_operator',
            'H/gauge/reflection_is_not_the_identity',
            'H/gauge/local_reflection_carries_sigma_plus_to_sigma_minus',
            'H/gauge/sigma_endpoints_share_a_characteristic_polynomial',
            'H/gauge/sigma_endpoints_are_therefore_not_the_witness_pair',
            'H/gauge/the_same_reflection_does_not_relate_the_witness_pair',
            'H/measurement_projectors_are_psd',
            'H/measurement_pairs_resolve_the_identity',
            'H/measurement_pairs_are_orthogonal',
            'H/the_two_measurement_bases_differ',
            'H/sigma_is_affine_in_t',
            'H/sigma_actually_moves_with_t',
            'H/interpolation/-1/8/weight_is_in_the_unit_interval',
            'H/interpolation/-1/8/convex_identity_holds',
            'H/interpolation/-1/16/weight_is_in_the_unit_interval',
            'H/interpolation/-1/16/convex_identity_holds',
            'H/interpolation/-1/100/weight_is_in_the_unit_interval',
            'H/interpolation/-1/100/convex_identity_holds',
            'H/interpolation/0/weight_is_in_the_unit_interval',
            'H/interpolation/0/convex_identity_holds',
            'H/interpolation/1/100/weight_is_in_the_unit_interval',
            'H/interpolation/1/100/convex_identity_holds',
            'H/interpolation/1/16/weight_is_in_the_unit_interval',
            'H/interpolation/1/16/convex_identity_holds',
            'H/interpolation/1/8/weight_is_in_the_unit_interval',
            'H/interpolation/1/8/convex_identity_holds',
            'H/interpolation_weights_reach_both_endpoints',
            'H/binding_minor/-7/matches_the_closed_form',
            'H/binding_minor/-1/3/matches_the_closed_form',
            'H/binding_minor/-1/8/matches_the_closed_form',
            'H/binding_minor/0/matches_the_closed_form',
            'H/binding_minor/1/8/matches_the_closed_form',
            'H/binding_minor/1/5/matches_the_closed_form',
            'H/binding_minor/3/matches_the_closed_form',
            'H/binding_minor_is_negative_outside_the_interval',
            'H/binding_minor_is_nonnegative_inside_the_interval',
            'H/psd_grid/-1/3/verdict_matches_the_interval',
            'H/psd_grid/-1/5/verdict_matches_the_interval',
            'H/psd_grid/-1/8/verdict_matches_the_interval',
            'H/psd_grid/0/verdict_matches_the_interval',
            'H/psd_grid/1/8/verdict_matches_the_interval',
            'H/psd_grid/1/5/verdict_matches_the_interval',
            'H/psd_grid/1/3/verdict_matches_the_interval',
            'H/control_family_members_are_states',
            'H/control_family_members_are_distinct',
            'H/control_family_is_separated_at_nine_probe_pairs',
            'W/R_is_the_stated_local_part',
            'W/R_lies_in_the_product_span',
            'W/rho_plus_definition_identity',
            'W/rho_minus_definition_identity',
            'W/rho_plus_is_a_density_matrix',
            'W/rho_minus_is_a_density_matrix',
            'W/the_pair_is_distinct',
            'W/the_difference_is_pure_composite_direction',
            'W/the_difference_is_hs_orthogonal_to_every_product_generator',
            'W/the_difference_pair_members_are_distinct',
            'W/charpoly_of_rho_plus_matches_the_stated_spectrum',
            'W/charpoly_of_rho_minus_matches_the_stated_spectrum',
            'W/the_two_spectra_are_different_multisets',
            'W/the_characteristic_polynomials_differ',
            'W/both_spectra_sum_to_one',
            'W/both_spectra_are_nonnegative',
            'W/a_wrong_spectrum_is_rejected',
            'W/conjugation_preserves_charpoly_on_an_orthogonal_witness',
            'W/conjugation_preserves_charpoly_on_a_non_orthogonal_witness',
            'W/the_superseded_sigma_pair_would_not_have_supported_this',
            'W/the_superseded_sigma_pair_members_are_distinct',
            'W/the_sweep_pair_is_the_witness_pair',
            'W/the_sweep_pair_members_are_distinct',
            'W/the_sweep_pair_difference_is_the_composite_direction',
            'W/the_self_comparison_is_refused',
            'W/the_self_comparison_exhibit_is_trivially_empty',
            'W/zero_of_the_nine_basis_product_observables_separate',
            'W/the_basis_sweep_has_nine_pairs',
            'W/zero_of_the_forty_nine_probe_pairs_separate',
            'W/the_probe_sweep_has_forty_nine_pairs',
            'W/the_two_sweeps_ran_over_different_numbers_of_pairs',
            'W/the_probe_sweep_ran_over_the_frozen_probe_list',
            'W/the_same_sweep_does_separate_the_control_family',
            'W/the_projective_measurement_pair_also_fails_to_separate',
            'W/the_projective_measurement_pair_members_are_distinct',
            'W/the_projective_joint_distribution_sums_to_one',
            'W/the_global_observable_separates_the_pair',
            'W/the_global_observable_values_are_plus_and_minus_one_eighth',
            'W/the_global_difference_is_exactly_one_quarter',
            'W/the_separating_observable_is_not_a_product',
            'W/the_horodecki_dimension_hypothesis_is_computed',
            'W/the_horodecki_field_hypothesis_is_recorded_not_checked',
            'W/this_module_works_in_the_smaller_real_ambient_space',
            'W/the_complex_ambient_space_is_strictly_larger_than_the_real_one',
            'W/rho_plus_is_ppt',
            'W/rho_minus_is_ppt',
            'W/the_ppt_test_is_live_it_rejects_the_singlet',
            'W/the_ppt_test_is_live_it_rejects_phi_plus',
            'W/the_ppt_test_accepts_the_maximally_mixed_state',
            'W/pt_maps_rho_plus_onto_rho_minus_exactly',
            'W/pt_maps_rho_minus_onto_rho_plus_exactly',
            'W/pt_of_rho_plus_has_rho_minus_spectrum',
            'W/pt_of_rho_minus_has_rho_plus_spectrum',
            'W/pt_fixes_the_local_part',
            'W/pt_flips_the_composite_direction',
            'W/pt_does_not_flip_a_product_generator',
            'W/trace_of_J_vanishes_on_a_basis_of_sym_R2',
            'W/that_basis_spans_sym_R2',
            'W/trace_of_J_does_not_vanish_on_an_antisymmetric_matrix',
            'W/every_real_product_generator_has_zero_composite_coefficient',
            'W/the_explicit_real_separable_state_is_a_density_matrix',
            'W/the_explicit_real_separable_state_has_zero_composite_coefficient',
            'W/the_witness_pair_has_a_nonzero_composite_coefficient',
            'W/the_pair_is_not_separable_in_the_real_product_cone',
            'W/the_composite_direction_is_minus_Y_tensor_Y_after_complexification',
            'W/the_complexified_factor_Y_is_hermitian_and_not_real',
            'K/pt_A_fixes_the_local_part',
            'K/pt_A_flips_the_composite_direction',
            'K/a_real_symmetric_product_effect_is_pt_A_even',
            'K/a_non_symmetric_local_factor_is_not_pt_A_even',
            'K/general/pt_A_maps_the_pair_onto_each_other_exactly',
            'K/general/pt_A_is_an_involution_on_the_single_copy_system',
            'K/1/binomial_expansion_reproduces_the_difference',
            'K/1/odd_subset_count_is_two_to_the_k_minus_one',
            'K/1/difference_is_pt_A_odd',
            'K/1/difference_is_pt_B_odd',
            'K/1/difference_is_nonzero',
            'K/1/pt_A_maps_the_plus_power_onto_the_minus_power',
            'K/1/pt_A_distributes_over_the_tensor_product_of_copies',
            'K/1/the_functoriality_probe_is_not_symmetric',
            'K/1/every_collective_local_effect_is_blind',
            'K/1/the_pairing_list_reads_the_difference_it_was_built_from',
            'K/1/the_effect_battery_is_nonvacuous',
            'K/1/a_real_symmetric_product_effect_is_pt_A_even_at_this_k',
            'K/1/the_effect_battery_has_five_distinct_matrices',
            'K/1/the_effect_pairs_are_pairwise_distinct',
            'K/1/no_effect_pair_repeats_one_matrix_on_both_sides',
            'K/1/the_effects_are_symmetric',
            'K/1/the_effects_are_not_all_multiples_of_the_identity',
            'K/1/the_seed_lists_are_distinct_and_of_the_frozen_sizes',
            'K/1/a_global_effect_separates_the_copies',
            'K/1/the_global_effect_is_pt_A_odd_hence_not_a_local_product',
            'K/2/binomial_expansion_reproduces_the_difference',
            'K/2/odd_subset_count_is_two_to_the_k_minus_one',
            'K/2/difference_is_pt_A_odd',
            'K/2/difference_is_pt_B_odd',
            'K/2/difference_is_nonzero',
            'K/2/pt_A_maps_the_plus_power_onto_the_minus_power',
            'K/2/pt_A_distributes_over_the_tensor_product_of_copies',
            'K/2/the_functoriality_probe_is_not_symmetric',
            'K/2/every_collective_local_effect_is_blind',
            'K/2/the_pairing_list_reads_the_difference_it_was_built_from',
            'K/2/the_effect_battery_is_nonvacuous',
            'K/2/a_real_symmetric_product_effect_is_pt_A_even_at_this_k',
            'K/2/the_effect_battery_has_five_distinct_matrices',
            'K/2/the_effect_pairs_are_pairwise_distinct',
            'K/2/no_effect_pair_repeats_one_matrix_on_both_sides',
            'K/2/the_effects_are_symmetric',
            'K/2/the_effects_are_not_all_multiples_of_the_identity',
            'K/2/the_seed_lists_are_distinct_and_of_the_frozen_sizes',
            'K/2/a_global_effect_separates_the_copies',
            'K/2/the_global_effect_is_pt_A_odd_hence_not_a_local_product',
            'K/3/binomial_expansion_reproduces_the_difference',
            'K/3/odd_subset_count_is_two_to_the_k_minus_one',
            'K/3/difference_is_pt_A_odd',
            'K/3/difference_is_pt_B_odd',
            'K/3/difference_is_nonzero',
            'K/3/pt_A_maps_the_plus_power_onto_the_minus_power',
            'K/3/pt_A_distributes_over_the_tensor_product_of_copies',
            'K/3/the_functoriality_probe_is_not_symmetric',
            'K/3/every_collective_local_effect_is_blind',
            'K/3/the_pairing_list_reads_the_difference_it_was_built_from',
            'K/3/the_effect_battery_is_nonvacuous',
            'K/3/a_real_symmetric_product_effect_is_pt_A_even_at_this_k',
            'K/3/the_effect_battery_has_five_distinct_matrices',
            'K/3/the_effect_pairs_are_pairwise_distinct',
            'K/3/no_effect_pair_repeats_one_matrix_on_both_sides',
            'K/3/the_effects_are_symmetric',
            'K/3/the_effects_are_not_all_multiples_of_the_identity',
            'K/3/the_seed_lists_are_distinct_and_of_the_frozen_sizes',
            'K/3/a_global_effect_separates_the_copies',
            'K/3/the_global_effect_is_pt_A_odd_hence_not_a_local_product',
            'K/the_executed_copy_counts_are_one_two_and_three',
            'K/the_executed_dimensions_are_four_sixteen_and_sixty_four',
            'K/the_executed_odd_subset_counts_are_one_two_and_four',
            'EV/every_certified_evidence_key_is_present',
            'EV/reported_spectra_are_the_frozen_spectra',
            'EV/reported_separation_counts_are_the_sweep_results',
            'EV/reported_global_observable_values_are_the_computed_ones',
            'EV/reported_bank_probe_values_are_the_bank_values',
            'EV/reported_sibling_mismatch_is_the_parsed_difference',
            'EV/reported_maximizer_numbers_are_the_computed_ones',
            'EV/reported_shape_table_carries_every_computed_column',
            'EV/reported_multicopy_rows_carry_every_computed_column',
        }),
    'check_L_bipartite_chsh_blind_to_composite_only_direction':
        frozenset({
            'P2/the_module_tier_is_three',
            'P2/the_grade_is_p_math_and_not_a_bare_p',
            'P2/agrees_with_the_banked_polytope_on_the_whole_battery',
            'P2/the_validation_battery_covers_both_verdicts',
            'P2/the_validation_alphabet_is_six_distinct_values',
            'P2/the_validation_alphabet_straddles_the_unit_box',
            'P2/the_validation_battery_is_one_thousand_two_hundred_ninety_six',
            'P2/box_only_witness_violates_no_facet',
            'P2/box_only_witness_is_rejected_at_k_1',
            'P2/box_witness_is_outside_at_k_2',
            'P2/box_witness_is_inside_at_k_4',
            'P2/box_witness_violates_no_facet_at_k_2',
            'P2/box_witness_violates_no_facet_at_k_4',
            'P2/the_two_scales_give_opposite_verdicts',
            'P2/box_variant/v^2 <= k*k/is_wrong_at_some_tested_scale',
            'P2/box_variant/v^2 <= 1/is_wrong_at_some_tested_scale',
            'P2/box_variant/|v| <= k/is_wrong_at_some_tested_scale',
            'P2/the_true_box_clause_agrees_with_itself_at_k_1',
            'P2/every_box_variant_agrees_with_the_true_clause_at_k_1',
            'P2/facet_witness_is_inside_the_box_at_k_2',
            'P2/facet_witness_is_rejected_at_k_2',
            'P2/facet_witness_is_accepted_at_a_large_enough_scale',
            'A2/state_is_a_rank_one_real_projector',
            'A2/state_is_psd',
            'A2/Z_is_a_traceless_symmetric_involution',
            'A2/X_is_a_traceless_symmetric_involution',
            'A2/alice_settings_do_not_commute',
            'A2/correlator_argument_order_is_pinned',
            'A2/both_parties_have_two_distinct_settings',
            'A2/scal_accepts_two_times_the_identity',
            'A2/scal_rejects_the_diagonal_trap',
            'A2/scal_rejects_unequal_diagonal_entries',
            'A2/bob_first_setting_squares_to_a_multiple_of_the_identity',
            'A2/both_bob_settings_share_one_rescale_constant',
            'A2/the_rescale_constant_is_positive',
            'A2/the_rescale_constant_differs_from_one',
            'A2/alice_settings_are_already_involutions',
            'B2/scaled_correlator_vector_is_the_expected_quadruple',
            'B2/raw_combination_is_minus_four',
            'B2/the_signed_value_is_negative',
            'B2/chsh_squared_is_eight_using_the_derived_scale',
            'C2/the_bank_offers_eight_facets',
            'C2/every_banked_facet_has_sign_product_minus_one',
            'C2/no_product_plus_one_pattern_is_banked',
            'C2/the_banked_facet_list_has_no_duplicates',
            'C2/the_banked_facet_set_is_closed_under_negation',
            'C2/guard/the_synthetic_half_list_has_four_facets',
            'C2/guard/the_half_list_is_not_negation_closed',
            'C2/guard/the_witness_is_inside_the_box',
            'C2/guard/a_half_list_facet_takes_a_large_negative_value',
            'C2/guard/no_half_list_facet_takes_a_large_positive_value',
            'C2/guard/the_guarded_procedure_accepts_the_witness',
            'C2/guard/the_witness_is_outside_on_the_full_banked_list',
            'C2/guard/the_bank_agrees_the_witness_is_outside',
            'D2/every_true_correlator_is_within_unit_magnitude',
            'D2/the_maximum_banked_facet_value_is_four',
            'D2/the_maximizing_facet_value_is_positive',
            'D2/the_facet_is_violated_on_the_true_vector',
            'D2/the_facet_value_equals_the_magnitude_of_the_raw_combination',
            'D2/the_facet_square_and_the_chsh_square_agree',
            'D2/the_facet_square_on_the_true_vector_is_eight',
            'D2/eight_exceeds_the_classical_bound_squared',
            'D2/every_true_correlator_squared_is_at_most_one',
            'D2/every_true_correlator_squared_is_one_half',
            'D2/the_true_vector_is_outside_the_banked_polytope',
            'D2/control_the_same_vector_at_four_times_the_scale_is_inside',
            'D2/control_the_unscaled_vector_is_outside',
            'E2/functional/-1/2/correlators_are_unchanged',
            'E2/functional/-1/4/correlators_are_unchanged',
            'E2/functional/0/correlators_are_unchanged',
            'E2/functional/1/4/correlators_are_unchanged',
            'E2/functional/1/2/correlators_are_unchanged',
            'E2/functional/7/3/correlators_are_unchanged',
            'E2/functional_sweep_ran_at_six_points',
            'E2/functional_control_a_local_direction_does_move_them',
            'E2/states/the_witness_pair_are_two_distinct_density_matrices',
            'E2/states/the_witness_pair_is_spectrally_inequivalent',
            'E2/states/the_compared_pair_is_the_witness_pair',
            'E2/states/the_compared_pair_members_are_distinct',
            'E2/states/the_self_comparison_is_refused',
            'E2/states/the_self_comparison_exhibit_is_trivially_equal',
            'E2/states/the_two_returned_vectors_come_from_the_two_pair_members',
            'E2/states/the_witness_pair_give_the_same_correlator_vector',
            'E2/states/the_witness_pair_sit_at_different_composite_coordinates',
            'E2/states/the_witness_pair_give_the_same_chsh_value',
            'E2/states/control_the_locally_differing_pair_moves_the_correlators',
            'E2/states/the_interval_endpoints_agree_too',
            'E2/states/the_interval_endpoints_are_distinct_states',
            'EV/every_certified_evidence_key_is_present',
            'EV/the_reported_chsh_square_is_the_computed_one',
            'EV/the_reported_raw_signed_value_is_the_computed_one',
            'EV/the_reported_scaled_correlators_are_the_computed_ones',
            'EV/the_reported_validation_counts_are_the_battery_counts',
            'EV/the_reported_facet_square_is_the_computed_one',
            'EV/the_reported_composite_coordinates_are_the_computed_ones',
        }),
}


# A SECOND LITERAL: the number of legs each check evaluates.  It is read
# inside _enforce_leg_inventory(), which _result() calls, so it is read on the
# path verify_all.run_module executes.  It is read unconditionally: not gated
# on the verdict, not gated on the inventory-difference lists.  Written out by
# hand and recomputed by hand whenever a leg is added or removed.  See KNOWN
# LIMITS in the module docstring for what deriving it from EXPECTED_LEGS would
# make this comparison.
EXPECTED_LEG_COUNTS: Dict[str, int] = {
    'check_L_real_composite_only_direction_is_lambda_tensor_lambda': 596,
    'check_L_bipartite_chsh_blind_to_composite_only_direction': 95,
}

# A THIRD LITERAL, over the LABELS rather than their number: the SHA-256 of
# the newline-joined sorted label list.  Written out by hand and recomputed by
# hand whenever a leg is added or removed, exactly as EXPECTED_LEGS is.  See
# KNOWN LIMITS in the module docstring.
EXPECTED_LEG_DIGEST: Dict[str, str] = {
    'check_L_real_composite_only_direction_is_lambda_tensor_lambda':
        '071a64675695d6702a00e9b6418baf1bb68a5093139c7b3723db8551759c7fb0',
    'check_L_bipartite_chsh_blind_to_composite_only_direction':
        'f1abd9ec4c6c9f62bb3b24523c11cbd83fe9e1ad047b234ba92da24c4013d251',
}


def _leg_digest(labels) -> str:
    return hashlib.sha256(
        '\n'.join(sorted(labels)).encode('utf-8')).hexdigest()


def all_of(n: int, verdicts) -> bool:
    """`all(...)` with the SIZE OF WHAT WAS QUANTIFIED written into the call.

    True iff `verdicts` yields EXACTLY n items and every one of them is
    literally True.  It replaces a bare `all(P(x) for x in xs)` at 61 sites.
    Bare `all(...)` survives at five further sites, listed under VACUITY AT A
    QUANTIFIER SITE in KNOWN LIMITS.

    WHY.  `all(P(x) for x in [])` is True with nothing evaluated, and the leg
    inventory cannot see the difference: the label is still there, the count
    is unchanged, and the record says the leg ran.  A guard written beside the
    quantifier as `len(xs) == n and all(P(x) for x in xs)` does not close it
    either -- an edit that writes `for x in []` INSIDE the comprehension
    leaves `len(xs)` untouched.  The count has to be taken from the SEQUENCE
    THE QUANTIFIER ACTUALLY CONSUMED, which is what this does.

    It also refuses a generator of non-bools: `[o1, o2] == [True, True]` is
    False for truthy objects that are not True, where `all(...)` accepts them.

    WHAT IT DOES NOT DO is in KNOWN LIMITS: `n` is a literal at the call site,
    so a two-site edit that empties the comprehension and moves `n` to 0
    together passes, and a leg that compares TWO quantifiers over one
    iterable still agrees with itself when that iterable is emptied."""
    vs = list(verdicts)
    return len(vs) == n and vs == [True] * n


def _leg(legs: Dict[str, bool], label: str, verdict) -> None:
    """Record one leg.

    Raises on a DUPLICATE LABEL: two writes to one key leave one predicate in
    the dictionary and the other discarded.

    Raises on a verdict that is not literally True or False.  This replaces an
    earlier `legs[label] = bool(verdict)`; under that coercion a bare
    generator expression, a container or a callable reads TRUTHY, and what
    would be recorded is then a fact about the object's type rather than the
    value of a predicate."""
    if label in legs:
        raise AssertionError(
            f"duplicate leg label {label!r} -- two writes to one key, so "
            f"one of the two predicate values would not be in the record")
    if verdict is not True and verdict is not False:
        raise AssertionError(
            f"leg {label!r} was handed a {type(verdict).__name__}, not a "
            f"bool.  A bare generator expression, a container, a callable or "
            f"a Fraction reads TRUTHY under bool() with the predicate never "
            f"evaluated; this helper refuses the coercion rather than "
            f"recording a leg that was never run")
    legs[label] = verdict


def _enforce_leg_inventory(record: dict) -> None:
    """The four inventory quantities, computed on the record _result() is
    about to return.

    IT IS HERE AND NOT ONLY IN run_all() because verify_all.run_module
    enumerates a module's attributes whose names start with `check_` and calls
    each one DIRECTLY; a module's own run_all() is never invoked by it.  This
    corpus has a standing note on that (v24.3.450: "the bank does not call
    run_all(); bank.py invokes each registered check_fn() directly and reads
    r['passed']").  So the frozen count literal, the frozen digest literal,
    the set-exact inventory comparison and the verdict re-derivation are
    computed HERE, inside the single function every check returns through.
    run_all() computes them again on the returned record.

    RAISE, NOT `passed = False`, AND DELIBERATELY.  verify_all classifies a
    returned passed=False as FLAG and a raised exception as FAIL.  The two
    genres are different and are graded differently here:

      A FALSE PREDICATE is a claim of this module turning out untrue.  The
      record is intact and legible, the failing labels are listed in it and
      named in its `summary` field, and a reader can act on it.  That is
      returned as passed=False -- a FLAG.

      A BROKEN INVENTORY is not a result at all.  It means the record no
      longer describes what ran, so no field of it -- including `passed` --
      should be read, quoted or aggregated.  Hence: false predicate -> FLAG,
      broken record -> FAIL.

    Every literal read below is read from the module-level frozen constants,
    NOT from whatever local variable the caller used."""
    name = record['name']
    if name not in EXPECTED_LEGS:
        raise AssertionError(
            f"{name}: no frozen leg inventory for this check")
    if name not in EXPECTED_LEG_COUNTS or name not in EXPECTED_LEG_DIGEST:
        raise AssertionError(
            f"{name}: no frozen leg-count / leg-digest literal")
    frozen: FrozenSet[str] = EXPECTED_LEGS[name]
    labels = list(record['leg_labels'])
    # (1) SET-EXACT, against the frozen literal read here.
    if set(labels) != set(frozen):
        raise AssertionError(
            f"{name}: the evaluated leg inventory does not match the frozen "
            f"literal -- missing {sorted(set(frozen) - set(labels))[:8]}, "
            f"unexpected {sorted(set(labels) - set(frozen))[:8]}")
    # (2) THE COUNT LITERAL, over every count in play at once.
    if not (len(labels) == record['legs_evaluated']
            == record['legs_expected'] == len(frozen)
            == EXPECTED_LEG_COUNTS[name]):
        raise AssertionError(
            f"{name}: leg counts disagree with the frozen literal "
            f"({len(labels)} labels, {record['legs_evaluated']} evaluated, "
            f"{record['legs_expected']} expected, {len(frozen)} frozen set, "
            f"{EXPECTED_LEG_COUNTS[name]} frozen count)")
    # (3) THE LABEL DIGEST, on the evaluated labels AND on the frozen set.
    for source, ls in (('evaluated', labels), ('expected', sorted(frozen))):
        got = _leg_digest(ls)
        if got != EXPECTED_LEG_DIGEST[name]:
            raise AssertionError(
                f"{name}: the {source} leg-label digest {got[:16]} does not "
                f"match the frozen literal {EXPECTED_LEG_DIGEST[name][:16]}")
    # (4) THE VERDICT, RE-DERIVED FROM THE RETURNED FIELDS.  A `passed` that
    # disagrees with the record it was supposedly computed from is a broken
    # record, not a failed claim.
    rederived = (not record['fail_reasons']
                 and not record['leg_inventory_missing']
                 and not record['leg_inventory_unexpected'])
    if record['passed'] != rederived:
        raise AssertionError(
            f"{name}: the reported verdict {record['passed']} disagrees with "
            f"the verdict re-derived from the returned records {rederived} -- "
            f"{len(record['fail_reasons'])} failed legs, "
            f"{len(record['leg_inventory_missing'])} missing, "
            f"{len(record['leg_inventory_unexpected'])} unexpected")


def _result(name, epistemic, key_result, evidence, legs, tier,
            dependencies, premises, negative_controls, cross_refs):
    """Build the result dict from the leg inventory.  No verdict is written
    down anywhere; `passed` is computed here and only here, and the frozen
    inventory literals are computed here too, by _enforce_leg_inventory().

    THE RECORD CARRIES A `summary`.  verify_all prints
    `ret.get("summary") or ret.get("key_result")` when a check returns
    passed=False, and this module's key_result is a statement of what the
    module found, not a failure message; without a `summary` a FLAG would
    print several thousand words of result text in place of the failing
    labels.  `summary` names them, and is None when nothing failed so the
    key_result remains the fallback everywhere else."""
    expected: FrozenSet[str] = EXPECTED_LEGS[name]
    seen = set(legs)
    missing = tuple(sorted(expected - seen))
    unexpected = tuple(sorted(seen - expected))
    fail_reasons = tuple(label for label, verdict in legs.items()
                         if not verdict)
    passed = (seen == expected) and all(legs.values())
    record = {
        'name': name,
        'epistemic': epistemic,
        'passed': passed,
        'tier': tier,
        'key_result': key_result,
        'summary': (('FAILED LEGS: ' + ', '.join(fail_reasons[:6]))
                    if fail_reasons else None),
        'evidence': evidence,
        'fail_reasons': list(fail_reasons),
        'leg_inventory_missing': list(missing),
        'leg_inventory_unexpected': list(unexpected),
        'legs_evaluated': len(legs),
        'legs_expected': len(expected),
        'leg_labels': sorted(legs),
        'dependencies': list(dependencies),
        'premises': list(premises),
        'negative_controls': list(negative_controls),
        'cross_refs': list(cross_refs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS),
        'bank_modified': BANK_MODIFIED,
    }
    _enforce_leg_inventory(record)
    return record


# ==========================================================================
# Exact rational linear algebra over R.  Fractions only; no floats anywhere.
# ==========================================================================


def mat(rows: Sequence[Sequence[object]]) -> Mat:
    return tuple(tuple(F(x) for x in r) for r in rows)


def eye(n: int) -> Mat:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n))
                 for i in range(n))


def zeros(n: int) -> Mat:
    return tuple(tuple(F(0) for _ in range(n)) for _ in range(n))


def add(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def sub(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(x - y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(c, a: Mat) -> Mat:
    return tuple(tuple(F(c) * x for x in r) for r in a)


def mm(a: Mat, b: Mat) -> Mat:
    inner = len(b)
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(inner)), F(0))
              for j in range(len(b[0])))
        for i in range(len(a)))


def trace(a: Mat) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def trace_product(a: Mat, b: Mat) -> F:
    """Tr(A B) without forming A B.  Used on the 64x64 k = 3 system."""
    n = len(a)
    return sum((a[i][j] * b[j][i] for i in range(n) for j in range(n)), F(0))


def kron(a: Mat, b: Mat) -> Mat:
    """Kronecker product of two SQUARE matrices, with the first factor
    indexing the slow axis."""
    n, m = len(a), len(b)
    return tuple(
        tuple(a[i // m][j // m] * b[i % m][j % m] for j in range(n * m))
        for i in range(n * m))


def flat(a: Mat) -> List[F]:
    return [x for r in a for x in r]


def hs(a: Mat, b: Mat) -> F:
    """Hilbert-Schmidt inner product sum_ij a_ij b_ij.  The FULL sum, not the
    diagonal.  Leg P computes this convention and the transposed one on a
    single non-symmetric pair and requires the two values to differ."""
    return sum((a[i][j] * b[i][j] for i in range(len(a))
                for j in range(len(a[0]))), F(0))


def linear_combination(*terms) -> Mat:
    """sum_k c_k M_k, given (c, M) pairs; all M of the same size."""
    out = zeros(len(terms[0][1]))
    for c, m in terms:
        out = add(out, scale(F(c), m))
    return out


def rank(vectors: Sequence[Sequence[F]]) -> int:
    rows = [list(v) for v in vectors]
    if not rows:
        return 0
    n, cols, r = len(rows), len(rows[0]), 0
    for c in range(cols):
        piv = next((i for i in range(r, n) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(n):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a2 - f * b2 for a2, b2 in zip(rows[i], rows[r])]
        r += 1
        if r == n:
            break
    return r


def mat_rank(ms: Sequence[Mat]) -> int:
    return rank([flat(m) for m in ms])


def in_span(v: Mat, basis: Sequence[Mat]) -> bool:
    r0 = mat_rank(basis)
    return mat_rank(list(basis) + [v]) == r0


def is_symmetric(a: Mat) -> bool:
    n = len(a)
    return all(a[i][j] == a[j][i] for i in range(n) for j in range(n))


def transpose(a: Mat) -> Mat:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a)))


def is_scalar_multiple(a: Mat, b: Mat) -> bool:
    """True iff a == c * b for some rational c.  EVERY entry is compared,
    off-diagonal included; b == 0 is accepted only for a == 0."""
    n, m = len(a), len(a[0])
    if len(b) != n or len(b[0]) != m:
        return False
    c = None
    for i in range(n):
        for j in range(m):
            if b[i][j] == 0:
                if a[i][j] != 0:
                    return False
            else:
                q = a[i][j] / b[i][j]
                if c is None:
                    c = q
                elif c != q:
                    return False
    if c is None:                       # b is the zero matrix
        return all(a[i][j] == 0 for i in range(n) for j in range(m))
    return a == scale(c, b)


def det(m: Mat) -> F:
    n = len(m)
    a = [list(r) for r in m]
    d = F(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if a[i][c] != 0), None)
        if piv is None:
            return F(0)
        if piv != c:
            a[c], a[piv] = a[piv], a[c]
            d = -d
        d *= a[c][c]
        pv = a[c][c]
        for i in range(c + 1, n):
            if a[i][c] != 0:
                f = a[i][c] / pv
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return d


def is_psd(m: Mat) -> bool:
    """Exact PSD test for a symmetric matrix: ALL principal minors >= 0.

    Not the LEADING principal minors -- those are Sylvester's criterion for
    positive DEFINITENESS and are not sufficient for PSD.  The leg-P witness
    [[0,0],[0,-1]] has non-negative leading minors and is not PSD.  A second
    leg-P witness has a binding principal minor of exactly -10^-6, and its
    value is computed by an adjacent leg.
    """
    n = len(m)
    if not is_symmetric(m):
        return False
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            if det(tuple(tuple(m[i][j] for j in idx) for i in idx)) < 0:
                return False
    return True


def sym_basis(n: int) -> List[Mat]:
    """The n(n+1)/2 symmetric elementary matrices E_ij + E_ji."""
    out = []
    for i in range(n):
        for j in range(i, n):
            m = [[F(0)] * n for _ in range(n)]
            m[i][j] = F(1)
            m[j][i] = F(1)
            out.append(tuple(tuple(r) for r in m))
    return out


def anti_basis(n: int) -> List[Mat]:
    """The n(n-1)/2 antisymmetric elementary matrices E_ij - E_ji."""
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            m = [[F(0)] * n for _ in range(n)]
            m[i][j] = F(1)
            m[j][i] = F(-1)
            out.append(tuple(tuple(r) for r in m))
    return out


def kernel_basis(a: Mat) -> List[List[F]]:
    """A basis of {v : A v = 0}, exact, by reduced row echelon form."""
    n = len(a)
    rows = [list(r) for r in a]
    piv_cols: List[int] = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv_cols.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv_cols]
    out: List[List[F]] = []
    for fc in free:
        v = [F(0)] * n
        v[fc] = F(1)
        for ri, pc in enumerate(piv_cols):
            v[pc] = -rows[ri][fc]
        out.append(v)
    return out


# --------------------------------------------------------------------------
# Characteristic polynomials, exact, by Faddeev-LeVerrier.  Used to decide
# SPECTRAL INEQUIVALENCE without ever extracting a root: two matrices with
# different characteristic polynomials are not conjugate, over any field.
# --------------------------------------------------------------------------


def charpoly(a: Mat) -> Tuple[F, ...]:
    """Coefficients (c_0, ..., c_n) of det(x I - A) = sum_i c_i x^i."""
    n = len(a)
    c = [F(0)] * (n + 1)
    c[n] = F(1)
    M = zeros(n)
    for k in range(1, n + 1):
        M = add(mm(a, M), scale(c[n - k + 1], eye(n)))
        c[n - k] = -trace(mm(a, M)) / k
    return tuple(c)


def poly_from_roots(roots: Sequence[F]) -> Tuple[F, ...]:
    """prod_i (x - r_i), as a coefficient tuple in the same convention."""
    p: List[F] = [F(1)]
    for r in roots:
        q = [F(0)] * (len(p) + 1)
        for i, ci in enumerate(p):
            q[i] += -F(r) * ci
            q[i + 1] += ci
        p = q
    return tuple(p)


# --------------------------------------------------------------------------
# Partial transposes.  The mechanism behind everything at legs W and K.
# --------------------------------------------------------------------------


def partial_transpose(m: Mat, dA: int, side: str) -> Mat:
    """Transpose the A or B factor of a dA x dB bipartite operator.

    Index convention i = a * dB + b, matching kron() with the first factor on
    the slow axis."""
    n = len(m)
    dB = n // dA
    out = [[F(0)] * n for _ in range(n)]
    for a in range(dA):
        for b in range(dB):
            for c in range(dA):
                for d in range(dB):
                    if side == 'A':
                        out[a * dB + b][c * dB + d] = m[c * dB + b][a * dB + d]
                    else:
                        out[a * dB + b][c * dB + d] = m[a * dB + d][c * dB + b]
    return tuple(tuple(r) for r in out)


def regroup_copies(m: Mat, k: int) -> Mat:
    """Reindex an operator on (A (x) B)^{(x)k} to A^{(x)k} (x) B^{(x)k}.

    Bit t of the source index runs a1 b1 a2 b2 ... ak bk; the target runs
    a1 ... ak b1 ... bk.  A permutation of basis labels, nothing more."""
    n = 4 ** k

    def perm(i: int) -> int:
        bits = [(i >> (2 * k - 1 - t)) & 1 for t in range(2 * k)]
        out = 0
        for x in [bits[2 * t] for t in range(k)] + \
                 [bits[2 * t + 1] for t in range(k)]:
            out = (out << 1) | x
        return out

    p = [perm(i) for i in range(n)]
    res = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            res[p[i]][p[j]] = m[i][j]
    return tuple(tuple(r) for r in res)


# ==========================================================================
# Exact Gaussian-rational complex linear algebra, for the leg-E(iii) control.
# A complex number is a pair (re, im) of Fractions.  Still no floats.
#
# EVERY primitive here is witnessed at leg P.  A split-complex product
# (i^2 = +1) reproduces every dimension count at leg E(iii) exactly and
# satisfies a Hermiticity test; what separates it from complex multiplication
# is the value of i^2, and leg P computes that value and two written-out ckron
# literals.
# ==========================================================================


def cx(re, im=0) -> Tuple[F, F]:
    return (F(re), F(im))


def cmul(u: Tuple[F, F], v: Tuple[F, F]) -> Tuple[F, F]:
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def ckron(a: CMat, b: CMat) -> CMat:
    n, m = len(a), len(b)
    return tuple(
        tuple(cmul(a[i // m][j // m], b[i % m][j % m]) for j in range(n * m))
        for i in range(n * m))


def cflat(a: CMat) -> List[F]:
    """Realify: real and imaginary parts as separate real coordinates."""
    return [x for r in a for e in r for x in e]


def cdagger(a: CMat) -> CMat:
    """Conjugate transpose."""
    n = len(a)
    return tuple(tuple((a[j][i][0], -a[j][i][1]) for j in range(n))
                 for i in range(n))


def herm_basis(n: int) -> List[CMat]:
    """The n^2 real-linearly-independent Hermitian generators of M_n(C)."""
    out = []
    for i in range(n):
        m = [[cx(0)] * n for _ in range(n)]
        m[i][i] = cx(1)
        out.append(tuple(tuple(r) for r in m))
    for i in range(n):
        for j in range(i + 1, n):
            m = [[cx(0)] * n for _ in range(n)]
            m[i][j] = cx(1)
            m[j][i] = cx(1)
            out.append(tuple(tuple(r) for r in m))
            m = [[cx(0)] * n for _ in range(n)]
            m[i][j] = cx(0, 1)
            m[j][i] = cx(0, -1)
            out.append(tuple(tuple(r) for r in m))
    return out


def cmat_rank(ms: Sequence[CMat]) -> int:
    return rank([cflat(m) for m in ms])


# ==========================================================================
# A two-variable polynomial ring over Q, for the symbolic proof at leg D_sym.
# A polynomial is a dict {(i, j): coefficient} for the monomial n^i m^j;
# zero coefficients are never stored, so equality of dicts IS equality of
# polynomials.
# ==========================================================================

Poly = Dict[Tuple[int, int], F]

P_ONE: Poly = {(0, 0): F(1)}
P_N: Poly = {(1, 0): F(1)}
P_M: Poly = {(0, 1): F(1)}


def p_add(p: Poly, q: Poly) -> Poly:
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v != 0}


def p_scale(c, p: Poly) -> Poly:
    return {k: F(c) * v for k, v in p.items() if F(c) * v != 0}


def p_mul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for a, ca in p.items():
        for b, cb in q.items():
            k = (a[0] + b[0], a[1] + b[1])
            out[k] = out.get(k, F(0)) + ca * cb
    return {k: v for k, v in out.items() if v != 0}


def p_eval(p: Poly, n: int, m: int) -> F:
    return sum((c * F(n) ** i * F(m) ** j for (i, j), c in p.items()), F(0))


# ==========================================================================
# The concrete objects at (n, m) = (2, 2).
# ==========================================================================

I2 = eye(2)
I4 = eye(4)
Z = mat([[1, 0], [0, -1]])
X = mat([[0, 1], [1, 0]])
J = mat([[0, -1], [1, 0]])              # the generator of Lam(R^2)
JJ = kron(J, J)                         # the composite-only direction at (2,2)
ZZ = kron(Z, Z)
XX = kron(X, X)

# The local reflection on Alice's side used at leg H to DISCLOSE the gauge
# relation between the sigma endpoints.
REFLECT = mat([[1, 0], [0, -1]])
REFLECT_A = kron(REFLECT, I2)

# Bob's settings, rescaled by sqrt(2) so every entry stays rational.
B0P = add(Z, X)
B1P = sub(Z, X)

# The complex orientation axis Y = iJ, used only as a ckron witness.
Y_C: CMat = ((cx(0), cx(0, -1)), (cx(0, 1), cx(0)))
Z_C: CMat = ((cx(1), cx(0)), (cx(0), cx(-1)))


def pure(v: Sequence[F]) -> Mat:
    """The projector onto the line through v, normalized exactly."""
    n = sum((x * x for x in v), F(0))
    return tuple(tuple(v[i] * v[j] / n for j in range(len(v)))
                 for i in range(len(v)))


PSI_MINUS = pure([F(0), F(1), F(-1), F(0)])     # the real singlet
PHI_PLUS = pure([F(1), F(0), F(0), F(1)])

# ---- THE INTERVAL FAMILY (leg H).  Its endpoints are NOT the witness pair;
# they are related by REFLECT_A, computed and disclosed at leg H.
LOCAL_PART_H = linear_combination((F(1, 4), I4), (F(1, 8), ZZ))


def sigma(t) -> Mat:
    return add(LOCAL_PART_H, scale(F(t), JJ))


def tau(t) -> Mat:
    """The control family: differs in a LOCALLY VISIBLE direction."""
    return add(scale(F(1, 4), I4), scale(F(t), ZZ))


# ---- THE WITNESS PAIR OF RECORD (legs W and K).  Spectrally inequivalent,
# so no conjugation of any kind relates them.
R_LOCAL = linear_combination((F(1, 4), I4), (F(1, 16), XX), (F(1, 16), ZZ))
EPS_W = F(1, 32)


def rho_w(sign: int) -> Mat:
    return add(R_LOCAL, scale(F(sign) * EPS_W, JJ))


RHO_PLUS = rho_w(1)
RHO_MINUS = rho_w(-1)

SPEC_PLUS = (F(13, 32), F(7, 32), F(7, 32), F(5, 32))
SPEC_MINUS = (F(11, 32), F(9, 32), F(9, 32), F(3, 32))

# Seven symmetric probes per side for the product-observable sweep.  At most
# THREE of them can be independent, since dim Sym(R^2) = 3; the extra four
# are duplicates inside the same span, not coverage.
PROBES: Tuple[Mat, ...] = (
    I2, Z, X,
    mat([[1, 2], [2, -3]]),
    mat([[-5, 1], [1, 7]]),
    mat([[0, 3], [3, 0]]),
    mat([[4, -1], [-1, 4]]),
)

# The three-element basis of Sym(R^2) whose nine products are the whole
# product-observable span at (2,2).
BASIS_2 = (I2, Z, X)

# THE hs CONVENTION WITNESS PAIR, named once so the two literal legs and the
# VALUE TIE between the two conventions all read the same matrices.  A
# previous version wrote the pair out twice and asserted two independent
# literals (hs == 0, trace_product == 1) with nothing comparing them, so a
# two-site edit moving both literals survived.
HS_NONSYM_A = mat([[0, 1], [0, 0]])
HS_NONSYM_B = mat([[0, 0], [1, 0]])

# THE k-COPY EFFECT SEEDS, hoisted (audit MAJOR-2).  The loop that BUILDS the
# effect battery and the legs that certify the battery is non-degenerate must
# read ONE variable.  A previous version consumed (1, 7, 99) x (3, 42) in the
# loop while three "the effects are pairwise distinct / symmetric / not all
# multiples of the identity" legs re-derived the seed list as a frozen
# literal, so changing the loop's seeds to (5,5,5) x (5,5) was one line, no
# pin touched, and left the battery with one distinct pair out of six while
# the negative control asserted the opposite in so many words.
K_EFFECT_SEEDS_A = (1, 7, 99)
K_EFFECT_SEEDS_B = (3, 42)


def correlator(rho: Mat, a: Mat, b: Mat) -> F:
    return trace(mm(rho, kron(a, b)))


def correlator_vector(rho: Mat) -> Tuple[F, F, F, F]:
    """The four SCALED correlators in the banked test's (00, 01, 10, 11)
    order.  Each true correlator is this value divided by sqrt(2)."""
    return (correlator(rho, Z, B0P), correlator(rho, Z, B1P),
            correlator(rho, X, B0P), correlator(rho, X, B1P))


def raw_chsh(v: Sequence[F]) -> F:
    return v[0] + v[1] + v[2] - v[3]


def _refuses(thunk) -> bool:
    """True iff calling `thunk` raises AssertionError.  Leg P computes it on a
    thunk that raises and on one that does not, and every self-comparison
    refusal below is recorded through it."""
    try:
        thunk()
    except AssertionError:
        return True
    return False


def _refuse_self_comparison(r1: Mat, r2: Mat, where: str) -> None:
    """Raise if the two arguments are the same matrix, by identity or by
    value.  A comparison of an object with itself returns the agreeing answer
    for a reason that has nothing to do with any result."""
    if r1 is r2 or r1 == r2:
        raise AssertionError(
            f"{where}: the two arguments are the same matrix.  They agree on "
            f"every observable for a reason that has nothing to do with any "
            f"result")


def _distinct(a: Mat, b: Mat, where: str) -> Tuple[Mat, Mat]:
    """Return (a, b) after _refuse_self_comparison.  Used at the comparison
    sites that do not go through product_sweep or
    correlator_vectors_of_pair."""
    _refuse_self_comparison(a, b, where)
    return a, b


def _difference_of_distinct(a: Mat, b: Mat, where: str) -> Mat:
    """sub(a, b), with the pair taken through _distinct first.  The leg that
    consumes this cannot name one of the two matrices twice, because it never
    sees them: it sees the difference."""
    x, y = _distinct(a, b, where)
    return sub(x, y)


def _charpolys_of_distinct(a: Mat, b: Mat,
                           where: str) -> Tuple[Tuple[F, ...],
                                                Tuple[F, ...]]:
    """(charpoly(a), charpoly(b)), with the pair taken through _distinct."""
    x, y = _distinct(a, b, where)
    return charpoly(x), charpoly(y)


def _joint_tables_of_distinct(a: Mat, b: Mat, projectors: Sequence[Mat],
                              where: str):
    """The two joint-outcome tables of a pair of states over one projector
    list, with the pair taken through _distinct."""
    x, y = _distinct(a, b, where)
    return ([[correlator(x, p, q) for q in projectors] for p in projectors],
            [[correlator(y, p, q) for q in projectors] for p in projectors])


def _distinct_lists(xs: Sequence[Mat], ys: Sequence[Mat],
                    where: str) -> Tuple[Sequence[Mat], Sequence[Mat]]:
    """Return (xs, ys), raising if the two are one list handed twice, by
    identity or by value.  Used by the leg-C orthogonality loop, whose two
    loop variables range over two different generator families."""
    if xs is ys or list(xs) == list(ys):
        raise AssertionError(
            f"{where}: the two generator lists are the same list.  A loop "
            f"over one family against itself is a different statement")
    return xs, ys


def _product_sweep_raw(r1: Mat, r2: Mat, probes: Sequence[Mat]
                       ) -> Tuple[List[Tuple[int, int]],
                                  List[Tuple[int, int]]]:
    """Sweep every ordered pair from `probes` and report (tested, separating).

    THE COUNT AND THE SWEEP COME FROM ONE VARIABLE.  A previous version
    returned only the separating list, and the leg that reported "the probe
    sweep has forty-nine pairs" re-derived 49 from the module constant PROBES
    rather than from the list the sweep actually ran.  `tested` is what ran."""
    tested = [(i, j) for i in range(len(probes)) for j in range(len(probes))]
    sep = [(i, j) for (i, j) in tested
           if correlator(r1, probes[i], probes[j])
           != correlator(r2, probes[i], probes[j])]
    return tested, sep


def product_sweep(r1: Mat, r2: Mat, probes: Sequence[Mat]
                  ) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """_product_sweep_raw, refusing a self-comparison.  THERE IS NO FLAG ON
    THIS ROUTINE.  An earlier version carried an allow_self_comparison
    keyword so that the deliberate exhibit could reuse the same function; the
    keyword then existed on the routine every content leg calls.  The exhibit
    is now a separate function below."""
    _refuse_self_comparison(r1, r2, 'product_sweep')
    return _product_sweep_raw(r1, r2, probes)


def product_sweep_self_comparison_exhibit(
        r: Mat, probes: Sequence[Mat]
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """The deliberate self-comparison, on its own routine: what a vacuous zero
    looks like.  It takes ONE matrix, so there is no second argument."""
    return _product_sweep_raw(r, r, probes)


def separating_pairs(r1: Mat, r2: Mat, probes: Sequence[Mat]
                     ) -> List[Tuple[int, int]]:
    """The separating half of product_sweep, with the same refusal."""
    return product_sweep(r1, r2, probes)[1]


def _correlator_vectors_raw(pair: Tuple[Mat, Mat]
                            ) -> Tuple[Tuple[F, F, F, F],
                                       Tuple[F, F, F, F]]:
    r1, r2 = pair
    return correlator_vector(r1), correlator_vector(r2)


def correlator_vectors_of_pair(pair: Tuple[Mat, Mat]
                               ) -> Tuple[Tuple[F, F, F, F],
                                          Tuple[F, F, F, F]]:
    """The two correlator vectors of a pair of states, refusing a pair whose
    two members are the same matrix.  "The two states give the same correlator
    vector" is the headline at leg E2, and a pair whose members are the same
    matrix gives it for a reason that has nothing to do with the result.  As
    with product_sweep, there is no flag; the exhibit is a separate
    function."""
    _refuse_self_comparison(pair[0], pair[1], 'correlator_vectors_of_pair')
    return _correlator_vectors_raw(pair)


def correlator_vectors_self_comparison_exhibit(
        r: Mat) -> Tuple[Tuple[F, F, F, F], Tuple[F, F, F, F]]:
    """The deliberate self-comparison, on its own routine.  It takes ONE
    matrix."""
    return _correlator_vectors_raw((r, r))


def sym_probe(d: int, seed: int) -> Mat:
    """A deterministic exact-rational SYMMETRIC matrix of size d.  Used as a
    collective local effect at leg K; the recursion is a fixed integer
    sequence, so the object is reproducible and contains no float."""
    m = [[F(0)] * d for _ in range(d)]
    v = seed
    for i in range(d):
        for j in range(i, d):
            v = (v * 1103515245 + 12345) % 2147483648
            x = F((v % 13) - 6, (v % 5) + 1)
            m[i][j] = x
            m[j][i] = x
    return tuple(tuple(r) for r in m)


# ==========================================================================
# The sqrt-free polytope decision, built on the banked facets.
# ==========================================================================


def inside_scaled(scaled: Sequence[F], k: F, facets=None) -> bool:
    """Is  scaled / sqrt(k)  inside the polytope cut by `facets`?  Sqrt-free.

    k is a positive rational.  Two exact translations:
      box   |v / sqrt(k)| <= 1        <=>  v^2 <= k ;
      facet <s, v> / sqrt(k) <= 2     <=>  <s, v> <= 0  OR  <s,v>^2 <= 4 k .
    The sign split is REQUIRED: squaring reverses the inequality for a
    negative dot product.  On the BANKED list it changes no verdict, because
    that list is closed under negation (computed at leg C2); leg C2 therefore
    computes the guarded and the unguarded procedure on a synthetic list that
    is NOT negation-closed, and they give opposite verdicts there.

    BOTH CLAUSES ARE EXERCISED AT k != 1, which is the only regime any
    downstream use is in.  At k = 1 the constants k, k^2 and 1 coincide; leg
    P2 computes each of three alternative box clauses against this one on a
    witness that is OUTSIDE at k = 2 and INSIDE at k = 4.
    """
    if k <= 0:
        raise ValueError("inside_scaled: k must be positive")
    bound = F(CLASSICAL_CHSH_BOUND)
    if facets is None:
        facets = _chsh_facets()
    for v in scaled:
        if F(v) * F(v) > k:
            return False
    for s in facets:
        d = _dot(s, scaled)
        if d > 0 and d * d > bound * bound * k:
            return False
    return True


_VALIDATION_VALUES = (F(-3, 2), F(-1), F(-7, 10), F(0), F(1, 2), F(1))

# The three plausible mis-scalings of the BOX clause, written out so leg P2
# can execute each of them against the true procedure rather than describe
# them.  Each is a complete alternative box test.


def _box_true(v: F, k: F) -> bool:
    return v * v <= k


def _box_k_squared(v: F, k: F) -> bool:
    return v * v <= k * k


def _box_unit(v: F, k: F) -> bool:
    return v * v <= F(1)


def _box_abs_k(v: F, k: F) -> bool:
    return (v if v >= 0 else -v) <= k


_BOX_VARIANTS = (('v^2 <= k*k', _box_k_squared),
                 ('v^2 <= 1', _box_unit),
                 ('|v| <= k', _box_abs_k))


# ==========================================================================
# CHECK 1
# ==========================================================================

# ==========================================================================
# WHICH EVIDENCE ENTRIES ARE CERTIFIED.  Audit item: the evidence dict sat
# OUTSIDE the leg inventory entirely -- inflating the reported CHSH^2 from 8
# to 16 in `ev` left every leg green, so a number a reader would quote was
# uncertified while every number a leg computed was not.  The entries named
# below are TIED BY VALUE to the computation that produced them, by the EV
# legs at the end of each check.  EVERY OTHER ENTRY OF `ev` IS DESCRIPTIVE
# AND UNCERTIFIED, and is labelled as such here rather than left to be found.
# ==========================================================================

CERTIFIED_EVIDENCE_KEYS_1: Tuple[str, ...] = (
    'real_shapes', 'rho_plus_spectrum', 'rho_minus_spectrum',
    'rho_basis_separations', 'rho_probe_separations', 'rho_global_JJ_values',
    'bank_probe_identity_count_defect', 'bank_probe_quaternionic_defect',
    'sibling_signed_mismatch', 'maximizer_eigenspace_dimension',
    'maximizer_family_size', 'multicopy',
)

CERTIFIED_EVIDENCE_KEYS_2: Tuple[str, ...] = (
    'chsh_squared', 'raw_signed', 'scaled_correlators', 'validation_vectors',
    'validation_inside', 'validation_mismatches', 'true_max_facet_squared',
    'witness_pair_composite_coordinates',
)

REAL_SHAPES = ((2, 2), (2, 3), (3, 3), (2, 4), (2, 5), (3, 4))
COMPLEX_SHAPES = ((2, 2), (2, 3), (3, 3))
# Shapes used ONLY at leg D''', for which this module ships no literal.
PROBE_SHAPES = ((4, 4), (3, 5), (5, 5))
PROBE_DROP = 3
BATTERY_LABELS = ("psi-", "phi+", "I/4", "|00><00|", "sigma_+1/8",
                  "sigma_-1/8", "(psi-+phi+)/2", "rho_+", "rho_-")
EIGEN_PARAMS = (F(0), F(1), F(-1), F(1, 2), F(2), F(3, 7))
COPY_COUNTS = (1, 2, 3)


def check_L_real_composite_only_direction_is_lambda_tensor_lambda() -> dict:
    """[P_math].  The state parameters of the real bipartite GPT that no
    product observable can read are exactly the Lam (x) Lam directions, their
    number is the bank's own Delta_R(n, m), and at (2,2) the single free
    parameter is realized by a spectrally inequivalent pair of PPT states that
    no number of local copies can tell apart.  PPT plus the named Horodecki
    import gives separability IN THE COMPLEX EMBEDDING; in the REAL product
    cone the pair is NOT separable, and that is computed here."""
    _NAME = 'check_L_real_composite_only_direction_is_lambda_tensor_lambda'
    legs: Dict[str, bool] = {}
    ev: Dict[str, object] = {}

    def L(label: str, verdict) -> None:
        _leg(legs, label, verdict)

    # THE GRADE STRING, BOUND ONCE.  This name is what the grade leg below
    # reads and what is handed to _result() at the bottom of this function;
    # the string is not written out a second time at either site.
    epistemic = (
        "[P_math | structural premises: "
        "LOCAL_PRODUCT_OBSERVABLE_MODEL and PSD_CONE_CONVEXITY. "
        "Named mathematical imports: HOROD_1996_PPT_SEPARABLE "
        "(leg W, COMPLEX 2x2 only), "
        "GL_BRANCHING_OF_THE_SYMMETRIC_SQUARE (the general-(n,m) "
        "span statement only), SPECTRAL_THEOREM_FINITE_DIM "
        "(legs G, H), PSD_TRACE_PAIRING (leg G), "
        "SIMILARITY_INVARIANCE_OF_CHARPOLY (leg W), "
        "PARTIAL_TRANSPOSE_TENSOR_FUNCTORIALITY (leg K), "
        "PARTIAL_TRANSPOSE_TRACE_TRANSFER (leg K), "
        "REAL_SYMMETRIC_PRODUCT_EFFECTS_ARE_PT_EVEN (leg K)]")

    # ---- LEG P: predicate witnesses, each on the axis it is used for -----
    L("P/kron_ZX_literal",
      kron(Z, X) == mat([[0, 1, 0, 0], [1, 0, 0, 0],
                         [0, 0, 0, -1], [0, 0, -1, 0]]))
    L("P/kron_XZ_literal",
      kron(X, Z) == mat([[0, 0, 1, 0], [0, 0, 0, -1],
                         [1, 0, 0, 0], [0, -1, 0, 0]]))
    L("P/kron_order_distinct", kron(Z, X) != kron(X, Z))
    L("P/mm_noncommuting_pair", mm(Z, X) != mm(X, Z))
    L("P/mm_ZX_value", mm(Z, X) == mat([[0, 1], [-1, 0]]))
    L("P/trace_offdiagonal_ignored", trace(mat([[1, 5], [7, 2]])) == 3)
    L("P/trace_product_agrees_with_trace_of_product",
      trace_product(mat([[1, 2], [3, 4]]), mat([[5, 6], [7, 8]]))
      == trace(mm(mat([[1, 2], [3, 4]]), mat([[5, 6], [7, 8]]))))
    L("P/trace_product_rejects_entrywise",
      trace_product(mat([[0, 1], [0, 0]]), mat([[0, 0], [1, 0]])) != 0)
    L("P/hs_X_with_itself_is_2", hs(X, X) == 2)
    L("P/hs_I_and_JJ_orthogonal", hs(I4, JJ) == 0)
    # hs is ENTRYWISE, sum_ij a_ij b_ij = Tr(A B^T).  The transposed
    # convention Tr(A B) returns 1 on this pair.  THE TWO LITERALS ARE TIED BY
    # VALUE, not merely written down beside each other: the third leg below
    # computes both conventions on the SAME named pair and requires the two
    # values to DISAGREE.  (Corpus rule: tie by value, not by verdict.)
    L("P/hs_is_entrywise_and_not_transposed",
      hs(HS_NONSYM_A, HS_NONSYM_B) == 0)
    L("P/hs_transposed_convention_would_have_returned_one",
      trace_product(HS_NONSYM_A, HS_NONSYM_B) == 1)
    L("P/hs_differs_from_the_transposed_convention_on_that_pair",
      hs(HS_NONSYM_A, HS_NONSYM_B) != trace_product(HS_NONSYM_A,
                                                    HS_NONSYM_B))
    L("P/the_hs_witness_pair_is_not_symmetric",
      not is_symmetric(HS_NONSYM_A) and not is_symmetric(HS_NONSYM_B))
    L("P/hs_and_the_transposed_convention_agree_on_a_symmetric_pair",
      hs(Z, X) == trace_product(Z, X))
    L("P/sym_accepts_JJ", is_symmetric(JJ))
    L("P/sym_rejects_J", not is_symmetric(J))
    L("P/sym_rejects_4x4_single_offdiagonal",
      not is_symmetric(mat([[1, 0, 0, 0], [0, 1, 0, 0],
                            [0, 0, 1, 2], [0, 0, 0, 1]])))
    L("P/transpose_is_not_identity", transpose(J) != J)
    L("P/transpose_of_J_is_minus_J", transpose(J) == scale(F(-1), J))
    L("P/scal_accepts_3JJ", is_scalar_multiple(scale(F(3), JJ), JJ))
    L("P/scal_accepts_JJ_over_3JJ", is_scalar_multiple(JJ, scale(F(3), JJ)))
    L("P/scal_rejects_diagonal_trap",
      not is_scalar_multiple(mat([[1, 1], [1, 1]]), I2))
    L("P/scal_rejects_nonzero_over_zero",
      not is_scalar_multiple(I2, zeros(2)))
    L("P/scal_accepts_zero_over_zero",
      is_scalar_multiple(zeros(2), zeros(2)))
    L("P/psd_accepts_identity", is_psd(I4))
    L("P/psd_rejects_negative_diagonal", not is_psd(mat([[2, 0], [0, -1]])))
    L("P/psd_rejects_leading_minor_trap",
      not is_psd(mat([[0, 0], [0, -1]])))
    L("P/psd_rejects_offdiagonal_2x2", not is_psd(mat([[1, 2], [2, 1]])))
    L("P/psd_rejects_offdiagonal_4x4",
      not is_psd(mat([[1, 0, 0, 2], [0, 1, 0, 0],
                      [0, 0, 1, 0], [2, 0, 0, 1]])))
    L("P/psd_rejects_JJ", not is_psd(JJ))
    # THE TOLERANCE WITNESS: the binding 2x2 minor of `_tiny` is exactly
    # -10^-6, computed by the leg below it, and is_psd is computed on `_tiny`
    # and on its positive-minor counterpart.
    _tiny = mat([[F(1), F(1)], [F(1), F(999999, 1000000)]])
    L("P/psd_rejects_tiny_negative_minor", not is_psd(_tiny))
    L("P/psd_tiny_witness_minor_is_minus_one_millionth",
      det(_tiny) == F(-1, 1000000))
    L("P/psd_accepts_tiny_positive_minor",
      is_psd(mat([[F(1), F(1)], [F(1), F(1000001, 1000000)]])))
    # THE SYMMETRY PRECONDITION, WITNESSED.  [[1,2],[0,1]] has principal
    # minors 1, 1 and 1 -- all non-negative, computed below -- and is not
    # symmetric, also computed below.  is_psd is computed on it.
    L("P/psd_rejects_a_non_symmetric_matrix_with_non_negative_minors",
      not is_psd(mat([[1, 2], [0, 1]])))
    L("P/psd_symmetry_witness_really_has_non_negative_minors",
      det(mat([[1, 2], [0, 1]])) >= 0 and mat([[1, 2], [0, 1]])[0][0] >= 0
      and mat([[1, 2], [0, 1]])[1][1] >= 0)
    L("P/psd_symmetry_witness_is_not_symmetric",
      not is_symmetric(mat([[1, 2], [0, 1]])))
    L("P/det_2x2_value", det(mat([[1, 2], [3, 4]])) == -2)
    L("P/det_singular_is_zero", det(mat([[1, 2], [2, 4]])) == 0)
    L("P/det_offdiagonal_sign", det(mat([[0, 1], [1, 0]])) == -1)
    L("P/det_3x3_diagonal", det(mat([[2, 0, 0], [0, 3, 0], [0, 0, -1]])) == -6)
    L("P/rank_of_rank_one_set",
      rank([[F(1), F(0)], [F(2), F(0)], [F(3), F(0)]]) == 1)
    L("P/rank_of_sym4_basis_is_10",
      rank([flat(m) for m in sym_basis(4)]) == 10)
    _loc22 = [kron(a, b) for a in sym_basis(2) for b in sym_basis(2)]
    L("P/span_accepts_identity_in_local", in_span(kron(I2, I2), _loc22))
    L("P/span_rejects_JJ_in_local", not in_span(JJ, _loc22))
    L("P/orth_summed_squares_zero_for_JJ",
      sum((hs(JJ, h) * hs(JJ, h) for h in _loc22), F(0)) == 0)
    L("P/orth_summed_squares_nonzero_for_contaminated",
      sum((hs(add(JJ, kron(I2, I2)), h) ** 2 for h in _loc22), F(0)) != 0)
    L("P/rank_increment_zero_for_member",
      mat_rank(_loc22 + [kron(I2, I2)]) == mat_rank(_loc22))
    L("P/rank_increment_one_for_JJ",
      mat_rank(_loc22 + [JJ]) == mat_rank(_loc22) + 1)
    _asym = pure([F(0), F(1), F(0), F(0)])          # |01><01|, not swap-sym
    L("P/corr_argument_order_values",
      correlator(_asym, Z, I2) == 1 and correlator(_asym, I2, Z) == -1)
    L("P/corr_argument_order_differs",
      correlator(_asym, Z, I2) != correlator(_asym, I2, Z))
    L("P/kernel_basis_of_zero_matrix_is_full",
      len(kernel_basis(zeros(3))) == 3)
    L("P/kernel_basis_of_identity_is_empty", kernel_basis(I4) == [])
    L("P/kernel_basis_vectors_are_annihilated",
      all_of(2, (mm(sub(JJ, I4), tuple((x,) for x in v))
                 == tuple((F(0),) for _ in v)
                 for v in kernel_basis(sub(JJ, I4)))))
    # charpoly, computed against a literal, against a wrong root list, and
    # against its own reversal.  The literal is NON-PALINDROMIC -- (6, -5, 1)
    # for diag(2,3) -- so the reversal leg has two different tuples to
    # compare; the identity's (1, -2, 1) reads the same reversed.
    L("P/charpoly_of_a_non_palindromic_diagonal_2x2",
      charpoly(mat([[2, 0], [0, 3]])) == (F(6), F(-5), F(1)))
    L("P/charpoly_coefficient_order_is_not_reversible",
      charpoly(mat([[2, 0], [0, 3]])) != (F(1), F(-5), F(6)))
    L("P/charpoly_matches_roots_for_diagonal",
      charpoly(mat([[2, 0], [0, 5]])) == poly_from_roots([F(2), F(5)]))
    L("P/charpoly_rejects_wrong_roots",
      charpoly(mat([[2, 0], [0, 5]])) != poly_from_roots([F(2), F(6)]))
    L("P/charpoly_sees_offdiagonal",
      charpoly(mat([[0, 1], [1, 0]])) != charpoly(zeros(2)))
    L("P/charpoly_invariant_under_conjugation",
      charpoly(mm(mm(REFLECT_A, sigma(F(1, 8))), REFLECT_A))
      == charpoly(sigma(F(1, 8))))
    # partial transpose, pinned as an involution, on the transfer identity,
    # and against the FULL transpose which is not the same map.
    L("P/pt_A_is_an_involution",
      partial_transpose(partial_transpose(JJ, 2, 'A'), 2, 'A') == JJ)
    L("P/pt_B_is_an_involution",
      partial_transpose(partial_transpose(JJ, 2, 'B'), 2, 'B') == JJ)
    L("P/pt_A_differs_from_full_transpose",
      partial_transpose(kron(J, mat([[1, 2], [3, 4]])), 2, 'A')
      != transpose(kron(J, mat([[1, 2], [3, 4]]))))
    L("P/pt_A_differs_from_pt_B",
      partial_transpose(kron(J, Z), 2, 'A')
      != partial_transpose(kron(J, Z), 2, 'B'))
    L("P/pt_A_on_a_product_transposes_only_A",
      partial_transpose(kron(J, Z), 2, 'A') == kron(transpose(J), Z))
    # THE TRANSFER-IDENTITY WITNESS LIST IS NAMED, AND ITS LENGTH, ITS
    # PAIRWISE DISTINCTNESS AND THE FACT THAT SOME VALUE ON IT IS NONZERO ARE
    # EACH COMPUTED AS LEGS.  It is load-bearing for the general-k step at leg
    # K, Tr(D E) = Tr(PT_A(D) PT_A(E)), and `all(... for ... in [])` is
    # vacuously True.  The grid, the P2 battery, the leg-C cross-pair count
    # and the k-copy effect battery carry the same three legs; this list did
    # not until now.
    _pt_transfer_witnesses = ((kron(J, Z), kron(X, J)),
                              (PSI_MINUS, kron(Z, X)),
                              (RHO_PLUS, kron(J, J)))
    _pt_transfer_values = [trace(mm(partial_transpose(m1, 2, 'A'), m2))
                           for m1, m2 in _pt_transfer_witnesses]
    L("P/pt_trace_transfer_identity",
      all_of(3, (trace(mm(partial_transpose(m1, 2, 'A'), m2))
                 == trace(mm(m1, partial_transpose(m2, 2, 'A')))
                 for m1, m2 in _pt_transfer_witnesses)))
    L("P/the_pt_transfer_witness_list_has_three_members",
      len(_pt_transfer_witnesses) == 3)
    L("P/the_pt_transfer_witnesses_are_pairwise_distinct",
      len(set(_pt_transfer_witnesses)) == 3)
    L("P/the_pt_transfer_witness_list_is_not_vacuous",
      len(_pt_transfer_values) == 3
      and any(v != 0 for v in _pt_transfer_values))
    # HONEST SCOPE ON THE TRANSFER IDENTITY.  It is NOT what distinguishes
    # the partial transpose: the FULL transpose satisfies it too, computed
    # here rather than assumed away.  What pins the map is the pair of legs
    # above -- PT_A acts on one factor only, and differs from PT_B.  What the
    # transfer identity IS needed for is the step Tr(D E) = Tr(PT_A(D)
    # PT_A(E)) at leg K, and it is exercised against a map that FAILS it.
    _ft_transfer_witnesses = ((kron(J, Z), kron(X, J)),
                              (mat([[1, 2], [3, 4]]), mat([[0, 1], [0, 0]])))
    L("P/trace_transfer_also_holds_for_the_full_transpose",
      all_of(2, (trace(mm(transpose(m1), m2))
                 == trace(mm(m1, transpose(m2)))
                 for m1, m2 in _ft_transfer_witnesses)))
    L("P/the_full_transpose_witness_list_is_not_vacuous",
      len(_ft_transfer_witnesses) == 2
      and any(trace(mm(transpose(m1), m2)) != 0
              for m1, m2 in _ft_transfer_witnesses))
    L("P/trace_transfer_fails_for_a_non_self_adjoint_map",
      trace(mm(mm(mat([[1, 1], [0, 1]]), mat([[1, 2], [3, 4]])),
               mat([[2, 0], [1, 5]])))
      != trace(mm(mat([[1, 2], [3, 4]]),
                  mm(mat([[1, 1], [0, 1]]), mat([[2, 0], [1, 5]])))))
    L("P/regroup_is_identity_at_k_1", regroup_copies(JJ, 1) == JJ)
    L("P/regroup_is_a_permutation_at_k_2",
      sorted(flat(regroup_copies(kron(JJ, ZZ), 2)))
      == sorted(flat(kron(JJ, ZZ))))
    L("P/regroup_moves_something_at_k_2",
      regroup_copies(kron(JJ, ZZ), 2) != kron(JJ, ZZ))
    # ---- THE SELF-COMPARISON REFUSALS, EXERCISED ON BOTH SIDES ----------
    # `_refuses` is itself computed against a thunk that raises nothing and
    # against one that raises.  The four routines that refuse an equal pair --
    # product_sweep, correlator_vectors_of_pair, _distinct and
    # _distinct_lists -- are each computed on an equal pair and on a distinct
    # one.
    L("P/refuses_helper_reports_false_when_nothing_raises",
      _refuses(lambda: None) is False)
    L("P/refuses_helper_reports_true_on_an_assertion",
      _refuses(lambda: (_ for _ in ()).throw(AssertionError('x'))) is True)
    L("P/product_sweep_refuses_the_identical_object",
      _refuses(lambda: product_sweep(RHO_PLUS, RHO_PLUS, BASIS_2)))
    L("P/product_sweep_refuses_an_equal_but_distinct_object",
      rho_w(1) is not RHO_PLUS
      and _refuses(lambda: product_sweep(RHO_PLUS, rho_w(1), BASIS_2)))
    L("P/the_self_comparison_exhibit_routine_returns_the_empty_list",
      product_sweep_self_comparison_exhibit(RHO_PLUS, BASIS_2)[1] == [])
    L("P/product_sweep_accepts_a_genuinely_distinct_pair",
      product_sweep(tau(F(1, 8)), tau(F(-1, 8)), BASIS_2)[1] != [])
    L("P/product_sweep_reports_every_ordered_pair_it_tested",
      len(product_sweep(tau(F(1, 8)), tau(F(-1, 8)), BASIS_2)[0])
      == len(BASIS_2) ** 2)
    L("P/product_sweep_tested_list_tracks_the_probe_list_it_was_handed",
      len(product_sweep(tau(F(1, 8)), tau(F(-1, 8)), PROBES)[0])
      == len(PROBES) ** 2
      != len(product_sweep(tau(F(1, 8)), tau(F(-1, 8)), BASIS_2)[0]))
    L("P/correlator_vectors_of_pair_refuses_the_identical_object",
      _refuses(lambda: correlator_vectors_of_pair((RHO_PLUS, RHO_PLUS))))
    L("P/correlator_vectors_of_pair_refuses_an_equal_but_distinct_object",
      _refuses(lambda: correlator_vectors_of_pair((RHO_PLUS, rho_w(1)))))
    L("P/correlator_vectors_of_pair_accepts_a_distinct_pair",
      correlator_vectors_of_pair((tau(F(1, 8)), tau(F(-1, 8))))[0]
      != correlator_vectors_of_pair((tau(F(1, 8)), tau(F(-1, 8))))[1])
    L("P/the_distinct_helper_refuses_an_equal_pair",
      _refuses(lambda: _distinct(RHO_PLUS, rho_w(1), 'leg P witness')))
    L("P/the_distinct_helper_accepts_a_distinct_pair",
      _distinct(RHO_PLUS, RHO_MINUS, 'leg P witness')
      == (RHO_PLUS, RHO_MINUS))
    L("P/the_distinct_lists_helper_refuses_one_list_handed_twice",
      _refuses(lambda: _distinct_lists(list(BASIS_2), list(BASIS_2),
                                       'leg P witness')))
    L("P/the_distinct_lists_helper_accepts_two_different_lists",
      _distinct_lists(list(BASIS_2), list(PROBES), 'leg P witness')
      == (list(BASIS_2), list(PROBES)))
    # ---- LEG P, COMPLEX HALF (audit item C-2).  Every one of these is new.
    L("P/cmul_i_squared_is_minus_one",
      cmul(cx(0, 1), cx(0, 1)) == cx(-1))
    L("P/cmul_i_squared_is_not_plus_one",
      cmul(cx(0, 1), cx(0, 1)) != cx(1))
    L("P/cmul_general_product",
      cmul(cx(1, 2), cx(3, -1)) == cx(5, 5))
    L("P/cmul_is_commutative_witness",
      cmul(cx(1, 2), cx(3, -1)) == cmul(cx(3, -1), cx(1, 2)))
    L("P/cmul_rejects_componentwise",
      cmul(cx(0, 1), cx(0, 1)) != cx(0, 1))
    # Y (x) Y is the packet's identity J (x) J = -(iJ) (x) (iJ) written out.
    # A split-complex product returns the NEGATIVE of this literal.
    L("P/ckron_YY_literal",
      ckron(Y_C, Y_C) == ((cx(0), cx(0), cx(0), cx(-1)),
                          (cx(0), cx(0), cx(1), cx(0)),
                          (cx(0), cx(1), cx(0), cx(0)),
                          (cx(-1), cx(0), cx(0), cx(0))))
    L("P/ckron_ZY_literal",
      ckron(Z_C, Y_C) == ((cx(0), cx(0, -1), cx(0), cx(0)),
                          (cx(0, 1), cx(0), cx(0), cx(0)),
                          (cx(0), cx(0), cx(0), cx(0, 1)),
                          (cx(0), cx(0), cx(0, -1), cx(0))))
    L("P/ckron_order_distinct", ckron(Z_C, Y_C) != ckron(Y_C, Z_C))
    L("P/ckron_YY_is_minus_JJ_realified",
      tuple(tuple(e[0] for e in r) for r in ckron(Y_C, Y_C))
      == scale(F(-1), JJ))
    L("P/ckron_YY_has_no_imaginary_part",
      all_of(16, (e[1] == 0 for r in ckron(Y_C, Y_C) for e in r)))
    L("P/cflat_separates_real_from_imaginary",
      cflat(((cx(0, 1),),)) != cflat(((cx(1),),)))
    L("P/cmat_rank_i_and_one_are_independent",
      cmat_rank([((cx(0, 1),),), ((cx(1),),)]) == 2)
    L("P/cmat_rank_of_herm2_is_4", cmat_rank(herm_basis(2)) == 4)
    L("P/cmat_rank_of_a_repeated_generator_is_1",
      cmat_rank([Y_C, Y_C, Y_C]) == 1)
    L("P/cdagger_fixes_hermitian_generators",
      all_of(9, (cdagger(h) == h for h in herm_basis(3))))
    L("P/cdagger_moves_a_non_hermitian_matrix",
      cdagger(((cx(0), cx(1)), (cx(0), cx(0))))
      != ((cx(0), cx(1)), (cx(0), cx(0))))
    L("P/cdagger_conjugates_the_imaginary_part",
      cdagger(((cx(0, 3),),)) == ((cx(0, -3),),))
    # THE QUANTIFIER HELPER, EXERCISED ON FALSE INPUTS.  `all_of` is read at
    # 61 call sites in this module, and what it returns on a short input, on
    # an empty one and on a truthy non-bool is computed here rather than
    # stated in the docstring.  The three FALSE cases are the axes of its two
    # clauses: the cardinality comparison and the element-wise comparison
    # against literal True.
    L("P/all_of_rejects_an_empty_quantifier",
      not all_of(3, (True for _ in [])))
    L("P/all_of_rejects_a_short_quantifier",
      not all_of(3, iter([True, True])))
    L("P/all_of_rejects_a_truthy_non_bool",
      not all_of(1, iter([[1]])))
    L("P/all_of_accepts_exactly_n_trues",
      all_of(3, iter([True, True, True])))
    # FIVE OF THE MODULE-LEVEL DECLARATIONS THE RECORD SHIPS.  An earlier
    # version of this comment said "THE THREE MODULE-LEVEL DECLARATIONS THE
    # RECORD SHIPS"; the record ships more than three, and the fields no leg
    # reads are named in KNOWN LIMITS.  What is read below:
    # PHYSICAL_PREMISES_CERTIFIED, BANK_MODIFIED and EXPORTS, which _result()
    # copies into every returned record; MODULE_TIER, which it ships as
    # record['tier']; and the `epistemic` string bound at the top of this
    # function and handed to _result() unchanged.
    L("P/the_module_certifies_no_physical_premises",
      PHYSICAL_PREMISES_CERTIFIED is False)
    L("P/the_module_declares_no_bank_modification",
      BANK_MODIFIED is False)
    L("P/the_module_exports_nothing", EXPORTS == ())
    L("P/the_module_tier_is_three", MODULE_TIER == 3)
    # THE GRADE, ON TWO CLAUSES.  Both are computed: the string begins
    # `[P_math`, and it does not begin with the bare `[P]` that grades a
    # result as certified physics.  The second clause is implied by the
    # first; it is written out anyway so that the bare `[P]` appears in the
    # predicate under its own name.
    L("P/the_grade_is_p_math_and_not_a_bare_p",
      epistemic.startswith("[P_math") and not epistemic.startswith("[P]"))

    # ---- LEGS A-D: the identification, on six shapes ---------------------
    shape_rows = []
    # THE SAME NUMBERS, HELD A SECOND TIME AS IMMUTABLE TUPLES, so the EV leg
    # can compare the SHIPPED row against something other than itself.
    # `ev['real_shapes'] is shape_rows`, so a comparison against shape_rows
    # would be a comparison of an object with itself.  See KNOWN LIMITS for
    # what this tie is and is not.
    shape_witness = []
    for (n, m) in REAL_SHAPES:
        tag = f"{n}x{m}"
        Sn, Sm = sym_basis(n), sym_basis(m)
        An, Am = anti_basis(n), anti_basis(m)
        N = n * m
        SN = sym_basis(N)
        loc = [kron(a, b) for a in Sn for b in Sm]
        lam = [kron(a, b) for a in An for b in Am]

        dim_sym_N = mat_rank(SN)
        L(f"A/{tag}/dim_sym_matches_basis_and_bank",
          dim_sym_N == len(SN) == K_dim_real(N))
        r_loc = mat_rank(loc)
        L(f"B/{tag}/local_rank_is_KR_product",
          r_loc == K_dim_real(n) * K_dim_real(m))
        L(f"B/{tag}/local_generators_symmetric",
          all_of(len(Sn) * len(Sm), (is_symmetric(g) for g in loc)))
        r_lam = mat_rank(lam)
        L(f"C/{tag}/lam_generators_symmetric",
          all_of(len(An) * len(Am), (is_symmetric(g) for g in lam)))
        L(f"C/{tag}/lam_rank_is_An_times_Am",
          r_lam == len(An) * len(Am))
        # THE TWO LOOP VARIABLES RANGE OVER TWO DIFFERENT FAMILIES.  Both
        # lists go through _distinct_lists, which raises if it is handed one
        # list twice, by identity or by value.
        _lam_side, _loc_side = _distinct_lists(
            lam, loc, f"leg C orthogonality loop at {tag}")
        L(f"C/{tag}/the_orthogonality_loop_reads_two_distinct_lists",
          _lam_side is lam and _loc_side is loc and list(lam) != list(loc))
        L(f"C/{tag}/lam_hs_orthogonal_to_every_local",
          all_of(len(lam) * len(loc),
                 (hs(g, h) == 0 for g in _lam_side for h in _loc_side)))
        cross = [hs(g, h) for g in _lam_side for h in _loc_side]
        L(f"C/{tag}/cross_pair_count_is_nonvacuous",
          len(cross) == len(lam) * len(loc) > 0)
        L(f"C/{tag}/summed_squares_certificate_is_zero",
          sum((x * x for x in cross), F(0)) == 0)
        L(f"C/{tag}/each_lam_generator_raises_rank_by_one",
          all_of(len(An) * len(Am),
                 (mat_rank(loc + [g]) == r_loc + 1 for g in lam)))
        r_all = mat_rank(loc + lam)
        L(f"C/{tag}/union_spans_sym", r_all == dim_sym_N)
        codim = dim_sym_N - r_loc
        banked = composite_defect(K_dim_real, n, m)
        closed = (n * (n - 1) // 2) * (m * (m - 1) // 2)
        # THE SUBTRACTION IS WRITTEN INTO THE LEGS, not routed through the
        # reporting variable.  `codim` and `r_lam` are numerically equal at
        # every shape here -- that equality IS the result -- so no arithmetic
        # relation among these numbers can tell `codim = dim_sym_N - r_loc`
        # from `codim = r_lam`.  Each headline leg below therefore computes
        # `dim_sym_N - r_loc` on the spot rather than reading the variable.
        # `codim` survives as a reported number and the last leg of this group
        # compares it against the subtraction.
        L(f"D/{tag}/codim_equals_banked_defect", dim_sym_N - r_loc == banked)
        L(f"D/{tag}/codim_equals_closed_form", dim_sym_N - r_loc == closed)
        L(f"D/{tag}/codim_equals_lam_rank", dim_sym_N - r_loc == r_lam)
        L(f"D/{tag}/the_reported_codimension_is_that_subtraction",
          codim == dim_sym_N - r_loc)
        L(f"D/{tag}/the_two_ranks_are_not_equal_so_the_subtraction_bites",
          r_loc != dim_sym_N and dim_sym_N - r_loc > 0)
        L(f"D/{tag}/under_generating_the_span_moves_the_subtraction",
          dim_sym_N - mat_rank(loc[:-1]) == (dim_sym_N - r_loc) + 1)
        shape_rows.append({
            'n': n, 'm': m, 'dim_sym_N': dim_sym_N, 'rank_local': r_loc,
            'rank_lam_lam': r_lam, 'rank_union': r_all, 'codim': codim,
            'banked_Delta_R': banked, 'A_n_times_A_m': closed,
        })
        shape_witness.append((n, m, dim_sym_N, r_loc, r_lam, r_all, codim,
                              banked, closed))
    ev['real_shapes'] = shape_rows
    L("D/codimension_is_not_constant_across_shapes",
      len({r['codim'] for r in shape_rows}) > 1)

    # ---- LEG D_sym: THE CLOSED FORM PROVED IN Q[n, m] --------------------
    # Three lines, and they are these three.  K_R(N) = N(N+1)/2 with N = nm.
    p_N = p_mul(P_N, P_M)
    p_joint = p_scale(F(1, 2), p_mul(p_N, p_add(p_N, P_ONE)))
    p_local = p_scale(F(1, 4), p_mul(p_mul(P_N, p_add(P_N, P_ONE)),
                                     p_mul(P_M, p_add(P_M, P_ONE))))
    p_closed = p_scale(F(1, 4), p_mul(p_mul(P_N, p_add(P_N, p_scale(-1, P_ONE))),
                                      p_mul(P_M, p_add(P_M, p_scale(-1, P_ONE)))))
    p_defect = p_add(p_joint, p_scale(-1, p_local))
    L("Dsym/polynomial_identity_defect_equals_closed_form",
      p_defect == p_closed)
    L("Dsym/identity_is_not_vacuous_polynomials_are_nonzero",
      p_defect != {} and p_closed != {})
    # The symbolic objects are the BANK's count, not a parallel definition.
    _grid = [(a, b) for a in range(1, 8) for b in range(1, 8)]
    # THE GRID IS MEASURED FOR NON-DEGENERACY, NOT ONLY FOR SIZE.
    # `all(... for ... in [])` is vacuously True, and at (1, 1) every
    # candidate polynomial here evaluates to 0 and coincides.  So the legs
    # below compute: the exact size, pairwise distinctness, the number of
    # points where the defect is actually nonzero, and two executed
    # rejections of perturbed candidates.
    L("Dsym/the_grid_is_forty_nine_points", len(_grid) == 49)
    L("Dsym/the_grid_points_are_pairwise_distinct",
      len(set(_grid)) == 49)
    L("Dsym/the_grid_has_thirty_six_points_with_a_nonzero_defect",
      len([(a, b) for (a, b) in _grid
           if composite_defect(K_dim_real, a, b) != 0]) == 36)
    L("Dsym/the_grid_contains_points_where_the_closed_form_is_nonzero",
      any(p_eval(p_closed, a, b) != 0 for (a, b) in _grid))
    L("Dsym/the_grid_rejects_a_perturbed_joint_polynomial",
      any(p_eval(p_add(p_joint, P_ONE), a, b) != K_dim_real(a * b)
          for (a, b) in _grid))
    L("Dsym/the_grid_rejects_a_perturbed_closed_form",
      any(p_eval(p_add(p_closed, P_ONE), a, b)
          != (a * (a - 1) // 2) * (b * (b - 1) // 2) for (a, b) in _grid))
    L("Dsym/joint_polynomial_matches_banked_K_on_grid",
      all_of(49, (p_eval(p_joint, a, b) == K_dim_real(a * b)
                  for a, b in _grid)))
    L("Dsym/local_polynomial_matches_banked_K_on_grid",
      all_of(49, (p_eval(p_local, a, b) == K_dim_real(a) * K_dim_real(b)
                  for a, b in _grid)))
    L("Dsym/defect_polynomial_matches_banked_defect_on_grid",
      all_of(49, (p_eval(p_defect, a, b)
                  == composite_defect(K_dim_real, a, b)
                  for a, b in _grid)))
    L("Dsym/closed_polynomial_matches_An_Am_on_grid",
      all_of(49, (p_eval(p_closed, a, b)
                  == (a * (a - 1) // 2) * (b * (b - 1) // 2)
                  for a, b in _grid)))
    # the polynomial engine itself, exercised against FALSE inputs.
    L("Dsym/engine_multiplication_witness",
      p_mul(p_add(P_N, P_ONE), p_add(P_N, p_scale(-1, P_ONE)))
      == {(2, 0): F(1), (0, 0): F(-1)})
    L("Dsym/engine_addition_cancels_to_the_empty_polynomial",
      p_add(P_N, p_scale(-1, P_N)) == {})
    L("Dsym/engine_rejects_a_false_identity",
      p_mul(p_add(P_N, P_ONE), p_add(P_N, P_ONE))
      != {(2, 0): F(1), (0, 0): F(1)})
    L("Dsym/engine_distinguishes_the_two_variables", P_N != P_M)
    L("Dsym/engine_evaluation_agrees_with_hand_arithmetic",
      p_eval(p_mul(P_N, P_M), 3, 5) == 15)
    # THE VARIABLE ORDER OF p_eval, COMPUTED.  Every polynomial in play here
    # is symmetric in n and m, so every other leg returns the same value
    # under a swap of the two arguments.  These two evaluate P_N and P_M at
    # an asymmetric point, where the two orders give different numbers.
    L("Dsym/engine_evaluation_reads_the_first_variable_as_n",
      p_eval(P_N, 2, 3) == 2 and p_eval(P_M, 2, 3) == 3)
    L("Dsym/engine_evaluation_is_not_symmetric_in_its_arguments",
      p_eval(P_N, 2, 3) != p_eval(P_N, 3, 2))
    L("Dsym/engine_evaluation_of_a_mixed_monomial_is_order_sensitive",
      p_eval(p_mul(P_N, p_mul(P_N, P_M)), 2, 3) == 12
      and p_eval(p_mul(P_N, p_mul(P_N, P_M)), 3, 2) == 18)
    ev['symbolic_defect_polynomial'] = {str(k): str(v)
                                        for k, v in sorted(p_defect.items())}
    ev['symbolic_closed_form_polynomial'] = {str(k): str(v)
                                             for k, v in sorted(p_closed.items())}

    # ---- LEG D': the BEHAVIOUR of the imported symbol --------------------
    L("Dp/composite_defect_computes_K_nm_minus_K_n_K_m",
      composite_defect(K_dim_real, 3, 4)
      == K_dim_real(12) - K_dim_real(3) * K_dim_real(4))
    d_id = composite_defect(_identity_count, 3, 4)
    L("Dp/identity_count_defect_is_zero", d_id == 0)
    d_h = composite_defect(K_dim_quaternionic, 2, 2)
    L("Dp/quaternionic_defect_matches_its_own_formula",
      d_h == K_dim_quaternionic(4) - K_dim_quaternionic(2) ** 2)
    L("Dp/quaternionic_defect_is_minus_eight", d_h == -8)
    L("Dp/quaternionic_defect_is_negative", d_h < 0)
    L("Dp/quaternionic_defect_differs_from_closed_form",
      d_h != (2 * 1 // 2) * (2 * 1 // 2))
    L("Dp/the_two_probes_disagree_with_each_other", d_id != d_h)
    ev['bank_probe_identity_count_defect'] = d_id
    ev['bank_probe_quaternionic_defect'] = d_h

    # ---- LEG D''': THREE MORE SHAPES, WITH NO SHIPPED LITERAL ------------
    # AUDIT ITEM C-1.  This does NOT certify the live call -- see the
    # docstring; composite_defect is a pure function of two integers and any
    # of its values can be transcribed.
    #
    # WHAT THIS LEG IS, STATED CORRECTLY.  An earlier version billed
    #     codim_under == bank_here + dropped
    # as "a NON-TRIVIAL relation with TWO live ranks".  It is not.  With
    # codim_under = dim_full - r_under and dropped = r_full - r_under, the
    # r_under on the two sides CANCELS and the statement is exactly
    #     dim_full - r_full == bank_here,
    # which involves ONE live rank and is the same codimension identity leg D
    # runs.  PROBE_DROP is unconstrained by it.  The billing is withdrawn.
    # What the leg actually buys is real and is kept: the bank value at THREE
    # FURTHER SHAPES for which this module ships no literal, taking the
    # codimension count from six shapes to nine.  The under-generation legs
    # stay as a second, coarser reading of the same ranks.
    L("Dppp/the_declared_drop_is_the_frozen_value", PROBE_DROP == 3)
    probe_rows = []
    probe_values = []
    for (n, m) in PROBE_SHAPES:
        tag = f"{n}x{m}"
        loc = [kron(a, b) for a in sym_basis(n) for b in sym_basis(m)]
        dim_full = K_dim_real(n * m)
        r_full = mat_rank(loc)
        under = loc[:-PROBE_DROP]
        r_under = mat_rank(under)
        dropped = r_full - r_under
        codim_under = dim_full - r_under
        bank_here = composite_defect(K_dim_real, n, m)
        closed_here = (n * (n - 1) // 2) * (m * (m - 1) // 2)
        # A DECLARED DROP OF ZERO IS A PYTHON SLICING TRAP: loc[:-0] is the
        # EMPTY list, so "drop nothing" reads as "drop everything" and the
        # under-generated relation below still holds.  The legs below compute
        # both halves: that PROBE_DROP is positive, and that the shortened
        # list is shorter by exactly PROBE_DROP.
        # THE HEADLINE, with r_under nowhere in it: the codimension of the
        # FULLY generated product span equals the bank value, at a shape this
        # module ships no literal for.
        L(f"Dppp/{tag}/full_codimension_equals_the_bank_value",
          dim_full - r_full == bank_here)
        L(f"Dppp/{tag}/full_codimension_equals_the_closed_form",
          dim_full - r_full == closed_here)
        L(f"Dppp/{tag}/the_declared_drop_is_positive", PROBE_DROP > 0)
        L(f"Dppp/{tag}/the_under_generated_list_is_shorter_by_the_drop",
          len(under) == len(loc) - PROBE_DROP)
        L(f"Dppp/{tag}/under_generation_lost_rank", dropped > 0)
        # The under-generated reading.  Algebraically this is the line above
        # with r_under added to both sides; it is kept as a coarser
        # cross-check, NOT billed as an independent relation.
        L(f"Dppp/{tag}/under_generated_reading_is_consistent",
          codim_under == bank_here + dropped)
        L(f"Dppp/{tag}/value_is_neither_zero_nor_the_closed_form",
          codim_under != 0 and codim_under != closed_here)
        L(f"Dppp/{tag}/value_is_not_the_banked_defect_either",
          codim_under != bank_here)
        probe_rows.append({'n': n, 'm': m, 'dim': dim_full,
                           'rank_full': r_full, 'rank_under': r_under,
                           'dropped': dropped, 'codim_under': codim_under,
                           'codim_full': dim_full - r_full,
                           'banked': bank_here})
        probe_values.append(codim_under)
    L("Dppp/probe_values_are_pairwise_distinct",
      len(set(probe_values)) == len(probe_values))
    L("Dppp/probe_shapes_are_disjoint_from_the_tested_shapes",
      not (set(PROBE_SHAPES) & set(REAL_SHAPES)))
    L("Dppp/probe_values_avoid_every_tested_codimension",
      not (set(probe_values) & {r['codim'] for r in shape_rows}))
    ev['bank_rank_relation_probes'] = probe_rows

    # ---- LEG D'': THE BANKED SIBLING, called live -----------------------
    # AUDIT ITEMS D-1 (the substring tripwire was dead) and D-2 (a competent
    # transcribed stub passed).  Provenance is asserted by OBJECT IDENTITY
    # against the freshly imported bank module -- a spoofed callable with
    # __module__ and __name__ reassigned passed all four of the previous
    # version's provenance legs -- and the numbers are parsed out of the R
    # clause BY POSITION.
    L("Dpp/sibling_symbol_is_a_function",
      callable(_sibling_tomographic_locality)
      and not isinstance(_sibling_tomographic_locality, dict))
    L("Dpp/sibling_symbol_module_provenance",
      getattr(_sibling_tomographic_locality, '__module__', None)
      == 'apf.closed_world_completeness')
    L("Dpp/sibling_symbol_name_provenance",
      getattr(_sibling_tomographic_locality, '__name__', None)
      == 'check_T_split_composite_gates_tomographic_locality')
    # IDENTITY, NOT DESCRIPTION.  A locally defined function with
    # __module__ and __name__ reassigned and a matching __doc__ / key_result
    # passed all four provenance legs of the previous version.  This one
    # compares the OBJECT against the attribute of the freshly imported bank
    # module, and reads the file its code came from.
    L("Dpp/sibling_symbol_is_the_object_the_bank_module_exports",
      hasattr(_sibling_tomographic_locality, '__code__')
      and _sibling_tomographic_locality
      is _cwc.check_T_split_composite_gates_tomographic_locality
      and _sibling_tomographic_locality.__code__.co_filename.endswith(
          'closed_world_completeness.py'))
    sib = _sibling_tomographic_locality()
    sib_key = str(sib.get('key_result', ''))
    # MAINTENANCE INSTRUCTION, WHERE A MAINTAINER WILL READ IT.  This leg and
    # the clause-value legs below compare a BANKED SIBLING's numbers against
    # literals, and this module does not adjudicate whether those numbers are
    # right.  An external audit has argued they are not -- that the sibling
    # applies a trace-1-derived dimension formula to full Hermitian counts,
    # and reads `joint < local` as the reconstruction failure when the
    # Wootters-Hardy failure is `joint > local`.  Nothing here endorses that
    # reading.  What follows from it is a maintenance liability worth naming:
    #
    #   IF THIS LEG (or any Dpp clause-value leg, or either of the two
    #   docstring legs at the end of this group) GOES RED BECAUSE THE
    #   SIBLING'S R CLAUSE, ITS CLAUSE HEADINGS OR ITS DOCSTRING MOVED, THE
    #   CORRECT RESPONSE IS TO UPDATE THIS LEG TO THE SIBLING'S NEW VALUE --
    #   NOT TO REVERT THE SIBLING.
    #
    # The tripwire exists to make a silent divergence loud, not to freeze the
    # sibling.
    L("Dpp/sibling_passes", sib.get('passed') is True)
    L("Dpp/sibling_record_name",
      sib.get('name') == 'T_split_composite_gates_tomographic_locality')
    L("Dpp/sibling_record_tier_and_summary",
      sib.get('tier') == 3
      and 'tomograph' in str(sib.get('summary', '')).lower())

    def _clause(text: str, head: str) -> str:
        """The parenthesised clause following `head`, or '' if absent."""
        i = text.find(head)
        if i < 0:
            return ''
        j = text.find('(', i)
        k = text.find(')', j)
        if j < 0 or k < 0:
            return ''
        return text[j + 1:k]

    def _field(clause: str, key: str):
        """The integer assigned to `key` inside ONE clause, or None.

        Tokenizes on commas AND whitespace, because the sibling writes its R
        clause as "joint=10, local=9, signed=+1, surplus" and its C clause as
        "joint=16 = local=16"."""
        for part in clause.replace(',', ' ').split():
            if part.startswith(key + '='):
                tail = part[len(key) + 1:].strip()
                return int(tail) if tail.lstrip('-').isdigit() else None
        return None

    r_clause = _clause(sib_key, 'R fails')
    c_clause = _clause(sib_key, 'C passes')
    h_clause = _clause(sib_key, 'H fails')
    L("Dpp/R_clause_is_present", r_clause != '')
    L("Dpp/C_clause_is_present", c_clause != '')
    L("Dpp/H_clause_is_present", h_clause != '')
    L("Dpp/the_three_clauses_are_distinct_sites",
      len({r_clause, c_clause, h_clause}) == 3)
    # ALL SIX SIBLING NUMBERS ARE PARSED, ONCE, INTO NAMED VARIABLES, AND
    # EVERY COMPARISON BELOW IS GUARDED ON `is not None`.  A previous version
    # parsed four -- R/joint, R/local, C/local, H/local -- and left C/joint
    # and H/joint unread.  Six of six now.
    #
    # WHY THE GUARDS.  `_clause` keys on the clause HEADINGS 'R fails',
    # 'C passes', 'H fails'.  If a heading moves rather than a number, the
    # clause comes back empty and `_field` returns None; an unguarded `<` or
    # `-` against an int then raises TypeError, and a raise inside a check
    # returns NO RECORD -- so the failing labels, and the maintenance
    # instruction they point at, would not reach the maintainer.  Guarded, the
    # same edit produces a record whose `summary` names the clause legs.
    r_joint, r_local = _field(r_clause, 'joint'), _field(r_clause, 'local')
    c_joint, c_local = _field(c_clause, 'joint'), _field(c_clause, 'local')
    h_joint, h_local = _field(h_clause, 'joint'), _field(h_clause, 'local')
    _all_parsed = all_of(6, (v is not None for v in
                             (r_joint, r_local, c_joint, c_local,
                              h_joint, h_local)))
    L("Dpp/R_clause_joint_is_10", r_joint == 10)
    L("Dpp/R_clause_local_is_9", r_local == 9)
    L("Dpp/C_clause_joint_is_16", c_joint == 16)
    L("Dpp/C_clause_local_is_16", c_local == 16)
    L("Dpp/H_clause_joint_is_28", h_joint == 28)
    L("Dpp/H_clause_local_is_36", h_local == 36)
    L("Dpp/the_six_parsed_sibling_numbers_are_all_present", _all_parsed)
    L("Dpp/the_C_clause_reports_joint_equal_to_local",
      c_joint is not None and c_local is not None and c_joint == c_local)
    L("Dpp/the_R_clause_reports_a_surplus",
      _all_parsed and r_joint > r_local)
    L("Dpp/the_H_clause_reports_a_deficit",
      _all_parsed and h_joint < h_local)
    L("Dpp/the_R_and_H_clauses_have_opposite_signs",
      _all_parsed and (r_joint - r_local) * (h_joint - h_local) < 0)
    # THE PARSER, COMPUTED ON AN EDITED COPY OF THE STRING.  The previous
    # version's substring test returned the same answer after the R-local was
    # moved from 15 to 9, because "local=15" also occurs in the C clause.
    # Here the same edit is made on a copy and the parser is run on it.
    _moved = sib_key.replace('local=9, signed', 'local=7, signed')
    L("Dpp/parser_detects_a_move_in_the_R_clause_alone",
      _field(_clause(_moved, 'R fails'), 'local') == 7
      and _field(_clause(_moved, 'C passes'), 'local') == 16)
    L("Dpp/the_simulated_move_actually_changed_the_string",
      _moved != sib_key)
    _moved_c = sib_key.replace('joint=16 = local=16', 'joint=16 = local=99')
    L("Dpp/parser_detects_a_move_in_the_C_clause_alone",
      _field(_clause(_moved_c, 'C passes'), 'local') == 99
      and _field(_clause(_moved_c, 'R fails'), 'local') == 9)
    # WHY THE PREVIOUS SUBSTRING TEST RETURNED THE SAME ANSWER AFTER THE
    # EDIT, computed on a SELF-CONTAINED string rather than on the live
    # sibling, so this leg does not depend on the sibling's current text.
    # The naive test was `"local=15" in key_result`; the string occurs twice,
    # so it is satisfied whatever the R value is.
    _naive_demo = ("R fails (joint=10, local=9, deficit), "
                   "C passes (joint=15 = local=15)")
    L("Dpp/naive_substring_test_is_demonstrably_insufficient",
      'local=15' in _naive_demo
      and _field(_clause(_naive_demo, 'R fails'), 'local') == 9)
    L("Dpp/structural_parser_reads_the_demo_C_clause_independently",
      _field(_clause(_naive_demo, 'C passes'), 'local') == 15)
    sib_joint = K_dim_real(4)
    sib_local = K_dim_real(2) * K_dim_real(2)
    here_local = shape_rows[0]['rank_local']
    here_codim = shape_rows[0]['codim']
    L("Dpp/reconstructed_sibling_joint_matches_the_parsed_value",
      r_joint is not None and r_joint == sib_joint)
    L("Dpp/reconstructed_sibling_local_matches_the_parsed_value",
      r_local is not None and r_local == sib_local)
    L("Dpp/local_counts_agree", sib_local == here_local)
    L("Dpp/joint_dimensions_agree",
      sib_joint == shape_rows[0]['dim_sym_N'])
    L("Dpp/this_module_signed_mismatch_is_plus_one", here_codim == 1)
    L("Dpp/the_two_mismatches_agree",
      sib_joint - sib_local == here_codim)
    # THE ONLY LEG HERE THAT READS THE SIBLING'S PROSE AT ALL.
    #
    # The clause legs above parse numbers out of the sibling's RETURNED
    # key_result.  That string is an f-string over the sibling's own
    # variables, so the legs cannot tell a computed value from a literal.  A
    # sibling replaced by a stub that returns the same record passes all
    # thirty Dpp legs, this one included.
    #
    # What a docstring CAN do is drift from the code, which is the defect the
    # corrigendum corrected: the sibling's prose carried the surplus reading
    # while its code computed a deficit.  The leg below requires the
    # docstring to contain the two sign words with the two magnitudes the
    # code computes.  IT IS TWO SUBSTRING TESTS AND NOTHING MORE.  A
    # docstring edit that leaves both substrings intact passes it,
    # including one that inverts the surrounding physics prose or restores
    # a superseded number elsewhere in the text.
    sib_doc = getattr(_sibling_tomographic_locality, '__doc__', None) or ''
    L("Dpp/the_sibling_prose_carries_the_signs_its_code_computes",
      r_joint is not None and r_local is not None
      and h_joint is not None and h_local is not None
      and ('SURPLUS of %d' % (r_joint - r_local)) in sib_doc
      and ('DEFICIT of %d' % (h_local - h_joint)) in sib_doc)
    ev['sibling_local_formula'] = ("d_R(n_A) d_R(n_B) with "
                                   "d_R(n) = n(n+1)/2, full observable "
                                   "dimensions")
    ev['sibling_joint_R'] = sib_joint
    ev['sibling_local_R'] = sib_local
    ev['sibling_signed_mismatch'] = sib_joint - sib_local
    ev['this_module_local_definition'] = "rank of span{A (x) B}"
    ev['this_module_local_rank_at_2_2'] = here_local
    ev['this_module_signed_mismatch'] = here_codim

    # ---- LEG E: must-bite controls ---------------------------------------
    S2 = sym_basis(2)
    loc22 = [kron(a, b) for a in S2 for b in S2]
    base_codim = K_dim_real(4) - mat_rank(loc22)
    under_codim = K_dim_real(4) - mat_rank(loc22[:-1])
    L("E/under_generation_moves_the_codimension",
      under_codim != base_codim)
    L("E/under_generation_codimension_is_2", under_codim == 2)
    over_codim = K_dim_real(4) - mat_rank(loc22 + [JJ])
    L("E/enlargement_sends_the_codimension_to_zero", over_codim == 0)
    complex_rows = []
    for (n, m) in COMPLEX_SHAPES:
        tag = f"{n}x{m}"
        Hn, Hm, HN = herm_basis(n), herm_basis(m), herm_basis(n * m)
        cloc = [ckron(a, b) for a in Hn for b in Hm]
        dim_h = cmat_rank(HN)
        r_c = cmat_rank(cloc)
        d_c = composite_defect(K_dim_complex, n, m)
        L(f"E3/{tag}/dim_herm_matches_banked_KC",
          dim_h == K_dim_complex(n * m))
        L(f"E3/{tag}/complex_codimension_and_banked_defect_both_zero",
          dim_h - r_c == d_c == 0)
        L(f"E3/{tag}/complex_local_rank_is_the_product_of_local_dimensions",
          r_c == K_dim_complex(n) * K_dim_complex(m))
        L(f"E3/{tag}/every_complex_local_generator_is_hermitian",
          all_of(len(Hn) * len(Hm), (cdagger(g) == g for g in cloc)))
        complex_rows.append({'n': n, 'm': m, 'dim_herm': dim_h,
                             'rank_local': r_c, 'codim': dim_h - r_c,
                             'banked_Delta_C': d_c})
    ev['complex_control'] = complex_rows
    ev['control_codim_under_generation'] = under_codim
    ev['control_codim_after_enlargement'] = over_codim

    # ---- LEG F: THE CORRECTION -- the direction is NOT the singlet -------
    # THE DIRECTION, TIED TO THE ROUTINE LEGS C AND D USE.  A previous
    # version wrote `is_scalar_multiple(JJ, kron(J, J))`, which compares JJ
    # with itself, JJ having been DEFINED as kron(J, J).  What is computed
    # here instead is that the hand-written J and the generator anti_basis()
    # emits are the same direction, so the (2,2) exhibit is the Lam (x) Lam
    # generator legs C and D range over and not a parallel object.
    _anti2 = anti_basis(2)
    L("F/the_exhibited_direction_is_the_lam_tensor_lam_generator",
      len(_anti2) == 1 and _anti2[0] == scale(F(-1), J)
      and kron(_anti2[0], _anti2[0]) == JJ)
    L("F/JJ_is_not_a_multiple_of_the_singlet_projector",
      not is_scalar_multiple(JJ, PSI_MINUS))
    L("F/the_singlet_projector_is_not_a_multiple_of_JJ",
      not is_scalar_multiple(PSI_MINUS, JJ))
    L("F/identity_and_JJ_are_independent", mat_rank([I4, JJ]) == 2)
    L("F/singlet_is_outside_span_of_identity_and_JJ",
      mat_rank([I4, JJ, PSI_MINUS]) == 3)
    L("F/JJ_equals_two_psi_plus_phi_minus_identity",
      sub(scale(F(2), add(PSI_MINUS, PHI_PLUS)), I4) == JJ)
    ev['direction_is_singlet_projector'] = is_scalar_multiple(JJ, PSI_MINUS)
    ev['direction_in_span_identity_and_singlet'] = in_span(PSI_MINUS,
                                                           [I4, JJ])

    # ---- LEG G: the singlet placed, and the maximality of 1/4 -----------
    local_summand = linear_combination((F(1, 4), kron(I2, I2)),
                                       (F(-1, 4), XX), (F(-1, 4), ZZ))
    L("G/singlet_decomposition_is_an_identity",
      add(local_summand, scale(F(1, 4), JJ)) == PSI_MINUS)
    L("G/local_summand_is_in_the_product_span",
      in_span(local_summand, loc22))
    L("G/local_summand_is_not_psd", not is_psd(local_summand))
    L("G/singlet_is_a_state",
      is_psd(PSI_MINUS) and trace(PSI_MINUS) == 1)
    coeff = hs(PSI_MINUS, JJ) / hs(JJ, JJ)
    L("G/JJ_hs_norm_squared_is_4", hs(JJ, JJ) == 4)
    L("G/singlet_composite_coefficient_is_one_quarter", coeff == F(1, 4))
    L("G/singlet_trace_against_JJ_is_one", trace(mm(PSI_MINUS, JJ)) == 1)
    L("G/phi_plus_co_attains_the_value_one",
      is_psd(PHI_PLUS) and trace(mm(PHI_PLUS, JJ)) == 1)
    L("G/JJ_squared_is_the_identity", mm(JJ, JJ) == I4)
    # `is_symmetric(JJ)` is computed once, at P/sym_accepts_JJ.  A leg here
    # and a third at leg W repeated the same expression under two further
    # names; both are deleted.
    L("G/JJ_is_traceless", trace(JJ) == 0)
    L("G/identity_minus_JJ_is_psd", is_psd(sub(I4, JJ)))
    L("G/identity_plus_JJ_is_psd", is_psd(add(I4, JJ)))
    L("G/identity_minus_twice_JJ_is_not_psd",
      not is_psd(sub(I4, scale(F(2), JJ))))
    L("G/half_identity_minus_JJ_is_not_psd",
      not is_psd(sub(scale(F(1, 2), I4), JJ)))
    battery = {
        "psi-": PSI_MINUS,
        "phi+": PHI_PLUS,
        "I/4": scale(F(1, 4), I4),
        "|00><00|": pure([F(1), F(0), F(0), F(0)]),
        "sigma_+1/8": sigma(F(1, 8)),
        "sigma_-1/8": sigma(F(-1, 8)),
        "(psi-+phi+)/2": linear_combination((F(1, 2), PSI_MINUS),
                                            (F(1, 2), PHI_PLUS)),
        "rho_+": RHO_PLUS,
        "rho_-": RHO_MINUS,
    }
    L("G/battery_labels_match_the_frozen_list",
      tuple(battery) == BATTERY_LABELS)
    bound_rows = []
    for label in BATTERY_LABELS:
        st = battery[label]
        L(f"G/battery/{label}/is_a_density_matrix",
          is_psd(st) and trace(st) == 1)
        val = trace(mm(st, JJ))
        L(f"G/battery/{label}/value_is_at_most_one", val <= 1)
        L(f"G/battery/{label}/coefficient_is_at_most_one_quarter",
          val / hs(JJ, JJ) <= coeff)
        bound_rows.append((label, str(val)))
    attained = [lb for lb, v in bound_rows if F(v) == 1]
    L("G/battery_bound_attained_by_at_least_three_members",
      len(attained) >= 3)
    L("G/battery_has_a_member_strictly_below_the_bound",
      any(F(v) < 1 for _, v in bound_rows))
    L("G/battery_has_a_member_on_the_negative_side",
      any(F(v) < 0 for _, v in bound_rows))
    max_coeff = max(F(v) for _, v in bound_rows) / hs(JJ, JJ)
    L("G/battery_maximum_coefficient_is_the_singlet_value",
      max_coeff == coeff)

    # THE MAXIMIZERS ARE A CONTINUUM, not the three exhibited states.
    # J (x) J is a traceless involution, so its +1 eigenspace has dimension 2
    # and EVERY state supported there attains the bound.
    eig_plus = kernel_basis(sub(JJ, I4))
    L("G/eigen/plus_one_eigenspace_has_dimension_2", len(eig_plus) == 2)
    L("G/eigen/eigenspace_basis_is_independent",
      rank(eig_plus) == 2)
    L("G/eigen/eigenspace_vectors_are_genuine_eigenvectors",
      all_of(2, (mm(JJ, tuple((x,) for x in v)) == tuple((x,) for x in v)
                 for v in eig_plus)))
    L("G/eigen/minus_one_eigenspace_also_has_dimension_2",
      len(kernel_basis(add(JJ, I4))) == 2)
    fam = []
    for s_ in EIGEN_PARAMS:
        v = [a + s_ * b for a, b in zip(eig_plus[0], eig_plus[1])]
        fam.append(pure(v))
    L("G/eigen/family_members_are_states",
      all_of(6, (is_psd(st) and trace(st) == 1 for st in fam)))
    L("G/eigen/family_members_all_attain_the_bound",
      all_of(6, (trace(mm(st, JJ)) == 1 for st in fam)))
    L("G/eigen/family_members_are_pairwise_distinct",
      len(set(fam)) == len(EIGEN_PARAMS))
    L("G/eigen/family_is_larger_than_the_three_exhibited_states",
      len(set(fam)) > 3)
    L("G/eigen/family_contains_states_outside_the_exhibited_three",
      len(set(fam) - {PSI_MINUS, PHI_PLUS,
                      linear_combination((F(1, 2), PSI_MINUS),
                                         (F(1, 2), PHI_PLUS))}) >= 3)
    L("G/eigen/an_off_eigenspace_state_falls_strictly_short",
      trace(mm(pure([F(1), F(0), F(0), F(0)]), JJ)) < 1)
    L("G/eigen/the_bound_is_not_attained_by_every_state",
      any(trace(mm(st, JJ)) < 1 for st in battery.values()))
    ev['singlet_composite_coefficient'] = str(coeff)
    ev['singlet_local_summand_is_psd'] = is_psd(local_summand)
    ev['composite_value_battery'] = bound_rows
    ev['composite_coefficient_max_over_battery'] = str(max_coeff)
    ev['identity_minus_direction_is_psd'] = is_psd(sub(I4, JJ))
    ev['bound_attained_by'] = attained
    ev['maximizer_eigenspace_dimension'] = len(eig_plus)
    ev['maximizer_family_size'] = len(set(fam))

    # ---- LEG H: the structural blindness, and the CLOSED INTERVAL -------
    fact_rows = []
    for i, (p, q, a, b) in enumerate(
            ((J, J, mat([[1, 2], [3, 4]]), mat([[5, 6], [7, 8]])),
             (Z, X, mat([[0, 1], [0, 0]]), mat([[2, 0], [5, 1]])),
             (X, J, mat([[1, 1], [0, 2]]), mat([[3, 0], [1, 1]])))):
        lhs = trace(mm(kron(p, q), kron(a, b)))
        rhs = trace(mm(p, a)) * trace(mm(q, b))
        L(f"H/factorization/{i}/product_trace_factorizes", lhs == rhs)
        fact_rows.append(str(lhs))
    L("H/factorization_battery_is_not_vacuous",
      any(x != '0' for x in fact_rows))
    L("H/trace_of_J_against_every_symmetric_probe_vanishes",
      all_of(7, (trace(mm(J, a)) == 0 for a in PROBES)))
    L("H/trace_of_J_against_a_nonsymmetric_matrix_does_not_vanish",
      trace(mm(J, mat([[0, 1], [0, 0]]))) != 0)
    L("H/probe_list_spans_sym_R2",
      mat_rank(list(PROBES)) == K_dim_real(2) == 3)
    L("H/every_probe_is_symmetric",
      all_of(7, (is_symmetric(p) for p in PROBES)))
    L("H/probe_list_is_longer_than_a_basis", len(PROBES) > K_dim_real(2))
    L("H/probe_list_is_linearly_dependent",
      mat_rank(list(PROBES)) < len(PROBES))
    L("H/basis_of_sym_R2_has_rank_three", mat_rank(list(BASIS_2)) == 3)
    L("H/nine_basis_products_span_the_whole_product_space",
      mat_rank([kron(a, b) for a in BASIS_2 for b in BASIS_2])
      == K_dim_real(2) * K_dim_real(2))

    sp, sn = sigma(F(1, 8)), sigma(F(-1, 8))
    L("H/sigma_endpoints_are_distinct", sp != sn)
    for label, st in (("sigma+", sp), ("sigma-", sn)):
        L(f"H/{label}/has_trace_one", trace(st) == 1)
        L(f"H/{label}/is_symmetric", is_symmetric(st))
        L(f"H/{label}/is_psd", is_psd(st))
    # THE DISCLOSED GAUGE RELATION.  AUDIT ITEM D-3: the sigma endpoints are
    # related by a LOCAL REFLECTION on Alice's side alone, so they cannot
    # carry the claim that the hidden parameter is not a local orientation
    # sign.  This is COMPUTED here rather than left for the next reader, and
    # the witness pair of record is the spectrally inequivalent rho_+- at
    # leg W.
    L("H/gauge/reflection_is_orthogonal",
      mm(REFLECT, transpose(REFLECT)) == I2)
    L("H/gauge/reflection_is_a_product_operator",
      REFLECT_A == kron(REFLECT, I2))
    L("H/gauge/reflection_is_not_the_identity", REFLECT_A != I4)
    L("H/gauge/local_reflection_carries_sigma_plus_to_sigma_minus",
      mm(mm(REFLECT_A, sp), transpose(REFLECT_A)) == sn)
    L("H/gauge/sigma_endpoints_share_a_characteristic_polynomial",
      charpoly(sp) == charpoly(sn))
    L("H/gauge/sigma_endpoints_are_therefore_not_the_witness_pair",
      charpoly(RHO_PLUS) != charpoly(RHO_MINUS))
    L("H/gauge/the_same_reflection_does_not_relate_the_witness_pair",
      mm(mm(REFLECT_A, RHO_PLUS), transpose(REFLECT_A)) != RHO_MINUS)

    P0 = scale(F(1, 2), add(I2, Z))
    P1 = scale(F(1, 2), sub(I2, Z))
    Q0 = scale(F(1, 2), add(I2, X))
    Q1 = scale(F(1, 2), sub(I2, X))
    L("H/measurement_projectors_are_psd",
      len({P0, P1, Q0, Q1}) == 4
      and all_of(4, (is_psd(P) for P in (P0, P1, Q0, Q1))))
    L("H/measurement_pairs_resolve_the_identity",
      add(P0, P1) == I2 and add(Q0, Q1) == I2)
    L("H/measurement_pairs_are_orthogonal",
      mm(P0, P1) == zeros(2) and mm(Q0, Q1) == zeros(2))
    L("H/the_two_measurement_bases_differ", P0 != Q0 and P1 != Q1)

    L("H/sigma_is_affine_in_t",
      all_of(4, (sub(sigma(t), sigma(F(0)))
                 == scale(t, sub(sigma(F(1)), sigma(F(0))))
                 for t in (F(-3), F(-1, 7), F(2, 5), F(11)))))
    L("H/sigma_actually_moves_with_t", sigma(F(1)) != sigma(F(0)))
    for t in (F(-1, 8), F(-1, 16), F(-1, 100), F(0), F(1, 100), F(1, 16),
              F(1, 8)):
        lam_t = F(4) * t + F(1, 2)
        L(f"H/interpolation/{t}/weight_is_in_the_unit_interval",
          F(0) <= lam_t <= F(1))
        L(f"H/interpolation/{t}/convex_identity_holds",
          sigma(t) == add(scale(lam_t, sp), scale(F(1) - lam_t, sn)))
    L("H/interpolation_weights_reach_both_endpoints",
      F(4) * F(1, 8) + F(1, 2) == 1 and F(4) * F(-1, 8) + F(1, 2) == 0)
    minor_rows = []
    for t in (F(-7), F(-1, 3), F(-1, 8), F(0), F(1, 8), F(1, 5), F(3)):
        st = sigma(t)
        minor = det(((st[1][1], st[1][2]), (st[2][1], st[2][2])))
        L(f"H/binding_minor/{t}/matches_the_closed_form",
          minor == F(1, 64) - t * t)
        minor_rows.append((str(t), str(minor)))
    L("H/binding_minor_is_negative_outside_the_interval",
      all_of(4, (det(((sigma(t)[1][1], sigma(t)[1][2]),
                      (sigma(t)[2][1], sigma(t)[2][2]))) < 0
                 for t in (F(-9), F(-1, 7), F(1, 6), F(4)))))
    L("H/binding_minor_is_nonnegative_inside_the_interval",
      all_of(5, (det(((sigma(t)[1][1], sigma(t)[1][2]),
                      (sigma(t)[2][1], sigma(t)[2][2]))) >= 0
                 for t in (F(-1, 8), F(-1, 9), F(0), F(1, 9), F(1, 8)))))
    psd_rows = []
    for t in (F(-1, 3), F(-1, 5), F(-1, 8), F(0), F(1, 8), F(1, 5), F(1, 3)):
        ok = is_psd(sigma(t))
        L(f"H/psd_grid/{t}/verdict_matches_the_interval",
          ok == (abs(t) <= F(1, 8)))
        psd_rows.append((str(t), ok))
    tp, tn = tau(F(1, 8)), tau(F(-1, 8))
    L("H/control_family_members_are_states",
      is_psd(tp) and is_psd(tn) and trace(tp) == 1 and trace(tn) == 1)
    L("H/control_family_members_are_distinct", tp != tn)
    seps = separating_pairs(tp, tn, PROBES)
    L("H/control_family_is_separated_at_nine_probe_pairs", len(seps) == 9)
    ev['sigma_binding_minor_closed_form'] = minor_rows
    ev['sigma_psd_grid'] = psd_rows
    ev['sigma_endpoints_related_by_local_reflection'] = (
        mm(mm(REFLECT_A, sp), transpose(REFLECT_A)) == sn)
    ev['control_pair_separating_probe_pairs'] = len(seps)

    # ---- LEG W: THE WITNESS PAIR OF RECORD ------------------------------
    # rho_+- = R +- (1/32) J (x) J with R = I/4 + (X(x)X + Z(x)Z)/16.
    # Spectrally inequivalent, so NO conjugation -- local or global,
    # orthogonal or unitary -- relates them.  The gauge objection that killed
    # the sigma pair is closed rather than mitigated.
    L("W/R_is_the_stated_local_part",
      R_LOCAL == add(scale(F(1, 4), I4),
                     scale(F(1, 16), add(XX, ZZ))))
    L("W/R_lies_in_the_product_span", in_span(R_LOCAL, loc22))
    L("W/rho_plus_definition_identity",
      RHO_PLUS == add(R_LOCAL, scale(EPS_W, JJ)))
    L("W/rho_minus_definition_identity",
      RHO_MINUS == sub(R_LOCAL, scale(EPS_W, JJ)))
    L("W/rho_plus_is_a_density_matrix",
      is_symmetric(RHO_PLUS) and is_psd(RHO_PLUS) and trace(RHO_PLUS) == 1)
    L("W/rho_minus_is_a_density_matrix",
      is_symmetric(RHO_MINUS) and is_psd(RHO_MINUS)
      and trace(RHO_MINUS) == 1)
    L("W/the_pair_is_distinct", RHO_PLUS != RHO_MINUS)
    L("W/the_difference_is_pure_composite_direction",
      sub(RHO_PLUS, RHO_MINUS) == scale(F(2) * EPS_W, JJ))
    # THE DIFFERENCE IS FORMED BY A HELPER THAT TAKES THE PAIR THROUGH
    # _distinct, so the leg below never sees the two states separately.
    _wdiff = _difference_of_distinct(RHO_PLUS, RHO_MINUS,
                                     'the difference-orthogonality leg')
    L("W/the_difference_pair_members_are_distinct",
      _wdiff == scale(F(2) * EPS_W, JJ) and _wdiff != zeros(4))
    L("W/the_difference_is_hs_orthogonal_to_every_product_generator",
      all_of(9, (hs(_wdiff, g) == 0 for g in loc22)))
    # SPECTRA, verified as an exact polynomial identity.  No root is ever
    # extracted; charpoly(rho) == prod(x - lambda_i) is the whole statement.
    cp_plus, cp_minus = charpoly(RHO_PLUS), charpoly(RHO_MINUS)
    L("W/charpoly_of_rho_plus_matches_the_stated_spectrum",
      cp_plus == poly_from_roots(SPEC_PLUS))
    L("W/charpoly_of_rho_minus_matches_the_stated_spectrum",
      cp_minus == poly_from_roots(SPEC_MINUS))
    L("W/the_two_spectra_are_different_multisets",
      sorted(SPEC_PLUS) != sorted(SPEC_MINUS))
    L("W/the_characteristic_polynomials_differ", cp_plus != cp_minus)
    L("W/both_spectra_sum_to_one",
      sum(SPEC_PLUS, F(0)) == 1 and sum(SPEC_MINUS, F(0)) == 1)
    L("W/both_spectra_are_nonnegative",
      all_of(8, (x >= 0 for x in SPEC_PLUS + SPEC_MINUS)))
    L("W/a_wrong_spectrum_is_rejected",
      cp_plus != poly_from_roots(SPEC_MINUS))
    # WHAT THE DIFFERING CHARPOLYS BUY, made explicit: conjugation preserves
    # the characteristic polynomial (named import), and the previous
    # candidate pair DID share one.  Both halves computed.
    L("W/conjugation_preserves_charpoly_on_an_orthogonal_witness",
      charpoly(mm(mm(REFLECT_A, RHO_PLUS), transpose(REFLECT_A)))
      == cp_plus)
    L("W/conjugation_preserves_charpoly_on_a_non_orthogonal_witness",
      charpoly(mm(mm(mat([[1, 2], [0, 1]]), mat([[3, 1], [4, 5]])),
                  mat([[1, -2], [0, 1]])))
      == charpoly(mat([[3, 1], [4, 5]])))
    # `cp_plus != cp_minus` is computed at W/the_characteristic_polynomials
    # _differ.  A second leg carried the same expression under the name
    # "no_conjugation_can_relate_the_pair" -- a name the PREDICATE does not
    # reach, since the step from differing charpolys to no conjugation is the
    # named import SIMILARITY_INVARIANCE_OF_CHARPOLY.  That leg is deleted.
    _cp_sig_p, _cp_sig_m = _charpolys_of_distinct(
        sigma(F(1, 8)), sigma(F(-1, 8)), 'the superseded sigma pair')
    L("W/the_superseded_sigma_pair_members_are_distinct",
      sigma(F(1, 8)) != sigma(F(-1, 8)))
    L("W/the_superseded_sigma_pair_would_not_have_supported_this",
      _cp_sig_p == _cp_sig_m)
    # PRODUCT-OBSERVABLE INVISIBILITY, on the basis and on the sweep.
    # THE SWEEP IS RUN THROUGH A NAMED PAIR, and the three legs below compute
    # what that pair is, that its two members differ, and that their
    # difference is the composite direction.  product_sweep itself refuses an
    # equal pair.
    sweep_pair = (RHO_PLUS, RHO_MINUS)
    sweep_basis_probes = BASIS_2
    sweep_probe_probes = PROBES
    L("W/the_sweep_pair_is_the_witness_pair",
      sweep_pair == (RHO_PLUS, RHO_MINUS))
    L("W/the_sweep_pair_members_are_distinct",
      sweep_pair[0] != sweep_pair[1])
    L("W/the_sweep_pair_difference_is_the_composite_direction",
      sub(sweep_pair[0], sweep_pair[1]) == scale(F(2) * EPS_W, JJ))
    # THE SWEEP AND ITS COUNT COME FROM ONE VARIABLE.  A previous version ran
    # the sweep over `PROBES` while the leg reporting "forty-nine pairs"
    # re-derived 49 from the module constant, so re-pointing the sweep at the
    # three-element basis left the count leg measuring a list the sweep never
    # touched.  `tested_*` is the list of ordered pairs the sweep ACTUALLY
    # ran, returned by the sweep itself.
    tested_basis, sep_basis = product_sweep(sweep_pair[0], sweep_pair[1],
                                            sweep_basis_probes)
    tested_probe, sep_probe = product_sweep(sweep_pair[0], sweep_pair[1],
                                            sweep_probe_probes)
    # THE SELF-COMPARISON, ON BOTH SIDES: product_sweep raises on it, and the
    # separate exhibit routine returns the empty list on it.
    L("W/the_self_comparison_is_refused",
      _refuses(lambda: product_sweep(sweep_pair[0], sweep_pair[0],
                                     sweep_probe_probes))
      and _refuses(lambda: product_sweep(sweep_pair[0], sweep_pair[0],
                                         sweep_basis_probes)))
    L("W/the_self_comparison_exhibit_is_trivially_empty",
      product_sweep_self_comparison_exhibit(
          sweep_pair[0], sweep_probe_probes)[1] == []
      and product_sweep_self_comparison_exhibit(
          sweep_pair[0], sweep_basis_probes)[1] == [])
    L("W/zero_of_the_nine_basis_product_observables_separate",
      sep_basis == [])
    L("W/the_basis_sweep_has_nine_pairs", len(tested_basis) == 9)
    L("W/zero_of_the_forty_nine_probe_pairs_separate", sep_probe == [])
    L("W/the_probe_sweep_has_forty_nine_pairs", len(tested_probe) == 49)
    L("W/the_two_sweeps_ran_over_different_numbers_of_pairs",
      len(tested_probe) > len(tested_basis) > 0)
    L("W/the_probe_sweep_ran_over_the_frozen_probe_list",
      sweep_probe_probes == PROBES and sweep_basis_probes == BASIS_2)
    L("W/the_same_sweep_does_separate_the_control_family",
      separating_pairs(tau(F(1, 8)), tau(F(-1, 8)),
                       sweep_probe_probes) != [])
    _proj_tp, _proj_tm = _joint_tables_of_distinct(
        RHO_PLUS, RHO_MINUS, (P0, P1), 'the projective measurement pair')
    L("W/the_projective_measurement_pair_members_are_distinct",
      RHO_PLUS != RHO_MINUS and len(_proj_tp) == len(_proj_tm) == 2)
    L("W/the_projective_measurement_pair_also_fails_to_separate",
      _proj_tp == _proj_tm)
    L("W/the_projective_joint_distribution_sums_to_one",
      sum((correlator(RHO_PLUS, a, b) for a in (P0, P1) for b in (P0, P1)),
          F(0)) == 1)
    # THE GLOBAL OBSERVABLE THAT DOES READ IT.  Honesty leg: what fails is
    # PRODUCT tomography, not distinguishability.
    gp, gn = trace(mm(RHO_PLUS, JJ)), trace(mm(RHO_MINUS, JJ))
    L("W/the_global_observable_separates_the_pair", gp != gn)
    L("W/the_global_observable_values_are_plus_and_minus_one_eighth",
      (gp, gn) == (F(1, 8), F(-1, 8)))
    L("W/the_global_difference_is_exactly_one_quarter",
      trace(mm(sub(RHO_PLUS, RHO_MINUS), JJ)) == F(1, 4))
    L("W/the_separating_observable_is_not_a_product",
      not in_span(JJ, loc22))
    # PPT.  COMPUTED.  What PPT buys at 2x2 is separability IN THE COMPLEX
    # EMBEDDING -- Horodecki (1996) is a theorem about C^2 (x) C^2, and its
    # FIELD hypothesis is as load-bearing as its dimension hypothesis.  Both
    # are checked below, and the REAL question is settled separately and in
    # the opposite direction.
    pt_plus = partial_transpose(RHO_PLUS, 2, 'B')
    pt_minus = partial_transpose(RHO_MINUS, 2, 'B')
    # THE DIMENSION HYPOTHESIS IS CHECKED; THE FIELD HYPOTHESIS IS RECORDED.
    # A field hypothesis is not a computational predicate -- there is nothing
    # to evaluate that could come back False -- and the previous form of this
    # leg conjoined a tautology (2*2 == 4) with two constant lookups and was
    # described as "checked".  What is computable is the ambient dimension of
    # the system, and the fact that the complex ambient space this module is
    # NOT working in is strictly larger than the real one it IS working in;
    # that is what makes the field a hypothesis worth naming rather than an
    # afterthought.  The word is now "recorded".
    L("W/the_horodecki_dimension_hypothesis_is_computed",
      len(RHO_PLUS) == 4 and len(RHO_PLUS[0]) == 4
      and len(RHO_PLUS) == len(kron(I2, I2)))
    L("W/the_horodecki_field_hypothesis_is_recorded_not_checked",
      K_dim_complex(4) == 16 and K_dim_real(4) == 10)
    L("W/this_module_works_in_the_smaller_real_ambient_space",
      K_dim_real(4) < K_dim_complex(4)
      and mat_rank(sym_basis(4)) == K_dim_real(4))
    L("W/the_complex_ambient_space_is_strictly_larger_than_the_real_one",
      K_dim_complex(4) > K_dim_real(4))
    L("W/rho_plus_is_ppt", is_psd(pt_plus))
    L("W/rho_minus_is_ppt", is_psd(pt_minus))
    L("W/the_ppt_test_is_live_it_rejects_the_singlet",
      not is_psd(partial_transpose(PSI_MINUS, 2, 'B')))
    L("W/the_ppt_test_is_live_it_rejects_phi_plus",
      not is_psd(partial_transpose(PHI_PLUS, 2, 'B')))
    L("W/the_ppt_test_accepts_the_maximally_mixed_state",
      is_psd(partial_transpose(scale(F(1, 4), I4), 2, 'B')))
    # THE MECHANISM: the partial transpose maps the pair onto each other, so
    # the composite-only direction IS the PT-odd part.
    L("W/pt_maps_rho_plus_onto_rho_minus_exactly",
      pt_plus == RHO_MINUS)
    L("W/pt_maps_rho_minus_onto_rho_plus_exactly",
      pt_minus == RHO_PLUS)
    L("W/pt_of_rho_plus_has_rho_minus_spectrum",
      charpoly(pt_plus) == cp_minus)
    L("W/pt_of_rho_minus_has_rho_plus_spectrum",
      charpoly(pt_minus) == cp_plus)
    L("W/pt_fixes_the_local_part", partial_transpose(R_LOCAL, 2, 'B')
      == R_LOCAL)
    L("W/pt_flips_the_composite_direction",
      partial_transpose(JJ, 2, 'B') == scale(F(-1), JJ))
    # The A-side flip is computed at K/pt_A_flips_the_composite_direction;
    # the leg that repeated it here is deleted.
    L("W/pt_does_not_flip_a_product_generator",
      partial_transpose(ZZ, 2, 'B') == ZZ)
    # ---- THE REAL PRODUCT CONE, DECIDED HERE AND NOT IMPORTED -----------
    # Tr(J A) = 0 for EVERY symmetric A: Tr(.) against J is linear, and it
    # vanishes on a basis of Sym(R^2), so it vanishes on all of it.  Hence
    # Tr[(A (x) B) (J (x) J)] = Tr(J A) Tr(J B) = 0 for every real symmetric
    # A, B, so the J (x) J coefficient of EVERY real-separable state -- any
    # convex combination of real product states -- is zero.  The witness pair
    # sits at +-1/8.  THE PAIR IS NOT SEPARABLE IN THE REAL PRODUCT CONE.
    L("W/trace_of_J_vanishes_on_a_basis_of_sym_R2",
      mat_rank(S2) == 3
      and all_of(3, (trace(mm(J, a)) == 0 for a in S2)))
    L("W/that_basis_spans_sym_R2", mat_rank(S2) == K_dim_real(2) == 3)
    L("W/trace_of_J_does_not_vanish_on_an_antisymmetric_matrix",
      trace(mm(J, J)) != 0)
    L("W/every_real_product_generator_has_zero_composite_coefficient",
      all_of(9, (hs(g, JJ) == 0 for g in loc22))
      and all_of(49, (hs(kron(a, b), JJ) == 0
                      for a in PROBES for b in PROBES)))
    _sep_state = linear_combination(
        (F(1, 3), kron(pure([F(1), F(0)]), pure([F(0), F(1)]))),
        (F(1, 3), kron(pure([F(1), F(1)]), pure([F(1), F(1)]))),
        (F(1, 3), kron(pure([F(1), F(-2)]), pure([F(3), F(1)]))))
    L("W/the_explicit_real_separable_state_is_a_density_matrix",
      is_psd(_sep_state) and trace(_sep_state) == 1)
    L("W/the_explicit_real_separable_state_has_zero_composite_coefficient",
      hs(_sep_state, JJ) == 0)
    L("W/the_witness_pair_has_a_nonzero_composite_coefficient",
      hs(RHO_PLUS, JJ) == F(1, 8) and hs(RHO_MINUS, JJ) == F(-1, 8))
    L("W/the_pair_is_not_separable_in_the_real_product_cone",
      hs(RHO_PLUS, JJ) != 0 and hs(RHO_MINUS, JJ) != 0
      and mat_rank(loc22) == 9
      and all_of(9, (hs(g, JJ) == 0 for g in loc22)))
    # THE SHARPER POSITIVE STATEMENT.  J (x) J is not a product of two real
    # symmetric observables -- computed above -- but it IS minus a product of
    # two Hermitian observables once the space is complexified: J (x) J =
    # -(iJ) (x) (iJ) = -Y (x) Y with Y Hermitian.  The missing direction
    # becomes an ordinary local product observable exactly at complexification
    # and not before.
    # `not in_span(JJ, loc22)` is computed at
    # W/the_separating_observable_is_not_a_product; the leg that repeated it
    # here under a second name is deleted.
    L("W/the_composite_direction_is_minus_Y_tensor_Y_after_complexification",
      tuple(tuple(e[0] for e in r) for r in ckron(Y_C, Y_C))
      == scale(F(-1), JJ)
      and all_of(16, (e[1] == 0 for r in ckron(Y_C, Y_C) for e in r)))
    L("W/the_complexified_factor_Y_is_hermitian_and_not_real",
      cdagger(Y_C) == Y_C and any(e[1] != 0 for r in Y_C for e in r))
    ev['rho_plus_spectrum'] = [str(x) for x in SPEC_PLUS]
    ev['rho_minus_spectrum'] = [str(x) for x in SPEC_MINUS]
    ev['rho_charpolys_differ'] = cp_plus != cp_minus
    ev['rho_basis_separations'] = len(sep_basis)
    ev['rho_probe_separations'] = len(sep_probe)
    ev['rho_global_JJ_values'] = [str(gp), str(gn)]
    ev['rho_pair_both_ppt'] = is_psd(pt_plus) and is_psd(pt_minus)
    ev['pt_maps_the_pair_onto_each_other'] = (pt_plus == RHO_MINUS
                                              and pt_minus == RHO_PLUS)

    # ---- LEG K: MULTI-COPY LOCAL INVISIBILITY ---------------------------
    # EXECUTED at k = 1, 2, 3.  For general k the argument is the binomial
    # expansion below, a FORMAL identity, consuming two matrix facts that are
    # computed here and the transfer identity pinned at leg P.  Nothing here
    # is cited as "verified for all k".
    L("K/pt_A_fixes_the_local_part",
      partial_transpose(R_LOCAL, 2, 'A') == R_LOCAL)
    L("K/pt_A_flips_the_composite_direction",
      partial_transpose(JJ, 2, 'A') == scale(F(-1), JJ))
    L("K/a_real_symmetric_product_effect_is_pt_A_even",
      all_of(9, (partial_transpose(kron(a, b), 2, 'A') == kron(a, b)
                 for a in BASIS_2 for b in BASIS_2)))
    L("K/a_non_symmetric_local_factor_is_not_pt_A_even",
      partial_transpose(kron(J, Z), 2, 'A') != kron(J, Z))
    # THE EXACT SINGLE-COPY IDENTITY.  This is the input that lifts the
    # general-k statement out of "verified at three values of k": PT_A maps
    # the pair onto each other EXACTLY, as matrices.
    L("K/general/pt_A_maps_the_pair_onto_each_other_exactly",
      partial_transpose(RHO_PLUS, 2, 'A') == RHO_MINUS
      and partial_transpose(RHO_MINUS, 2, 'A') == RHO_PLUS)
    L("K/general/pt_A_is_an_involution_on_the_single_copy_system",
      partial_transpose(partial_transpose(RHO_PLUS, 2, 'A'), 2, 'A')
      == RHO_PLUS)

    def _pt_functoriality_probe(t: int) -> Mat:
        """A deterministic NON-symmetric 4x4 rational, used only to witness
        that PT_A distributes over the tensor product of copies."""
        return kron(mat([[1 + t, 2], [3, 4 - t]]),
                    mat([[0, 1 + t], [5, -2]]))

    copy_rows = []
    # As with shape_witness: `ev['multicopy'] is copy_rows`, so the EV leg
    # needs a second, immutable record of the same numbers to compare against.
    copy_witness = []
    for k in COPY_COUNTS:
        d = 2 ** k
        a_pow, b_pow = RHO_PLUS, RHO_MINUS
        for _ in range(k - 1):
            a_pow = kron(a_pow, RHO_PLUS)
            b_pow = kron(b_pow, RHO_MINUS)
        diff = regroup_copies(sub(a_pow, b_pow), k)
        # THE BINOMIAL EXPANSION, EXECUTED at this k.  Every subset S of the
        # k slots contributes (+-eps)^{|S|} times the tensor with J (x) J in
        # the slots of S and R elsewhere; the even-|S| terms cancel.
        expansion = zeros(4 ** k)
        odd_terms = 0
        for mask in range(2 ** k):
            size = bin(mask).count('1')
            if size % 2 == 0:
                continue
            odd_terms += 1
            term = None
            for slot in range(k):
                factor = JJ if (mask >> slot) & 1 else R_LOCAL
                term = factor if term is None else kron(term, factor)
            expansion = add(expansion,
                            scale(F(2) * EPS_W ** size, term))
        L(f"K/{k}/binomial_expansion_reproduces_the_difference",
          regroup_copies(expansion, k) == diff)
        L(f"K/{k}/odd_subset_count_is_two_to_the_k_minus_one",
          odd_terms == 2 ** (k - 1))
        L(f"K/{k}/difference_is_pt_A_odd",
          partial_transpose(diff, d, 'A') == scale(F(-1), diff))
        L(f"K/{k}/difference_is_pt_B_odd",
          partial_transpose(diff, d, 'B') == scale(F(-1), diff))
        L(f"K/{k}/difference_is_nonzero", diff != zeros(4 ** k))
        # THE EXACT k-COPY IDENTITY, not merely the parity of the difference.
        # PT_A on the regrouped k-copy bipartition carries rho_+^{(x)k} onto
        # rho_-^{(x)k} exactly, which is the single-copy identity above
        # transported by the functoriality leg that follows.
        L(f"K/{k}/pt_A_maps_the_plus_power_onto_the_minus_power",
          partial_transpose(regroup_copies(a_pow, k), d, 'A')
          == regroup_copies(b_pow, k))
        _fp = [_pt_functoriality_probe(t) for t in range(k)]
        _prod = _fp[0]
        _ptwise = partial_transpose(_fp[0], 2, 'A')
        for _M in _fp[1:]:
            _prod = kron(_prod, _M)
            _ptwise = kron(_ptwise, partial_transpose(_M, 2, 'A'))
        L(f"K/{k}/pt_A_distributes_over_the_tensor_product_of_copies",
          partial_transpose(regroup_copies(_prod, k), d, 'A')
          == regroup_copies(_ptwise, k))
        L(f"K/{k}/the_functoriality_probe_is_not_symmetric",
          not is_symmetric(_fp[0]))
        # THE BATTERY IS BUILT ONCE, AND EVERY LEG READS THE OBJECT THAT WAS
        # BUILT.  Audit MAJOR-2, found independently by two auditors: a
        # previous version consumed (1, 7, 99) x (3, 42) in the loop while
        # the distinctness, symmetry and non-scalar legs re-derived the seed
        # list as a frozen literal.  Changing the loop's seeds to (5,5,5) x
        # (5,5) was one line, touched no pin, and left the battery holding a
        # single distinct pair out of six while all three legs stayed green.
        # Corpus rule: derive the list and the gate from ONE variable.
        effect_pairs = [(sym_probe(d, s1), sym_probe(d, s2))
                        for s1 in K_EFFECT_SEEDS_A
                        for s2 in K_EFFECT_SEEDS_B]
        effects = [e for pair in effect_pairs for e in pair]
        # THE GLOBAL EFFECT IS BUILT HERE, before the pairing list, so that it
        # can be an entry OF that list.  J (x) J on the FIRST copy pair,
        # identity on the rest: not of the form E_A (x) E_B on the regrouped
        # bipartition.
        glob = JJ
        for _ in range(k - 1):
            glob = kron(glob, I4)
        glob = regroup_copies(glob, k)
        # ONE LIST, ONE OBJECT.  The headline blindness values and a value
        # that is NOT zero are entries of the SAME comprehension over the SAME
        # `diff`.  Written the other way -- a `vals` comprehension of its own
        # -- every entry of it is zero when the statement is true, so no
        # equality among those entries has a value to distinguish; the last
        # entry here does, and it is required to be 1/4.
        probe_ops = [kron(ea, eb) for ea, eb in effect_pairs] + [glob]
        pair_vals = [trace_product(diff, E) for E in probe_ops]
        vals = pair_vals[:len(effect_pairs)]
        L(f"K/{k}/every_collective_local_effect_is_blind",
          all_of(6, (v == 0 for v in vals)))
        L(f"K/{k}/the_pairing_list_reads_the_difference_it_was_built_from",
          len(pair_vals) == len(effect_pairs) + 1 == 7
          and pair_vals[-1] == F(1, 4))
        L(f"K/{k}/the_effect_battery_is_nonvacuous",
          len(vals) == len(effect_pairs) == 6 > 0)
        # A COUNT IS NOT NON-VACUITY.  Six copies of one matrix pass a length
        # test.  TWO DIFFERENT COUNTS ARE COMPUTED ON THE OBJECT THAT WAS
        # BUILT, and the first is not pairwise distinctness: `effects` holds
        # TWELVE entries of which FIVE are distinct (the A-side seeds and the
        # B-side seeds overlap in nothing, but each seed is reused across the
        # cross product).  The previous label called that "pairwise distinct",
        # which is a different and stronger statement and is not what the
        # expression computes.  The PAIRS are pairwise distinct, and that leg
        # is the one below.
        L(f"K/{k}/the_effect_battery_has_five_distinct_matrices",
          len(set(effects)) == 5)
        L(f"K/{k}/the_effect_pairs_are_pairwise_distinct",
          len(set(effect_pairs)) == 6)
        L(f"K/{k}/no_effect_pair_repeats_one_matrix_on_both_sides",
          all_of(6, (ea != eb for ea, eb in effect_pairs)))
        L(f"K/{k}/the_effects_are_symmetric",
          all_of(12, (is_symmetric(e) for e in effects)))
        # THE THIRD INPUT TO THE GENERAL-k CHAIN, EXECUTED AT THIS k.  The
        # premise REAL_SYMMETRIC_PRODUCT_EFFECTS_ARE_PT_EVEN claimed execution
        # "at k = 1, 2, 3 on the collective effect battery" while the only
        # sites computing PT_A-evenness of a product effect were at d = 2,
        # outside this loop.  This is that leg.
        L(f"K/{k}/a_real_symmetric_product_effect_is_pt_A_even_at_this_k",
          all_of(6, (partial_transpose(kron(ea, eb), d, 'A') == kron(ea, eb)
                     for ea, eb in effect_pairs)))
        L(f"K/{k}/the_effects_are_not_all_multiples_of_the_identity",
          any(not is_scalar_multiple(e, eye(d)) for e in effects))
        L(f"K/{k}/the_seed_lists_are_distinct_and_of_the_frozen_sizes",
          len(K_EFFECT_SEEDS_A) == 3 and len(K_EFFECT_SEEDS_B) == 2
          and len(set(K_EFFECT_SEEDS_A + K_EFFECT_SEEDS_B)) == 5)
        # THE CONTROL: a GLOBAL effect on the k-copy system does separate,
        # so the blindness is a property of the product structure and not of
        # a vanishing difference.  `glob` was built above, before the pairing
        # list, and is the last entry of it.
        L(f"K/{k}/a_global_effect_separates_the_copies",
          trace_product(diff, glob) == F(1, 4))
        # It is not a local product effect, and that is computed rather
        # than asserted: every real symmetric E_A (x) E_B is PT_A-EVEN, and
        # this one is PT_A-ODD.
        L(f"K/{k}/the_global_effect_is_pt_A_odd_hence_not_a_local_product",
          partial_transpose(glob, d, 'A') == scale(F(-1), glob)
          and glob != zeros(4 ** k))
        # THE TRANSFER CHAIN IS NOT EXECUTED AS A CHAIN, AND TWO LEGS THAT
        # CLAIMED TO BE ARE WITHDRAWN.  The argument is: for a real symmetric
        # product effect E, Tr(D E) = Tr(PT_A(D) PT_A(E)) by the transfer
        # identity and the involution, = Tr(-D . E) because D is PT_A-odd and
        # E is PT_A-even, = -Tr(D E), hence 0.  A previous version wrote
        # _lhs = Tr(D E), _mid = Tr(PT_A(D) PT_A(E)) and asserted
        # `_lhs == _mid and _mid == -_lhs`.  EVERY ONE OF THOSE QUANTITIES IS
        # ZERO when the statement holds, so the assertion reduces to
        # `0 == 0 and 0 == -0` and substituting the literal F(0) for _mid left
        # both legs green.  There is nothing there to repair.  What is
        # computed instead, non-vacuously, is each INPUT to the chain: the
        # difference is PT_A-odd (above), a real symmetric collective product
        # effect is PT_A-even (below), and the transfer identity itself is
        # executed at leg P on a witness list required to carry a nonzero
        # reading.
        # COMPUTED, not transcribed.  The adjacent legs compute the same
        # predicates.  Each value is bound to a name so the shipped row and
        # the witness tuple below carry the SAME computation rather than two.
        _row_pt_odd = partial_transpose(diff, d, 'A') == scale(F(-1), diff)
        _row_pt_maps = (partial_transpose(regroup_copies(a_pow, k), d, 'A')
                        == regroup_copies(b_pow, k))
        _row_global = str(trace_product(diff, glob))
        copy_rows.append({
            'k': k, 'dim': 4 ** k, 'odd_terms': odd_terms,
            'pt_A_odd': _row_pt_odd,
            'pt_A_maps_the_powers_onto_each_other': _row_pt_maps,
            'global_value': _row_global})
        copy_witness.append((k, 4 ** k, odd_terms, _row_pt_odd, _row_pt_maps,
                             _row_global))
    # THESE THREE COMPARE THE LOOP'S OUTPUT AGAINST WRITTEN-OUT LITERALS, not
    # against COPY_COUNTS.  The previous form compared the output to the
    # constant the loop iterates over, which is the same quantity twice.
    L("K/the_executed_copy_counts_are_one_two_and_three",
      tuple(r['k'] for r in copy_rows) == (1, 2, 3) and len(copy_rows) == 3)
    L("K/the_executed_dimensions_are_four_sixteen_and_sixty_four",
      tuple(r['dim'] for r in copy_rows) == (4, 16, 64))
    L("K/the_executed_odd_subset_counts_are_one_two_and_four",
      tuple(r['odd_terms'] for r in copy_rows) == (1, 2, 4))
    ev['multicopy'] = copy_rows

    # ---- LEG EV: THE SHIPPED EVIDENCE, TIED BY VALUE --------------------
    # `ev` used to sit outside the inventory altogether.  These legs put the
    # entries a reader would quote back inside it, by comparing the SHIPPED
    # value against a recomputation.  What is not named here is descriptive
    # and uncertified, and CERTIFIED_EVIDENCE_KEYS_1 says which is which.
    L("EV/every_certified_evidence_key_is_present",
      all_of(12, (kk in ev for kk in CERTIFIED_EVIDENCE_KEYS_1))
      and len(CERTIFIED_EVIDENCE_KEYS_1) == 12)
    L("EV/reported_spectra_are_the_frozen_spectra",
      ev['rho_plus_spectrum'] == [str(x) for x in SPEC_PLUS]
      and ev['rho_minus_spectrum'] == [str(x) for x in SPEC_MINUS])
    L("EV/reported_separation_counts_are_the_sweep_results",
      ev['rho_basis_separations'] == len(sep_basis) == 0
      and ev['rho_probe_separations'] == len(sep_probe) == 0)
    L("EV/reported_global_observable_values_are_the_computed_ones",
      ev['rho_global_JJ_values'] == [str(trace(mm(RHO_PLUS, JJ))),
                                     str(trace(mm(RHO_MINUS, JJ)))]
      == ['1/8', '-1/8'])
    L("EV/reported_bank_probe_values_are_the_bank_values",
      ev['bank_probe_identity_count_defect']
      == composite_defect(_identity_count, 3, 4) == 0
      and ev['bank_probe_quaternionic_defect']
      == composite_defect(K_dim_quaternionic, 2, 2) == -8)
    L("EV/reported_sibling_mismatch_is_the_parsed_difference",
      r_joint is not None and r_local is not None
      and ev['sibling_signed_mismatch'] == r_joint - r_local == here_codim)
    L("EV/reported_maximizer_numbers_are_the_computed_ones",
      ev['maximizer_eigenspace_dimension'] == len(eig_plus) == 2
      and ev['maximizer_family_size'] == len(set(fam)) == 6)
    # EVERY COLUMN OF BOTH TABLES, NOT THE ONE COLUMN SOME OTHER LEG HAPPENED
    # TO CROSS-REFERENCE.  A previous version compared only `codim` and the
    # (n, m) pairs of `real_shapes` and only `global_value` of `multicopy`, so
    # ev['real_shapes'][i]['rank_local'] = 999 and a literal True written over
    # ev['multicopy'][i]['pt_A_odd'] both passed while the sentence above
    # asserted certification at KEY granularity.
    L("EV/reported_shape_table_carries_every_computed_column",
      len(shape_witness) == 6 and len(ev['real_shapes']) == 6
      and [(r['n'], r['m'], r['dim_sym_N'], r['rank_local'],
            r['rank_lam_lam'], r['rank_union'], r['codim'],
            r['banked_Delta_R'], r['A_n_times_A_m'])
           for r in ev['real_shapes']] == shape_witness
      and [(r['n'], r['m']) for r in ev['real_shapes']] == list(REAL_SHAPES)
      and [r['codim'] for r in ev['real_shapes']] == [1, 3, 9, 6, 10, 18]
      # RECOMPUTED rather than retained, for the two columns where that is
      # cheap: the bank value and the closed form are recomputed HERE from the
      # (n, m) read out of the shipped row.
      and all_of(6, (r['banked_Delta_R']
                     == composite_defect(K_dim_real, r['n'], r['m'])
                     and r['A_n_times_A_m']
                     == ((r['n'] * (r['n'] - 1) // 2)
                         * (r['m'] * (r['m'] - 1) // 2))
                     for r in ev['real_shapes'])))
    L("EV/reported_multicopy_rows_carry_every_computed_column",
      len(copy_witness) == 3 and len(ev['multicopy']) == 3
      and [(r['k'], r['dim'], r['odd_terms'], r['pt_A_odd'],
            r['pt_A_maps_the_powers_onto_each_other'], r['global_value'])
           for r in ev['multicopy']] == copy_witness
      and [r['global_value'] for r in ev['multicopy']] == ['1/4', '1/4', '1/4']
      and all_of(3, (r['pt_A_odd'] is True
                     and r['pt_A_maps_the_powers_onto_each_other'] is True
                     for r in ev['multicopy'])))

    key_result = (
        "THE COMPOSITE-ONLY DIRECTION OF THE REAL BIPARTITE GPT, IDENTIFIED. "
        "Sym(R^n (x) R^m) splits as [Sym(R^n) (x) Sym(R^m)] (+) "
        "[Lam(R^n) (x) Lam(R^m)], computed on six shapes (2,2), (2,3), (3,3), "
        "(2,4), (2,5), (3,4): the Lam (x) Lam generators are symmetric, "
        "independent, HS-orthogonal to EVERY product generator, and together "
        "with them span Sym(R^{nm}) -- so span(Lam (x) Lam) IS the orthogonal "
        "complement of the locally generated span, both directions executed. "
        "TWO COUNTS, AND THEY ARE EXECUTED ON DIFFERENT NUMBERS OF SHAPES. "
        "The CODIMENSION equality -- dim Sym(R^{nm}) minus the rank of the "
        "product-observable span equals composite_defect(K_dim_real, n, m), "
        "called live from quantum_admissibility.py -- is executed on NINE "
        "shapes: the six above, at values (1, 3, 9, 6, 10, 18), and (4,4), "
        "(3,5), (5,5) at leg D'''. The ORTHOGONAL-COMPLEMENT "
        "identification -- that span(Lam (x) Lam) is exactly the orthogonal "
        "complement, which needs the HS-orthogonality and the spanning legs "
        "and not a rank alone -- is executed on the SIX shapes only. The "
        "bank's integer is thereby given a referent. "
        "THE ARITHMETIC IDENTITY IS PROVED FOR ALL n AND m, SYMBOLICALLY: leg "
        "D_sym computes K_R(nm) - K_R(n) K_R(m) = nm(n-1)(m-1)/4 = "
        "[n(n-1)/2][m(m-1)/2] as an identity in the bivariate polynomial ring "
        "Q[n, m], with the three polynomials pinned against the banked "
        "K_dim_real on a 49-point integer grid. WHAT IS NOT PROVED IN GENERAL "
        "is the SPAN statement -- that the codimension of the "
        "product-observable span equals that integer -- which is executed on "
        "nine shapes and rests on the standard branching identity. "
        "NO LEG CERTIFIES ANY LIVE BANK CALL, and this module says so rather "
        "than claiming otherwise. composite_defect is a deterministic pure "
        "function of two integers, so any of its values can be transcribed as "
        "a literal and no leg can see the difference -- and the same is true "
        "of _chsh_facets, _in_local_polytope, K_dim_complex and "
        "K_dim_quaternionic, each of which is a pure function or a constant "
        "list and each of which a faithful local reimplementation would "
        "reproduce with no leg going red. ONE EXCEPTION, in this module's "
        "favour, and NARROWER THAN A PREVIOUS VERSION STATED IT: K_dim_real "
        "patched INSIDE the bank module is caught at leg A, where K_dim_real"
        "(N) is compared against the rank of an explicitly constructed "
        "symmetric basis -- two independent computations of one integer -- "
        "but only at the arguments this module exercises, N in "
        "{4, 6, 8, 9, 10, 12} there and N = ab with a, b <= 7 on the "
        "leg-D_sym grid. A patch that moves no value in that range is not "
        "caught. What IS executed elsewhere "
        "is a larger set of simultaneous constraints -- leg D' computes the "
        "imported symbol's behaviour as a higher-order function of the K it "
        "is handed "
        "(0 on the synthetic count K(N) = N; -8 on the banked quaternionic "
        "count, a value no A_n A_m can take), and leg D''' computes the "
        "bank value at THREE FURTHER SHAPES for which this module ships no "
        "literal -- (4,4), (3,5), (5,5), where the codimensions are 36, 30 "
        "and 100. That is a stronger surface, not a certification. A "
        "previous version billed the under-generated form of that leg as a "
        "NON-TRIVIAL relation with TWO live ranks. It is not: with "
        "codim_under = dim - r_under and dropped = r_full - r_under, the "
        "r_under cancels between the two sides and the statement reduces to "
        "dim - r_full = Delta_R, the ordinary codimension identity with ONE "
        "live rank, leaving PROBE_DROP unconstrained by it. The billing is "
        "withdrawn; the three extra shapes are real content and are kept. "
        "THE BANKED SIBLING AGREES, computed live: "
        "check_T_split_composite_gates_tomographic_locality "
        "(closed_world_completeness.py) compares joint_R = d_R(4) = 10 "
        "against local_R = d_R(2) d_R(2) = 9 and reports a SURPLUS of 1; "
        "this module compares the same 10 against the RANK of the "
        "product-observable span, also 9, and computes the same surplus. "
        "Leg D'' asserts provenance on the CALLABLE and parses all six "
        "numbers -- R, C and H, joint and local -- out of their own clauses "
        "BY POSITION, each comparison guarded on the parse having returned "
        "an integer; the substring test it replaces returned the same "
        "answer after the R-local moved. THE PARSED NUMBERS COME OUT OF A "
        "RETURNED STRING AND THE LEGS CANNOT TELL A COMPUTED VALUE FROM A "
        "LITERAL: a sibling replaced by a stub returning the same record "
        "would pass every one of them, this one included. One further leg "
        "reads the sibling's __doc__ and requires its prose to contain the "
        "two sign words with the two magnitudes the code computes; it is two "
        "substring tests and a docstring edit leaving both intact passes it. "
        "CONTROLS THAT BITE: dropping one product generator moves the "
        "codimension to 2; adding J (x) J to the product list sends it to 0; "
        "and the SAME routine over the complex field returns codimension 0 "
        "at (2,2), (2,3), (3,3), matching Delta_C = 0 live. "
        "A PROPOSED IDENTIFICATION IS REFUTED, not restated: at (2,2) the "
        "direction is J (x) J, which is NOT a scalar multiple of the real "
        "singlet projector and is NOT related to it by an additive identity "
        "term either -- {I, J (x) J, |psi-><psi-|} has rank 3. The singlet's "
        "composite-only coefficient is 1/4, and 1/4 is the MAXIMUM any state "
        "can carry -- computed, not asserted: I - J (x) J is PSD by exact "
        "principal minors, so Tr(rho J (x) J) <= 1 for every density matrix "
        "(Tr(AB) >= 0 for PSD A, B, named), and the same bound follows from "
        "(J (x) J)^2 = I with Tr(J (x) J) = 0 by the spectral theorem, also "
        "named. THE MAXIMIZERS ARE A CONTINUUM, not three states: J (x) J is "
        "a traceless involution whose +1 eigenspace has dimension 2, computed "
        "as a kernel, and a one-parameter family of six distinct pure states "
        "inside it all attain the bound. 'The direction singles out the "
        "singlet' therefore fails on a two-dimensional eigenspace. "
        "THE WITNESS PAIR: rho_+- = I/4 + (X(x)X + Z(x)Z)/16 +- (J(x)J)/32. "
        "Both are density matrices; their CHARACTERISTIC POLYNOMIALS DIFFER, "
        "verified as exact polynomial identities against the spectra "
        "{13/32, 7/32, 7/32, 5/32} and {11/32, 9/32, 9/32, 3/32} with no root "
        "ever extracted. Distinct spectra rule out every conjugation, local "
        "or global, orthogonal or unitary, so the hidden coefficient is NOT a "
        "local frame-orientation gauge. (The superseded pair sigma_{+-1/8} "
        "WAS: the local reflection diag(1,-1) (x) I carries one to the other, "
        "computed and disclosed at leg H, where those two remain as the "
        "endpoints of the closed interval |t| <= 1/8 and nothing else.) "
        "Zero of the nine basis product observables and zero of the 49 probe "
        "pairs separate rho_+ from rho_-, while the GLOBAL observable J (x) J "
        "takes +1/8 and -1/8 on them, a difference of exactly 1/4 -- so what "
        "fails is PRODUCT tomography, not distinguishability. "
        "BOTH ARE PPT, COMPUTED -- AND THE FIELD MATTERS. Horodecki (1996) "
        "is a theorem about a COMPLEX Hilbert space: at 2x2 over C, PPT is "
        "equivalent to separability. What PPT buys here is therefore "
        "separability IN THE COMPLEX EMBEDDING, and that is the only "
        "separability sentence this module makes. IN THE REAL PRODUCT CONE "
        "THE PAIR IS NOT SEPARABLE, and that is COMPUTED rather than "
        "imported: Tr(J A) = 0 for every real SYMMETRIC A -- the functional "
        "is linear and vanishes on a basis of Sym(R^2) -- so "
        "Tr[(A (x) B)(J (x) J)] = Tr(JA) Tr(JB) = 0, and EVERY "
        "real-separable state, being a convex combination of real product "
        "states, has composite coefficient exactly zero. An explicit "
        "three-term real product mixture is exhibited at coefficient 0; the "
        "witness pair sits at +1/8 and -1/8. AT (2,2) A NONZERO COMPOSITE-ONLY "
        "COORDINATE THEREFORE IMPLIES REAL-INSEPARABILITY, and nothing here "
        "may be read as saying the defect is not an entanglement "
        "phenomenon. THAT IMPLICATION RUNS ONE WAY ONLY: the converse, that "
        "every real-inseparable state at (2,2) carries a nonzero J (x) J "
        "coefficient, is computed nowhere here and is barred. THE SHARPER POSITIVE STATEMENT, also computed: "
        "J (x) J is not a product of two real symmetric observables, but it "
        "is -(iJ) (x) (iJ) = -Y (x) Y with Y Hermitian, so the missing "
        "direction becomes an ordinary local product observable exactly at "
        "complexification and not before. "
        "THE MECHANISM IS THE PARTIAL TRANSPOSE, executed: PT(rho_+) = rho_- "
        "exactly and conversely, because PT fixes the product part R and "
        "flips J (x) J. The composite-only direction IS the PT-odd part, "
        "which is simultaneously why the pair is locally invisible and why "
        "both are PPT. "
        "MULTI-COPY: at k = 1, 2 and 3 the difference rho_+^{(x)k} - "
        "rho_-^{(x)k} is reproduced by its binomial expansion over odd "
        "subsets (2^{k-1} terms), is PT_A-odd and PT_B-odd, and is "
        "annihilated by every real symmetric collective local effect in a "
        "battery of six pairwise distinct effect PAIRS built from five "
        "distinct matrices -- both counts computed on the object that was "
        "built, and the first of them was mis-labelled 'pairwise "
        "distinctness' by a previous version -- while "
        "J (x) J on the first copy pair reads it at value 1/4 at every k. "
        "GENERAL k IS NOW CARRIED BY AN EXACT MATRIX IDENTITY rather than "
        "by a k-by-k expansion. PT_A(rho_+) = rho_- EXACTLY -- as matrices, "
        "not merely up to characteristic polynomial -- and PT_A(rho_-) = "
        "rho_+; the partial transpose distributes over the tensor product "
        "of copies, executed at k = 1, 2, 3 on a non-symmetric probe; so "
        "PT_A(rho_+^{(x)k}) = rho_-^{(x)k} for EVERY k and the difference "
        "D_k is PT_A-odd at every k. Every real symmetric E_A (x) E_B is "
        "PT_A-even, computed; the transfer identity Tr(PT_A(M) N) = "
        "Tr(M PT_A(N)) with the involution then gives Tr(D_k E) = "
        "Tr(PT_A(D_k) PT_A(E)) = -Tr(D_k E), hence 0, for ALL k. THE CHAIN "
        "IS NOT EXECUTED AS A CHAIN, and a previous version of this sentence "
        "said it was. Every quantity along it vanishes when the statement "
        "holds, so an equality among them has nothing to distinguish; the "
        "two legs per k that compared them are WITHDRAWN rather than "
        "repaired. What is executed, with something at stake, is each INPUT: "
        "the difference is computed PT_A-odd at each k, a real symmetric "
        "collective product effect is computed PT_A-even at each k on the "
        "battery actually used, and the transfer identity runs at leg P on a "
        "witness list required to carry a nonzero reading. WHAT "
        "REMAINS IMPORTED is elementary and named: tensor functoriality of "
        "the partial transpose, and the transfer identity. The finite "
        "verification at k = 1, 2, 3 is kept as corroboration, not as the "
        "argument. "
        "SCOPE: the underlying decomposition and the failure of local "
        "tomography in real quantum theory are standard (Wootters 1990; "
        "Hardy 2001; the branching identity is Fulton-Harris 1991). NOT "
        "CLAIMED: nothing here says the exhibited "
        "system is APF-inadmissible -- that step is the [P_regime] half of "
        "check_T_field_selection_complex and is not consumed."
    )

    return _result(
        name=_NAME,
        epistemic=epistemic,
        key_result=key_result,
        evidence=ev,
        legs=legs,
        tier=MODULE_TIER,
        dependencies=["quantum_admissibility.composite_defect",
                      "quantum_admissibility.K_dim_real",
                      "quantum_admissibility.K_dim_complex",
                      "quantum_admissibility.K_dim_quaternionic",
                      "closed_world_completeness."
                      "check_T_split_composite_gates_tomographic_locality "
                      "(leg D'' only, to pin its six reported numbers)"],
        premises=[
            "LOCAL_PRODUCT_OBSERVABLE_MODEL (STRUCTURAL -- this is where the "
            "physics enters): 'what a pair of local measurements can read' is "
            "modelled as the real span of {A (x) B : A in Sym(R^n), B in "
            "Sym(R^m)}.  This is the standard local-tomography span and it is "
            "a DEFINITION OF THE MODEL, not a theorem proved here.  It covers "
            "joint outcome statistics of arbitrary local measurements, since "
            "each joint outcome operator is a product of the two local "
            "spectral projectors; leg H exercises this on an explicit "
            "projective pair, and leg K extends the same modelling choice to "
            "collective effects on k copies per side.",
            "PSD_CONE_CONVEXITY (STRUCTURAL): the set of PSD matrices is "
            "convex.  Used at leg H to close the interval |t| <= 1/8 from its "
            "two endpoints, so the seven-point grid is a witness and not the "
            "argument.  The EXTERIOR is closed without it, by the exact "
            "closed form 1/64 - t^2 for the binding principal minor.",
            "HOROD_1996_PPT_SEPARABLE (NAMED MATHEMATICAL IMPORT, "
            "load-bearing at leg W): M. Horodecki, P. Horodecki and R. "
            "Horodecki, Phys. Lett. A 223, 1 (1996) -- on a COMPLEX Hilbert "
            "space of dimension 2x2 or 2x3, positivity under partial "
            "transpose is EQUIVALENT to separability.  THE FIELD HYPOTHESIS "
            "IS AS LOAD-BEARING AS THE DIMENSION HYPOTHESIS.  The "
            "dimension hypothesis is COMPUTED at leg W; the field hypothesis "
            "is RECORDED there, because a field hypothesis is not a "
            "computational predicate.  THIS MODULE COMPUTES PPT AND DOES NOT "
            "COMPUTE "
            "SEPARABILITY.  What the import licenses is separability IN THE "
            "COMPLEX EMBEDDING and nothing else.  The REAL question is "
            "settled here, in the opposite direction, and computed rather "
            "than imported -- see REAL_PRODUCT_CONE_COEFFICIENT.",
            "REAL_PRODUCT_CONE_COEFFICIENT (COMPUTED HERE, NOT AN IMPORT; "
            "leg W): Tr(J A) = 0 for every real symmetric A, because the "
            "functional is linear and vanishes on a basis of Sym(R^2).  Hence "
            "Tr[(A (x) B)(J (x) J)] = Tr(JA) Tr(JB) = 0 for all real "
            "symmetric A, B, so every real-separable state has composite "
            "coefficient exactly zero, while the witness pair sits at +1/8 "
            "and -1/8.  THE PAIR IS NOT SEPARABLE IN THE REAL PRODUCT CONE, "
            "and at (2,2) a NONZERO composite-only coordinate implies "
            "real-inseparability.  ONE DIRECTION ONLY: the converse is not "
            "computed here.  This is why no sentence of the form 'the defect "
            "is not an entanglement phenomenon' appears anywhere in this "
            "module.",
            "GL_BRANCHING_OF_THE_SYMMETRIC_SQUARE (NAMED MATHEMATICAL "
            "IMPORT, LOAD-BEARING FOR THE GENERAL-(n,m) SPAN STATEMENT AND "
            "FOR NOTHING ELSE): S^2(V (x) W) = (S^2 V (x) S^2 W) (+) "
            "(Lam^2 V (x) Lam^2 W) as a GL(V) x GL(W) representation.  "
            "W. Fulton and J. Harris, Representation Theory: A First Course, "
            "GTM 129, Springer (1991), Ex. 6.11; equivalently the Cauchy "
            "identity, I. G. Macdonald, Symmetric Functions and Hall "
            "Polynomials, 2nd ed., Oxford (1995), I.(4.3) and its dual "
            "(4.3').  The module "
            "EXECUTES the span statement on six shapes and the codimension "
            "count on nine; the step from those to ALL n, m is this import "
            "and was previously carried in prose with no citation while five "
            "more elementary facts were named.  The ARITHMETIC identity "
            "Delta_R = A_n A_m is proved here for all n, m at leg D_sym and "
            "consumes nothing from this premise.",
            "SPECTRAL_THEOREM_FINITE_DIM (NAMED IMPORT, legs G and H): the "
            "passage from the computed facts (J (x) J)^2 = I and "
            "Tr(J (x) J) = 0 to the eigenvalue list (+1, +1, -1, -1).  Every "
            "positivity verdict actually reported is computed independently "
            "by exact principal minors and does not rest on this import.",
            "PARTIAL_TRANSPOSE_TENSOR_FUNCTORIALITY (NAMED STRUCTURAL FACT, "
            "leg K): the partial transpose of a tensor product of bipartite "
            "operators, taken on the regrouped A-side, is the tensor product "
            "of the per-copy partial transposes.  Elementary index "
            "bookkeeping, EXECUTED at k = 1, 2, 3 on a non-symmetric probe, "
            "and named because together with the exact identity "
            "PT_A(rho_+) = rho_- it is what carries the multi-copy result to "
            "ALL k rather than to the three executed values.",
            "PARTIAL_TRANSPOSE_TRACE_TRANSFER (NAMED STRUCTURAL FACT, leg "
            "K): Tr(PT_A(M) N) = Tr(M PT_A(N)) for all M, N on the bipartite "
            "system.  The general-k conclusion was described as resting on "
            "'an exact matrix identity plus two named elementary facts' "
            "while only the functoriality was in this list; the transfer "
            "identity is the second of those two facts and is named here.  "
            "It is EXECUTED at leg P on a three-member witness list whose "
            "length, distinctness and nonzero reading are each computed, and "
            "it is computed against a map that FAILS it.  It is what turns "
            "Tr(D_k E) into Tr(PT_A(D_k) PT_A(E)) at every k.",
            "REAL_SYMMETRIC_PRODUCT_EFFECTS_ARE_PT_EVEN (NAMED STRUCTURAL "
            "FACT, leg K): every real symmetric E_A (x) E_B is PT_A-even, at "
            "every dimension 2^k -- PT_A acts on the A factor alone and a "
            "symmetric matrix is its own transpose.  This is the third input "
            "to the general-k chain and was likewise absent from this list.  "
            "EXECUTED at k = 1 over the nine basis products and at k = 1, 2, "
            "3 on the collective effect battery, with a NON-symmetric local "
            "factor exhibited as PT_A-ODD so the property is not vacuous.  "
            "Together with the two facts above and the exact identity "
            "PT_A(rho_+) = rho_-, this is the whole general-k argument; the "
            "finite verification at k = 1, 2, 3 is corroboration.",
            "PSD_TRACE_PAIRING (NAMED IMPORT, leg G): Tr(A B) >= 0 whenever "
            "A and B are both positive semidefinite.  The route leg G "
            "EXECUTES for the maximality of the coefficient 1/4.",
            "SIMILARITY_INVARIANCE_OF_CHARPOLY (NAMED IMPORT, leg W): "
            "conjugation preserves the characteristic polynomial.  This is "
            "what turns the computed fact 'the charpolys differ' into 'no "
            "conjugation, local or global, relates the pair'.  Elementary, "
            "and named because it carries the whole gauge refutation; both "
            "an orthogonal and a non-orthogonal conjugation witness are "
            "computed at leg W.",
            "NO REGIME PREMISE IS CONSUMED.  Only the [P_math] arithmetic of "
            "check_T_field_selection_complex is used; its [P_regime] step "
            "from a positive defect to inadmissibility is NOT taken, and no "
            "inadmissibility conclusion is drawn.",
        ],
        negative_controls=[
            "under-generation: dropping one product generator moves the "
            "codimension from 1 to 2; enlargement by J (x) J sends it to 0",
            "the same routine over C returns codimension 0, so it does not "
            "always answer 'positive' and is not R-specific",
            "the imported composite_defect returns 0 on the synthetic count "
            "K(N) = N and -8 on the banked quaternionic count, so it reads "
            "the K it is handed and is not a hardwired A_n A_m",
            "the polynomial engine at leg D_sym rejects a false identity and "
            "distinguishes its two variables, so the symbolic proof is not "
            "carried by a degenerate ring",
            "the leg-D'' parser is run on a copy of the sibling string with "
            "the R-local moved, and on a copy with the C-local moved, and "
            "returns the moved value in each case; the substring test it "
            "replaces is run on the same string and returns the same answer "
            "before and after",
            "the PSD certificate for the maximality of 1/4 is not vacuous: "
            "I - 2 J (x) J and (1/2) I - J (x) J are both rejected, and the "
            "battery contains members strictly below and below zero",
            "the maximizer eigenspace is exhibited as 2-dimensional and a "
            "state outside it falls strictly short, so the continuum claim "
            "has a matching negative case",
            "the PPT test is live: it REJECTS the singlet and |phi+><phi+| "
            "and accepts the maximally mixed state",
            "the partial transpose is distinguished from the full transpose, "
            "from itself on the other side, and shown to be an involution",
            "the sigma endpoints ARE related by a local reflection and DO "
            "share a characteristic polynomial -- computed, which is exactly "
            "why they are not the witness pair",
            "the control state family I/4 + t Z (x) Z is separated by the "
            "same 49-pair product sweep, at 9 pairs, and by the k-copy "
            "battery's global effect at every k",
            "is_psd is computed on a matrix whose only failing principal "
            "minor is exactly -10^-6, and returns False; the minor's value "
            "is computed by an adjacent leg, and is_psd is computed on the "
            "positive-minor counterpart and returns True.  This BOUNDS a "
            "float tolerance at 1e-6; a tolerance of 1e-9 returns the same "
            "two answers",
            "is_psd's SYMMETRY precondition is exercised on [[1,2],[0,1]], "
            "whose principal minors 1, 1 and 1 are computed to be "
            "non-negative and whose non-symmetry is computed, and on which "
            "is_psd returns False",
            "hs is computed on a NON-SYMMETRIC argument pair on which the "
            "transposed convention Tr(A B) returns 1 while the entrywise "
            "convention returns 0; both values are computed, the two are "
            "compared with each other and required to differ, and the two "
            "conventions are also computed on a symmetric pair and required "
            "to agree",
            "the charpoly literal is NON-PALINDROMIC -- (6, -5, 1) for "
            "diag(2,3) -- so the leg comparing charpoly against the reversed "
            "tuple has two different tuples to compare; the identity's "
            "(1, -2, 1) reads the same reversed",
            "the k-copy effect battery is measured for CONTENT and not "
            "only for length: six copies of one matrix have length six.  Two "
            "separate counts are computed on the battery object that was "
            "built -- the twelve assembled matrices contain FIVE distinct "
            "ones, and the six PAIRS they were assembled into are pairwise "
            "distinct.  A previous version called the five-distinct count "
            "'pairwise distinctness', which it is not, and read the seed list "
            "re-derived as a literal rather than the object; with degenerate "
            "loop seeds the battery held one distinct pair out of six while "
            "all three battery-quality legs were green",
            "the leg-D_sym integer grid has its size (49), its pairwise "
            "distinctness and the number of its points carrying a nonzero "
            "defect (36) computed as legs, and a perturbed joint polynomial "
            "and a perturbed closed form are each evaluated on it and "
            "rejected.  `all(... for ... in [])` is vacuously true, and at "
            "(1,1) every candidate polynomial here evaluates to 0",
            "the invisibility sweep RAISES on a pair whose two members are "
            "the same matrix, by identity or by value; the raise is recorded "
            "as a leg through _refuses, and the deliberate self-comparison "
            "is computed on a SEPARATE routine that takes one matrix and "
            "returns the empty list.  The routine the content legs call has "
            "no flag on it.  The same shape covers "
            "correlator_vectors_of_pair, _distinct (the "
            "projective-measurement pair, the difference pair, the "
            "superseded sigma pair) and _distinct_lists (the leg-C "
            "orthogonality loop)",
            "the sweep returns the ordered pairs it TESTED, and 'nine' and "
            "'forty-nine' are the lengths of those returned lists rather "
            "than re-derivations from the module constants",
            "the PT trace-transfer witness list has its length, its pairwise "
            "distinctness and the presence of a nonzero value among its "
            "readings each computed as a leg",
            "the k-copy blindness values and a nonzero global value are "
            "entries of ONE comprehension over ONE difference matrix, so the "
            "list carrying the headline all-zero statement also carries a "
            "value that is required to be 1/4",
            "p_eval is pinned on its VARIABLE ORDER -- every polynomial in "
            "play is symmetric in n and m, so nothing else could see a swap",
            "the shipped evidence entries named in CERTIFIED_EVIDENCE_KEYS_1 "
            "are tied by value to the computation that produced them; the "
            "rest of the evidence dict is descriptive and uncertified, and "
            "is declared so rather than left to be found",
            "the real product cone is exercised in BOTH directions: an "
            "explicit three-term real product mixture has composite "
            "coefficient 0, and the witness pair has +-1/8, so the pair is "
            "NOT real-separable",
            "cmul(i, i) = -1 and two written-out ckron literals reject the "
            "split-complex product i^2 = +1, which reproduces every leg-E(iii) "
            "dimension count and is invisible to a Hermiticity test",
        ],
        cross_refs=[
            "check_T_field_selection_complex -- supplies the integer "
            "Delta_R(n, m) this module identifies; only its [P_math] half "
            "is consumed",
            "check_T_split_composite_gates_tomographic_locality -- a "
            "CONCORDANT count, by different means.  It compares "
            "joint_R = d_R(4) = 10 against local_R = d_R(2) d_R(2) = 9 with "
            "d_R(n) = n(n+1)/2 the full symmetric dimension, a SURPLUS of "
            "1.  This module compares the same 10 against the RANK of the "
            "product-observable span, also 9, and computes the same "
            "surplus.  Agreement between a dimension count and a rank is "
            "concordance, not independent corroboration: the sibling "
            "recomputes the closed form this module proves.  Leg D'' "
            "parses all three clauses structurally, compares each parsed "
            "number against a literal, and requires the sibling's prose to "
            "carry the same signs as its code",
            "check_L_bipartite_chsh_blind_to_composite_only_direction"],
    )


# ==========================================================================
# CHECK 2
# ==========================================================================


def check_L_bipartite_chsh_blind_to_composite_only_direction() -> dict:
    """[P_math | bipartite single-source: a READING FENCE, not a premise]

    A real bipartite exhibit outside the banked local polytope, and the
    computed fact that its CHSH value cannot see the composite-only
    coordinate."""
    _NAME = 'check_L_bipartite_chsh_blind_to_composite_only_direction'
    legs: Dict[str, bool] = {}
    ev: Dict[str, object] = {}

    def L(label: str, verdict) -> None:
        _leg(legs, label, verdict)

    # THE GRADE STRING, BOUND ONCE.  This name is what the grade leg below
    # reads and what is handed to _result() at the bottom of this function;
    # the string is not written out a second time at either site.
    epistemic = (
        "[P_math | bipartite single-source: a READING FENCE on "
        "what the result may be taken to say, not a premise "
        "consumed by any leg.  Structural premises: "
        "LOCAL_PRODUCT_OBSERVABLE_MODEL, "
        "RESCALE_CONSTANT_IS_DERIVED]")

    # TWO OF THE MODULE-LEVEL DECLARATIONS THIS RECORD SHIPS.  MODULE_TIER is
    # shipped as record['tier'], and the string bound just above is shipped as
    # record['epistemic'].  The record fields no leg reads are named in KNOWN
    # LIMITS.  The other three declarations -- PHYSICAL_PREMISES_CERTIFIED,
    # BANK_MODIFIED, EXPORTS -- are read at the P/ legs of the companion
    # check, which is the same module-level state.
    L("P2/the_module_tier_is_three", MODULE_TIER == 3)
    # THE GRADE, ON TWO CLAUSES.  Both are computed: the string begins
    # `[P_math`, and it does not begin with the bare `[P]` that grades a
    # result as certified physics.  The second clause is implied by the
    # first; it is written out anyway so that the bare `[P]` appears in the
    # predicate under its own name.
    L("P2/the_grade_is_p_math_and_not_a_bare_p",
      epistemic.startswith("[P_math") and not epistemic.startswith("[P]"))

    # ---- LEG P2: the sqrt-free decision validated against the bank --------
    battery = [t for t in product(_VALIDATION_VALUES, repeat=4)]
    mismatches = [t for t in battery
                  if inside_scaled(t, F(1)) != _in_local_polytope(list(t))]
    n_in = sum(1 for t in battery if _in_local_polytope(list(t)))
    L("P2/agrees_with_the_banked_polytope_on_the_whole_battery",
      mismatches == [])
    L("P2/the_validation_battery_covers_both_verdicts",
      0 < n_in < len(battery))
    # THE BATTERY'S SIZE IS COMPUTED AS A LEG.  `_VALIDATION_VALUES` is
    # otherwise only EVIDENCE, and the two legs above range over whatever the
    # battery happens to contain.  The alphabet's length, its distinctness,
    # its straddling of the unit box and the product size are each legs here.
    L("P2/the_validation_alphabet_is_six_distinct_values",
      len(_VALIDATION_VALUES) == 6 and len(set(_VALIDATION_VALUES)) == 6)
    L("P2/the_validation_alphabet_straddles_the_unit_box",
      any(v * v > 1 for v in _VALIDATION_VALUES)
      and any(v * v <= 1 for v in _VALIDATION_VALUES))
    L("P2/the_validation_battery_is_one_thousand_two_hundred_ninety_six",
      len(battery) == 1296 == 6 ** 4)
    box_only = (F(0), F(1, 2), F(-3, 2), F(0))
    L("P2/box_only_witness_violates_no_facet",
      all_of(8, (_dot(s, box_only) <= F(CLASSICAL_CHSH_BOUND)
                 for s in _chsh_facets())))
    L("P2/box_only_witness_is_rejected_at_k_1",
      not inside_scaled(box_only, F(1)))
    # ---- THE BOX CLAUSE AT k != 1 (audit item C-3) -----------------------
    # Every downstream use of inside_scaled is at k = Ksq = 2 or k = 4 Ksq.
    # At k = 1 the constants k, k^2 and 1 coincide, so each of the three
    # alternative box clauses below returns the same verdict as the true one
    # there.  This witness is evaluated at two scales, where each alternative
    # returns a different verdict from the true clause on one of the two.  The
    # verdict is carried by the BOX at both scales, not by a facet.
    w = (F(3, 2), F(0), F(0), F(0))
    L("P2/box_witness_is_outside_at_k_2", not inside_scaled(w, F(2)))
    L("P2/box_witness_is_inside_at_k_4", inside_scaled(w, F(4)))
    L("P2/box_witness_violates_no_facet_at_k_2",
      all_of(8, (not (_dot(s, w) > 0
                      and _dot(s, w) ** 2
                      > F(CLASSICAL_CHSH_BOUND) ** 2 * F(2))
                 for s in _chsh_facets())))
    L("P2/box_witness_violates_no_facet_at_k_4",
      all_of(8, (not (_dot(s, w) > 0
                      and _dot(s, w) ** 2
                      > F(CLASSICAL_CHSH_BOUND) ** 2 * F(4))
                 for s in _chsh_facets())))
    L("P2/the_two_scales_give_opposite_verdicts",
      inside_scaled(w, F(2)) != inside_scaled(w, F(4)))
    # each mis-scaling, EXECUTED against the true clause on the witness.
    for name_, variant in _BOX_VARIANTS:
        wrong = [k_ for k_ in (F(2), F(4))
                 if all(variant(x, k_) for x in w)
                 != all(_box_true(x, k_) for x in w)]
        L(f"P2/box_variant/{name_}/is_wrong_at_some_tested_scale",
          wrong != [])
    # DISCLOSED: this leg and the next compare TWO quantifiers over ONE
    # iterable, so emptying that iterable leaves the two agreeing.  The
    # cardinality is asserted separately here; see KNOWN LIMITS.
    L("P2/the_true_box_clause_agrees_with_itself_at_k_1",
      len(box_only) == 4
      and (all_of(4, (_box_true(x, F(1)) for x in box_only))
           == all_of(4, (x * x <= F(1) for x in box_only))))
    L("P2/every_box_variant_agrees_with_the_true_clause_at_k_1",
      len(w) == 4
      and all_of(3, (all_of(4, (v(x, F(1)) for x in w))
                     == all_of(4, (_box_true(x, F(1)) for x in w))
                     for _, v in _BOX_VARIANTS)))
    # ---- THE FACET CLAUSE AT k != 1 --------------------------------------
    v_facet = (F(6, 5), F(6, 5), F(6, 5), F(-6, 5))
    L("P2/facet_witness_is_inside_the_box_at_k_2",
      all_of(4, (_box_true(x, F(2)) for x in v_facet)))
    L("P2/facet_witness_is_rejected_at_k_2",
      not inside_scaled(v_facet, F(2)))
    L("P2/facet_witness_is_accepted_at_a_large_enough_scale",
      inside_scaled(v_facet, F(9)))
    ev['validation_vectors'] = len(battery)
    ev['validation_inside'] = n_in
    ev['validation_mismatches'] = len(mismatches)
    ev['box_clause_witness'] = [str(x) for x in w]
    ev['box_clause_verdicts_at_k_2_and_4'] = [inside_scaled(w, F(2)),
                                              inside_scaled(w, F(4))]

    # ---- LEG A2: the exhibit is well formed ------------------------------
    L("A2/state_is_a_rank_one_real_projector",
      trace(PSI_MINUS) == 1 and is_symmetric(PSI_MINUS)
      and mm(PSI_MINUS, PSI_MINUS) == PSI_MINUS)
    L("A2/state_is_psd", is_psd(PSI_MINUS))
    for label, M in (("Z", Z), ("X", X)):
        L(f"A2/{label}_is_a_traceless_symmetric_involution",
          mm(M, M) == I2 and is_symmetric(M) and trace(M) == 0)
    L("A2/alice_settings_do_not_commute", mm(Z, X) != mm(X, Z))
    _asym = pure([F(0), F(1), F(0), F(0)])          # |01><01|
    L("A2/correlator_argument_order_is_pinned",
      correlator(_asym, Z, I2) == 1 and correlator(_asym, I2, Z) == -1)
    L("A2/both_parties_have_two_distinct_settings",
      B0P != B1P and Z != X)
    L("A2/scal_accepts_two_times_the_identity",
      is_scalar_multiple(scale(F(2), I2), I2))
    L("A2/scal_rejects_the_diagonal_trap",
      not is_scalar_multiple(mat([[1, 1], [1, 1]]), I2))
    L("A2/scal_rejects_unequal_diagonal_entries",
      not is_scalar_multiple(mat([[1, 0], [0, 2]]), I2))
    b0sq, b1sq = mm(B0P, B0P), mm(B1P, B1P)
    L("A2/bob_first_setting_squares_to_a_multiple_of_the_identity",
      is_scalar_multiple(b0sq, I2))
    Ksq = b0sq[0][0]
    L("A2/both_bob_settings_share_one_rescale_constant",
      b0sq == scale(Ksq, I2) and b1sq == scale(Ksq, I2))
    L("A2/the_rescale_constant_is_positive", Ksq > 0)
    L("A2/the_rescale_constant_differs_from_one", Ksq != 1)
    L("A2/alice_settings_are_already_involutions",
      mm(Z, Z) == I2 and mm(X, X) == I2)
    ev['rescale_constant_squared'] = str(Ksq)

    # ---- LEG B2: the value, sign kept ------------------------------------
    scaled = correlator_vector(PSI_MINUS)
    raw = raw_chsh(scaled)
    L("B2/scaled_correlator_vector_is_the_expected_quadruple",
      scaled == (F(-1), F(-1), F(-1), F(1)))
    L("B2/raw_combination_is_minus_four", raw == -4)
    L("B2/the_signed_value_is_negative", raw < 0)
    L("B2/chsh_squared_is_eight_using_the_derived_scale",
      raw * raw / Ksq == 8)
    ev['scaled_correlators'] = [str(x) for x in scaled]
    ev['raw_signed'] = str(raw)
    ev['chsh_squared'] = str(raw * raw / Ksq)

    # ---- LEG C2: the banked facet set, consulted live --------------------
    facets = _chsh_facets()
    L("C2/the_bank_offers_eight_facets", len(facets) == 8)
    L("C2/every_banked_facet_has_sign_product_minus_one",
      all_of(8, (s[0] * s[1] * s[2] * s[3] == -1 for s in facets)))
    L("C2/no_product_plus_one_pattern_is_banked",
      (1, 1, 1, 1) not in facets and (1, 1, -1, -1) not in facets)
    L("C2/the_banked_facet_list_has_no_duplicates", len(set(facets)) == 8)
    negation_closed = all_of(8, (tuple(-x for x in s) in set(facets)
                                 for s in facets))
    L("C2/the_banked_facet_set_is_closed_under_negation", negation_closed)
    ev['facets_negation_closed'] = negation_closed
    # ---- THE SIGN GUARD, EXERCISED ---------------------------------------
    bound_c2 = F(CLASSICAL_CHSH_BOUND)
    half = [s_ for s_ in facets if s_[0] == 1]
    L("C2/guard/the_synthetic_half_list_has_four_facets", len(half) == 4)
    L("C2/guard/the_half_list_is_not_negation_closed",
      not all_of(4, (tuple(-x for x in s_) in set(half) for s_ in half)))
    guard_witness = (F(-1), F(-1), F(-1), F(0))
    gdots = [_dot(s_, guard_witness) for s_ in half]
    L("C2/guard/the_witness_is_inside_the_box",
      all_of(4, (v * v <= 1 for v in guard_witness)))
    L("C2/guard/a_half_list_facet_takes_a_large_negative_value",
      any(d < 0 and d * d > bound_c2 * bound_c2 for d in gdots))
    L("C2/guard/no_half_list_facet_takes_a_large_positive_value",
      all_of(4, (not (d > 0 and d * d > bound_c2 * bound_c2)
                 for d in gdots)))
    L("C2/guard/the_guarded_procedure_accepts_the_witness",
      inside_scaled(guard_witness, F(1), facets=half))
    L("C2/guard/the_witness_is_outside_on_the_full_banked_list",
      not inside_scaled(guard_witness, F(1)))
    L("C2/guard/the_bank_agrees_the_witness_is_outside",
      not _in_local_polytope(list(guard_witness)))
    ev['sign_guard_witness'] = [str(x) for x in guard_witness]
    ev['sign_guard_half_list_dots'] = [str(d) for d in gdots]

    # ---- LEG D2: the TRUE vector decided, sqrt-free ----------------------
    L("D2/every_true_correlator_is_within_unit_magnitude",
      all_of(4, (v * v <= Ksq for v in scaled)))
    dots = [(s, _dot(s, scaled)) for s in facets]
    best_s, best = max(dots, key=lambda p: p[1])
    L("D2/the_maximum_banked_facet_value_is_four", best == 4)
    L("D2/the_maximizing_facet_value_is_positive", best > 0)
    bound = F(CLASSICAL_CHSH_BOUND)
    L("D2/the_facet_is_violated_on_the_true_vector",
      best * best > bound * bound * Ksq)
    L("D2/the_facet_value_equals_the_magnitude_of_the_raw_combination",
      best == -raw)
    true_facet_sq = best * best / Ksq
    L("D2/the_facet_square_and_the_chsh_square_agree",
      true_facet_sq == raw * raw / Ksq)
    L("D2/the_facet_square_on_the_true_vector_is_eight",
      true_facet_sq == 8)
    L("D2/eight_exceeds_the_classical_bound_squared",
      true_facet_sq > bound * bound)
    true_sq = [v * v / Ksq for v in scaled]
    L("D2/every_true_correlator_squared_is_at_most_one",
      all_of(4, (x <= 1 for x in true_sq)))
    L("D2/every_true_correlator_squared_is_one_half",
      all_of(4, (x == F(1, 2) for x in true_sq)))
    L("D2/the_true_vector_is_outside_the_banked_polytope",
      not inside_scaled(scaled, Ksq))
    wrong_k = F(4) * Ksq
    L("D2/control_the_same_vector_at_four_times_the_scale_is_inside",
      inside_scaled(scaled, wrong_k))
    L("D2/control_the_unscaled_vector_is_outside",
      not inside_scaled(scaled, F(1)))
    ev['true_correlators_squared'] = [str(x) for x in true_sq]
    ev['violating_facet'] = list(best_s)
    ev['max_facet_on_scaled'] = str(best)
    ev['true_max_facet_squared'] = str(true_facet_sq)

    # ---- LEG E2: THE BRIDGE ---------------------------------------------
    func_rows = []
    for t in (F(-1, 2), F(-1, 4), F(0), F(1, 4), F(1, 2), F(7, 3)):
        v = correlator_vector(add(PSI_MINUS, scale(t, JJ)))
        L(f"E2/functional/{t}/correlators_are_unchanged", v == scaled)
        func_rows.append(str(t))
    L("E2/functional_sweep_ran_at_six_points", len(func_rows) == 6)
    L("E2/functional_control_a_local_direction_does_move_them",
      correlator_vector(add(PSI_MINUS, scale(F(1, 4), ZZ))) != scaled)
    # THE STATES: the witness pair of record, not the sigma endpoints.
    L("E2/states/the_witness_pair_are_two_distinct_density_matrices",
      is_psd(RHO_PLUS) and is_psd(RHO_MINUS) and trace(RHO_PLUS) == 1
      and trace(RHO_MINUS) == 1 and RHO_PLUS != RHO_MINUS)
    L("E2/states/the_witness_pair_is_spectrally_inequivalent",
      charpoly(RHO_PLUS) != charpoly(RHO_MINUS))
    # THE COMPARISON IS RUN THROUGH A NAMED PAIR, and the two legs below
    # compute what that pair is and that its members differ.
    state_pair = (RHO_PLUS, RHO_MINUS)
    L("E2/states/the_compared_pair_is_the_witness_pair",
      state_pair == (RHO_PLUS, RHO_MINUS))
    L("E2/states/the_compared_pair_members_are_distinct",
      state_pair[0] != state_pair[1])
    # THE COMPARISON GOES THROUGH A ROUTINE THAT REFUSES A SELF-COMPARISON.
    # The two legs above read the TUPLE; the refusal is at the CALL.  The
    # routine has no flag on it: the deliberate exhibit below is a separate
    # function taking one matrix.
    vp, vn = correlator_vectors_of_pair(state_pair)
    L("E2/states/the_self_comparison_is_refused",
      _refuses(lambda: correlator_vectors_of_pair((state_pair[0],
                                                   state_pair[0]))))
    L("E2/states/the_self_comparison_exhibit_is_trivially_equal",
      correlator_vectors_self_comparison_exhibit(state_pair[0])[0]
      == correlator_vectors_self_comparison_exhibit(state_pair[0])[1])
    L("E2/states/the_two_returned_vectors_come_from_the_two_pair_members",
      vp == correlator_vector(state_pair[0])
      and vn == correlator_vector(state_pair[1]))
    L("E2/states/the_witness_pair_give_the_same_correlator_vector",
      vp == vn)
    L("E2/states/the_witness_pair_sit_at_different_composite_coordinates",
      trace(mm(RHO_PLUS, JJ)) != trace(mm(RHO_MINUS, JJ)))
    L("E2/states/the_witness_pair_give_the_same_chsh_value",
      raw_chsh(vp) == raw_chsh(vn))
    L("E2/states/control_the_locally_differing_pair_moves_the_correlators",
      correlator_vector(tau(F(1, 8))) != correlator_vector(tau(F(-1, 8))))
    # THE INTERVAL ENDPOINTS GO THROUGH THE SAME REFUSING ROUTINE.
    _endpoints = (sigma(F(1, 8)), sigma(F(-1, 8)))
    _ep, _en = correlator_vectors_of_pair(_endpoints)
    L("E2/states/the_interval_endpoints_are_distinct_states",
      _endpoints[0] != _endpoints[1])
    L("E2/states/the_interval_endpoints_agree_too", _ep == _en)
    ev['functional_invariant_over_t'] = func_rows
    ev['witness_pair_same_correlators'] = [str(x) for x in vp]
    ev['witness_pair_composite_coordinates'] = [
        str(trace(mm(RHO_PLUS, JJ))), str(trace(mm(RHO_MINUS, JJ)))]

    # ---- LEG EV: THE SHIPPED EVIDENCE, TIED BY VALUE --------------------
    # Inflating ev['chsh_squared'] from 8 to 16 left every leg of the previous
    # version green.  These legs compare the shipped entries against the
    # computation that produced them.
    L("EV/every_certified_evidence_key_is_present",
      all_of(8, (kk in ev for kk in CERTIFIED_EVIDENCE_KEYS_2))
      and len(CERTIFIED_EVIDENCE_KEYS_2) == 8)
    L("EV/the_reported_chsh_square_is_the_computed_one",
      ev['chsh_squared'] == str(raw * raw / Ksq) == '8')
    L("EV/the_reported_raw_signed_value_is_the_computed_one",
      ev['raw_signed'] == str(raw) == '-4')
    L("EV/the_reported_scaled_correlators_are_the_computed_ones",
      ev['scaled_correlators'] == [str(x) for x in scaled]
      == ['-1', '-1', '-1', '1'])
    L("EV/the_reported_validation_counts_are_the_battery_counts",
      ev['validation_vectors'] == len(battery) == 1296
      and ev['validation_mismatches'] == len(mismatches) == 0
      and ev['validation_inside'] == n_in)
    L("EV/the_reported_facet_square_is_the_computed_one",
      ev['true_max_facet_squared'] == str(true_facet_sq) == '8')
    L("EV/the_reported_composite_coordinates_are_the_computed_ones",
      ev['witness_pair_composite_coordinates']
      == [str(trace(mm(RHO_PLUS, JJ))), str(trace(mm(RHO_MINUS, JJ)))]
      == ['1/8', '-1/8'])

    key_result = (
        "A REAL BIPARTITE EXHIBIT OUTSIDE THE BANKED LOCAL POLYTOPE, AND ITS "
        "BLINDNESS TO THE COMPOSITE-ONLY DIRECTION. The real singlet with the "
        "real Pauli settings Z, X and B' = Z +- X (each squaring to 2I) gives "
        "the exact scaled correlator vector (-1,-1,-1,1); the raw combination "
        "is -4, so the signed CHSH is -2 sqrt(2) and CHSH^2 = raw^2 / Ksq = 8. "
        "THE SIGN IS KEPT: the certificate is on |CHSH|. THE RESCALE CONSTANT "
        "IS NOT A FREE LITERAL: Ksq is READ OFF the settings at leg A2 -- "
        "recovered from B0'^2, required to be the same for both of Bob's "
        "settings, positive, and different from 1, with Alice's settings "
        "required to square to the identity -- and it is the only scale used "
        "downstream. Leg A2 computes that Ksq differs from 1; taking Ksq = 1 "
        "instead, which is what forgetting Bob's rescaling amounts to, would "
        "INFLATE the reported violation. NONCLASSICALITY IS DECIDED ON THE "
        "TRUE CORRELATOR VECTOR, "
        "sqrt-free: the banked _chsh_facets are consulted live (8 patterns, "
        "sign product -1 each, closed under negation), the maximum facet "
        "value on the scaled vector is 4, and 16 > 8 = 2^2 . Ksq, so that "
        "facet exceeds 2 on the true vector while every true correlator "
        "squared is 1/2. OUTSIDE. "
        "THE DECISION PROCEDURE IS VALIDATED ON BOTH OF ITS CLAUSES AT THE "
        "SCALES IT IS ACTUALLY USED AT. Against the banked "
        "_in_local_polytope on 1296 rational vectors covering both verdicts "
        "at k = 1; and, because every downstream use is at k != 1 where the "
        "constants k, k^2 and 1 stop coinciding, on a box witness "
        "(3/2, 0, 0, 0) that is OUTSIDE at k = 2 and INSIDE at k = 4 while "
        "violating no facet at either scale -- each of the three plausible "
        "mis-scalings (v^2 <= k*k, v^2 <= 1, |v| <= k) is executed here and "
        "gets one of those two verdicts wrong. The FACET clause is separately "
        "exercised at k = 2 on a vector inside the box. THE SIGN GUARD IS "
        "EXERCISED, not disclaimed: on the banked list it changes no verdict "
        "because that list is negation-closed (computed), so it is exercised "
        "on a synthetic half list that is NOT, on a witness inside the box "
        "that violates no positive facet value and takes -3 at (1,1,1,-1) -- "
        "with the guard the procedure accepts it, without it 9 > 4 rejects "
        "it, so the verdict flips. "
        "THE BRIDGE: every CHSH correlator is an expectation of a product "
        "observable, so it is blind to the composite-only coordinate -- "
        "computed twice, once on the FUNCTIONAL (the four correlators are "
        "unchanged by adding t J (x) J at six values of t, including values "
        "where the matrix is not a state) and once on STATES, using the "
        "SPECTRALLY INEQUIVALENT witness pair rho_+- of the companion check: "
        "two distinct density matrices with different characteristic "
        "polynomials, at composite coordinates +1/8 and -1/8, giving "
        "identical correlators and identical CHSH. A control family that "
        "DOES move the correlators is computed alongside. CONSEQUENCE: a "
        "bipartite CHSH test and the surplus counted by Delta_R(2,2) = 1 "
        "live in complementary summands of Sym(R^4); neither is evidence "
        "about the other. "
        "SCOPE, A READING FENCE AND NOT A PREMISE -- no leg consumes "
        "single-sourcedness, and what the fence governs is what the result "
        "may be read as saying: this is BIPARTITE AND SINGLE-SOURCE ONLY. In "
        "networks with independent sources real and complex quantum theory "
        "differ and the real theory has been experimentally falsified (Renou "
        "et al., Nature 600, 625 (2021); Li et al. and Chen et al., PRL 128, "
        "040402 and 040403 (2022)). This module cites ONE side of that "
        "question and surveys no rebuttal literature. The exhibit itself is "
        "textbook and is NOT ATTRIBUTED, because it is not attributable: the "
        "singlet measured in two real planar bases at 45 degrees is the "
        "standard CHSH/Tsirelson configuration, written down in CHSH, PRL "
        "23, 880 (1969) and in Cirel'son, Lett. Math. Phys. 4, 93 (1980), "
        "and it predates the real-representation literature. A previous "
        "version credited it to Gisin and Peres, Phys. Lett. A 162, 15 "
        "(1992); that over-credits and is withdrawn, and so is the "
        "description of that paper this module used to carry. Phys. Lett. A "
        "162, 15 (1992) is N. Gisin and A. Peres, 'Maximal violation of "
        "Bell's "
        "inequality for arbitrarily large spin'; it does not carry a general "
        "real-representability statement. McKague, Mosca and Gisin cite it "
        "for the narrower fact that the optimal CHSH observables can be "
        "written real in the Schmidt bases. MMG, PRL 102, 020505 (2009), "
        "attribute the BIPARTITE real-representation result to a PERSONAL "
        "COMMUNICATION (2007) from Navascues, Acin, Pironio and Gisin -- "
        "that entry in their reference list is a personal communication and "
        "not a paper, and an earlier version of this module cited it as "
        "though it were one -- and to Pal and Vertesi, PRA 77, 042105 "
        "(2008); an earlier version of this module named only Pal and "
        "Vertesi out of that list. MMG's own contribution is the "
        "multipartite extension, and they remain the citation of record for "
        "the real-Hilbert-space simulation claim, not for this exhibit. "
        "That 2 sqrt(2) is the "
        "MAXIMUM is Cirel'son, Lett. Math. Phys. 4, 93 (1980), a named "
        "import used by no leg, so nothing here 'saturates' anything."
    )

    return _result(
        name=_NAME,
        epistemic=epistemic,
        key_result=key_result,
        evidence=ev,
        legs=legs,
        tier=MODULE_TIER,
        dependencies=["third_boat_no_extension._chsh_facets",
                      "third_boat_no_extension._dot",
                      "third_boat_no_extension._in_local_polytope",
                      "third_boat_no_extension.CLASSICAL_CHSH_BOUND"],
        premises=[
            "LOCAL_PRODUCT_OBSERVABLE_MODEL (STRUCTURAL): as in the "
            "companion check -- 'what a pair of local measurements can read' "
            "is the real span of {A (x) B}.  A definition of the model, not "
            "a theorem.  It is what makes 'CHSH cannot see the composite-only "
            "coordinate' a consequence rather than a coincidence.",
            "BIPARTITE_SINGLE_SOURCE_SCOPE: a READING FENCE, not a premise.  "
            "No leg consumes single-sourcedness -- every leg is exact linear "
            "algebra on a 4x4 matrix plus a call into the banked (2,2,2) "
            "polytope, and would return the same values whatever the source "
            "structure.  What the fence governs is what the RESULT may be "
            "read as saying: nothing here speaks to network scenarios with "
            "independent sources, where real quantum theory is falsified.",
            "RESCALE_CONSTANT_IS_DERIVED, not assumed: Ksq is read off "
            "B0'^2 at leg A2, both of Bob's settings are required to return "
            "the same value, Alice's are required to square to the identity, "
            "and Ksq is required to differ from 1.  It is the only scale "
            "used at legs B2 and D2.",
            "REAL_SINGLET_CHSH_EXHIBIT_PROVENANCE: the exhibit is standard "
            "and is NOT ATTRIBUTED here, because it is not attributable.  "
            "The singlet with two real planar bases at 45 degrees is the "
            "CHSH/Tsirelson configuration -- Clauser, Horne, Shimony and "
            "Holt, PRL 23, 880 (1969); Cirel'son, Lett. Math. Phys. 4, 93 "
            "(1980) -- and predates the real-representation literature.  Two "
            "earlier attributions are withdrawn: to McKague, Mosca and Gisin "
            "(2009), and to Gisin and Peres, Phys. Lett. A 162, 15 (1992).  "
            "A THIRD WITHDRAWAL, of a description rather than an "
            "attribution: an earlier version said Gisin and Peres carry 'the "
            "general real-representability statement'.  They do not.  Phys. "
            "Lett. A 162, 15 (1992) is N. Gisin and A. Peres, 'Maximal "
            "violation of Bell's inequality for arbitrarily large spin'; MMG "
            "cite it for the narrower fact that the optimal CHSH observables "
            "can be written real in the Schmidt bases, and that is the only "
            "thing it is cited for here.  MMG attribute the bipartite "
            "real-representation result to a PERSONAL COMMUNICATION (2007) "
            "from Navascues, Acin, Pironio and Gisin -- a personal "
            "communication in their reference list, not a paper, and an "
            "earlier version of this module cited it as though it were one "
            "-- and to Pal and Vertesi, PRA 77, 042105 (2008); naming only "
            "Pal and Vertesi out of that list, as an earlier version did, is "
            "also withdrawn.  MMG's own contribution is the multipartite "
            "extension and they remain the citation of record for the "
            "real-Hilbert-space SIMULATION claim only.",
            "CIRELSON_1980_MAXIMALITY: B. S. Cirel'son, Lett. Math. Phys. 4, "
            "93 (1980).  A named import, LOAD-BEARING FOR NO LEG.  This "
            "check computes one correlation point and never uses maximality; "
            "no result here is described as saturation.",
            "The local bound and the polytope description (CHSH 1969; Fine "
            "1982) are not restated -- the banked facet set is called.",
        ],
        negative_controls=[
            "the sqrt-free procedure reproduces the banked _in_local_polytope "
            "on 1296 rational vectors, both verdicts represented",
            "THE BOX CLAUSE AT k != 1: one witness OUTSIDE at k = 2 and "
            "INSIDE at k = 4, violating no facet at either, on which each of "
            "the three plausible mis-scalings is executed and each gets one "
            "verdict wrong",
            "THE FACET CLAUSE AT k != 1: a vector inside the box at k = 2 "
            "that the facet clause rejects, and which a large enough scale "
            "accepts",
            "the SIGN GUARD is exercised on a synthetic facet list that is "
            "NOT closed under negation, on a witness inside the box that "
            "violates no positive facet value: with the guard the procedure "
            "accepts it, without it 9 > 4 rejects it, so the verdict flips",
            "the rescale constant is read off B0'^2 rather than written "
            "down, is computed to be positive, is computed to be the same "
            "for both of Bob's settings, and is computed to differ from 1; "
            "the value it would take if Bob's sqrt(2) rescaling were "
            "forgotten is 1, and that value would INFLATE the reported "
            "violation",
            "a vector inside every CHSH facet but outside the box is "
            "rejected, so the box clause is live",
            "the same correlator vector at scale sqrt(4 Ksq) is INSIDE",
            "adding Z (x) Z to the state DOES move the correlator vector, so "
            "the invariance under J (x) J is not vacuous",
            "the control state family I/4 + t Z (x) Z gives different "
            "correlator vectors",
            "correlator() is pinned on its ARGUMENT ORDER against |01><01|, "
            "which is not swap-invariant -- every state used elsewhere in "
            "this module is",
            "the validation battery's SIZE is computed as a leg, 6^4 = 1296 "
            "over a six-value alphabet whose distinctness and whose values "
            "inside and outside the unit box are also computed as legs -- in "
            "the previous version the alphabet was evidence, not a leg",
            "the state comparison goes through a routine that RAISES on a "
            "pair whose two members are the same matrix; the raise is "
            "recorded as a leg through _refuses, and the deliberate "
            "self-comparison is computed on a SEPARATE routine taking one "
            "matrix.  The routine the content legs call has no flag on it.  "
            "The interval-endpoint comparison goes through the same routine",
            "the shipped evidence entries named in CERTIFIED_EVIDENCE_KEYS_2 "
            "-- including the reported CHSH^2 -- are compared by value "
            "against the computation that produced them.  In the previous "
            "version inflating that number from 8 to 16 left every leg "
            "green",
        ],
        cross_refs=["check_T_third_boat_iff_local",
                    "check_T_field_selection_complex",
                    "check_L_real_composite_only_direction_is_lambda_tensor_"
                    "lambda"],
    )


# Registry keying follows the neighbouring closed_world_completeness.py
# convention: BARE theorem names, no `check_` prefix.
_CHECKS = {
    'L_real_composite_only_direction_is_lambda_tensor_lambda':
        check_L_real_composite_only_direction_is_lambda_tensor_lambda,
    'L_bipartite_chsh_blind_to_composite_only_direction':
        check_L_bipartite_chsh_blind_to_composite_only_direction,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    """The module's own driver: it calls each check and then computes the
    same four inventory quantities on each returned record.

    verify_all.run_module calls each `check_*` attribute directly and never
    calls this function.  Everything computed here is also computed inside
    _result(); this is a second site, run under `python module.py` and by the
    mutation harness.

    A previous version of this module had these computations HERE ONLY, so
    six edits that raised under __main__ returned normally when the check
    function was called the way verify_all calls it."""
    out = {}
    for n, fn in _CHECKS.items():
        r = fn()
        # The same four quantities as _enforce_leg_inventory, computed at a
        # second site on the returned record.  Not gated on `passed` and not
        # gated on the inventory-difference lists.
        _enforce_leg_inventory(r)
        full = r['name']
        if not (r['legs_expected'] == r['legs_evaluated']
                == EXPECTED_LEG_COUNTS[full]):
            raise AssertionError(
                f"{n}: leg counts disagree with the frozen literal "
                f"({r['legs_evaluated']} evaluated, {r['legs_expected']} "
                f"expected, {EXPECTED_LEG_COUNTS[full]} frozen)")
        for source, labels in (('evaluated', r['leg_labels']),
                               ('expected', sorted(EXPECTED_LEGS[full]))):
            got = _leg_digest(labels)
            if got != EXPECTED_LEG_DIGEST[full]:
                raise AssertionError(
                    f"{n}: the {source} leg-label digest {got[:16]} does not "
                    f"match the frozen literal "
                    f"{EXPECTED_LEG_DIGEST[full][:16]}")
        out[n] = r
    return out


if __name__ == '__main__':
    import sys
    bad = False
    try:
        _runs = run_all()
    except AssertionError as _exc:
        print('INVENTORY GATE RAISED (this is a FAIL, not a FLAG):')
        print('   ', _exc)
        sys.exit(1)
    for n, r in _runs.items():
        print(r['name'], '::', r['epistemic'][:60], '::',
              'PASS' if r['passed'] else 'FAIL',
              f"({r['legs_evaluated']}/{r['legs_expected']} legs)")
        for k, v in r['evidence'].items():
            print(f'    {k} = {v}')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons'][:25]:
                print('  FAILED LEG:', f)
            for f in r['leg_inventory_missing'][:25]:
                print('  MISSING LEG:', f)
            for f in r['leg_inventory_unexpected'][:25]:
                print('  UNEXPECTED LEG:', f)
    sys.exit(1 if bad else 0)
