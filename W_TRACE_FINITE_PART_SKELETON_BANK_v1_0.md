# W_TRACE Finite-Part Skeleton Bank v1.0

Status: `[P_w_finite_part_skeleton]`.

This layer adds a typed symbolic component algebra for the eight W-route finite-part slots after the v9.5 evaluator gate. It is deliberately symbolic: it names the finite functions, checks the dependency graph, declares terminal `Delta_r_symbolic_sum`, and forbids observed-W or target-fitted leaves.

Closed here: symbolic shell for all eight finite-part components; acyclic component dependency graph; terminal symbolic-sum codomain; source-filled non-W numeric leaves inherited from the constants ledger; APF-anchor `Delta_r` barred as a component/symbolic input; observed `M_W`, W residuals, and tuned counterterms barred as inputs.

Still open: independent numerical loop/counterterm finite parts; covariance and uncertainty propagation; component-sum certificate; physical W/on-shell transport; physical scheme masses.
