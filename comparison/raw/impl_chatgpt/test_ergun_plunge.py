"""Regression and limiting-case tests for ergun_plunge.py."""

import json
from pathlib import Path

import pytest

from ergun_plunge import plunge


KEYS = {
    "k", "dP", "dP_cake", "dP_mesh", "force", "Re_b", "f_p",
    "inertial_share", "d32", "d_s", "L_cake", "u",
}


def _examples():
    """Load reference inputs (SI units) and outputs (SI units) from JSON."""
    path = Path(__file__).with_name("public_examples.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("cases", data.get("examples", data))
    if isinstance(data, dict):
        data = list(data.values())
    assert len(data) == 2, "Expected two reference cases"
    return data


@pytest.mark.parametrize("case", _examples())
def test_public_examples(case):
    inputs = case.get("inputs", case.get("input", case.get("parameters")))
    expected = case.get("expected", case.get("outputs", case.get("output")))
    assert isinstance(inputs, dict) and isinstance(expected, dict)
    actual = plunge(**inputs)
    assert set(actual) == KEYS
    for key in KEYS:
        assert actual[key] == pytest.approx(expected[key], rel=1e-6), key


@pytest.mark.parametrize("d,T", [(300e-6, 293.15), (700e-6, 341.0), (1200e-6, 373.0)])
def test_ergun_friction_identity(d, T):
    """f_p and Re_b are dimensionless."""
    result = plunge(d, T)
    assert result["f_p"] == pytest.approx(150 / result["Re_b"] + 1.75, rel=1e-12)


def test_inertial_share_tends_to_zero():
    """Increasing flow time makes u (m/s) approach zero."""
    shares = [plunge(600e-6, 341.0, plunge_time=t)["inertial_share"]
              for t in (20.0, 2000.0, 200000.0)]  # s
    assert shares[0] > shares[1] > shares[2]
    assert shares[-1] < 1e-6


@pytest.mark.parametrize("changes", [
    {"T": 273.15}, {"T": 373.01}, {"d": 0}, {"d": -1e-6},
    {"eps_bed": 0}, {"eps_bed": 1},
])
def test_invalid_inputs(changes):
    arguments = {"d": 600e-6, "T": 341.0, **changes}
    with pytest.raises(ValueError):
        plunge(**arguments)
