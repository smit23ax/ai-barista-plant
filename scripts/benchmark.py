"""Re-run the strategy benchmark shown in the app and save plant/benchmark.json.
Usage: python scripts/benchmark.py   (takes a few minutes on a laptop)"""
import json
import os
import sys
import warnings
from pathlib import Path

os.environ.setdefault("PYTHONHASHSEED", "0")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
warnings.filterwarnings("ignore")          # sklearn GP convergence notes are expected on tiny data sets
from plant import ai

BUDGET, SEEDS = 12, 20
results = {}
for strategy in ["ai", "ofat", "random"]:
    results[strategy] = []
    for seed in range(SEEDS):
        results[strategy].append(ai.run_campaign(strategy, BUDGET, seed)[1])
        print(f"{strategy}: seed {seed + 1}/{SEEDS}", flush=True)
out = Path(__file__).resolve().parents[1] / "plant" / "benchmark.json"
out.write_text(json.dumps({"budget": BUDGET, "seeds": SEEDS, "results": results}, indent=1))
print("saved", out)
