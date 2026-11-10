"""Website checks: the static explorer shows exactly what the tested model computes, and the numbers quoted on the
pages come from the model. These guard against transcription errors; they do not test the physics itself."""
import numpy as np
import pytest

from plant import physics as ph
from site_src import analysis, explorer

# absolute floors (SI units) for values near zero, next to a 1e-9 relative tolerance
ATOL = {"k": 1e-20, "dP": 1e-9, "dP_cake": 1e-9, "dP_mesh": 1e-9, "force": 1e-12, "Re_b": 1e-12, "f_p": 1e-12,
        "inertial_share": 1e-12}


def test_grid_matches_app_slider():
    assert explorer.GRID_UM[0] == 300 and explorer.GRID_UM[-1] == 1200 and np.all(np.diff(explorer.GRID_UM) == 10)


def test_sweep_equals_plunge_at_every_grid_point():
    data = explorer.sweep()
    for i, g in enumerate(explorer.GRID_UM):
        ref = ph.plunge(g * 1e-6, explorer.T_PLUNGE)
        for key in explorer.OUTPUTS:
            assert np.isclose(data[key][i], ref[key], rtol=1e-9, atol=ATOL[key]), (g, key)


@pytest.mark.parametrize("narrow", [False, True])
def test_figure_slider_steps_carry_the_model_values(narrow):
    data = explorer.sweep()
    fig = explorer.figure(data, narrow=narrow)
    steps = fig.layout.sliders[0].steps
    assert len(steps) == len(explorer.GRID_UM)
    for i, step in enumerate(steps):
        y = step.args[0]["y"]
        assert y[0][0] == data["k"][i] and y[1][0] == data["dP"][i] and y[2][0] == data["force"][i] and y[3][0] == data["f_p"][i]
        assert list(step.args[2]) == [7, 8, 9, 10]          # only the four marker traces move
    assert list(fig.data[1].y) == list(data["dP"])     # the total pressure-drop curve is the one the marker follows


def test_plunge_temperature_is_end_of_steep_for_default_recipe():
    b = ph.brew(800e-6, 93 + 273.15, 240, m_coffee=0.015, m_water=0.015 * 16.7)
    assert abs(b["T"][-1] - explorer.T_PLUNGE) < 0.5


def test_quoted_numbers():
    n = analysis.numbers()
    assert round(n["c15_min"], 1) == 1.9 and round(n["c15_max"]) == 16
    assert round(n["Re_cross"]) == 86
    assert round(n["eps_implied"]["eps"], 2) == 0.36
    assert 45 < n["w21"]["ratio_ergun"] < 50                 # Ergun vs Wadsworth 2021 measured permeability
    assert n["K1200"] / n["K300"] < 2                         # fines dominate in the model
    assert not ph.in_target(n["TDS"], n["EY"])                # default recipe is off-spec, as the pages say


def test_sensitivity_default_row_equals_base():
    s = analysis.sensitivity()
    base_rows = [r for r in s["rows"] if (r["input"].startswith("porosity") and r["value"] == 0.40)]
    assert np.isclose(base_rows[0]["force"], s["base"])
