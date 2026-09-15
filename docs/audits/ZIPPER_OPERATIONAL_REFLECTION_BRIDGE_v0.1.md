# APF Zipper Reduction — Operational Reflection Realization Bridge v0.1

**Status:** unbanked audit candidate; no theorem-bank, registry, census, version, or export changes  
**Branch:** `audit/zipper-reduction-v0.1`  
**Module:** `apf/zipper_reflection_bridge.py`  
**Tests:** `tests/test_zipper_reflection_bridge.py`

## 1. Purpose

The local zipper formula

\[
A=\frac12\dot\tau\tau,
\qquad
J=\frac{A}{\sqrt{-\frac12\operatorname{tr}(A^2)}}
\]

is exact once a differentiable non-stationary metric reflection \(\tau(s)\) is physically realised on a positive rank-two Held plane.

This packet decomposes that physical premise:

1. why an effective binary Held exchange is a reflection on the completion-faithful common/defect carrier;
2. when a record-neutral coherent-loop path turns that reflection into a conjugation orbit whose derivative reconstructs the Paper 5 holonomy generator.

The packet certifies exact finite algebra and countermodels only. It does not certify the physical leaves.

## 2. Port exchange gives the operational reflection

Let the two co-available Held ports be exchanged by

\[
P=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Let the completion-faithful zipper retain common and defect response:

\[
F=\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad
(c,d)^T=F(a,b)^T.
\]

Then

\[
\boxed{
\tau_0=FPF^{-1}
=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
}
\]

The exchange fixes the common line, reverses the defect line, squares to the identity, and is self-adjoint and isometric for the induced metric

\[
g_{cd}=F^{-T}F^{-1}=\frac12 I.
\]

This becomes physical only when the port exchange is an admitted record-neutral continuation and the defect survives the complete operational quotient.

### Defect-killing control

The total-only readout

\[
S(a,b)=a+b
\]

has rank one and satisfies \(SP=S\). Thus the raw swap descends to the identity when the defect is killed. A nominal label swap is not an operational reflection.

### Static-effect control

The projectors

\[
E_\pm=\frac12(I\pm\tau_0)
\]

may exist algebraically while the physical process set is only \(\{I\}\). Static effect completeness does not imply dynamic exchange availability.

## 3. Conjugated exchange recovers the holonomy generator

Let \(U(s)\) be a record-neutral, export-free coherent-loop path and let

\[
K=\dot U U^{-1}.
\]

Transport the operational reflection actively:

\[
\tau(s)=U(s)\tau_0U(s)^{-1}.
\]

Then

\[
\dot\tau=[K,\tau]
\]

and therefore

\[
\boxed{
\frac12\dot\tau\tau
=\frac12\left(K-\tau K\tau\right).
}
\]

Moving-exchange data reconstruct the component of \(K\) that anticommutes with the current reflection.

On a positive oriented real two-plane, coherent holonomy has \(K\in\mathfrak{so}(2)\), and every metric reflection reverses the oriented generator:

\[
\tau K\tau=-K.
\]

Hence

\[
\boxed{
\frac12\dot\tau\tau=K=\dot U U^{-1}.
}
\]

The zipper formula is therefore the normalized infinitesimal Paper 5 holonomy generator.

### Active/passive sign fence

The packet fixes

\[
\tau=U\tau_0U^{-1}.
\]

The passive convention \(\tau=U^{-1}\tau_0U\) reverses the sign. Global orientation synchronization remains separate.

### Commuting-transport control

If \([K,\tau_0]=0\), then \(\dot\tau=0\) even when \(K\ne0\). Therefore \(A=K\) requires the positive rank-two isometric holonomy condition; otherwise only the anti-commuting projection is recovered.

## 4. Exact live 3–4–5 transported-exchange witness

The packet reproduces

\[
F_{345}=\frac15
\begin{pmatrix}-1&7\\7&1\end{pmatrix},
\qquad
\det F_{345}=-2.
\]

Transporting the effective binary port exchange gives

\[
S_u=F_{345}PF_{345}^{-1}
=\frac1{25}
\begin{pmatrix}-7&24\\24&7\end{pmatrix}.
\]

Together with \(S_0=\operatorname{diag}(1,-1)\),

\[
R=S_uS_0
=\frac1{25}
\begin{pmatrix}-7&-24\\24&-7\end{pmatrix},
\]

with

\[
\det R=1,
\qquad
\operatorname{tr}R=-\frac{14}{25}.
\]

This shows that a second physically realised binary Held presentation supplies a second reflection without assuming that every sharp projector is dynamically implementable.

If the second exchange is label-only and dies in the operational quotient, its represented image is \(I\), and the rotation disappears.

## 5. Physical premise surface

The bridge remains conditional on:

1. `BINARY_HELD_PRESENTATION_REALIZED`;
2. `EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE`;
3. `COMPLETION_FAITHFUL_DEFECT_QUOTIENT`;
4. `EXCHANGE_LEDGER_NEUTRALITY`;
5. `SAME_TYPE_RETURN`;
6. `RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH`;
7. `POSITIVE_LEDGER_ISOMETRY`;
8. `FIRST_ORDER_FAITHFUL_ACTION`;
9. `NONTRIVIAL_CONJUGATION_ORBIT`;
10. `FIXED_RANK_TWO_HELD_STRATUM`.

The broad premise `PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY` is forbidden. Only targeted effective binary exchange paths are used.

## 6. Relation to Paper 5

Paper 5 v1.7 supplies the conditional whole-circle route

\[
\text{occupied coherent component}
\to SO(2)\to J.
\]

The present bridge supplies the local differential identification

\[
\tau=U\tau_0U^{-1}
\quad\Longrightarrow\quad
\frac12\dot\tau\tau=\dot U U^{-1}
\]

on the positive rank-two branch.

The routes agree only when the comparison reflection, its effective quotient action, and its record-neutral conjugation orbit are physically realised on the same carrier.

The bridge does not discharge occupancy, the positive ledger metric, path connectedness, naturality, centrality, global orientation, tensor, CP, Born, or \(\hbar\) gates.

## 7. Exact checks

- `T_effective_port_exchange_is_operational_reflection`: exact port-to-common/defect conjugation, induced metric, defect-killing quotient, and static-effect/process separation.
- `T_conjugated_exchange_orbit_recovers_holonomy_generator`: exact identity \(A=(K-\tau K\tau)/2=K\) on a rational rotation family, passive-sign control, and commuting-transport control.
- `T_live_345_zipper_transports_second_exchange`: exact \(F_{345}\), transported reflection \(S_u\), and trace \(-14/25\) rotation, with label-only control.
- `T_operational_reflection_bridge_dependency_contract`: rejects effect saturation, label-only action, assumed quarter-turn or \(SO(2)\), Hilbert/Born/complex smuggling, cycles, and gate drift.

## 8. May-not-cite fence

This packet may not be cited for physical occupancy, physical realization of either binary presentation, admission of the port exchanges or 3–4–5 intertwiner, existence of the smooth record-neutral path, positivity of the ledger, global orientation synchronization, or theorem-bank/export closure.

The strongest licensed statement is:

> On a physically realised completion-faithful binary Held presentation, an effective record-neutral port exchange is exactly a common/defect reflection. If a positive rank-two record-neutral coherent holonomy path conjugates that reflection, the moving-exchange generator equals the infinitesimal holonomy generator and the zipper normalization recovers the same local complex structure.

## 9. Reproduction

```bash
python -m compileall -q apf/zipper_reflection_bridge.py
python -m apf.zipper_reflection_bridge
python -m pytest -q tests/test_zipper_reflection_bridge.py
```

The parent workflow also runs the original zipper and downstream-frontier certificates and confirms that the canonical theorem bank remains unchanged.
