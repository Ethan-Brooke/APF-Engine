# APF v23.0 — Bottom MSbar Transport Route

Status: `BOTTOM_MSBAR_TRANSPORT_ROUTE_PASS`.

This sprint begins the colored-fermion trace-to-scheme program after EW sector closure.  It closes the bottom TRACE/MSbar validation neighborhood, target contract, pole knockout, and no-smuggling audit while keeping physical MSbar export gated by an explicit transport/codomain theorem.

## Core numerical state

\[
m_b^{\rm APF\text{-}TRACE}=4.177490455927\ {\rm GeV}.
\]

The PDG/pdgLive bottom listing gives

\[
\bar m_b(\bar m_b)_{\overline{\rm MS}}=4.183\pm0.007\ {\rm GeV}
\]

at quoted CL = 90%.  Therefore

\[
\Delta m_b = -5.509544\ {\rm MeV},
\]

or \(-0.787\) on the quoted PDG scale.  If the 90% CL interval is converted to a Gaussian one-sigma equivalent, the pull is \(-1.294\sigma\).  Both numbers are reported to avoid hiding the confidence-level convention.

## Claim boundary

Closed here:

\[
\boxed{m_b^{\rm APF\text{-}TRACE}:[P_{\rm validation}+P_{\rm MSbar\ route\ contract}]}
\]

Not closed here:

\[
\boxed{m_b^{\rm APF\to\overline{MS}}(m_b):[OPEN]}
\]

First failed gate:

`APF_TRACE_TO_MSBAR_CODOMAIN_IDENTITY_OR_QCD_TRANSPORT_MAP`.

Next route gate:

`BOTTOM_QCD_RUNNING_THRESHOLD_COVARIANCE_LEDGER`.

## Interpretation

The bottom TRACE value is short-distance-like and not pole-like.  The comparison to the PDG pole-mass context \(4.78\pm0.06\) GeV is displaced by roughly \(-10\sigma\), while the MSbar self-scale comparison is within a few MeV.  This supports bottom as the next clean physical-export candidate, but does not by itself prove that the APF_TRACE codomain is identical to \(\overline{\rm MS}\) at \(\mu=m_b\).
