"""Tests for ergun_plunge.plunge."""
import json
import pathlib

import pytest

from ergun_plunge import plunge

EXAMPLES = json.loads(
    (pathlib.Path(__file__).parent / "public_examples.json").read_text())


@pytest.mark.parametrize("case", EXAMPLES)
def test_public_examples(case):
    out = plunge(**case["inputs"])
    for key, expected in case["expected"].items():
        assert out[key] == pytest.approx(expected, rel=1e-6), key


@pytest.mark.parametrize("d", [300e-6, 800e-6, 1200e-6])
@pytest.mark.parametrize("plunge_time", [2.0, 20.0, 200.0])
def test_friction_factor_identity(d, plunge_time):
    out = plunge(d, 341.0, plunge_time=plunge_time)
    assert out["f_p"] == pytest.approx(150.0 / out["Re_b"] + 1.75, rel=1e-12)


def test_inertial_share_vanishes_at_low_velocity():
    shares = [plunge(800e-6, 341.0, plunge_time=t)["inertial_share"]
              for t in (20.0, 2e3, 2e5, 2e7)]
    assert all(a > b for a, b in zip(shares, shares[1:]))
    assert shares[-1] < 1e-6


def test_viscous_limit_matches_darcy():
    # At very low u the cake obeys Darcy: dP_cake = mu u L / k
    from CoolProp.CoolProp import PropsSI
    out = plunge(800e-6, 341.0, plunge_time=2e7)
    mu = PropsSI("V", "T", 341.0, "P", 101325.0, "Water")
    darcy = mu * out["u"] * out["L_cake"] / out["k"]
    assert out["dP_cake"] == pytest.approx(darcy, rel=1e-6)


def test_no_fines_d32_equals_d():
    out = plunge(500e-6, 300.0, fines_fraction=0.0)
    assert out["d32"] == pytest.approx(500e-6)


@pytest.mark.parametrize("kwargs", [
    dict(d=800e-6, T=273.0), dict(d=800e-6, T=374.0),
    dict(d=0.0, T=341.0), dict(d=-1e-4, T=341.0),
    dict(d=800e-6, T=341.0, eps_bed=0.0), dict(d=800e-6, T=341.0, eps_bed=1.0),
])
def test_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        plunge(**kwargs)
