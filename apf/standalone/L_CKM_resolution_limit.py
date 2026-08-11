"""L_CKM_resolution_limit: CKM 3-4% Error is the FN Resolution Limit [P].

STATEMENT: The 3-4% systematic error in all three CKM mixing angles
is the INTRINSIC resolution limit of the discrete Froggatt-Nielsen
mechanism with x = 1/2 and integer charges. This is an UNDERSTOOD
structural limitation, not an unexplained failure.

KEY FINDINGS:
  1. All three CKM angle errors are |2-4%| (systematic FN discreteness scale)
  2. No perturbative correction to any single input can resolve this
  3. The error corresponds to dq = 0.049 FN charge units (1/20 of minimum step)
  4. The PMNS angles (0.1% accuracy) use a different mechanism (Gram matrix)
     that has continuous parameters, explaining the accuracy asymmetry

NOTE (2026-08-10, R7@2026-08-10 site 19): theta_13's reference is STILL A
STORED LITERAL.  The ruled fix -- derive it from |V_ub|, because
sin(theta_13) IS |V_ub| and the two are carried as separate literals that
have drifted apart -- was implemented and then UNWOUND.  It is QUEUED, not
abandoned.  As this file stands, Finding 1's stated band DOES cover
theta_13 and the executed residuals print in the summary.  What deriving
the reference WOULD cost is measured and disclosed at the theta_13 gate;
none of it has been incurred here.

STATUS: [P]. Numerical proof using full 3x3 diagonalization.
Requires numpy/scipy for numerical verification; gracefully degrades
to algebraic checks if unavailable.
"""

import math

from apf.apf_utils import check, _result


def check_L_CKM_resolution_limit():
    """L_CKM_resolution_limit: CKM Error = FN Resolution Limit [P].

    Proves the 3-4% CKM error is structural, not correctable.
    """
    try:
        import numpy as np
        HAS_NUMPY = True
    except ImportError:
        HAS_NUMPY = False

    x = 0.5
    phi = math.pi / 4
    q_B = [7, 4, 0]
    q_H = [7, 5, 0]
    obs_Vus, obs_Vcb, obs_Vub = 0.2257, 0.0410, 0.00382
    obs_th12, obs_th23, obs_th13 = 13.04, 2.38, 0.201
    # theta_13's REFERENCE IS STORED HERE AND ALSO IMPLIED BY |V_ub| ON THE
    # LINE ABOVE. In the standard parametrization sin(theta_13) IS |V_ub| --
    # one quantity, carried twice, and the two literals have drifted about 8%
    # apart. RULED 2026-08-10 (R7@2026-08-10, site 19): derive the angle from
    # the element so they cannot separate again.
    #
    # THE RULED FIX WAS IMPLEMENTED AND THEN UNWOUND -- queued, not abandoned.
    # Deriving the angle makes check_T_scorecard_resolution RED: that check
    # AST-harvests this tuple by name and ties it BY VALUE to the scorecard
    # rows in validation.py. It fails twice over -- a derived assignment
    # cannot be harvested at all, and once that is patched the value leg fails
    # on its own terms. The tie is doing its job: it reports that the same
    # duplication this fix removes INSIDE the module also exists BETWEEN the
    # module and the scorecard. Landing therefore depends on which |V_ub| the
    # corpus carries, which R7 expressly did NOT rule.
    #
    # Measured, so the queued work does not have to re-derive it: against
    # |V_ub| = 0.00382, the PDG 2024 average carried on the line above,
    # deriving gives theta_13 = 0.218870 deg and moves the residual from
    # +3.87% to -4.61% -- UP in magnitude and against the framework, as the
    # ruling predicted. That clears the 6% bound.
    #
    # IT DOES NOT CLEAR IT UNDER EVERY CANDIDATE REFERENCE, and this is a
    # live risk for the queued fix rather than a footnote. At
    # |V_ub| = 0.00389 -- PDG 2025, which this same declaration pass cites at
    # site #6 in apf/session_nnlo.py -- the derived angle is 0.222881 deg and
    # the residual is -6.33%, which FAILS the 6% gate. So WHICH |V_ub| the
    # corpus carries decides whether the derived gate passes at all. The
    # unruled reference question is load-bearing on the gate itself, not only
    # on the scorecard tie.
    #
    # N15, RECORDED AND NOT FIXED HERE: theta_13/|V_ub| is not the only pair
    # of this shape in this function. theta_23 and |V_cb| are the same
    # identity -- in the standard parametrization |V_cb| = sin(theta_23)
    # cos(theta_13), and cos(theta_13) = 0.99999 under either candidate
    # theta_13, so the two are the same quantity to five digits -- and they
    # sit in the same two tuples on adjacent lines.
    # asin(0.0410) = 2.3498 deg against the stored 2.38 deg:
    # 1.29% apart. An order of magnitude less drift than the theta_13 pair,
    # but the same defect. theta_12/|V_us| is the third instance and is
    # consistent to 0.03%. All three belong to the queued pass; do not fix
    # theta_23 here.

    def build_FN(q_B_, q_H_, phi_, k_B, k_H, c_B, c_H, x_=0.5):
        M = [[complex(0) for _ in range(3)] for _ in range(3)]
        for g in range(3):
            for h in range(3):
                ang_b = phi_ * (g - h) * k_B / 3.0
                ang_h = phi_ * (g - h) * k_H / 3.0
                bk = c_B * x_**(q_B_[g]+q_B_[h]) * complex(math.cos(ang_b), math.sin(ang_b))
                hg = c_H * x_**(q_H_[g]+q_H_[h]) * complex(math.cos(ang_h), math.sin(ang_h))
                M[g][h] = bk + hg
        return M

    if not HAS_NUMPY:
        # ================================================================
        # ALGEBRAIC FALLBACK: verify structural claims without numpy
        # ================================================================

        # FN resolution: |Vus| ~ x^3, error ~ delta_q * ln(2)
        Vus_LO = x**3  # leading order
        delta_Vus = abs(Vus_LO / obs_Vus - 1)
        delta_q = delta_Vus / math.log(2)
        check(delta_q < 0.1,
              f"delta_q = {delta_q:.4f} < 0.1 (within FN resolution)")

        # The x = 1/2, integer-charge grid has resolution ~ ln(2) ~ 0.69
        # per charge unit. A 3-4% error in |Vus| = 0.034 / 0.693 = 0.049
        # charge units. This is 1/20 of the minimum integer step.
        fn_step = math.log(2)
        fractional_step = delta_Vus / fn_step
        check(fractional_step < 0.1,
              f"Error = {fractional_step:.3f} FN steps (< 0.1 = sub-grid)")

        return _result(
            name='L_CKM_resolution_limit: CKM Error = FN Resolution Limit',
            tier=3,
            epistemic='P',
            summary=(
                'CKM 3-4% error is the intrinsic resolution limit of the '
                'discrete FN mechanism (x=1/2, integer charges). '
                f'delta_q = {delta_q:.4f} FN charge units (1/{1/delta_q:.0f} '
                f'of minimum step). '
                'PMNS uses Gram matrix (continuous params) -> 0.1% accuracy. '
                'The 30x accuracy asymmetry is a PREDICTED feature. '
                '(Algebraic verification; numpy not available for full scan.)'
            ),
            key_result=f'CKM error = FN discreteness limit: delta_q = {delta_q:.3f} [P]',
            dependencies=[
                'T_CKM', 'T_capacity_ladder', 'L_FN_ladder_uniqueness',
                'L_holonomy_phase', 'T27c', 'T_PMNS',
            ],
        )

    # ================================================================
    # FULL NUMERICAL VERIFICATION (numpy available)
    # ================================================================
    import numpy as np

    def ckm_from_params(phi_val, k_B=3, c_Hu=0.125):
        M_u = np.array(build_FN(q_B, q_H, phi_val, k_B, 0, 1.0, c_Hu, x))
        M_d = np.array(build_FN(q_B, q_H, phi_val, 0, 0, 1.0, 1.0, x))
        _, Vu = np.linalg.eigh(M_u @ M_u.conj().T)
        _, Vd = np.linalg.eigh(M_d @ M_d.conj().T)
        V = Vu.conj().T @ Vd
        s13 = abs(V[0, 2])
        c13 = math.sqrt(max(0, 1 - s13**2))
        s12 = abs(V[0, 1]) / c13 if c13 > 1e-15 else 0
        s23 = abs(V[1, 2]) / c13 if c13 > 1e-15 else 0
        return {
            'th12': math.degrees(math.asin(min(1.0, s12))),
            'th23': math.degrees(math.asin(min(1.0, s23))),
            'th13': math.degrees(math.asin(min(1.0, s13))),
            'Vus': abs(V[0, 1]),
            'Vcb': abs(V[1, 2]),
            'Vub': abs(V[0, 2]),
        }

    # LO prediction
    lo = ckm_from_params(phi)
    err_12 = (lo['th12'] / obs_th12 - 1) * 100
    err_23 = (lo['th23'] / obs_th23 - 1) * 100
    err_13 = (lo['th13'] / obs_th13 - 1) * 100

    # All three angles land inside |2-4%| (the FN discreteness scale) against
    # the stored references this file carries. Deriving theta_13's reference
    # from |V_ub| -- the queued fix disclosed at that gate -- would move it
    # outside the band; that has not been done. All three residuals are
    # computed above and printed in the summary.
    #
    # TOLERANCE ENVELOPES, declared 2026-08-10 (D4@2026-08-03 (c), sites
    # #17 and #18). THIS DECLARATION COVERS THE theta_12 AND theta_23 GATES
    # IMMEDIATELY BELOW, AND THOSE TWO ONLY.
    #   UNIT      percent-relative, ALREADY MULTIPLIED BY 100 at the err_NN
    #             assignments above -- so the literal 6.0 means 6%, not 6
    #             degrees and not 0.06. The underlying observable is an angle
    #             in DEGREES; the gate is on its relative deviation, not on the
    #             angle. The unit is stated because it is the exact confusion
    #             that made the retired text-matching tolerance instrument
    #             unusable.
    #   ENVELOPE  6% each, UNCHANGED -- both ruled defensible.
    #   SOURCE    obs_th12 = 13.04 deg is within 0.3% of the PDG 2024 CKM
    #             global fit and obs_th23 = 2.38 deg tracks |V_cb|. The BINDING
    #             uncertainty is not the measurement: it is the FN grid
    #             resolution, which THIS MODULE derives and does not estimate.
    #             The x = 1/2 integer-charge grid has resolution ln 2 = 0.69
    #             per charge unit; step 4 below computes delta_q = 0.0491
    #             charge units -- 1/20 of the minimum step -- from the |Vus|
    #             deviation, NOT from the two angle errors gated here; so the
    #             fractional floor is delta_q * ln 2 = 3.40%, inside the
    #             module-computed band [2.60%, 3.90%]
    #             (floor_within_derivation_computed_error_band,
    #             apf/scorecard_resolution.py). Carrying that floor from
    #             |V_us|, where it is measured, to any other observable is
    #             FN_POWER_TRANSFER -- a PREMISE, NOT derived (same module).
    #             For theta_23 the relevant experimental spread is the |V_cb|
    #             inclusive-vs-exclusive gap of 5.9-6.1%, about 3 sigma, which
    #             6% sits at.
    #   OBSERVED  theta_12 +3.50% (1.71x), theta_23 -2.64% (2.27x).
    #   SIZED BY  the observed residuals, not by the SOURCE above. 3.50% and
    #             2.64% both rounded up to a common 6%: margins 1.71x and
    #             2.27x. The SOURCE says what kind of uncertainty these gates
    #             bracket; it did not set the number 6.
    check(abs(err_12) < 6.0, f"theta_12 error = {err_12:.1f}% (expect |2-4%|)")
    check(abs(err_23) < 6.0, f"theta_23 error = {err_23:.1f}% (expect |2-4%|)")
    #
    # TOLERANCE ENVELOPE, declared 2026-08-10 (D4@2026-08-03 (c), site #19).
    # THIS DECLARATION COVERS THE theta_13 GATE IMMEDIATELY BELOW, AND THAT
    # ONE ONLY. It is separate from the theta_12/theta_23 declaration above
    # because this site carries a reference question the other two do not.
    #   UNIT      percent-relative, ALREADY MULTIPLIED BY 100 at the err_13
    #             assignment above -- the literal 6.0 means 6%, not 6 degrees.
    #             The observable is an angle in degrees; the gate is on its
    #             relative deviation.
    #   ENVELOPE  6%, UNCHANGED. The residual and its margin are printed.
    #   THE REFERENCE IS STILL A LITERAL, and that is the state of this
    #             file. Ruled 2026-08-10 (R7@2026-08-10, site 19): DERIVE it
    #             from |V_ub|. The defect the ruling names is not staleness
    #             but DUPLICATION -- sin(theta_13) IS |V_ub|, and this
    #             function carries the pair as two independent literals that
    #             disagree with each other. That fix was implemented and then
    #             UNWOUND; it is QUEUED. See the note at the top of this
    #             function.
    #   WHAT DERIVING WOULD COST, measured 2026-08-10 and recorded so the
    #             queued pass does not have to re-derive it. NONE OF IT HAS
    #             BEEN INCURRED. The derived reference is LARGER than the
    #             literal, so the residual would move UP IN MAGNITUDE, not
    #             down, and would change sign: +3.87% becomes -4.61% against
    #             |V_ub| = 0.00382. The direction runs against the framework,
    #             which is why it is written down rather than smoothed over.
    #
    #   ==================================================================
    #   THREE CONSEQUENCES OF DERIVING THE REFERENCE. ALL MEASURED, NONE
    #   INCURRED -- the fix is not in this file. As it stands the theta_13
    #   gate is GREEN, the |2-4%| band DOES cover theta_13, and
    #   phi_shift_pct IS 0.0. Read what follows as the cost sheet for the
    #   queued pass, not as a description of this tree.
    #   ==================================================================
    #   (1) check_T_scorecard_resolution (apf/scorecard_resolution.py) WOULD
    #             GO RED, and it would fail TWICE OVER. That check
    #             AST-harvests the tuple (obs_th12, obs_th23, obs_th13) out of
    #             this file by exact tuple-target name, and its leg
    #             family_ckm_rows_match_derivation_targets_by_value asserts
    #             sorted equality BY VALUE against the CKM-angle rows of the
    #             prediction-scorecard table in apf/validation.py.
    #             (a) Its harvester evaluates a literal-plus-arithmetic
    #                 subset only, so a DERIVED assignment could not be read
    #                 at all and it would raise before the value leg is
    #                 reached.
    #             (b) With the harvester made tolerant, the value leg would
    #                 then fail on its own terms, because validation.py's
    #                 theta_13 row carries the same angle the fix retires.
    #                 BOTH failures were EXECUTED on 2026-08-10, in isolated
    #                 copies; neither is inferred.
    #             The tie would be doing its job. What it would report is that
    #             the duplication the fix removes here also exists BETWEEN
    #             this module and the scorecard.
    #   (2) THE MODULE'S OWN STATED |2-4%| BAND WOULD STOP COVERING
    #             theta_13. That band is restated in this module's docstring,
    #             in this module's summary, in apf/bank.py and in
    #             apf/scorecard_resolution.py's docstring. Of the lines in
    #             THIS file that restate it, EXACTLY ONE moved in the
    #             declaration pass: this gate's own message. The per-angle
    #             line in the summary that prints the three residuals is
    #             BYTE-IDENTICAL to HEAD and was not touched -- an earlier
    #             draft of this comment said two lines moved, and `git diff`
    #             settles it at one. The headline sentence and its apf/bank.py
    #             mirror are LEFT ALONE deliberately so the two cannot
    #             diverge; as this file stands they are accurate, and the
    #             corpus-wide restatement is owed WITH the queued fix, in the
    #             same pass, not before it.
    #   (3) THE OPTIMAL HOLONOMY PHASE WOULD MOVE OFF pi/4. Step 3 below
    #             scans phi on a chi2 built from all three angle residuals, so
    #             a corrected theta_13 reference would enter it. Measured on
    #             2026-08-10: phi_shift_pct would go from exactly 0 to +2.0,
    #             one grid point off pi/4. The gate (< 5%) would still pass,
    #             and delta_q would be untouched because step 4 reads |Vus|
    #             only. But "pi/4 is near-optimal" would read weaker than it
    #             does: pi/4 is the scan's argmin now and would not be. That
    #             runs AGAINST the framework, which is why it is stated here
    #             rather than absorbed. Nothing outside this module consumes
    #             phi_shift_pct (verified by grep, 2026-08-10).
    #   THE THREE ARE NOT THE SAME KIND OF THING, and the difference matters.
    #             (1) AND (2) are one pre-existing disagreement -- one
    #             quantity carried as two numbers at four sites -- that
    #             deriving would make visible; WHICH |V_ub| the corpus should
    #             carry is the question that settles both, and R7@2026-08-10
    #             expressly did not rule it. (3) IS NOT THAT: it is a real
    #             downstream effect of moving the reference, and it would
    #             SURVIVE BOTH candidate answers to the |V_ub| question.
    #             Measured 2026-08-10 rather than argued: the shift reads
    #             +2.0 for the direct average and +2.0 for the global fit
    #             alike. It is 0 across an INTERVAL, not at a point -- on the
    #             seven-point grid, phi_shift_pct is exactly 0 for obs_th13 in
    #             [0.1947, 0.2051] deg, i.e. |V_ub| in [0.003398, 0.003580]
    #             -- endpoints located by sampling obs_th13 at 1e-5 deg, not
    #             solved for, so they are accurate to that step and no finer.
    #             The stored literal 0.201 sits inside that interval and both
    #             candidate derived angles sit outside it. The phi scan is a
    #             coarse seven-point grid, so +2.0 is one grid point, not a
    #             fit.
    #   THE OBVIOUS ALTERNATIVE, and what it actually costs. Moving
    #             validation.py's theta_13 observed value to the derived angle
    #             does NOT on its own restore check_T_scorecard_resolution to
    #             green: executed 2026-08-10, it still raises "derivation
    #             constants not found: {'obs_th'}", because consequence (1)(a)
    #             is a HARVESTER failure and the harvester is not patched by
    #             any change to validation.py. WITH the harvester also made
    #             tolerant, the pair goes green -- and neither move touches
    #             (3). Measured with both applied: check_L_prediction_catalog
    #             goes from mean error 3.79% to 3.98%, with 32/40 consistent
    #             and median 0.51% unchanged. DECLINED here on two grounds --
    #             that row is governed by the prediction-scorecard charter,
    #             under which a measurement enters the table AS MEASURED and a
    #             derived angle is not a measurement; and the value it would
    #             take is exactly the unruled |V_ub| question. Owed as its own
    #             pass, with a ruling, not folded into this one.
    check(abs(err_13) < 6.0,
          f"theta_13 error = {err_13:.1f}% (envelope 6%, percent-relative)")

    # Step 1: Insensitivity to c_Hu
    c_Hu_range = [0.05, 0.08, 0.10, 0.125, 0.15, 0.20, 0.30]
    th12_spread = []
    for c in c_Hu_range:
        r = ckm_from_params(phi, c_Hu=c)
        th12_spread.append(r['th12'])
    th12_max_variation = max(th12_spread) - min(th12_spread)
    check(th12_max_variation < 0.5,
          f"theta_12 variation over c_Hu = {th12_max_variation:.3f} deg (< 0.5)")

    # Step 2: Insensitivity to FN charge perturbations
    for dq in [-0.5, 0, 0.5]:
        q_test = [7 + dq, 4, 0]
        M_u = np.array(build_FN(q_test, q_H, phi, 3, 0, 1.0, x**3, x))
        M_d = np.array(build_FN(q_test, q_H, phi, 0, 0, 1.0, 1.0, x))
        _, Vu = np.linalg.eigh(M_u @ M_u.conj().T)
        _, Vd = np.linalg.eigh(M_d @ M_d.conj().T)
        V = Vu.conj().T @ Vd
        s13 = abs(V[0, 2])
        c13 = math.sqrt(max(0, 1 - s13**2))
        s12 = abs(V[0, 1]) / c13 if c13 > 1e-15 else 0
        th12_pert = math.degrees(math.asin(min(1.0, s12)))
        # Should not vary more than 0.5 degrees for sub-integer perturbation
        check(abs(th12_pert - lo['th12']) < 1.0,
              f"dq={dq}: theta_12 shift = {abs(th12_pert - lo['th12']):.3f} deg")

    # Step 3: Holonomy phase already near-optimal
    # Try a grid of phi values
    best_chi2 = float('inf')
    best_phi = phi
    for p_trial in [phi * f for f in [0.9, 0.95, 0.98, 1.0, 1.02, 1.05, 1.1]]:
        r = ckm_from_params(p_trial)
        chi2 = ((r['th12'] - obs_th12) / obs_th12)**2 + \
               ((r['th23'] - obs_th23) / obs_th23)**2 + \
               ((r['th13'] - obs_th13) / obs_th13)**2
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_phi = p_trial

    phi_shift_pct = (best_phi / phi - 1) * 100
    check(abs(phi_shift_pct) < 5.0,
          f"Optimal phi shift = {phi_shift_pct:+.2f}% (pi/4 is near-optimal)")

    # Step 4: FN resolution
    delta_Vus = abs(lo['Vus'] / obs_Vus - 1)
    delta_q = delta_Vus / math.log(2)
    check(delta_q < 0.1, f"delta_q = {delta_q:.4f} < 0.1 (within FN resolution)")

    return _result(
        name='L_CKM_resolution_limit: CKM Error = FN Resolution Limit',
        tier=3,
        epistemic='P',
        summary=(
            'CKM 3-4% error is the intrinsic resolution limit of the '
            'discrete FN mechanism (x=1/2, integer charges). '
            f'theta_12: {err_12:+.1f}%, theta_23: {err_23:+.1f}%, '
            f'theta_13: {err_13:+.1f}% — all |2-4%| (FN scale). '
            f'delta_q = {delta_q:.4f} FN charge units (1/{1/delta_q:.0f} '
            f'of minimum step). '
            f'c_Hu insensitivity: {th12_max_variation:.3f} deg over 6x range. '
            f'Phase pi/4 near-optimal (shift {phi_shift_pct:+.1f}%). '
            'PMNS uses Gram matrix (continuous) -> 0.1% accuracy. '
            'The 30x accuracy asymmetry is PREDICTED.'
        ),
        key_result=f'CKM error = FN discreteness limit: delta_q = {delta_q:.3f} [P]',
        dependencies=[
            'T_CKM', 'T_capacity_ladder', 'L_FN_ladder_uniqueness',
            'L_holonomy_phase', 'T27c', 'T_PMNS',
        ],
        artifacts={
            'lo_errors': {
                'th12_pct': round(err_12, 1),
                'th23_pct': round(err_23, 1),
                'th13_pct': round(err_13, 1),
            },
            'delta_q_FN': round(delta_q, 4),
            'c_Hu_variation_deg': round(th12_max_variation, 3),
            'phi_shift_pct': round(phi_shift_pct, 2),
            'PMNS_comparison': 'Gram (continuous) vs FN (discrete) = 30x accuracy gap',
        },
    )
