"""Professor-standard checks, run by the tests and shown live as a badge in the app.

  1. every symbol in every equation is defined in steps.SYMBOLS
  2. every symbol has a meaning and a real SI unit (parsed by pint)
  3. the symbol table has no unused entries
  4. Stokes' law is dimensionally consistent (pint) and matches physics.settling
  5. out-of-range inputs raise errors instead of extrapolating silently
The strict KaTeX parse needs node, so it runs in tests/test_standards.py only.
"""
import re

import numpy as np
import pint

from plant import physics, steps

UREG = pint.UnitRegistry()
# Formatting commands that are not symbols.
NON_SYMBOLS = [r"\frac", r"\Rightarrow", r"\rightarrow", r"\log_{10}", r"\times", r"\pm", r"\!", r"\left", r"\right",
               r"\cdot", r"\sum", r"\exp", r"\ln", r"\sqrt", r"\;", r"\,", r"\quad", r"\int", r"\approx",
               r"\propto", r"\max"]


def _symbol_pattern(sym):
    return r"(?<![A-Za-z\\])" + re.escape(sym) + r"(?![A-Za-z_'])"


def all_equations():
    """(unit name, LaTeX) for every Write line."""
    return [(name, st["write"]) for name, unit in steps.UNITS.items() for st in unit["steps"]]


def undefined_symbols(tex):
    """What is left of an equation after removing every SYMBOLS entry, formatting command, number and
    operator. Anything alphabetic left over is an undefined symbol."""
    s = re.sub(r"\\text\{[^}]*\}", " ", tex).replace(r"\mathrm{d}", " ")
    s = re.sub(r"(?<![A-Za-z\\])e\^", " ^", s)          # Euler's number in e^{...}
    for cmd in NON_SYMBOLS:
        s = s.replace(cmd, " ")
    for sym in sorted(steps.SYMBOLS, key=len, reverse=True):
        s = re.sub(_symbol_pattern(sym), " ", s)
    return re.findall(r"\\?[A-Za-z]+", s)


def unused_symbols():
    tex = " ".join(t for _, t in all_equations())
    return [k for k in steps.SYMBOLS if not re.search(_symbol_pattern(k), tex)]


def bad_units():
    """Symbols whose unit string pint cannot parse, or that have no meaning."""
    bad = []
    for sym, (meaning, unit) in steps.SYMBOLS.items():
        try:
            UREG(unit.replace("^", "**"))
        except Exception:
            bad.append(sym)
        if not meaning.strip():
            bad.append(sym)
    return bad


def stokes_units_ok(T=350.0, d=30e-6):
    """Stokes' law evaluated with units: result must be m/s and equal physics.settling; Re_p dimensionless."""
    rho, mu, _ = physics.water(T)
    rho_p = physics.RHO_SOLID * (1 - physics.EPS_PARTICLE) + rho * physics.EPS_PARTICLE
    v = ((rho_p - rho) * UREG("kg/m^3") * physics.G * UREG("m/s^2") * (d * UREG.m) ** 2
         / (18 * mu * UREG("Pa*s"))).to_base_units()
    Re = (rho * UREG("kg/m^3") * v * d * UREG.m / (mu * UREG("Pa*s"))).to_base_units()
    return (v.units == UREG("m/s").units and Re.dimensionless
            and np.isclose(v.magnitude, physics.settling(d, T)["v"], rtol=1e-12))


def extrapolation_guards_ok():
    """Water outside 0-100 C and grinds outside 100-2000 um must raise."""
    for call in (lambda: physics.water(400.0), lambda: physics.brew(50e-6, 366.15, 240)):
        try:
            call()
            return False
        except ValueError:
            pass
    return True


def run_checks():
    """List of (check, passed, detail) for the app's standards badge."""
    undefined = {f"{u}: {', '.join(undefined_symbols(t))}" for u, t in all_equations() if undefined_symbols(t)}
    n_eq = len(all_equations())
    return [
        ("Every symbol in every equation is defined", not undefined,
         f"{n_eq} equations, {len(steps.SYMBOLS)} symbols" if not undefined else "; ".join(sorted(undefined))),
        ("Every symbol has a meaning and an SI unit", not bad_units(), ", ".join(bad_units()) or "parsed by pint"),
        ("No unused symbols in the table", not unused_symbols(), ", ".join(unused_symbols()) or "all used"),
        ("Stokes' law is dimensionally consistent", bool(stokes_units_ok()), "m/s, Re_p dimensionless, matches the model"),
        ("No silent extrapolation", extrapolation_guards_ok(), "out-of-range water and grind raise errors"),
    ]
