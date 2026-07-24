# APF Zipper Reduction — Paper 5 Crosswalk v0.1

**Status:** unbanked audit reconciliation; no theorem-bank, registry, census, version, or export changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Parent packet:** `docs/audits/ZIPPER_REDUCTION_AUDIT_PACKET_v0.1.md`  
**Frontier companion:** `docs/audits/ZIPPER_REDUCTION_FRONTIER_PROGRESS_v0.1.md`

## 1. Audited source inputs

This crosswalk was prepared against the exact user-supplied source files below. The paper sources are not copied into this repository; the hashes identify the audit inputs.

| Source | SHA-256 |
|---|---|
| `Paper_5_Continuation_Symmetry_Degenerate_Occupied_Minima_v1.7(1).tex` | `0a4126f1425006f4f63814910d0043971e7810e847acd8bed6ca3a03580072f4` |
| `Paper_5_Quantum_Structure_Hilbert_Born_Supplement_v6.14(3).tex` | `b3f4122ecbfd0863f16f07861814e13c82392c841e0dfd3d1968314d6bc39943` |

## 2. Executive disposition

The two Paper 5 supplements materially help, but they change the novelty account.

`Continuation Symmetry ... v1.7` already contains a conditional whole-circle occupant–zipper route:

1. an occupied record-free coherent component with a later non-null recombination witness;
2. path connectedness in unsaturated Regime R;
3. a completion-faithful first-order rank-two bipolar lift;
4. admitted record-free coherent loops and reverses with ledger isometry;
5. smooth represented loop action;
6. a nontrivial path-connected effective image in `SO(2)`;
7. the quarter-turn `J^2=-I`, naturality, centrality, and a composite-orientation dichotomy.

`Quantum Structure ... v6.14` already contains conditional finite downstream closure for:

- IJC-to-QAC record incompatibility in a record-complete coherent interface;
- noncommutative finite record representations;
- split composite gates: tensor closure, tomographic locality, and zero-defect product accounting;
- finite complex matrix sectors and Born trace probabilities;
- extension-stability as the physical criterion that becomes complete positivity after the complex-matrix gate.

Therefore the zipper packet must **not** be billed as the first APF route to a quarter-turn, complex finite blocks, tensor structure, CP, or Born form.

Its genuine delta is narrower and useful:

> Given a realised positive rank-two Held-event plane and a differentiable non-stationary metric exchange involution, it constructs the local complex structure directly and pointwise from the moving comparison frame,
>
> \[
> A=\frac12\dot\tau\tau,
> \qquad
> J=\frac{A}{\sqrt{-\frac12\operatorname{tr}(A^2)}}.
> \]

This is a **local differential reduction and executable audit instrument**. It may shorten the local-orientation step and expose exact failure modes without first invoking the full effective-circle theorem. It does not replace Paper 5's occupancy, connectedness, naturality, centrality, composite, CP, or Born gates.

## 3. Relation between the two local-J routes

### 3.1 Paper 5 v1.7 route

The v1.7 route is global-to-local:

\[
\text{occupied coherent component}
\to
G_A^{\mathrm{eff}}=SO(2)
\to
\text{quarter-turn }J_A.
\]

The non-null recombination witness makes the effective action nontrivial. Path connectedness and exact ledger isometry place the effective image in `SO(2)`. A nontrivial path-connected subgroup of `SO(2)` is the full circle, and the quarter-turn is then selected from that circle.

### 3.2 Moving-exchange route

The zipper-reduction route is infinitesimal:

\[
\text{moving metric reflection }\tau(s)
\to
A=\tfrac12\dot\tau\tau
\to
J=A/\omega.
\]

It proves `J^2=-I` before a global circle image is assumed or derived. The formula additionally exposes the local angular speed

\[
\omega=\sqrt{-\frac12\operatorname{tr}(A^2)}.
\]

### 3.3 Non-duplication boundary

The routes agree only after a bridge identifies the moving operational comparison frames with a differentiable family of admitted exchange involutions on the same positive rank-two carrier.

The current packet does not derive that bridge. In particular:

- path-connected holonomy does not automatically supply a distinguished moving reflection family;
- a moving reflection family does not automatically prove naturality or centrality in the full observable algebra;
- a pointwise `J` does not automatically synchronize orientation across sectors;
- Paper 5's canonical coordinate formula for `J` may not be used upstream to self-certify the moving-exchange formula.

## 4. Five-premise reconciliation

| Zipper physical premise | Paper 5 surface | Reconciliation status |
|---|---|---|
| `ACTIVE_RECORD_KERNEL_REALIZED` | v6.14: IJC produces a QAC witness only in a record-complete coherent interface that already contains at least two physically co-available coherent families. v1.7 L1 starts from an actual multiply-trajectoried record-free coherent component with later recombination. | **Not discharged.** Paper 5 sharpens the occupied object and the record incompatibility it must exhibit, but explicitly leaves occupancy/co-availability as input. The new admissibility-event argument should be audited as a proposed reduction of this exact input, not treated as already banked. |
| `COMPLETION_FAITHFUL_RANK_TWO_QUOTIENT` | v1.7 L3: Paper 10's universal local continuation quotient is operationally first order and gives the total rank-two bipolar lift `W_A`; the effective loop image is faithful by passage to the represented image. | **Strong prior match, still conditional.** The mathematical carrier is already specified. Physical realization of the complete first-order response quotient remains a gate. |
| `POSITIVE_EVENT_METRIC_REALIZED` | v1.7 assumes a faithful positive ledger form and uses `T^sharp=T^{-1}` to obtain exact orthogonality. | **Not discharged.** The packet should treat v1.7 as a compatible consumer. A residual-Hessian or loop-ledger derivation of the positive form remains independently valuable. |
| `SMOOTH_NONSTATIONARY_OPERATIONAL_EXCHANGE_REALIZED` | v1.7 L2/L5 give a path-connected coherent component and smooth represented loop action; recombination gives nontriviality. | **Partially matched, not identical.** These hypotheses give nontrivial smooth holonomy, but do not by themselves identify a non-stationary family of metric exchange involutions `tau(s)`. That identification is the central new bridge to audit. |
| `RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH` | v1.7 L1/L4 require a record-free coherent component and admitted record-free coherent loops and reverses; closed-world completeness accounts for consequential exits. | **Close prior match, still contingent.** The physical existence of such a path is assumed in v1.7, not derived universally. |

## 5. Orientation and centrality reconciliation

Paper 5 v1.7 already separates three orientation questions that the zipper package must keep distinct.

### Local orientation

The repaired occupant–zipper theorem gives a local quarter-turn on the elementary bipolar plane.

### Naturality and centrality

The v1.7 naturality theorem uses the functorial first-jet lift: typed elementary comparison morphisms act as

\[
W(f)=Df_0\oplus Df_0=a_f I,
\]

so they commute with the canonical quarter-turn. Centrality then additionally requires that these typed continuations generate the completed observable algebra and that the physical quarter-turn loop is admitted.

The moving-exchange formula does not discharge generator completeness or admission of the quarter-turn as an observable-algebra element.

### Composite synchronization

Before quotienting,

\[
S_A^1\times S_B^1\cong S_{\mathrm{diag}}^1\times S_{\mathrm{rel}}^1.
\]

Paper 5 v1.7 gives an exact dichotomy:

1. a completed witness for the relative circle makes it an additional physical relative-orientation record; or
2. no completed witness makes the relative circle operationally null, so closed-world quotienting leaves the diagonal complex action and the composite factors through `A_A tensor_C A_B`.

This is stronger and more physical than a bare sign-cocycle statement. The existing cocycle/double-cover frontier check remains useful as the network consistency schema; the v1.7 dichotomy supplies the event-level witness/null criterion that decides whether synchronization is licensed.

## 6. Tensor-composition reconciliation

The two Paper 5 supplements substantially reduce this lane.

### v1.7

If the relative orientation circle is operationally null, the product is balanced over the common central `j`:

\[
(j_Aa)\boxtimes b=a\boxtimes(j_Bb),
\]

and factors through the complex tensor product.

### v6.14

Closed finite composite completeness with no hidden boundary debt implies:

- finite tensor closure;
- finite tomographic locality;
- zero-defect product accounting.

For the product-record map

\[
\Pi_{AB}:V_A\otimes_{\mathbb R}V_B\to V_{AB},
\]

zero-defect composition requires both

\[
\ker\Pi_{AB}=0,
\qquad
\operatorname{coker}\Pi_{AB}=0,
\]

plus order-unit preservation.

### Revised status

The generic matrix-unit calculation in `zipper_reduction_frontier.py` is an independent exact model check, not the physical tensor theorem. The physical burden is now most cleanly expressed as:

1. closed finite same-type composite;
2. no hidden boundary debt;
3. zero kernel and cokernel after APF-null quotienting;
4. order-unit preservation;
5. relative-orientation witness/null classification;
6. common-orientation balancing when the relative circle is null.

## 7. Complete-positivity reconciliation

Paper 5 v6.14 supplies the correct logical direction:

1. upstream transformations are finite affine/order-preserving maps of the certified ordered record theory;
2. after the complex matrix gate, a physical channel must be **extension-stable**;
3. extension-stability means `T tensor id_B` preserves positivity, normalization/order unit, quotient ideals, and record-locking constraints for every certified ancilla, or a generating ancilla family with closure;
4. in the matrix representation, extension-stability is complete positivity and normalization preservation is trace preservation;
5. Kraus and Stinespring forms are downstream representation theorems, not the physical premise.

Therefore the frontier package's dilation/Kraus/Choi computation must be read as an exact downstream witness and negative-control suite. It may not replace the extension-stability gate with an assumed dilation.

The remaining physical CP surface is:

- certified same-type ancilla/reference family;
- tensor-faithful identity extension;
- joint positivity and quotient-ideal preservation;
- record-lock/cost preservation under extension;
- normalization preservation;
- a closure proof if only a generating ancilla family is tested.

## 8. Born reconciliation

Paper 5 v6.14 already states the finite conditional endpoint:

\[
\mathcal A_Q\simeq\bigoplus_k M_{n_k}(\mathbb C),
\]

with normalized positive states represented by density matrices, effects by positive operators, and

\[
\omega(E)=\sum_k p_k\operatorname{Tr}(\rho_kE_k),
\]

reducing to `Tr(rho E)` in an irreducible sector.

The arbitrary-`n` trace-uniqueness check in the frontier module is therefore best billed as:

- an independent exact regression of the finite trace functional;
- a compact executable cross-check of cyclicity and normalization;
- not a new physical derivation of the Born rule.

The physical Born leaves remain the actual realization and completeness of the state/effect/readout package, including score linearity/cyclicity, contextual effect identity, finite measurement normalization, and the relevant tomography/sandwich gates.

The coherent-hold economics does not close this seam. `G-hold-exact`—that what is held is what feeds exact selection at commitment—is explicitly granted rather than derived, and APF's own record-side analysis says the grant may be permanently unverifiable after commitment.

## 9. Action-scale reconciliation

Neither Paper 5 supplement derives the numerical value of `hbar`.

The v6.14 supplement uses `hbar` downstream in the quantum master equation, transition frequencies, field normalization, and the Einstein-A coefficient. Those formulas are consistency checks after the scale is supplied; they are not an APF derivation of the action quantum.

The zipper frontier conclusion therefore stands:

\[
\theta=S/\hbar
\]

fixes only a dimensionless phase. The simultaneous rescaling

\[
(S,\hbar)\mapsto(cS,c\hbar)
\]

is invisible to the local geometry. One dimensional action calibration remains.

## 10. Empirical moving-frame reconciliation

Paper 5 v1.7 provides a strong definition of the quantum-capable coherent sector. A first empirical census should test the v1.7 L1–L5 surface together with the moving-exchange-specific bridge:

1. actual record-free co-availability and a later non-null recombination witness;
2. path connectedness within an unsaturated fixed stratum;
3. completion-faithful rank-two first-order bipolar response;
4. admitted loops and reverses with no record/export leakage;
5. smooth represented action;
6. reconstruction of at least two distinct operational exchange frames on the same positive carrier;
7. verification that their local derivative produces the same orientation as the observed holonomy quarter-turn.

Static, discrete-jump, rank-changing, exporting, and record-forming branches remain valid non-moving controls.

## 11. Revised dependency order

The crosswalk recommends the following noncircular order:

\[
\text{admissibility-event clearance / physical co-availability}
\]

\[
\Downarrow
\]

\[
\text{QAC-type record incompatibility and noncommutative branch}
\]

\[
\Downarrow
\]

\[
\text{rank-two positive Held carrier + moving operational exchange}
\]

\[
\Downarrow
\]

\[
T_{\mathrm{zipper\ local\ }J}
\]

\[
\Downarrow
\]

\[
\text{naturality / centrality / orientation synchronization}
\]

\[
\Downarrow
\]

\[
\text{zero-defect finite complex composite}
\]

\[
\Downarrow
\]

\[
\text{extension-stable CPTP dynamics and finite Born representation}.
\]

The following reverse uses are forbidden:

- Born weighting to justify the Held carrier;
- complete positivity to justify coherence or recombination;
- complex tensor composition to synchronize the local orientation that it consumes;
- the v1.7 canonical quarter-turn formula to self-certify the moving-exchange construction;
- observed quantum behavior to infer the universal occupancy premise without the declared admissibility-event bridge.

## 12. What this crosswalk changes in the audit disposition

### Strengthens

- identifies exact prior Paper 5 hypotheses matching four of the five zipper gates;
- provides a prior event-level orientation synchronization dichotomy;
- replaces a generic CP-dilation narrative with the extension-stability gate;
- establishes that finite tensor and Born mathematics are already substantially present in Paper 5;
- sharpens the empirical moving-frame census to the L1–L5 coherent branch.

### Reduces

- any novelty claim for the existence of a quarter-turn or full `SO(2)` local holonomy;
- any novelty claim for finite complex tensor, CP, or Born mathematics;
- any suggestion that the current papers derive occupancy or `G-hold-exact`;
- any suggestion that `hbar` is fixed by the Paper 5 dynamics formulas.

### Retains as genuine zipper delta

- the pointwise invariant formula `J proportional to dot(tau) tau`;
- exact metric covariance and orientation-sign control;
- stationary, indefinite, bad-tangent, and higher-rank falsifiers;
- a proposed route for reducing Paper 5's smooth-circle hypotheses to a directly reconstructible moving comparison frame;
- the admissibility-event program's attempt to derive, rather than merely assume, the occupied record-kernel in context-sensitive interfaces.

## 13. May-not-cite fence

This crosswalk may not be cited for:

- unconditional physical occupancy of the coherent hold;
- unconditional discharge of v1.7 L1–L5;
- proof that every smooth holonomy path is generated by moving operational exchanges;
- proof that the positive ledger metric is derived from bare APF primitives;
- universal orientation synchronization;
- arbitrary physical tensor equality without zero-defect accounting;
- universal extension-stability of reduced events;
- unconditional Born weighting in nature;
- derivation of the numerical value of `hbar`;
- theorem-bank closure.

## 14. Audit questions created by the reconciliation

1. Does the operational comparison structure in v1.7 canonically supply a differentiable reflection family `tau(s)`, or only a connected `SO(2)` holonomy action?
2. Can the moving-exchange formula replace the full-circle argument for local `J` while leaving v1.7 naturality and centrality downstream unchanged?
3. Is the v1.7 positive ledger form independently derived, or should the residual-Hessian/closed-loop metric lane remain a named prerequisite?
4. Can the admissibility-event clearance theorem discharge the co-availability part of v1.7 L1 without importing `G-hold-exact`?
5. In composite synchronization, what finite protocol decides whether `S_rel^1` has a completed witness?
6. Can v6.14's zero-kernel/zero-cokernel product-record criterion be turned into the physical tensor-faithfulness certificate consumed by the CP gate?
7. Should the CP frontier be rewritten around extension-stability, with the existing Kraus/Choi code retained only as downstream representation checks?
8. Which Born leaves remain genuinely independent after importing the zipper metric and Paper 5's finite robust-query quotient?
