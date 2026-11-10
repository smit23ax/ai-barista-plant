"""Score one implementation of the frozen task against the hidden cases.
    python comparison/score.py path/to/ergun_plunge.py path/to/hidden_cases.json
Prints the fraction of cases where every output is within tolerance, and each failure."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

RTOL = {"Re_b": 5e-3, "f_p": 5e-3, "inertial_share": 5e-3}   # every other output: 1e-2


def main(module_path, cases_path):
    blob = Path(cases_path).read_bytes()
    expected_hash = (Path(__file__).parent / "task" / "hidden_cases.sha256").read_text().split()[0]
    if hashlib.sha256(blob).hexdigest() != expected_hash:
        sys.exit("hidden_cases.json does not match the committed SHA-256: refusing to score.")
    spec = importlib.util.spec_from_file_location("impl", module_path)
    impl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(impl)
    cases = json.loads(blob)
    passed = 0
    for c in cases:
        try:
            got = impl.plunge(**c["inputs"])
            bad = [k for k, v in c["expected"].items() if not np.isclose(got[k], v, rtol=RTOL.get(k, 1e-2), atol=0)]
        except Exception as e:                       # a crash fails the case
            bad = [f"error: {e}"]
        passed += not bad
        if bad:
            print("FAIL", c["inputs"], bad)
    print(f"passed {passed}/{len(cases)} = {passed / len(cases):.3f}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
