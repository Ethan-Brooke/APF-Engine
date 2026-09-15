"""Regression checks against the printed P37 ODE and its stopping protocol."""
import math
import subprocess
import sys

import pytest
from apf import class_transition as m


@pytest.mark.parametrize('slots,a,r,phi0', [(4, 1., 0., 4.), (4, 1., .01, 100.),
                                          (2, .3, 2., 200.), (1, 2., .4, 20.)])
def test_solution_against_independent_ode_integration(slots, a, r, phi0):
    # Integrate the two original RHS expressions, not a rearranged solution.
    end = .8 * m.completion_time(slots, a, phi0, gamma_rel=r)
    count = 1600
    h = end / count
    y = (phi0, 0.)

    def rhs(state):
        load, fill = state
        return (-slots * a * (42. - fill), a * (42. - fill) - r * fill)

    for _ in range(count):
        k1 = rhs(y)
        k2 = rhs(tuple(x + h * k / 2 for x, k in zip(y, k1)))
        k3 = rhs(tuple(x + h * k / 2 for x, k in zip(y, k2)))
        k4 = rhs(tuple(x + h * k for x, k in zip(y, k3)))
        y = tuple(x + h * (u + 2*v + 2*w + z) / 6
                  for x, u, v, w, z in zip(y, k1, k2, k3, k4))
    assert m.ijc_load(end, phi0, slots, a, r) == pytest.approx(y[0], abs=1e-8)
    assert m.per_slot_phi(end, a, r) == pytest.approx(y[1], abs=1e-8)


def test_decisive_zero_release_regression_and_initial_slope():
    t = math.log(56 / 55)
    assert m.ijc_load(t, 4., 4, 1.) == pytest.approx(1., abs=1e-12)
    assert m.completion_time(4, 1., 4.) == pytest.approx(t, abs=1e-14)
    h = 1e-7
    assert (m.ijc_load(h, 4., 4, 1.) - 4.) / h == pytest.approx(-168., rel=1e-6)


@pytest.mark.parametrize('phi0,finite', [(168.9, True), (169., False), (170., False)])
def test_zero_release_reachability_boundary(phi0, finite):
    t = m.completion_time(4, 1., phi0)
    assert math.isfinite(t) is finite
    if finite:
        assert m.ijc_load(t, phi0, 4, 1.) == pytest.approx(1.)


@pytest.mark.parametrize('r', [1e-7, .01, .2, 2., 20.])
def test_release_reopens_capacity_and_threshold_is_first_crossing(r):
    t = m.completion_time(4, 1., 250., gamma_rel=r)
    assert math.isfinite(t) and t > 0
    assert m.ijc_load(t, 250., 4, 1., r) == pytest.approx(1., abs=1e-10)
    assert m.ijc_load(t * (1 - 1e-6), 250., 4, 1., r) > 1
    assert m.ijc_load(t * (1 + 1e-6), 250., 4, 1., r) < 1


def test_release_changes_completion():
    times = [m.completion_time(4, 1., 100., gamma_rel=r) for r in (0, .01, .2, 2)]
    assert all(x > y for x, y in zip(times, times[1:]))


def test_stopped_protocol_preserves_residual_and_releases_slots():
    stop = m.completion_time(4, 1., 100., gamma_rel=.2)
    before = m.transition_state(stop - 1e-8, 100., 4, 1., .2)
    at = m.transition_state(stop, 100., 4, 1., .2)
    after = m.transition_state(stop + 5., 100., 4, 1., .2)
    assert before == pytest.approx(at, abs=2e-6)
    assert at[0] == after[0] == 1.
    assert after[1] == pytest.approx(at[1] / math.e)
    assert after[1] > 0  # release is not finite-time exact clearing
    assert m.ijc_load(stop + 100, 100., 4, 1., .2) < 0  # explicitly raw continuation
    assert m.transition_state(stop + 100, 100., 4, 1., .2)[0] == 1.


def test_zero_release_does_not_clear_slots_after_stop():
    stop = m.completion_time(4, 1., 4.)
    assert m.transition_state(stop, 4., 4, 1.) == m.transition_state(stop + 10, 4., 4, 1.)


def test_initial_threshold_no_drive_no_slots_and_stable_short_times():
    assert m.completion_time(0, 0., .5) == 0
    assert m.transition_state(10., .5, 0, 0.) == (.5, 0.)
    assert math.isinf(m.completion_time(4, 0., 4.))
    assert math.isinf(m.completion_time(0, 1., 4.))
    assert m.transition_state(2., 4., 0, 1.) == (4., 0.)
    assert m.per_slot_phi(1e-20, 1.) == pytest.approx(42e-20, rel=1e-14, abs=0)


@pytest.mark.parametrize('kwargs', [dict(gamma_rel=-1), dict(eps_min=0),
                                   dict(gamma_rel=math.nan), dict(eps_min=math.inf)])
def test_invalid_parameters_are_rejected(kwargs):
    with pytest.raises(ValueError):
        m.completion_time(4, 1., 4., **kwargs)


def test_all_registered_checks_execute():
    registry = {}
    m.register(registry)
    assert set(registry) == {'T_class_transition', 'L_per_slot_capacity_flow',
                             'T_class_transition_completion',
                             'T_realignment_floor_is_epsilon_star',
                             'T_coherent_free_spend_permanent'}
    for name, check in registry.items():
        result = check()
        assert result['name'] == name
        assert result['passed'] is True, result


@pytest.mark.parametrize('mutation', ['load', 'time', 'both', 'drop_release'])
def test_bank_check_rejects_regressions_in_isolated_process(mutation):
    # Includes the coordinated old-load/old-time mutation that formerly passed.
    script = '''
import importlib.util, math, sys
spec = importlib.util.spec_from_file_location('flow_mutant', sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
mutation = sys.argv[2]
if mutation in ('load', 'both'):
    m.ijc_load = lambda t, p, n, a, r=0: p * math.exp(-n*a*t)
if mutation in ('time', 'both'):
    def wrong_time(n,a,p,eps_min=1.,gamma_rel=0.):
        return 0. if p <= eps_min else (math.log(p/eps_min)/(n*a) if n*a else math.inf)
    m.completion_time = wrong_time
if mutation == 'drop_release':
    original = m._drained_load
    m._drained_load = lambda t,n,a,r: original(t,n,a,0.)
    # Keep the root calculation finite while reintroducing release independence.
    original_time = m.completion_time
    m.completion_time = lambda n,a,p,eps_min=1.,gamma_rel=0.: original_time(n,a,p,eps_min,0.)
assert not m.check_T_class_transition_completion()['passed']
'''
    result = subprocess.run([sys.executable, '-c', script, m.__file__, mutation],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('r', [1e-12, 1e-20, 1e-100, 1e-200])
def test_near_zero_release_at_capacity_uses_unsaturated_residual(r):
    # Independent high-precision evaluation of the printed integral. This
    # catches a double-precision D(t) that rounds to capacity too early.
    from decimal import Decimal as D, localcontext
    with localcontext() as context:
        context.prec = 280
        release = D.from_float(r)
        rate = 1 + release
        low, high = D(0), D(1024)
        for _ in range(200):
            midpoint = (low + high) / 2
            drained = D(168) * (release * midpoint / rate
                        + (1 - (-rate * midpoint).exp()) / rate**2)
            if drained < 168:
                low = midpoint
            else:
                high = midpoint
        expected = float((low + high) / 2)
    assert m.completion_time(4, 1., 169., gamma_rel=r) == pytest.approx(expected, rel=2e-13)


def test_zero_release_just_below_capacity_preserves_small_gap():
    from decimal import Decimal as D, localcontext
    phi0 = math.nextafter(169., 0.)
    with localcontext() as context:
        context.prec = 80
        gap = D(168) - (D.from_float(phi0) - D(1))
        expected = float((D(168) / gap).ln())
    assert m.completion_time(4, 1., phi0) == pytest.approx(expected, rel=1e-14)
