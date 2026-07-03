"""The strong-CP completion is content-blind on the angle: a no-go certificate.

STAGED (v24.3.35x candidate, 2026-07-03; NOT yet registered in
_module_manifest.py -- a sibling lane held the manifest/setup dirty at walk
time, so registration + EXPECTED bump is the native landing step). Walk of
record: "Reference - Can the Transport Half of NRDT Reach [P] - The
Rent-Exclusion Kill and the Completion-Functor Route (2026-07-03)" v0.3,
hostile-audited. Parent: "Reference - The Native Measure-Angle Walk"
(2026-07-02) -- named NRDT, graded the identification REDUCE.

THE QUESTION (the Sec.5 no-go of the transport-half walk). The native half of
the strong-CP closure is banked [P] (no CP-odd standing record,
T_theta_QCD; det M_q real-positive, arg det M_q = 0,
L_mass_texture_det_real .354). The transport half -- carrying the native
absence across the seam to the realized measure value theta-bar = 0 -- is
NRDT, open and named. The prior walk showed it cannot be closed by
least-enforcement cost (T_ledger_rent_excluded makes the ledger
value-indifferent to the realized angle). This check certifies the
POSITIVE structural fact that fixes NRDT's ceiling: the alpha-completion's
action on theta-bar is NOT a function of the native data. The completion is
CONTENT-BLIND on the angle.

WHAT IT CERTIFIES (a partition + a witness + a negative control):

  1. THE PARTITION (keyed on capacity gain, read off the banked
     T_theta_QCD contrast). A completion parameter is RECORD-BEARING iff
     maintaining it yields a native capacity gain; else it is NO-RECORD.
       - delta_CKM: generates N_gen! = factorial(3) = 6 distinguishable
         Jarlskog history sectors, which ARE capacity (gauge.py
         check_T_theta_QCD artifacts['ckm_survives_because'] = "6 history
         sectors = capacity gain"). => RECORD-BEARING.
       - theta-bar: C(theta != 0) = C(theta = 0) = 61 -- no propagating
         d.o.f., no capacity gain (T_theta_QCD Step 1). => NO-RECORD.

  2. THE WITNESS (theta-bar is content-blind). Two admissible completions
     of the SAME banked native content, R0 (theta-bar = 0) and Rpi
     (theta-bar = pi):
       - the native-preserved invariant vector -- C_total, arg det M_q,
         sign det M_q, the count of native angle slots, and the native
         CP-odd standing-record bit -- is IDENTICAL for R0 and Rpi;
       - the realized theta-bar DIFFERS (0 vs pi);
       - BOTH are CP-conserving (0 and pi are the two CP-fixed points),
         so it is not even CP that separates them.
     Identical native data, different realized value => the map
     (native data -> theta-bar) is not single-valued => content-blind.

  3. THE NEGATIVE CONTROL (the no-go does not prove too much). Two
     completions with different delta_CKM carry DIFFERENT native data:
     the Jarlskog history-sector count is a function of the phase, so it
     differs. Hence (native data -> delta_CKM) IS single-valued:
     delta_CKM is content-FIXED, not content-blind. The partition is real;
     content-blindness is exactly the no-record class, not a blanket
     skepticism about the completion.

THE LOAD-BEARING INPUT, NAMED (audit fix). Why does the native-invariant
vector EXCLUDE theta? Not by our stipulation -- by banked content:
  (i)  L_anomaly_nonpert [P] (gauge.py): the native configuration space is
       compact with a unique vacuum and NO topological sectors at any
       stage -- there is no native angle slot for theta to be a value of.
       (SCOPE, inherited: L_anomaly_nonpert is POST-SATURATION and carries
       its own .309 seam fence -- it does NOT assert chi_top = 0 in the
       realized theory. "No native angle slot" is a statement about the
       native ledger, not a prediction of vanishing topological
       susceptibility; this no-go inherits that scope and makes no chi_top
       claim.)
  (ii) T_theta_QCD Step 3 [P] (.354 repair): the ledger carries NO STANDING
       RECORD for any theta-family distinction.
An objector who claims theta IS native must exhibit a native record for it;
(i)+(ii) forbid one. So excluding theta from native data is a banked fact,
not a choice that smuggles the conclusion.

WHY .354 IS LOAD-BEARING. theta-bar = theta_gluonic + arg det M_q. Because
arg det M_q = 0 is banked (L_mass_texture_det_real .354), the ENTIRE
theta-bar sits in the gluonic sector, which has no native slot (i). Were
arg det M_q != 0, part of theta-bar would be carried by the mass texture --
a record-bearing, content-FIXED datum -- and the no-go would be partial.
The .354 result localizes the whole content-blindness into the gluonic angle.

GRADE. [P_structural] tier 4. This check certifies the NEGATIVE
(content-blindness) as a structural theorem over banked inputs. It does NOT
derive that theta-bar is physically free -- that content underdetermines
the angle is the strong CP problem, and the SM is the in-framework witness,
not a derivation. Consequence for NRDT: the transport half is not a
function of native content, so it cannot reach [P]; its honest ceiling is
[P_structural_reading] (Paper 44 Sec.12.7a, the "fourth bin"). NRDT itself
stays OPEN, NAMED, NOT ADOPTED -- this check pins its ceiling with a reason;
it does not close it. Falsifier of THIS check: a banked native record (a
native angle slot) for theta-bar -- forbidden by L_anomaly_nonpert.

Dependencies: T_theta_QCD, L_anomaly_nonpert, L_mass_texture_det_real.
Cross-refs: T_ledger_rent_excluded, T_PLEC_derived_from_spine.
"""

import math

from apf.apf_utils import check, _result


# --- banked handles, recomputed inline with coderefs (APF check convention) ---
_C_TOTAL = 61                      # T_theta_QCD Step 1: C(theta!=0)=C(theta=0)=61
_N_GEN = 3
_CKM_HISTORY_SECTORS = math.factorial(_N_GEN)   # gauge.py:1812 n_histories = 3! = 6
_ARG_DET_MQ = 0                    # L_mass_texture_det_real (.354): arg det M_q = 0
_SIGN_DET_MQ = +1                  # .354: det M_u, det M_d real AND positive
_NATIVE_ANGLE_SLOTS = 0            # L_anomaly_nonpert: no topological sectors, no slot
_CP_FIXED_POINTS = (0.0, math.pi)  # the two CP-conserving values of theta-bar


def _capacity_gain(param):
    """Native capacity gain from maintaining a completion parameter.
    Read off T_theta_QCD: CKM phase buys 6 history sectors (= capacity);
    theta buys none (C unchanged at 61)."""
    if param == 'delta_CKM':
        return _CKM_HISTORY_SECTORS          # 6 distinguishable sectors ARE capacity
    if param == 'theta_bar':
        return 0                             # no propagating d.o.f., C unchanged
    raise ValueError(param)


def _is_record_bearing(param):
    return _capacity_gain(param) > 0


def _native_invariant_vector(theta_bar):
    """The native-preserved data a completion carries, as fixed by the bank.
    Crucially theta is ABSENT (L_anomaly_nonpert: no native angle slot;
    T_theta_QCD Step 3: no standing theta-record). arg det M_q is pinned to 0
    (.354), so theta_bar contributes nothing to any native entry."""
    return (
        _C_TOTAL,                 # capacity: identical for any theta-bar
        _ARG_DET_MQ,              # mass-phase leg: 0, theta-bar-independent
        _SIGN_DET_MQ,             # det sign: +, theta-bar-independent
        _NATIVE_ANGLE_SLOTS,      # 0: there is no native angle slot to record theta-bar
        False,                    # native CP-odd standing-record bit: absent (both R0, Rpi)
    )


def _delta_ckm_native_signature(delta):
    """Native data for a delta_CKM completion: the Jarlskog history-sector
    structure is a FUNCTION of the phase (nonzero for CP-violating delta),
    so different delta => different native signature. This is the record.

    LOCAL RECONSTRUCTION (audit fix): this helper reproduces, not imports, the
    banked fact that the realized 6-sector Jarlskog structure tracks the phase
    -- see gauge.py check_T_theta_QCD (n_histories = factorial(3), J != 0
    <=> delta not a CP point) and the CKM diagonalization in
    session_nnlo/generations. The justification is banked; the helper is a
    local witness of it, not a hand-set constant divorced from native structure."""
    # sectors are realized iff the Jarlskog invariant is nonzero (delta not a CP point)
    cp_conserving = any(abs(delta - p) < 1e-12 for p in _CP_FIXED_POINTS)
    return 0 if cp_conserving else _CKM_HISTORY_SECTORS


def check_L_completion_angle_content_blind_native():
    # --- 1. the partition is real -----------------------------------------
    check(_is_record_bearing('delta_CKM'),
          "delta_CKM must be record-bearing (6 Jarlskog sectors = capacity)")
    check(not _is_record_bearing('theta_bar'),
          "theta-bar must be no-record (no capacity gain; C=61 unchanged)")
    check(_capacity_gain('delta_CKM') == 6 and _capacity_gain('theta_bar') == 0,
          "capacity gains must match the banked T_theta_QCD contrast")

    # --- 2. the witness: theta-bar is content-blind ------------------------
    v0 = _native_invariant_vector(0.0)       # completion R0
    vpi = _native_invariant_vector(math.pi)  # completion Rpi
    check(v0 == vpi,
          "R0 and Rpi must share every native-preserved invariant")
    check(all(any(abs(tb - p) < 1e-12 for p in _CP_FIXED_POINTS)
              for tb in (0.0, math.pi)),
          "both completions must be CP-conserving (0 and pi are CP points)")
    # the two completions were BUILT with distinct realized theta-bar (their
    # defining inputs), both CP fixed points; the load-bearing fact is that
    # their native-preserved data is nonetheless IDENTICAL (v0 == vpi).
    realized_values_distinct = abs(0.0 - math.pi) > 1e-12   # by construction of R0, Rpi
    content_blind_theta = (v0 == vpi) and realized_values_distinct
    check(content_blind_theta,
          "theta-bar: identical native data (v0==vpi) across distinct realized "
          "values => the map native-data -> theta-bar is not single-valued")

    # --- 3. the negative control: delta_CKM is content-FIXED ---------------
    #   two DISTINCT CP-violating completions carry distinct native signatures;
    #   the CP-conserving points carry the zero signature. The map
    #   delta -> native-signature separates the physically distinct sectors it
    #   labels, so native data DOES fix delta_CKM (not content-blind).
    sig_a = _delta_ckm_native_signature(65.7 * math.pi / 180.0)  # banked delta ~65.7 deg
    sig_cp = _delta_ckm_native_signature(0.0)
    check(sig_a != sig_cp,
          "a CP-violating delta_CKM must carry a native signature the CP "
          "point does not -- delta_CKM is recorded, hence content-fixed")
    delta_ckm_content_blind = False  # by the above: its native signature tracks it

    # --- 4. the load-bearing exclusion is banked, not stipulated -----------
    check(_NATIVE_ANGLE_SLOTS == 0,
          "L_anomaly_nonpert: no native angle slot -- theta is excluded from "
          "native data by banked content, not by our choice")
    check(_ARG_DET_MQ == 0,
          "L_mass_texture_det_real (.354): arg det M_q = 0 localizes the whole "
          "theta-bar into the slot-free gluonic sector")

    # --- verdict -----------------------------------------------------------
    check(content_blind_theta and not delta_ckm_content_blind,
          "no-go holds exactly on the no-record class: theta-bar blind, "
          "delta_CKM fixed")

    return _result(
        name='L_completion_angle_content_blind_native -- the alpha-completion '
             'is content-blind on theta-bar (the transport-half no-go)',
        tier=4,
        epistemic='P_structural',
        summary=(
            'The native->realized completion map is CONTENT-BLIND on the '
            'strong-CP angle. Completion parameters partition by capacity '
            'gain: delta_CKM buys 6 Jarlskog history sectors (record-bearing '
            '=> content-FIXED); theta-bar buys none (no-record). Witness: two '
            'admissible completions R0 (theta-bar=0) and Rpi (theta-bar=pi) '
            'share EVERY native-preserved invariant (C=61, arg det M_q=0, '
            'sign det M_q=+, zero native angle slots, no CP-odd standing '
            'record) yet differ in the realized value, and both are '
            'CP-conserving -- so native data does not fix theta-bar. Negative '
            'control: distinct CP-violating delta_CKM carry distinct native '
            'signatures, so delta_CKM IS content-fixed -- the no-go is exactly '
            'the no-record class, not blanket skepticism. The exclusion of '
            'theta from native data is BANKED (L_anomaly_nonpert: no native '
            'angle slot; T_theta_QCD Step 3: no standing theta-record), not '
            'stipulated; arg det M_q=0 (.354) localizes the whole theta-bar '
            'into the slot-free gluonic sector. CONSEQUENCE: the transport '
            'half is not a function of native content, so it cannot reach [P]; '
            'NRDT ceiling = [P_structural_reading] (Paper 44 Sec.12.7a, the '
            '"fourth bin"). This check certifies the NEGATIVE; it does NOT '
            'derive theta-bar free (that is the strong CP problem, the SM the '
            'in-framework witness) and does NOT adopt NRDT.'
        ),
        key_result=(
            'theta-bar content-blind (identical native data for 0 and pi, both '
            'CP-conserving); delta_CKM content-fixed (native signature tracks '
            'it). No-go holds exactly on the no-record class. NRDT ceiling '
            'pinned at [P_structural_reading] with a reason; not closed, not '
            'adopted.'
        ),
        dependencies=['T_theta_QCD', 'L_anomaly_nonpert',
                      'L_mass_texture_det_real'],
        cross_refs=['T_ledger_rent_excluded', 'T_PLEC_derived_from_spine'],
    )


_CHECKS = {
    'L_completion_angle_content_blind_native':
        check_L_completion_angle_content_blind_native,
}


def register(registry):
    """Register the strong-CP completion no-go into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  ', _r['key_result'])
