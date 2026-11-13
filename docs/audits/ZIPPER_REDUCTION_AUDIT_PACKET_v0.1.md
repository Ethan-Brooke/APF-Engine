# APF Zipper Reduction — Audit Packet v0.1

**Status:** audit candidate; not banked; no registry or census changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Module:** `apf/zipper_reduction.py`  
**Tests:** `tests/test_zipper_reduction.py`

## 1. Claim under audit

Let \((E,g)\) be a realised positive real two-dimensional Held-event plane. Let
\(\tau(s)\) be a differentiable family of metric-self-adjoint involutions representing the operational comparison frame:

\[
\tau^2=I,
\qquad
\tau^{\dagger_g}=\tau,
\qquad
\tau^{\dagger_g}\tau=I.
\]

For a non-stationary frame define

\[
A=\frac12\dot\tau\,\tau,
\qquad
\omega=\sqrt{-\frac12\operatorname{tr}(A^2)},
\qquad
J=\frac{A}{\omega}.
\]

The candidate theorem is:

\[
\boxed{
J^2=-I,
\qquad
J^{\dagger_g}=-J,
\qquad
g(Ju,Jv)=g(u,v).
}
\]

The normalization is equivalently

\[
\boxed{
J=
\frac{\frac12\dot\tau\tau}
{\sqrt{-\frac12\operatorname{tr}\left[\left(\frac12\dot\tau\tau\right)^2\right]}}.
}
\]

The formula is scoped to a **positive rank-two** event carrier. It is undefined for a stationary comparison frame and is not asserted as a canonical higher-rank construction.

## 2. Exact proof skeleton represented in code

Differentiating \(\tau^2=I\) gives

\[
\dot\tau\tau+\tau\dot\tau=0.
\]

Therefore

\[
A=\frac12\dot\tau\tau
\]

is skew-adjoint relative to \(g\). On a positive real two-plane, every nonzero skew-adjoint endomorphism has the form \(A=\omega J\), where \(\omega>0\) and \(J^2=-I\). The trace formula computes \(\omega\) without selecting coordinates.

The module verifies this on an exact rational tangent-half-angle family

\[
\tau(t)=R(t)S_0R(t)^T,
\]

with

\[
R(t)=\frac1{1+t^2}
\begin{pmatrix}
1-t^2&-2t\\
2t&1-t^2
\end{pmatrix},
\qquad
S_0=\operatorname{diag}(1,-1).
\]

For this family,

\[
\omega(t)=\frac{2}{1+t^2}
\]

and the normalized generator is exactly

\[
J=
\begin{pmatrix}
0&-1\\
1&0
\end{pmatrix}.
\]

## 3. Check inventory

### `T_moving_exchange_formula_exact`

Exact rational witness over seven parameter values. Checks:

- \(\tau^2=I\);
- metric orthogonality and self-adjointness;
- differentiated involution compatibility;
- \(A^{\dagger}=-A\);
- exact rational normalization;
- \(J^2=-I\);
- exact formula \(\omega=2/(1+t^2)\).

### `T_moving_exchange_metric_covariance`

Conjugates the construction into a non-Euclidean positive metric plane and verifies:

- \(J\mapsto QJQ^{-1}\);
- \(\omega\) is invariant;
- the result is not an artefact of Euclidean coordinates.

### `T_moving_exchange_orientation_sign`

Verifies:

- positive reparameterization speed leaves \(J\) unchanged;
- reversing the context orientation sends \(J\mapsto-J\);
- the local result therefore carries the expected orientation-sign ambiguity.

### `T_two_exchange_product_holonomy`

Checks that two distinct operational exchange frames are reflections whose product is a nontrivial orientation-preserving rotation. Each reflection anticommutes with \(J\), while their product commutes with \(J\).

### `T_zipper_formula_negative_controls`

Owns four sharp controls:

1. **stationary frame:** \(\dot\tau=0\), so no normalized generator exists;
2. **bad tangent:** \(\dot\tau\tau+\tau\dot\tau\neq0\);
3. **indefinite signature:** an \(O(1,1)\) moving reflection produces a negative normalization radicand and is rejected;
4. **rank-four unequal frequencies:** trace normalization does not yield \(J^2=-I\), fencing the elementary rank-two scope.

### `T_zipper_reduction_dependency_contract`

Pins the derivation order:

\[
\text{positive event metric}
+
\text{moving operational exchange}
\Longrightarrow
T_{\rm zipper\ local\ J}.
\]

The graph explicitly forbids the following upstream:

- Hilbert space;
- Born rule;
- complex scalars;
- operator positivity;
- connected \(SO(2)\) image;
- assumed quarter-turn.

Mutation controls own cycle insertion, Hilbert smuggling, direct-gate deletion, and direct-gate addition.

## 4. Physical premises named but not certified

The packet does **not** certify:

1. `ACTIVE_RECORD_KERNEL_REALIZED`;
2. `COMPLETION_FAITHFUL_RANK_TWO_QUOTIENT`;
3. `POSITIVE_EVENT_METRIC_REALIZED`;
4. `SMOOTH_NONSTATIONARY_OPERATIONAL_EXCHANGE_REALIZED`;
5. `RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH`.

These are the physical/categorical burden surface. The code certifies only the exact rank-two consequence once those gates obtain.

## 5. Falsifiers

The theorem packet is falsified by any of the following:

- a positive rank-two metric-self-adjoint involution path satisfying the differentiated involution identity for which the normalized formula does not obey \(J^2=-I\);
- a basis change with the induced metric that changes \(\omega\) or fails to send \(J\) to \(QJQ^{-1}\);
- a stationary frame accepted as defining a normalized \(J\);
- an indefinite-signature branch accepted as a positive complex structure;
- a higher-rank unequal-frequency carrier silently promoted by the rank-two constructor;
- dependency drift that imports Hilbert, Born, complex scalars, or an assumed quarter-turn upstream.

## 6. May-not-cite fence

This packet may **not** be cited for any of the following:

- that the zipper-clearance sector is physically occupied;
- that its first-order quotient is rank two;
- that its ledger form is positive;
- that the operational exchange frame varies smoothly or nontrivially;
- that local orientation signs synchronize globally;
- that the full physical image is \(SO(2)\);
- that Hilbert space, Born weighting, collapse dynamics, or quantum measurement is derived;
- that the candidate is banked.

The strongest allowed statement is:

> On a realised positive rank-two Held-event plane with a differentiable non-stationary metric exchange involution, the normalized moving-frame generator is an exact complex structure, with the expected orientation-sign ambiguity.

## 7. Audit questions

1. Is \(A=\frac12\dot\tau\tau\) the correct left/right convention for the intended transport orientation, or should the canonical convention be \(-\frac12\tau\dot\tau\)? The two coincide here but the sign convention must be fixed explicitly.
2. Does the physical exchange frame satisfy metric self-adjointness, or only metric orthogonality?
3. Is trace normalization the correct invariant frequency scale under every allowed rank-two basis change?
4. Is positivity truly upstream, or can a weaker compactness condition replace it without circularity?
5. Does the rank-two first-order carrier refer to the active defect-germ plane rather than the full common/defect pair carrier?
6. Is the orientation ambiguity correctly fenced from global synchronization?
7. Should this theorem live inside `held_holonomy`, `graded_orientation_closure`, or remain a separate zipper-reduction family?
8. Which exact banked gates, if any, already discharge part of the five physical premises?

## 8. Reproduction

```bash
python -m compileall -q apf/zipper_reduction.py
python -m apf.zipper_reduction
python -m pytest -q tests/test_zipper_reduction.py
```

The audit branch also runs the existing bank audit to confirm that the unregistered candidate does not perturb the canonical theorem bank:

```bash
python verify_all.py --bank-audit
```

## 9. Disposition sought

The desired audit disposition is one of:

- **LAND AS AUDIT CANDIDATE:** exact mathematics and fences are sound; physical premises remain named;
- **REDUCE:** formula sound, but theorem scope or dependency language is overbilled;
- **REVISE:** a repair is available without changing the core formula;
- **KILL:** a conclusion-breaking countermodel survives the declared premises.
