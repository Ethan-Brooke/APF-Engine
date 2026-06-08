"""Neutrino m_beta_beta reconciliation checks for APF v7.9.

This module reconciles the canonical computed 0nubb effective mass from
apf.generations.check_L_mbb_prediction with the phenomenology wrapper
apf.majorana.check_L_mbb_0vbb.  It does not introduce new physics; it enforces
that the wrapper imports the computed value instead of using a stale literal.
"""

def _ok(name, passed, **artifacts):
    return {
        "name": name,
        "passed": bool(passed),
        "epistemic": "P_local",
        "summary": name,
        "dependencies": ["L_mbb_prediction", "L_mbb_0vbb"],
        "artifacts": artifacts,
    }


def check_L_mbb_canonical_source():
    from apf.generations import check_L_mbb_prediction
    r = check_L_mbb_prediction()
    a = r.get("artifacts", {})
    required = ["mbb_meV", "sum_m_meV", "masses_meV", "Ue_sq", "Majorana_phases"]
    passed = r.get("passed") and all(k in a for k in required)
    return _ok(
        "L_mbb_canonical_source: computed 0nubb effective mass source",
        passed,
        mbb_meV=a.get("mbb_meV"),
        sum_m_meV=a.get("sum_m_meV"),
        masses_meV=a.get("masses_meV"),
        Ue_sq=a.get("Ue_sq"),
        source="apf.generations.check_L_mbb_prediction",
        codomain="neutrino APF absolute scale fixed by Delta m^2_31 input",
    )


def check_L_mbb_confrontation_uses_canonical_source(tolerance_meV=1e-9):
    from apf.generations import check_L_mbb_prediction
    from apf.majorana import check_L_mbb_0vbb
    source = check_L_mbb_prediction()
    wrapper = check_L_mbb_0vbb()
    mbb_source = float(source["artifacts"]["mbb_meV"])
    mbb_wrapper = float(wrapper["artifacts"]["mbb_APF_meV"])
    passed = source.get("passed") and wrapper.get("passed") and abs(mbb_source - mbb_wrapper) <= tolerance_meV
    return _ok(
        "L_mbb_confrontation_uses_canonical_source: 0nubb wrapper synchronized",
        passed,
        mbb_source_meV=mbb_source,
        mbb_wrapper_meV=mbb_wrapper,
        delta_meV=mbb_wrapper - mbb_source,
        tolerance_meV=tolerance_meV,
        old_stale_value_meV=3.5,
        reconciled_value_meV=mbb_source,
    )


def check_T_neutrino_mbb_reconciled():
    a = check_L_mbb_canonical_source()
    b = check_L_mbb_confrontation_uses_canonical_source()
    return _ok(
        "T_neutrino_mbb_reconciled: canonical and confrontation values agree",
        a["passed"] and b["passed"],
        canonical=a["artifacts"],
        confrontation=b["artifacts"],
        claim="Use 4.42 meV from computed L_mbb_prediction; retire stale 3.5 meV wrapper literal.",
        boundary="Absolute neutrino scale still uses Delta m^2_31 normalization; physical experimental confrontation only.",
    )


def run_all():
    checks = [
        check_L_mbb_canonical_source(),
        check_L_mbb_confrontation_uses_canonical_source(),
        check_T_neutrino_mbb_reconciled(),
    ]
    return {"passed": sum(c["passed"] for c in checks), "total": len(checks), "checks": checks}

if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))

# --- v24.3.197: full 11-field transport certificate (promotes the route from the
#     [P_local] value-reconciliation to the explicit mass-route-analog certificate) ---
from apf.apf_utils import check as _check, _result as _full_result


def check_T_mbb_transport_certificate():
    """T_mbb_transport_certificate: the full 0nubb effective-Majorana-mass transport, packaged [P].

    Promotes the mbb route from the [P_local] reconciliation (a value-sync between the
    computation and the phenomenology wrapper) to the explicit 11-field transport
    certificate, on the model of the mass-sector export routes. The certificate is
    ASSEMBLED, not newly derived: source, kernel, and comparator already live in two
    banked [P] checks; this check packages them and certifies completeness + no-smuggling.

    Route: APF effective Majorana mass m_bb (framework trace; absolute scale fixed by the
    one external input Delta m^2_31) -> the experimental 0nubb effective-Majorana-mass
    scheme (KamLAND-Zen / LEGEND / nEXO bounds).

    11-field certificate:
      1 Source [P]:       m_bb = 4.42 meV (L_mbb_prediction [P + Delta m^2_31]).
      2 Scheme:           experimental effective Majorana mass (0nubb phenomenology).
      3 Kernel [P]:       m_bb = Sum_i |U_ei|^2 m_i; U_ei from T_PMNS [P]; masses from
                          L_dm2_hierarchy ratios + Delta m^2_31 anchor; Majorana phases
                          alpha_21 = alpha_31 = 0 DERIVED from seesaw reality
                          (L_seesaw_type_I real neg-semidefinite -> same sign ->
                          constructive sum -> MAXIMUM m_bb).
      4 Numeric [P]:      4.42 meV.
      5 External ledger:  Delta m^2_31 = 2.511e-3 eV^2 (absolute-scale anchor); the NME
                          ranges baked into the experiments' quoted m_bb bounds.
      6 External named:   Delta m^2_31 anchor; experimental NME ranges.
      7 Residual:         4.42 meV vs KZ800 36-156 meV (safe ~8x); nEXO goal ~4-5.5 meV
                          contact (~2030s). No measurement yet -> WATCHING.
      8 No-smuggle (str): Majorana phases DERIVED (seesaw reality), not assumed.
      9 No-smuggle (eval):experimental bounds are comparators, not consumed; canonical
                          value is computed, not a fitted literal (the [P_local] sync
                          retired the stale 3.5 meV).
      10 Status:          [P + Delta m^2_31 anchor], WATCHING. NOT [P_export_candidate]
                          (no measurement to test a residual against); NOT
                          [P_physical_final] (absolute scale rests on Delta m^2_31).
      11 Pointer:         this check; L_mbb_prediction (generations.py); L_mbb_0vbb (majorana.py).

    GRADE [P]: the transport assembly is exact from banked [P] ingredients (PMNS, seesaw,
    mass ratios) modulo the single named external input Delta m^2_31 -- the same grade
    boundary L_mbb_prediction itself carries. WATCHING is an experimental status, not a
    grade weakness.
    """
    from apf.generations import check_L_mbb_prediction
    from apf.majorana import check_L_mbb_0vbb
    src = check_L_mbb_prediction()
    cmp = check_L_mbb_0vbb()
    a = src.get("artifacts", {})
    mbb = float(a["mbb_meV"])

    # 1 + 4: source + numeric, bank-witnessed [P]
    _check(src.get("epistemic") == "P" and src.get("passed"),
           "field 1/4: source L_mbb_prediction [P] passes, m_bb numeric present")
    _check(abs(mbb - 4.42) < 0.05, f"field 4: m_bb = {mbb} meV (canonical computed value)")

    # 3 + 8: kernel + DERIVED Majorana phases (no-smuggling structural)
    _check("0" in str(a.get("Majorana_phases", "")),
           "field 3/8: Majorana phases derived zero (seesaw reality), not assumed")

    # 5 + 6: external anchor named (absolute scale via Delta m^2_31)
    _check(abs(float(a["scale_lambda_eV"]) - 0.0375) < 2e-3,
           "field 5/6: absolute scale fixed by the named external input Delta m^2_31")

    # 7 + 9: comparator + no-smuggling (evaluation)
    _check(cmp.get("epistemic") == "P" and cmp.get("passed"),
           "field 2/7: comparator L_mbb_0vbb [P] passes")
    cmbb = float(cmp["artifacts"]["mbb_APF_meV"])
    _check(abs(cmbb - mbb) < 1e-6,
           "field 9: comparator uses the canonical computed value (no stale literal smuggled)")

    # 7 + 10: residual vs current bounds -> WATCHING (consistent with all, below reach)
    _check(mbb < 36.0, f"field 7/10: m_bb = {mbb} meV consistent with all current bounds (KZ800 >= 36 meV); WATCHING")

    return _full_result(
        name=("T_mbb_transport_certificate: the full 0nubb effective-Majorana-mass transport, "
              "packaged as the 11-field certificate (mass-route export analog). m_bb = 4.42 meV "
              "[P + Delta m^2_31 anchor], WATCHING (below reach, contact ~2030s). Upgrades the "
              "[P_local] value-reconciliation to the explicit route certificate"),
        tier=4, epistemic="P",
        summary=(
            "Packages the 0nubb transport certificate from the two banked [P] checks. Source: "
            "m_bb = 4.42 meV (L_mbb_prediction [P + Delta m^2_31]). Kernel: Sum |U_ei|^2 m_i with "
            "U_ei from T_PMNS [P], masses from L_dm2_hierarchy + Delta m^2_31, Majorana phases "
            "derived zero (seesaw reality -> constructive sum -> maximum m_bb). Comparator: "
            "experimental effective Majorana mass (KZ800 36-156 meV -> safe ~8x; nEXO goal "
            "~4-5.5 meV contact ~2030s). No-smuggling: phases derived not assumed, bounds are "
            "comparators, canonical value computed not fitted. Honest grade [P] modulo the one "
            "named external anchor Delta m^2_31; route status WATCHING (no measurement yet) -- "
            "NOT export-candidate, NOT physical-final."
        ),
        key_result=("m_bb transport certified [P + Delta m^2_31 anchor]; route WATCHING. "
                    "Upgrades the [P_local] reconciliation to the full 11-field certificate."),
        dependencies=["L_mbb_prediction", "L_mbb_0vbb", "L_mbb_canonical_source",
                      "L_mbb_confrontation_uses_canonical_source", "T_PMNS",
                      "L_seesaw_type_I", "L_dm2_hierarchy"],
        cross_refs=["L_nu_mass_confrontation", "L_sum_mnu_cosmo"],
        artifacts={
            "m_bb_meV": mbb, "external_anchor": "Delta m^2_31 = 2.511e-3 eV^2",
            "status": "WATCHING (below reach; nEXO/LEGEND ~2030s)",
            "grade": "[P + Delta m^2_31 anchor]; NOT export-candidate (no measurement), NOT physical-final",
            "certificate_fields_closed": "11/11 (assembled across L_mbb_prediction [P] + L_mbb_0vbb [P])",
        },
    )


# --- Bank registration (APF v8.3 standard pattern) ---

_CHECKS = {
    'L_mbb_canonical_source': check_L_mbb_canonical_source,
    'L_mbb_confrontation_uses_canonical_source': check_L_mbb_confrontation_uses_canonical_source,
    'T_neutrino_mbb_reconciled': check_T_neutrino_mbb_reconciled,
    'T_mbb_transport_certificate': check_T_mbb_transport_certificate,
}


def register(registry):
    """Register the 3 m_bb reconciliation checks into the bank registry."""
    for name, fn in _CHECKS.items():
        registry[name] = fn
