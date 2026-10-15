import numpy as np

from plant import packed_bed as pb, physics as ph

STD = ph.plunge(800e-6, 341.0)


def test_brewers_sit_on_ergun_curve_in_viscous_regime():
    pts = pb.brewer_points(STD, 341.0)
    assert [p["name"] for p in pts] == ["Espresso", "Pour-over", "French press (live)"]
    for p in pts:
        assert np.isclose(p["f_p"], pb.ergun_curve(p["Re_b"]), rtol=1e-12)
        assert p["Re_b"] < 10 and p["inertial_share"] < 0.05
    # espresso is the finest, slowest bed: lowest Re_b
    assert pts[0]["Re_b"] < pts[1]["Re_b"] < pts[2]["Re_b"]


def test_espresso_recipe_velocity():
    # 36 g in 27 s through a 58 mm basket is about 0.5 mm/s
    assert round(1000 * pb.brewer_points(STD, 341.0)[0]["u"], 1) == 0.5


def test_corrochano_inputs_copied():
    assert pb.C15["d32_m"] == [79.73e-6, 101.60e-6, 112.86e-6, 131.36e-6]
    assert pb.C15["k_m2"][3][1] == 4.38e-13
    eps = np.array(pb.C15["eps_bed"])
    assert eps.min() >= 0.11 and eps.max() <= 0.33          # paper's text: all lie in 0.12-0.33
    assert np.all(np.diff(eps, axis=1) < 0)                  # denser packing -> lower porosity, every grind


def test_corrochano_check():
    rows = pb.corrochano_check()
    assert len(rows) == 12
    for r in rows:
        assert np.isclose(r["C_eff"], 150 * r["ratio"])     # identity: C_eff / 150 = k_ergun / k_measured
    ratio = {g: np.mean([r["ratio"] for r in rows if r["grind"] == g]) for g in "ABCD"}
    assert all(v > 1 for v in ratio.values())               # Ergun always over-predicts, as the paper found
    assert ratio["A"] < ratio["B"] < ratio["C"] < ratio["D"] # and the gap grows with grind size
    assert round(min(r["ratio"] for r in rows), 1) == 1.9 and round(max(r["ratio"] for r in rows)) == 16


def test_grind_sweep_trade_off():
    sw = pb.grind_sweep([300, 600, 900, 1200], 366.15, 240, 0.015, 0.25, False, 20, 0.15)
    assert np.all(np.diff(sw["EY"]) < 0) and np.all(np.diff(sw["force"]) < 0)
    assert np.all(np.array(sw["force_no_fines"]) < np.array(sw["force"]))
    # the cup changes a lot, the plunge only a little: EY falls by more than half, force by less than half
    assert sw["EY"][-1] / sw["EY"][0] < 0.5 and sw["force"][-1] / sw["force"][0] > 0.5


def test_collapse_three_curves_become_one():
    beds = pb.collapse_data(341.0)
    # dimensional: at the same u the beds differ by orders of magnitude
    assert beds[0]["dPdL"][0] / beds[2]["dPdL"][0] > 100
    # dimensionless: every point is on 150/Re_b + 1.75
    for b in beds:
        assert np.allclose(b["f_p"], pb.ergun_curve(b["Re_b"]), rtol=1e-12)


def test_corrochano_re_range_is_viscous():
    lo, hi = pb.C15_RE_RANGE
    assert (lo, hi) == (0.04, 4.0)
    assert 1.75 * hi / 150 < 0.05     # inertial share stays under 5 % across their whole range


def test_cameron_fig4_and_psd():
    c = pb.C20
    assert len(c["grind_setting"]) == len(c["EY_pct"]) == len(c["shot_time_s"]) == 7
    i = int(np.argmax(c["EY_pct"]))
    assert c["grind_setting"][i] == 1.7                          # the paper's peak
    assert np.all(np.diff(c["shot_time_s"]) < 0)                 # coarser -> faster shot
    s = {g: pb.psd_summary(g) for g in ["2.5", "2.0", "1.5", "1.0"]}
    fines = [s[g]["fines_volume"] for g in ["2.5", "2.0", "1.5", "1.0"]]
    d32 = [s[g]["d32"] for g in ["2.5", "2.0", "1.5", "1.0"]]
    assert np.all(np.diff(fines) > 0) and np.all(np.diff(d32) < 0)   # finer setting: more fines, smaller d32
    assert 85e-6 < min(d32) and max(d32) < 145e-6                    # same range as Corrochano's 80-131 um
    assert all(v["fines_surface"] > 0.6 for v in s.values())          # fines carry most of the surface


def test_model_fines_surface_share():
    assert round(pb.model_fines_surface_share(800e-6, 0.15), 2) == 0.82
    assert pb.model_fines_surface_share(800e-6, 0.0) == 0.0
