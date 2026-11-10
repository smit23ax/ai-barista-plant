"""Known-variable tables for the degree-of-freedom analyses: one per unit, every row complete, values tied to code."""
import inspect

from plant import physics as ph
from plant.known import known_variables
from plant.steps import UNITS


def test_every_unit_has_known_rows():
    k = known_variables()
    assert set(k) == set(UNITS)
    for name, rows in k.items():
        assert rows, name
        for row in rows:
            assert len(row) == 5 and all(row), (name, row)


def test_plunge_rows_match_function_defaults():
    defaults = {n: p.default for n, p in inspect.signature(ph.plunge).parameters.items()}
    rows = {r[0]: r[2] for r in known_variables()["Plunge filtration (F-101)"]}
    assert rows["t_p"] == f"{defaults['plunge_time']:.3g}"
    assert rows["rho_b"] == f"{defaults['rho_bulk']:.3g}"
    assert rows["epsilon"] == f"{defaults['eps_bed']:.3g}"
