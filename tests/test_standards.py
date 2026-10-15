"""Professor-standard compliance checks: symbols defined with SI units, strict KaTeX, dimensional
consistency (pint), and no silent extrapolation."""
import json, os, re, shutil, subprocess
import numpy as np
import pint
import pytest
from plant import physics, steps

HERE = os.path.dirname(__file__)
# Formatting commands that are not symbols.
NON_SYMBOLS = [r"\frac", r"\Rightarrow", r"\rightarrow", r"\log_{10}", r"\times", r"\pm", r"\!", r"\left", r"\right", r"\cdot", r"\sum", r"\exp", r"\ln",
               r"\sqrt", r"\;", r"\,", r"\quad", r"\int", r"\approx", r"\propto", r"\max"]


def undefined_symbols(tex):
    """Return what is left of an equation after removing every SYMBOLS entry, formatting command,
    number and operator. Anything alphabetic left over is an undefined symbol."""
    s = re.sub(r"\\text\{[^}]*\}", " ", tex).replace(r"\mathrm{d}", " ")
    s = re.sub(r"(?<![A-Za-z\\])e\^", " ^", s)          # Euler's number in e^{...}
    for cmd in NON_SYMBOLS:
        s = s.replace(cmd, " ")
    for sym in sorted(steps.SYMBOLS, key=len, reverse=True):
        s = re.sub(r"(?<![A-Za-z\\])" + re.escape(sym) + r"(?![A-Za-z_'])", " ", s)
    return re.findall(r"\\?[A-Za-z]+", s)


def all_equations():
    return [(name, st["write"]) for name, unit in steps.UNITS.items() for st in unit["steps"]]


@pytest.mark.parametrize("unit,tex", all_equations())
def test_every_symbol_is_defined(unit, tex):
    assert undefined_symbols(tex) == [], f"{unit}: undefined symbol(s) in {tex}"


def test_symbol_audit_catches_a_broken_equation():
    assert undefined_symbols(r"v_t = \frac{\Delta x}{q}") == [r"\Delta", "x", "q"]


def test_symbol_table_has_no_unused_entries():
    tex = " ".join(t for _, t in all_equations())
    unused = [k for k in steps.SYMBOLS
              if not re.search(r"(?<![A-Za-z\\])" + re.escape(k) + r"(?![A-Za-z_'])", tex)]
    assert unused == []


def test_every_symbol_has_meaning_and_si_unit():
    ureg = pint.UnitRegistry()
    for sym, (meaning, unit) in steps.SYMBOLS.items():
        assert meaning.strip(), sym
        ureg(unit.replace("^", "**"))   # raises if the unit string is not a real unit


def test_every_unit_is_complete():
    for name, u in steps.UNITS.items():
        assert u["sign"] and u["dof"]["result"] and len(u["steps"]) >= 4, name
        assert all(st["title"] and st["write"] and st["say"] for st in u["steps"]), name
        assert len(u["checks"]) >= 3 and len(u["questions"]) >= 3, name


def node_katex():
    node = shutil.which("node")
    if node is None:
        return None
    env = dict(os.environ)
    for p in [os.environ.get("KATEX_NODE_PATH", ""), os.path.join(HERE, "..", "docs", "node_modules")]:
        if p and os.path.isdir(os.path.join(p, "katex")):
            env["NODE_PATH"] = p
    ok = subprocess.run([node, "-e", "require('katex')"], env=env, capture_output=True).returncode == 0
    return (node, env) if ok else None


def run_katex(exprs):
    found = node_katex()
    if found is None:
        pytest.skip("node with katex not installed")
    node, env = found
    out = subprocess.run([node, os.path.join(HERE, "katex_check.js")], input=json.dumps(exprs),
                         env=env, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_every_equation_passes_strict_katex():
    assert run_katex([tex for _, tex in all_equations()]) == []


def test_katex_check_catches_a_broken_equation():
    assert len(run_katex([r"\frac{1}{"])) == 1


# ---------- dimensional consistency with pint, cross-checked against the physics code ----------
ureg = pint.UnitRegistry()


def test_stokes_units_and_value():
    rho, mu, _ = physics.water(350.0)
    d = 30e-6 * ureg.m
    rho_p = (physics.RHO_SOLID * (1 - physics.EPS_PARTICLE) + rho * physics.EPS_PARTICLE) * ureg("kg/m^3")
    g = physics.G * ureg("m/s^2")
    v = ((rho_p - rho * ureg("kg/m^3")) * g * d**2 / (18 * mu * ureg("Pa*s"))).to_base_units()
    assert v.units == ureg("m/s").units
    assert np.isclose(v.magnitude, physics.settling(30e-6, 350.0)["v"], rtol=1e-12)
    Re = (rho * ureg("kg/m^3") * v * d / (mu * ureg("Pa*s"))).to_base_units()
    assert Re.dimensionless


# ---------- no silent extrapolation ----------
def test_out_of_range_inputs_raise():
    with pytest.raises(ValueError):
        physics.water(400.0)
    with pytest.raises(ValueError):
        physics.brew(50e-6, 366.15, 240)


# ---------- numbers quoted in the Say lines match the model (standard recipe) ----------
def test_quoted_numbers_match_the_model():
    b = physics.brew(800e-6, 366.15, 240)
    T_end = b["T"][-1]
    assert round(b["T0"] - 273.15, 1) == 76.5
    assert round(100 * b["TDS"], 2) == 1.10 and round(100 * b["EY"], 1) == 17.9
    assert round(physics.fast_fraction(800e-6), 2) == 0.21
    s = physics.settling(30e-6, T_end)
    assert round(T_end - 273.15) == 68 and round(1000 * s["v"], 1) == 0.2
    assert round(s["t_settle"] / 60) == 7 and round(s["Re_p"], 3) == 0.014 and round(s["rho_p"], -1) == 1150
    assert round(physics.plunge(800e-6, T_end)["force"]) == 2
    rho, _, cp = physics.water(366.15)
    C = 0.25 * cp + 0.015 * physics.CP_COFFEE + 0.35 * 840
    assert round(C, -1) == 1370 and round(C / 60) == 23
    V_k = physics.EPS_PARTICLE * 0.015 / (physics.RHO_SOLID * (1 - physics.EPS_PARTICLE))
    V_b = 0.25 / rho - V_k
    assert round(100 * physics.X_EXTRACTABLE * V_b / (V_b + V_k), 1) == 28.5
    assert round(b["m_l"][-1] / V_b) == 11
