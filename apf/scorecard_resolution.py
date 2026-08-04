"""scorecard_resolution: three scorecard statistics computed side by side.

Built 2026-08-04 by a fresh execution seat under the 2026-08-02 charter
"Reference - CHARTER - What the Prediction Scorecard Measures".  The seat
that found the question was barred from executing it because the change
plausibly moves the headline statistic in the framework's own favour.

AUDIT RECORD (all 2026-08-04): two mutually-blind cold audits,
LAND-WITH-FIXES 0.84 / 0.85, zero arithmetic disagreements, convergent
fixes carried same day by a separate fix seat (three-headline split with
the FN-power transfer premise named, discriminator witnessed both ways,
auxiliary headlines value-tied), auditors' escapes re-run CAUGHT; third
blinded cold audit LAND-WITH-FIXES 0.89.  Banked as v24.3.466
(2026-08-04).

ADOPTION RULED 2026-08-04 (Ethan): the headline stays 32/40 (banked check
and its zero-margin gate unchanged); the three-number table is presented
together wherever the scorecard appears; FN_POWER_TRANSFER is CHARTERED
as a derivation target, not adopted; the three surviving reds are
promoted to the named anomaly list (wiki/Open Problems.md 2026-08-04).

WHAT THIS MODULE COMPUTES (and nothing else):

1. The banked statistic, recomputed. The prediction rows are extracted from
   the banked source (`check_L_prediction_catalog`, apf/validation.py) by AST
   parse of its `predictions` literal — not re-typed — and the banked
   comparison sigma = |APF - obs| / sigma_obs is reproduced row by row. The
   recomputed headline (n_consistent / n_tested, mean, median) is compared BY
   VALUE against the artifacts returned by executing the banked check itself.
   The 3-sigma consistency threshold is AST-harvested from the banked source
   (the `sigma <= ...` comparison inside the banked check), not re-typed, and
   the same harvested value is the threshold on every statistic below.

2. THREE headline numbers, side by side:

   (a) BANKED: the banked statistic, reproduced as above.

   (b) LICENSED: sigma_eff = |APF - obs| / sqrt(sigma_obs^2 + sigma_model^2)
       with sigma_model nonzero ONLY for the three CKM theta rows — the rows
       the banked Froggatt-Nielsen grid-discreteness derivation
       (`check_L_CKM_resolution_limit`, apf/standalone/L_CKM_resolution_limit
       .py) actually computes. This is the derivation's computed scope.

   (c) EXTENDED: the same sigma_eff with sigma_model additionally applied to
       the six T_mass_ratios rows, carried under a NAMED PREMISE — the
       FN-power transfer premise (FN_POWER_TRANSFER in the premises
       artifact): that a pure-FN-power observable (proportional to x^q on
       the integer charge grid) inherits the grid's fractional resolution
       delta_q * ln 2, transferred from the Vus-derived measurement to the
       mass-ratio family. This is a premise, not derived; every
       extended-family per-row record carries it as conditional_on.

3. The floor, and what it is: sigma_model / |obs| = delta_q_FN * ln 2, and
   because the derivation defines delta_q = delta_Vus / ln 2, the ln 2
   round-trips — the floor is ALGEBRAICALLY IDENTICAL to delta_Vus, the
   derivation's own fractional miss on |Vus|. It is the derivation's
   measured residual promoted to a model resolution, NOT a grid-geometric
   quantity, and two different licenses carry the promotion: on the
   licensed CKM rows the license is the banked lemma's own stated
   conclusion (the 3-4% error IS the intrinsic resolution limit) —
   interpretive prose backed by the lemma's insensitivity scans, not a
   computed transfer; on the mass-ratio rows the license is the
   FN_POWER_TRANSFER premise. A leg computes the identity
   floor == delta_Vus by value from an independent FN diagonalization, and
   another leg computes the per-row minimum flip floors, recording that the
   outcome is floor-insensitive: every floor at or above the computed
   maximum (well below the derivation's own error band) flips the same
   five rows.

4. The family classification, computed from row identity, with the
   discriminating rule stated and witnessed BOTH ways: the licensed family
   is the pure-FN-power side of a two-mechanism split (pure-FN-power
   observable vs continuous-Gram observable). AST harvest witnesses that
   check_T_PMNS declares the Gram-route lemma L_Gram as a direct dependency
   while check_T_mass_ratios does not, and that T_mass_ratios declares the
   FN charge ladder T_capacity_ladder (kept as a secondary witness only:
   the harvest also records that T_PMNS declares the same T_capacity_ladder
   edge, so that anchor alone does not separate the two mechanisms). A leg
   proves by value that the CKM-angle rows' observed values are exactly the
   observed targets hardcoded in the derivation module (AST-extracted); the
   PMNS rows and the CP phase delta are outside every family. The family
   membership is additionally pinned set-exactly by name, and the
   post-floor red set and both changed-verdict sets are pinned by name and
   value.

5. Falsifiability, by value: the rows with sigma_eff above threshold are
   enumerated (a leg requires at least two such real rows and records
   their names); a clearly labeled SYNTHETIC control row inside the family,
   constructed with a fractional miss far above the floor, is shown to
   produce sigma_eff above threshold. The synthetic row is never counted
   in any headline. A leg also records that no real row has sigma_eff in
   the marginal gap (threshold, threshold + 1].

6. Auxiliaries, all value-tied and recorded: the linear-window variant
   (consistent iff |APF - obs| <= sigma_model + 3 sigma_obs, the natural
   reading if the floor is a hard discreteness window), recomputed through
   a second code path plus a hand-computed witness row; the extended
   headline recomputed at the floor-band edges read from the derivation's
   own executed artifacts (not from prose), through a second code path;
   and the one moving corner of the 2x2 sensitivity square (hard window
   evaluated at the band minimum), computed and recorded, including the
   name of the row that returns red there. The known outcome-neutral
   invariances on this data (linear equals quadrature at the exact floor;
   the quadrature headline is constant across the artifact band) are
   computed and recorded as facts, not assumed. Each auxiliary is
   computed with the floor on the extended family, so each is
   conditional on FN_POWER_TRANSFER exactly as the extended headline is;
   each carries that tag in the artifacts, and a leg checks the tags.

Numbers are computed and printed by the legs and the report; the docstring
deliberately carries none. This module does not modify, and its output does
not supersede, the banked scorecard; it computes the three statistics side
by side. Adoption of any of them as the headline is a separate ruling and
is not made here. Requires numpy (for the independent FN recomputation).
"""

import ast
import math
import os

__all__ = ['check_T_scorecard_resolution', 'main', 'register']


def _banked_source_paths():
    """Resolve the banked sources from the imported package itself, so the
    files AST-parsed here are the same files Python executes."""
    import apf.validation as _v
    import apf.standalone.L_CKM_resolution_limit as _r
    validation_py = os.path.abspath(_v.__file__)
    resolution_py = os.path.abspath(_r.__file__)
    return validation_py, resolution_py, os.path.dirname(validation_py)

EXPECTED_LEGS = frozenset([
    'rows_extracted_from_banked_source',
    'banked_headline_reproduced_n_consistent',
    'banked_headline_reproduced_mean_median',
    'threshold_harvested_and_tied_by_value',
    'floor_independent_recomputation_matches_banked_artifact',
    'floor_equals_derivation_Vus_residual_by_value',
    'floor_within_derivation_computed_error_band',
    'family_ckm_rows_match_derivation_targets_by_value',
    'family_discriminator_witnessed_both_ways',
    'family_mass_ratio_anchor_direct_dependency',
    'family_excludes_pmns_and_phase_rows',
    'derivation_contrast_names_the_excluded_mechanism',
    'family_split_set_exact',
    'family_rows_set_exact_by_name',
    'quadrature_identity_by_value',
    'floor_zero_outside_family_by_value',
    'licensed_headline_double_count',
    'extended_headline_double_count',
    'mean_median_unchanged_by_floor',
    'post_floor_red_set_pinned_by_value',
    'changed_verdict_sets_pinned_by_name',
    'floor_insensitivity_min_flip_floors',
    'real_rows_exceeding_three_sigma_eff_exist',
    'synthetic_control_goes_red',
    'linear_window_variant_tied_by_value',
    'sensitivity_band_headlines_tied_by_value',
    'window_at_band_edges_corner_computed',
    'premise_ledger_auxiliary_headlines_tagged',
])

# ---------------------------------------------------------------------------
# Pins. These are the module's own previously computed outputs, frozen by
# name and value. They are facts about the current banked catalog; if the
# catalog changes, they must be re-derived and the module re-audited.
# ---------------------------------------------------------------------------
FN_POWER_TRANSFER_PREMISE = (
    'FN_POWER_TRANSFER (premise, NOT derived): a pure-FN-power observable '
    '(proportional to x^q on the integer FN charge grid) inherits the '
    "grid's fractional resolution delta_q * ln 2, transferred from the "
    'Vus-derived measurement to the T_mass_ratios family. The EXTENDED '
    'headline, the linear-window / band-sensitivity / moving-corner '
    'auxiliaries and their computed invariances, and every '
    'extended-family per-row record are conditional on this premise.')

FAMILY_CKM_NAMES = frozenset(['θ₁₂_CKM (°)', 'θ₂₃_CKM (°)', 'θ₁₃_CKM (°)'])
FAMILY_MASS_RATIO_NAMES = frozenset([
    'm_d/m_s', 'm_d/m_b', 'm_s/m_b', 'm_e/m_μ', 'm_e/m_τ', 'm_μ/m_τ'])
RED_SET_PIN = {'sin²θ_W': 11.2692, '1/α_em(M_Z)': 13.0, 'Δm_np (MeV)': 177.4}
CHANGED_EXTENDED_PIN = frozenset([
    'm_s/m_b', 'm_e/m_τ', 'm_μ/m_τ', 'm_e/m_μ', 'θ₁₂_CKM (°)'])
CHANGED_LICENSED_PIN = frozenset(['θ₁₂_CKM (°)'])
MAX_FLIP_FLOOR_PIN = 0.0136          # 4dp: the largest per-row minimum floor
CORNER_RETURNING_RED = 'm_μ/m_τ'     # hard window x band minimum


class ScorecardCheckFailure(AssertionError):
    pass


def _safe_eval(node):
    """Evaluate the literal-plus-arithmetic subset used by the predictions
    table and the derivation module's constant assignments."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_eval(node.operand)
    if isinstance(node, ast.BinOp):
        a, b = _safe_eval(node.left), _safe_eval(node.right)
        if isinstance(node.op, ast.Div):
            return a / b
        if isinstance(node.op, ast.Mult):
            return a * b
        if isinstance(node.op, ast.Add):
            return a + b
        if isinstance(node.op, ast.Sub):
            return a - b
        if isinstance(node.op, ast.Pow):
            return a ** b
    if isinstance(node, ast.Attribute):
        # permits math.pi only
        if (isinstance(node.value, ast.Name) and node.value.id == 'math'
                and node.attr == 'pi'):
            return math.pi
    if isinstance(node, (ast.Tuple, ast.List)):
        return ([_safe_eval(e) for e in node.elts] if isinstance(node, ast.List)
                else tuple(_safe_eval(e) for e in node.elts))
    raise ScorecardCheckFailure(f'unsupported node in source literal: {ast.dump(node)}')


def _extract_prediction_rows():
    """AST-extract the `predictions` literal from the banked scorecard."""
    validation_py, _, _ = _banked_source_paths()
    with open(validation_py, encoding='utf-8') as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'check_L_prediction_catalog':
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Assign)
                        and isinstance(sub.targets[0], ast.Name)
                        and sub.targets[0].id == 'predictions'):
                    return [_safe_eval(t) for t in sub.value.elts]
    raise ScorecardCheckFailure('predictions literal not found in banked source')


def _harvest_banked_threshold():
    """AST-harvest the consistency threshold from the banked scorecard: the
    unique constant C in the `sigma <= C` comparison inside
    check_L_prediction_catalog. Harvested, not re-typed."""
    validation_py, _, _ = _banked_source_paths()
    with open(validation_py, encoding='utf-8') as f:
        tree = ast.parse(f.read())
    vals = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'check_L_prediction_catalog':
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Compare)
                        and isinstance(sub.left, ast.Name)
                        and sub.left.id == 'sigma'
                        and len(sub.ops) == 1
                        and isinstance(sub.ops[0], ast.LtE)
                        and isinstance(sub.comparators[0], ast.Constant)):
                    vals.add(float(sub.comparators[0].value))
    if len(vals) != 1:
        raise ScorecardCheckFailure(
            f'banked sigma threshold not uniquely harvested: {sorted(vals)}')
    return vals.pop()


def _extract_derivation_constants():
    """AST-extract the derivation module's own constants: the three CKM
    angle targets it compares against, plus the FN inputs needed for the
    independent recomputation (x, phi, q_B, q_H, obs_Vus)."""
    _, resolution_py, _ = _banked_source_paths()
    with open(resolution_py, encoding='utf-8') as f:
        tree = ast.parse(f.read())
    out = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        tgt = node.targets[0]
        if isinstance(tgt, ast.Name) and tgt.id in ('x', 'phi', 'q_B', 'q_H'):
            out.setdefault(tgt.id, _safe_eval(node.value))
        if isinstance(tgt, ast.Tuple):
            names = [e.id for e in tgt.elts if isinstance(e, ast.Name)]
            if names == ['obs_th12', 'obs_th23', 'obs_th13']:
                vals = _safe_eval(node.value)
                out['obs_th'] = tuple(vals)
            if names == ['obs_Vus', 'obs_Vcb', 'obs_Vub']:
                vals = _safe_eval(node.value)
                out['obs_Vus'] = vals[0]
    missing = {'x', 'phi', 'q_B', 'q_H', 'obs_th', 'obs_Vus'} - set(out)
    if missing:
        raise ScorecardCheckFailure(f'derivation constants not found: {missing}')
    return out


def _harvest_direct_dependencies(check_name):
    """AST-harvest the dependencies=[...] literal of one banked check
    function, scanning apf/*.py."""
    import glob
    _, _, apf_dir = _banked_source_paths()
    deps = []
    for fn in glob.glob(os.path.join(apf_dir, '*.py')):
        try:
            with open(fn, encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'check_' + check_name:
                for sub in ast.walk(node):
                    if (isinstance(sub, ast.keyword) and sub.arg == 'dependencies'
                            and isinstance(sub.value, (ast.List, ast.Tuple))):
                        deps += [e.value for e in sub.value.elts
                                 if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return deps


def _recompute_delta_q(consts):
    """Independent recomputation of the derivation's delta_Vus and delta_q:
    build the FN LO texture from the derivation's own AST-extracted inputs,
    diagonalize, and express the |Vus| deviation both as a fraction
    (delta_Vus) and in FN charge-grid units (delta_q = delta_Vus / ln 2)."""
    import numpy as np
    x, phi = consts['x'], consts['phi']
    q_B, q_H = consts['q_B'], consts['q_H']

    def build(k_B, k_H, c_B, c_H):
        M = np.zeros((3, 3), dtype=complex)
        for g in range(3):
            for h in range(3):
                ang_b = phi * (g - h) * k_B / 3.0
                ang_h = phi * (g - h) * k_H / 3.0
                M[g, h] = (c_B * x ** (q_B[g] + q_B[h]) * complex(math.cos(ang_b), math.sin(ang_b))
                           + c_H * x ** (q_H[g] + q_H[h]) * complex(math.cos(ang_h), math.sin(ang_h)))
        return M

    M_u = build(3, 0, 1.0, 0.125)
    M_d = build(0, 0, 1.0, 1.0)
    _, Vu = np.linalg.eigh(M_u @ M_u.conj().T)
    _, Vd = np.linalg.eigh(M_d @ M_d.conj().T)
    V = Vu.conj().T @ Vd
    Vus = abs(V[0, 1])
    delta_Vus = float(abs(Vus / consts['obs_Vus'] - 1))
    return delta_Vus / math.log(2), delta_Vus


def _classify(name, source_theorem):
    """Family classification, computed from row identity (name + source
    theorem), returning 'FN_mass_ratio', 'FN_CKM_angle', or None. The
    licensed family is FN_CKM_angle alone; FN_mass_ratio joins only the
    extended statistic, under the FN_POWER_TRANSFER premise."""
    if source_theorem == 'T_mass_ratios':
        return 'FN_mass_ratio'
    if source_theorem == 'L_CKM_phase_bracket' and name.startswith('θ'):
        return 'FN_CKM_angle'
    return None


LICENSED_FAMILIES = ('FN_CKM_angle',)
EXTENDED_FAMILIES = ('FN_CKM_angle', 'FN_mass_ratio')


def _recount(table, floor_val, families, window, thr):
    """Second code path for a floored headline: squared comparison instead
    of sqrt-division for the quadrature window; used by the double-count
    and sensitivity legs against the primary loop."""
    n = 0
    verdicts = {}
    for r in table:
        sm = floor_val * abs(r['obs']) if r['family'] in families else 0.0
        if r['err'] == 0:
            ok = r['consistent_banked']
        elif window == 'quad':
            ok = (r['apf'] - r['obs']) ** 2 <= thr ** 2 * (r['err'] ** 2 + sm ** 2)
        else:
            ok = abs(r['apf'] - r['obs']) <= sm + thr * r['err']
        verdicts[r['name']] = ok
        n += 1 if ok else 0
    return n, verdicts


def check_T_scorecard_resolution():
    legs_run = []

    def leg(label, ok, msg):
        legs_run.append(label)
        if not ok:
            raise ScorecardCheckFailure(f'[{label}] {msg}')

    # ------------------------------------------------------------------
    # 1. Rows from the banked source; banked statistic reproduced with
    #    the threshold harvested from the banked source itself.
    # ------------------------------------------------------------------
    rows = _extract_prediction_rows()
    thr = _harvest_banked_threshold()
    tested = [r for r in rows if r[2] is not None]
    n_total, n_tested = len(rows), len(tested)

    n_cons = 0
    errors = []
    table = []  # per-row dicts, built once, re-derived where legs need a second path
    for name, apf, obs, err, unit, src, *_rest in rows:
        if obs is None:
            continue
        if err == 0:
            sigma = 0.0
            pct = 0.0
            consistent = (apf == obs)
            n_cons += 1 if consistent else 0
        else:
            pct = abs(apf - obs) / abs(obs) * 100 if obs != 0 else abs(apf - obs)
            sigma = abs(apf - obs) / err
            consistent = sigma <= thr
            n_cons += 1 if consistent else 0
        errors.append(pct)
        table.append({'name': name, 'apf': apf, 'obs': obs, 'err': err,
                      'source': src, 'pct': pct, 'sigma': sigma,
                      'consistent_banked': consistent})
    mean_err = sum(errors) / len(errors)
    median_err = sorted(errors)[len(errors) // 2]

    from apf.validation import check_L_prediction_catalog
    banked = check_L_prediction_catalog()['artifacts']

    leg('rows_extracted_from_banked_source',
        n_tested == banked['n_tested'] and n_total == banked['n_predictions'],
        f'extracted {n_total} rows / {n_tested} tested vs banked '
        f"{banked['n_predictions']} / {banked['n_tested']}")

    leg('banked_headline_reproduced_n_consistent',
        n_cons == banked['n_consistent'],
        f"recomputed n_consistent={n_cons} vs banked {banked['n_consistent']}")

    leg('banked_headline_reproduced_mean_median',
        round(mean_err, 2) == banked['mean_error_pct']
        and round(median_err, 2) == banked['median_error_pct'],
        f"recomputed mean/median {mean_err:.2f}/{median_err:.2f} vs banked "
        f"{banked['mean_error_pct']}/{banked['median_error_pct']}")

    # ------------------------------------------------------------------
    # 2. The floor, read off the banked derivation and tied by value.
    # ------------------------------------------------------------------
    from apf.standalone.L_CKM_resolution_limit import check_L_CKM_resolution_limit
    deriv = check_L_CKM_resolution_limit()
    deriv_arts = deriv['artifacts']
    banked_delta_q = float(deriv_arts['delta_q_FN'])

    consts = _extract_derivation_constants()
    my_delta_q, my_delta_Vus = _recompute_delta_q(consts)

    leg('floor_independent_recomputation_matches_banked_artifact',
        round(my_delta_q, 4) == round(banked_delta_q, 4),
        f'independent delta_q={my_delta_q:.6f} vs banked artifact {banked_delta_q}')

    floor_frac = banked_delta_q * math.log(2)

    # The floor is the derivation's own fractional |Vus| residual: the ln 2
    # in delta_q = delta_Vus / ln 2 round-trips. Executed, not just stated.
    leg('floor_equals_derivation_Vus_residual_by_value',
        round(floor_frac, 4) == round(my_delta_Vus, 4)
        and 0.0 < floor_frac < 0.10,
        f'floor {floor_frac:.6f} != independent delta_Vus {my_delta_Vus:.6f} '
        'at 4dp, or outside (0, 0.10)')

    # The residual -> family-wide-resolution promotion is the transfer
    # premise; pin the floor's scale to the derivation's own computed LO
    # angle errors: it must lie inside the band spanned by |lo_errors|
    # (read from the executed check's artifacts).
    lo_abs = sorted(abs(v) / 100.0 for v in deriv_arts['lo_errors'].values())
    band_lo, band_hi = lo_abs[0], lo_abs[-1]
    leg('floor_within_derivation_computed_error_band',
        band_lo <= floor_frac <= band_hi,
        f'floor {floor_frac:.4f} outside the derivation-computed band '
        f'[{band_lo:.4f}, {band_hi:.4f}]')

    # ------------------------------------------------------------------
    # 3. Family classification, computed from row identity, discriminator
    #    witnessed both ways, and membership pinned set-exactly by name.
    # ------------------------------------------------------------------
    for row in table:
        row['family'] = _classify(row['name'], row['source'])

    fam_ckm = [r for r in table if r['family'] == 'FN_CKM_angle']
    fam_mr = [r for r in table if r['family'] == 'FN_mass_ratio']
    fam_all = fam_ckm + fam_mr

    leg('family_ckm_rows_match_derivation_targets_by_value',
        sorted(r['obs'] for r in fam_ckm) == sorted(consts['obs_th']),
        f"CKM-angle rows obs={sorted(r['obs'] for r in fam_ckm)} vs derivation "
        f"targets {sorted(consts['obs_th'])}")

    # The discriminating rule: pure-FN-power observable (x^q on the integer
    # grid; T_mass_ratios) vs continuous-Gram observable (T_PMNS). Witnessed
    # BOTH ways by AST harvest of the banked dependency declarations.
    mr_deps = _harvest_direct_dependencies('T_mass_ratios')
    pmns_deps = _harvest_direct_dependencies('T_PMNS')
    leg('family_discriminator_witnessed_both_ways',
        'L_Gram' in pmns_deps and 'L_Gram' not in mr_deps,
        f'discriminator broken: L_Gram in T_PMNS deps = {"L_Gram" in pmns_deps}, '
        f'L_Gram in T_mass_ratios deps = {"L_Gram" in mr_deps}; the Gram-route '
        'edge must separate the two mechanisms')
    # Computed fact: the T_capacity_ladder anchor is SHARED by both sides
    # (it appears in the T_PMNS list too), so it is a secondary witness of
    # FN-ladder contact, not the discriminator.
    shared_anchor = 'T_capacity_ladder' in pmns_deps

    leg('family_mass_ratio_anchor_direct_dependency',
        'T_capacity_ladder' in mr_deps,
        f'T_mass_ratios direct dependencies {mr_deps} lack the FN charge ladder')

    delta_rows = [r for r in table
                  if r['source'] == 'L_CKM_phase_bracket' and not r['name'].startswith('θ')]
    leg('family_excludes_pmns_and_phase_rows',
        all('PMNS' not in r['name'] for r in fam_all)
        and len(delta_rows) >= 1
        and all(r['family'] is None for r in delta_rows)
        and all(r['family'] is None for r in table if 'PMNS' in r['name']),
        'a PMNS row or a non-angle L_CKM_phase_bracket row was classified in-family')

    leg('derivation_contrast_names_the_excluded_mechanism',
        'Gram' in str(deriv_arts.get('PMNS_comparison', '')),
        "derivation artifacts do not name the continuous (Gram) contrast mechanism")

    fam_names = {r['name'] for r in fam_all}
    recomputed_fam_names = {r['name'] for r in table
                            if _classify(r['name'], r['source']) is not None}
    leg('family_split_set_exact',
        fam_names == recomputed_fam_names
        and {r['source'] for r in fam_all} == {'T_mass_ratios', 'L_CKM_phase_bracket'}
        and len(fam_all) == len(fam_ckm) + len(fam_mr),
        'family membership sets disagree between the two computation paths')

    leg('family_rows_set_exact_by_name',
        {r['name'] for r in fam_ckm} == set(FAMILY_CKM_NAMES)
        and {r['name'] for r in fam_mr} == set(FAMILY_MASS_RATIO_NAMES),
        f'family membership moved off the pinned names: '
        f"CKM {sorted(r['name'] for r in fam_ckm)} vs {sorted(FAMILY_CKM_NAMES)}; "
        f"MR {sorted(r['name'] for r in fam_mr)} vs {sorted(FAMILY_MASS_RATIO_NAMES)}")

    # ------------------------------------------------------------------
    # 4. The three statistics, side by side: banked (above), licensed
    #    (floor on the CKM rows only), extended (floor also on the
    #    T_mass_ratios rows, under the FN_POWER_TRANSFER premise).
    # ------------------------------------------------------------------
    n_lic = 0
    n_ext = 0
    for row in table:
        sm_lic = floor_frac * abs(row['obs']) if row['family'] in LICENSED_FAMILIES else 0.0
        sm_ext = floor_frac * abs(row['obs']) if row['family'] in EXTENDED_FAMILIES else 0.0
        row['sigma_model_licensed'] = sm_lic
        row['sigma_model'] = sm_ext
        if row['err'] == 0:
            row['sigma_eff_licensed'] = row['sigma']
            row['consistent_licensed'] = row['consistent_banked']
            row['sigma_eff'] = row['sigma']
            row['consistent_eff'] = row['consistent_banked']
        else:
            row['sigma_eff_licensed'] = abs(row['apf'] - row['obs']) / math.sqrt(
                row['err'] ** 2 + sm_lic ** 2)
            row['consistent_licensed'] = row['sigma_eff_licensed'] <= thr
            row['sigma_eff'] = abs(row['apf'] - row['obs']) / math.sqrt(
                row['err'] ** 2 + sm_ext ** 2)
            row['consistent_eff'] = row['sigma_eff'] <= thr
        n_lic += 1 if row['consistent_licensed'] else 0
        n_ext += 1 if row['consistent_eff'] else 0

    bad_quad = [r['name'] for r in table if r['err'] != 0 and (
        abs(r['sigma_eff'] * math.hypot(r['err'], r['sigma_model'])
            - abs(r['apf'] - r['obs'])) > 1e-9 * max(1.0, abs(r['apf'] - r['obs']))
        or abs(r['sigma_eff_licensed'] * math.hypot(r['err'], r['sigma_model_licensed'])
               - abs(r['apf'] - r['obs'])) > 1e-9 * max(1.0, abs(r['apf'] - r['obs'])))]
    leg('quadrature_identity_by_value', not bad_quad,
        f'sigma_eff * hypot(sigma_obs, sigma_model) != |APF - obs| on {bad_quad}')

    bad_zero = ([r['name'] for r in table
                 if r['family'] is None and r['sigma_eff'] != r['sigma']]
                + [r['name'] for r in table
                   if r['family'] not in LICENSED_FAMILIES
                   and r['sigma_eff_licensed'] != r['sigma']])
    leg('floor_zero_outside_family_by_value', not bad_zero,
        f'rows outside the respective family were altered: {bad_zero}')

    thr_second = _harvest_banked_threshold()
    marginal_gap_rows = [r['name'] for r in table
                        if thr_second < r['sigma_eff'] <= thr_second + 1.0
                        or thr_second < r['sigma_eff_licensed'] <= thr_second + 1.0]
    leg('threshold_harvested_and_tied_by_value',
        thr == thr_second and marginal_gap_rows == [],
        f'threshold used {thr} vs re-harvested {thr_second}; rows in the '
        f'marginal gap (thr, thr+1]: {marginal_gap_rows}')

    n_lic_second, v_lic = _recount(table, floor_frac, LICENSED_FAMILIES, 'quad', thr_second)
    leg('licensed_headline_double_count',
        n_lic == n_lic_second
        and all(v_lic[r['name']] == r['consistent_licensed'] for r in table),
        f'licensed headline {n_lic} vs second-path count {n_lic_second}')

    n_ext_second, v_ext = _recount(table, floor_frac, EXTENDED_FAMILIES, 'quad', thr_second)
    leg('extended_headline_double_count',
        n_ext == n_ext_second
        and all(v_ext[r['name']] == r['consistent_eff'] for r in table),
        f'extended headline {n_ext} vs second-path count {n_ext_second}')

    leg('mean_median_unchanged_by_floor',
        round(sum(r['pct'] for r in table) / len(table), 10) == round(mean_err, 10)
        and sorted(r['pct'] for r in table)[len(table) // 2] == median_err,
        'the floor changed the percent-error columns; it must not')

    # ------------------------------------------------------------------
    # 5. Pins by name and value: the post-floor red set, both
    #    changed-verdict sets, and the per-row minimum flip floors.
    # ------------------------------------------------------------------
    red_eff = [r for r in table if not r['consistent_eff']]
    red_map = {r['name']: round(r['sigma_eff'], 4) for r in red_eff}
    leg('post_floor_red_set_pinned_by_value',
        red_map == RED_SET_PIN,
        f'post-floor red set {red_map} moved off the pin {RED_SET_PIN}')

    changed_ext = {r['name'] for r in table
                   if r['consistent_eff'] != r['consistent_banked']}
    changed_lic = {r['name'] for r in table
                   if r['consistent_licensed'] != r['consistent_banked']}
    leg('changed_verdict_sets_pinned_by_name',
        changed_ext == set(CHANGED_EXTENDED_PIN)
        and changed_lic == set(CHANGED_LICENSED_PIN),
        f'changed-verdict sets moved off the pins: extended {sorted(changed_ext)} '
        f'vs {sorted(CHANGED_EXTENDED_PIN)}; licensed {sorted(changed_lic)} '
        f'vs {sorted(CHANGED_LICENSED_PIN)}')

    # Per-row minimum floor that flips each changed row green, from the
    # quadrature identity: f_min = sqrt((|APF-obs|/thr)^2 - err^2) / |obs|.
    # The outcome is floor-insensitive: the largest of these sits below the
    # bottom of the derivation's own error band, so every floor in (and
    # above) the band produces the same five flips.
    min_floors = {}
    for r in table:
        if r['name'] in changed_ext:
            min_floors[r['name']] = math.sqrt(
                max(0.0, (abs(r['apf'] - r['obs']) / thr) ** 2 - r['err'] ** 2)
            ) / abs(r['obs'])
    max_flip_floor = max(min_floors.values())
    leg('floor_insensitivity_min_flip_floors',
        round(max_flip_floor, 4) == MAX_FLIP_FLOOR_PIN
        and max_flip_floor < band_lo,
        f'max per-row minimum flip floor {max_flip_floor:.6f} moved off the '
        f'pin {MAX_FLIP_FLOOR_PIN} or is not below the band bottom {band_lo}')

    # ------------------------------------------------------------------
    # 6. Falsifiability, by value.
    # ------------------------------------------------------------------
    leg('real_rows_exceeding_three_sigma_eff_exist', len(red_eff) >= 2,
        f'only {len(red_eff)} real rows exceed the threshold in sigma_eff; '
        'the demonstration requires at least two')

    syn_name = 'SYNTHETIC_CONTROL (not a catalog row)'
    syn_apf, syn_obs, syn_err = 1.20, 1.00, 0.001  # a 20% miss against a 0.1% experiment
    syn_sm = floor_frac * abs(syn_obs)             # in-family floor, by construction
    syn_sigma_eff = abs(syn_apf - syn_obs) / math.sqrt(syn_err ** 2 + syn_sm ** 2)
    leg('synthetic_control_goes_red',
        syn_sigma_eff > thr and syn_name not in {r['name'] for r in table},
        f'synthetic control sigma_eff={syn_sigma_eff:.2f} did not exceed the '
        'threshold, or collided with a real row')

    # ------------------------------------------------------------------
    # 7. Auxiliaries, value-tied: linear-window variant, floor-band
    #    sensitivity at the artifact band edges, and the moving corner.
    # ------------------------------------------------------------------
    n_linear = 0
    for r in table:
        if r['err'] == 0:
            ok = r['consistent_banked']
        else:
            ok = abs(r['apf'] - r['obs']) <= r['sigma_model'] + thr * r['err']
        r['consistent_linear'] = ok
        n_linear += 1 if ok else 0

    # Tie by value: full second-path recount, a hand-computed in-family
    # witness row, a hand-computed out-of-family red witness, and the
    # computed invariance n_linear == n_ext on this data.
    n_lin_second, v_lin = _recount(table, floor_frac, EXTENDED_FAMILIES, 'lin', thr_second)
    r_th12 = next(r for r in table if r['name'] == 'θ₁₂_CKM (°)')
    th12_window_ok = (abs(r_th12['apf'] - r_th12['obs'])
                      <= floor_frac * abs(r_th12['obs']) + thr_second * r_th12['err'])
    r_alpha = next(r for r in table if r['name'] == '1/α_em(M_Z)')
    alpha_window_red = (abs(r_alpha['apf'] - r_alpha['obs'])
                        > 0.0 + thr_second * r_alpha['err'])  # out of family: sm = 0
    leg('linear_window_variant_tied_by_value',
        n_linear == n_lin_second
        and all(v_lin[r['name']] == r['consistent_linear'] for r in table)
        and th12_window_ok and r_th12['consistent_linear']
        and alpha_window_red and not r_alpha['consistent_linear']
        and n_linear == n_ext,
        f'linear-window variant untied: {n_linear} vs second path {n_lin_second}; '
        f'witness rows th12={th12_window_ok}, alpha_red={alpha_window_red}; '
        f'computed invariance n_linear == n_ext ({n_linear} vs {n_ext}) broken')

    # Sensitivity at the derivation's OWN band edges (artifact-derived, not
    # prose): the extended quadrature headline at band_lo and band_hi.
    band_headlines = {}
    for f_band in (band_lo, band_hi):
        n_band = 0
        for r in table:
            sm = f_band * abs(r['obs']) if r['family'] in EXTENDED_FAMILIES else 0.0
            if r['err'] == 0:
                ok = r['consistent_banked']
            else:
                ok = abs(r['apf'] - r['obs']) / math.sqrt(r['err'] ** 2 + sm ** 2) <= thr
            n_band += 1 if ok else 0
        band_headlines[f_band] = n_band
    # Tie by value: second-path recount at each edge, and the computed
    # invariance that the quadrature headline is constant across the band.
    band_second = {f_band: _recount(table, f_band, EXTENDED_FAMILIES, 'quad', thr_second)[0]
                   for f_band in (band_lo, band_hi)}
    leg('sensitivity_band_headlines_tied_by_value',
        len(band_headlines) == 2
        and band_headlines == band_second
        and all(v == n_ext for v in band_headlines.values()),
        f'band headlines {band_headlines} vs second path {band_second}; '
        f'computed invariance (constant {n_ext} across the band) broken')

    # The one moving corner of the 2x2 sensitivity square: HARD WINDOW
    # evaluated at the band MINIMUM. Computed and recorded: exactly one row
    # returns red there relative to the extended statistic.
    n_corner, v_corner = _recount(table, band_lo, EXTENDED_FAMILIES, 'lin', thr_second)
    corner_reds = {name for name, ok in v_corner.items() if not ok}
    returning = corner_reds - {r['name'] for r in red_eff}
    n_lin_hi, _ = _recount(table, band_hi, EXTENDED_FAMILIES, 'lin', thr_second)
    leg('window_at_band_edges_corner_computed',
        returning == {CORNER_RETURNING_RED}
        and n_corner == n_ext - 1
        and n_lin_hi == n_ext,
        f'moving corner moved: hard window at band min gives {n_corner} with '
        f'returning red(s) {sorted(returning)} (pin: {CORNER_RETURNING_RED}); '
        f'hard window at band max gives {n_lin_hi} vs extended {n_ext}')

    # ------------------------------------------------------------------
    # Result path: artifacts built first (so the premise-ledger leg checks
    # the emitted records themselves), then funnel probe, then set-exact
    # leg inventory.
    # ------------------------------------------------------------------
    artifacts = {
            'n_total': n_total,
            'n_tested': n_tested,
            'threshold_banked_harvested': thr,
            'headline_banked': n_cons,
            'headline_licensed': n_lic,
            'headline_extended': n_ext,
            'headline_extended_conditional_on': ['FN_POWER_TRANSFER'],
            'headline_linear_window_variant': n_linear,
            'headline_linear_window_variant_conditional_on': ['FN_POWER_TRANSFER'],
            'premises': {'FN_POWER_TRANSFER': FN_POWER_TRANSFER_PREMISE},
            'mean_error_pct': round(mean_err, 2),
            'median_error_pct': round(median_err, 2),
            'floor_fraction': floor_frac,
            'floor_delta_q_banked': banked_delta_q,
            'floor_delta_q_independent': my_delta_q,
            'floor_delta_Vus_independent': my_delta_Vus,
            'floor_is_Vus_residual': bool(round(floor_frac, 4) == round(my_delta_Vus, 4)),
            'min_flip_floors': {k: round(v, 4) for k, v in min_floors.items()},
            'max_flip_floor': round(max_flip_floor, 4),
            'family_rows_licensed': sorted(r['name'] for r in fam_ckm),
            'family_rows_extended_only': sorted(r['name'] for r in fam_mr),
            'family_rows': sorted(fam_names),
            'n_family': len(fam_all),
            'n_family_mass_ratio': len(fam_mr),
            'n_family_ckm_angle': len(fam_ckm),
            'discriminator': {
                'rule': 'pure-FN-power observable (x^q, integer grid) vs '
                        'continuous-Gram observable',
                'gram_route_edge': 'L_Gram',
                'L_Gram_in_T_PMNS_deps': 'L_Gram' in pmns_deps,
                'L_Gram_in_T_mass_ratios_deps': 'L_Gram' in mr_deps,
                'secondary_anchor': 'T_capacity_ladder',
                'anchor_shared_by_T_PMNS': shared_anchor,
            },
            'red_rows_sigma_eff': {r['name']: round(r['sigma_eff'], 2) for r in red_eff},
            'rows_changed_verdict_extended': sorted(changed_ext),
            'rows_changed_verdict_licensed': sorted(changed_lic),
            'rows_in_marginal_threshold_gap': marginal_gap_rows,
            'synthetic_control_sigma_eff': round(syn_sigma_eff, 2),
            'band_edges_from_artifacts': [band_lo, band_hi],
            'sensitivity_band_headlines': {f'{k:.3f}': v for k, v in band_headlines.items()},
            'sensitivity_band_headlines_conditional_on': ['FN_POWER_TRANSFER'],
            'moving_corner': {
                'window': 'linear', 'floor': band_lo,
                'headline': n_corner, 'returning_red': sorted(returning),
                'conditional_on': ['FN_POWER_TRANSFER']},
            'invariances_computed': {
                'linear_equals_quadrature_at_exact_floor': n_linear == n_ext,
                'quadrature_headline_constant_across_band':
                    all(v == n_ext for v in band_headlines.values()),
                'hard_window_at_band_max_equals_extended': n_lin_hi == n_ext,
                'conditional_on': ['FN_POWER_TRANSFER'],
            },
            'per_row': [
                {'name': r['name'], 'source': r['source'], 'family': r['family'],
                 'pct_error': round(r['pct'], 3), 'sigma_banked': round(r['sigma'], 2),
                 'sigma_eff_licensed': round(r['sigma_eff_licensed'], 2),
                 'sigma_eff': round(r['sigma_eff'], 2),
                 'consistent_banked': r['consistent_banked'],
                 'consistent_licensed': r['consistent_licensed'],
                 'consistent_eff': r['consistent_eff'],
                 'consistent_linear': r['consistent_linear'],
                 'conditional_on': (['FN_POWER_TRANSFER']
                                    if r['family'] == 'FN_mass_ratio' else [])}
                for r in table],
    }

    # The premise tag on the extended headline, the three auxiliary
    # headlines, and the computed invariances, checked on the artifacts
    # dict itself, not on a parallel variable.
    _tag = ['FN_POWER_TRANSFER']
    leg('premise_ledger_auxiliary_headlines_tagged',
        artifacts.get('headline_extended_conditional_on') == _tag
        and artifacts.get('headline_linear_window_variant_conditional_on') == _tag
        and artifacts.get('sensitivity_band_headlines_conditional_on') == _tag
        and artifacts['moving_corner'].get('conditional_on') == _tag
        and artifacts['invariances_computed'].get('conditional_on') == _tag,
        'a headline or record computed with the floor on EXTENDED_FAMILIES '
        'is emitted without its FN_POWER_TRANSFER conditional_on tag')

    # Funnel probe: a counter inside the funnel — verify the leg mechanism
    # itself raises on a false condition before trusting any green leg above.
    try:
        leg('__funnel_probe__', False, 'probe')
    except ScorecardCheckFailure:
        legs_run.remove('__funnel_probe__')
    else:
        raise ScorecardCheckFailure(
            'the leg funnel did not raise on a false condition; every green '
            'leg above is unwitnessed')

    if set(legs_run) != set(EXPECTED_LEGS) or len(legs_run) != len(EXPECTED_LEGS):
        raise ScorecardCheckFailure(
            f'leg inventory mismatch: missing={sorted(set(EXPECTED_LEGS) - set(legs_run))} '
            f'extra={sorted(set(legs_run) - set(EXPECTED_LEGS))} '
            f'count={len(legs_run)} expected={len(EXPECTED_LEGS)}')

    return {
        'name': 'T_scorecard_resolution: banked, licensed, and extended '
                'statistics, side by side',
        'passed': True,
        'banked_registered': True,
        'legs': list(legs_run),
        'artifacts': artifacts,
    }


def main():
    res = check_T_scorecard_resolution()
    a = res['artifacts']
    print('=' * 76)
    print('scorecard_resolution  (banked v24.3.466; adoption ruled 2026-08-04: '
          'headline stays 32/40)')
    print('=' * 76)
    print(f"rows: {a['n_total']} total, {a['n_tested']} tested "
          f"(extracted from the banked source by AST; threshold "
          f"{a['threshold_banked_harvested']} harvested, not re-typed)")
    print(f"(a) BANKED statistic, reproduced by value : "
          f"{a['headline_banked']}/{a['n_tested']} within threshold "
          f"(mean {a['mean_error_pct']}%, median {a['median_error_pct']}%)")
    print(f"(b) LICENSED (floor on CKM angles only)   : "
          f"{a['headline_licensed']}/{a['n_tested']} within sigma_eff threshold")
    print(f"(c) EXTENDED (+ T_mass_ratios rows)       : "
          f"{a['headline_extended']}/{a['n_tested']}, conditional on "
          f"{', '.join(a['headline_extended_conditional_on'])}")
    print(f"  premise: {a['premises']['FN_POWER_TRANSFER']}")
    print(f"  floor = delta_q * ln 2 = {a['floor_fraction'] * 100:.3f}%  "
          f"== the derivation's own |Vus| residual "
          f"(independent delta_Vus {a['floor_delta_Vus_independent']:.6f}; "
          f"identity holds: {a['floor_is_Vus_residual']})")
    print(f"  floor-insensitive: every floor >= {a['max_flip_floor']} "
          f"(largest per-row minimum; band bottom "
          f"{a['band_edges_from_artifacts'][0]:.3f}) flips the same rows")
    print(f"  licensed family ({a['n_family_ckm_angle']} rows): "
          + ', '.join(a['family_rows_licensed']))
    print(f"  extended adds ({a['n_family_mass_ratio']} rows, conditional): "
          + ', '.join(a['family_rows_extended_only']))
    print(f"  discriminator: {a['discriminator']['rule']}; L_Gram in T_PMNS "
          f"deps: {a['discriminator']['L_Gram_in_T_PMNS_deps']}, in "
          f"T_mass_ratios deps: {a['discriminator']['L_Gram_in_T_mass_ratios_deps']} "
          f"(anchor {a['discriminator']['secondary_anchor']} shared by both: "
          f"{a['discriminator']['anchor_shared_by_T_PMNS']} — secondary witness only)")
    print(f"  rows changing verdict, licensed  : "
          f"{', '.join(a['rows_changed_verdict_licensed'])}")
    print(f"  rows changing verdict, extended  : "
          f"{', '.join(a['rows_changed_verdict_extended'])}")
    print(f"  rows still red in sigma_eff      : "
          + ', '.join(f"{k} ({v})" for k, v in a['red_rows_sigma_eff'].items()))
    print(f"  marginal gap (thr, thr+1]        : "
          f"{a['rows_in_marginal_threshold_gap'] or 'empty'}")
    print(f"  synthetic control (labeled, uncounted): sigma_eff = "
          f"{a['synthetic_control_sigma_eff']} > threshold")
    print(f"linear-window variant                 : "
          f"{a['headline_linear_window_variant']}/{a['n_tested']}, conditional on "
          f"{', '.join(a['headline_linear_window_variant_conditional_on'])}")
    print(f"floor-band sensitivity at artifact edges "
          f"({' / '.join(a['sensitivity_band_headlines'])}): "
          + ' / '.join(f"{v}/{a['n_tested']}"
                       for v in a['sensitivity_band_headlines'].values())
          + ', conditional on '
          + ', '.join(a['sensitivity_band_headlines_conditional_on']))
    print(f"moving corner (hard window x band min): "
          f"{a['moving_corner']['headline']}/{a['n_tested']}, returning red: "
          f"{', '.join(a['moving_corner']['returning_red'])}, conditional on "
          f"{', '.join(a['moving_corner']['conditional_on'])}")
    print(f"legs run (set-exact, enforced in the result path): {len(res['legs'])}")
    print('The three statistics are computed side by side; adoption of any of')
    print('them as the headline is a separate ruling and is not made here.')
    return res


# ---------------------------------------------------------------------------
# registration -- BARE-name key per the 2026-08-03 D6 ruling (canonical for
# new modules; by-name gates check both spellings)
# ---------------------------------------------------------------------------

_CHECKS = {
    'T_scorecard_resolution': check_T_scorecard_resolution,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == '__main__':
    main()
