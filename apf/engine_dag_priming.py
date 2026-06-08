"""APF Engine DAG-priming helper.

Architecture-only utility. Added v24.3.41 per Fourth Law Step D audit Finding 2.

The framework's strict no-fallback policy refuses silent substitution of canonical
defaults for upstream capacity-derivation outputs (e.g. ``acc_SM`` requires the
DAG cache key ``C_total`` populated by ``L_count`` in ``apf/gauge.py`` + ``d_eff``
populated by ``L_self_exclusion`` in ``apf/gravity.py``). Under the canonical
``verify_all`` module-loading order this populates correctly. But standalone
callers — including the engine pipeline's ``interface_solver_descent_bridge``
when it is extended to certify ACC unification — must explicitly prime the
chain or hit ``RuntimeError: acc_SM: DAG key 'C_total' is missing``.

This module exposes ``prime_dag_cache_for(top_check_name)`` which runs the
named prerequisite chain before the consumer evaluates the top check. The
priming map is data-driven and extensible; new top checks register their
prerequisites here rather than relying on implicit module-load order.

This is correct audit-first discipline preservation, not a fallback. The
prerequisites are CALLED, not substituted with defaults. The no-silent-fallback
policy in ``acc_SM`` etc remains intact.

Architecture-only — no ``register()``, no ``check_*`` functions. The module is
imported by engine-pipeline consumers when they need to evaluate a top check
that has named upstream-DAG requirements.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


# Map: top-check-name -> ordered sequence of prerequisite-check names that must
# run first to populate the DAG cache. The prerequisite chain is what
# verify_all already does naturally via module-load order; this map exposes
# the same dependency information in a callable form for ad-hoc consumers.
#
# Per Fourth Law Step D audit Finding 2: three top theorems require explicit
# priming with L_count + L_self_exclusion.
PRIMING_MAP: Dict[str, Tuple[str, ...]] = {
    "I2_gauge_cosmological": ("L_count", "L_self_exclusion"),
    "T_ACC_unification": ("L_count", "L_self_exclusion"),
    "T_three_level_unification": ("L_count", "L_self_exclusion"),
}


def prerequisites_for(top_check_name: str) -> Tuple[str, ...]:
    """Return the prerequisite-check chain for a named top check.

    Returns an empty tuple if the top check has no known DAG-priming requirement.
    Consumers can call ``prime_dag_cache_for()`` if the tuple is non-empty.
    """
    return PRIMING_MAP.get(top_check_name, ())


def prime_dag_cache_for(
    top_check_name: str,
    registry: Mapping[str, object],
    *,
    raise_on_missing: bool = False,
) -> List[str]:
    """Run the prerequisite chain for ``top_check_name`` against ``registry``.

    Parameters
    ----------
    top_check_name:
        Name of the top check the caller intends to evaluate.
    registry:
        Mapping check-name -> callable. Typically ``apf.bank.REGISTRY``.
    raise_on_missing:
        If True, raise ``KeyError`` when a prerequisite is absent from the
        registry. If False (default), skip silently — appropriate during the
        pre-load phase where prerequisites may legitimately not be present yet.

    Returns
    -------
    List of prerequisite-check names that were actually called (in order).

    Notes
    -----
    This function CALLS the prerequisite checks — it does not substitute their
    outputs with canonical defaults. The audit-first no-fallback policy in
    ``apf/unification.py::acc_SM`` and similar remains intact.
    """
    prereqs = prerequisites_for(top_check_name)
    called: List[str] = []
    for name in prereqs:
        fn = registry.get(name) if hasattr(registry, "get") else None
        if fn is None:
            if raise_on_missing:
                raise KeyError(
                    f"prime_dag_cache_for: prerequisite '{name}' for top check "
                    f"'{top_check_name}' is not in the supplied registry."
                )
            continue
        # The prereq is a check function; call it. It populates DAG cache state
        # as a side effect of its evaluation.
        fn()
        called.append(name)
    return called


def prime_and_call(
    top_check_name: str,
    registry: Mapping[str, object],
) -> Dict[str, object]:
    """Prime the DAG cache for ``top_check_name`` then call the top check.

    Convenience wrapper. Returns the top check's result dict.

    Raises
    ------
    KeyError
        If ``top_check_name`` is not in ``registry``.
    """
    prime_dag_cache_for(top_check_name, registry)
    fn = registry[top_check_name] if hasattr(registry, "__getitem__") else None
    if fn is None:
        raise KeyError(f"prime_and_call: top check '{top_check_name}' not in registry")
    return fn()


def known_top_checks() -> Tuple[str, ...]:
    """Return all top-check names that have registered DAG-priming requirements."""
    return tuple(sorted(PRIMING_MAP.keys()))


def architecture_posture() -> Mapping[str, object]:
    """Public posture describing this module's role in the engine pipeline."""
    return {
        "module": "apf.engine_dag_priming",
        "version_added": "v24.3.41",
        "audit_finding_source": "Fourth Law Step D audit Finding 2 (APF_FOURTH_LAW_UNIFICATION_CLAIM_AUDIT_v1)",
        "classification": "ARCHITECTURE_ONLY",
        "purpose": "Exposes DAG-priming requirements for top checks that depend on upstream capacity derivations",
        "preserves_no_silent_fallback_policy": True,
        "prerequisite_chain_is_called_not_substituted": True,
        "registered_top_checks": list(PRIMING_MAP.keys()),
    }
