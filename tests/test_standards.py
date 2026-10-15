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
