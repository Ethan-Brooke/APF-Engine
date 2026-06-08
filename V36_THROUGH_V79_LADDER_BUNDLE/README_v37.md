# APF v37 — Top MSR Scale-Selection Theorem

This package extends the v35 Trace-to-Scheme Export Theorem and the v36 derivation of G1--G6 from APF.

New closure:

\[
m_t^{\rm APF\text{-}TRACE}\to m_t^{\rm MSR}(R_\star),\qquad R_\star=85.86\,\mathrm{GeV}.
\]

The scale selector is APF-native:

\[
R_\star={1\over2}\left(T_t+{3\over68}T_W\right).
\]

It uses APF trace anchors and integer route counts only.  It does not use external top pole, MC, MSbar, MSR, PDG, or world-average top data.

Run:

```bash
python3 scripts/check_top_msr_scale_selection_v37.py
```

Expected stamp:

```text
TOP_MSR_SCALE_SELECTION_THEOREM_PASS
```
