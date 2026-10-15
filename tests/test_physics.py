import numpy as np
import pytest
from plant import physics as ph


def test_water_properties_match_steam_tables():
    rho, mu, cp = ph.water(293.15)
    assert rho == pytest.approx(998.2, abs=0.1)        # kg/m^3 at 20 C
    assert mu == pytest.approx(1.002e-3, rel=0.01)     # Pa s at 20 C


def test_water_rejects_steam():
    with pytest.raises(ValueError):
        ph.water(380.0)


def test_brew_mass_balance_closes():
    r = ph.brew(800e-6, 366.15, 240)
    assert r["balance_error"] < 1e-6


def test_standard_french_press_lands_near_sca_box():
    # 15 g coffee, 250 g water at 93 C, coarse 800 um grind, 4 min steep (a common recipe)
    r = ph.brew(800e-6, 366.15, 240)
    assert 0.010 < r["TDS"] < 0.014
    assert 0.16 < r["EY"] < 0.22


def test_finer_grind_extracts_more():
    assert ph.brew(500e-6, 366.15, 240)["EY"] > ph.brew(900e-6, 366.15, 240)["EY"]


def test_extraction_never_exceeds_extractable_fraction():
    r = ph.brew(150e-6, 368.15, 3000)
    assert r["EY"] < ph.X_EXTRACTABLE


def test_cooling_follows_energy_balance():
    r = ph.brew(800e-6, 366.15, 600)
    assert r["T0"] < 366.15                         # cold grounds and vessel cool the water at once
    assert np.all(np.diff(r["T"]) < 0)              # then it keeps cooling
    assert r["T"][-1] > 295.15                      # but never below room temperature


def test_finer_grind_is_harder_to_plunge():
    assert ph.plunge(300e-6, 360)["force"] > ph.plunge(900e-6, 360)["force"]


def test_stokes_validity_flag():
    assert ph.settling(40e-6, 340)["valid"]
    assert not ph.settling(500e-6, 340)["valid"]


def test_invalid_grind_fails_loudly():
    with pytest.raises(ValueError):
        ph.brew(5e-3, 366.15, 240)
