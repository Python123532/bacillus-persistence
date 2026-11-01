import os
import pandas as pd
from src.run_series import load_series, DATA_DIR
from src.piecewise import compare

QUALIFYING = [
    "tetteh2026_peatmoss_control.csv",
    "tetteh2026_rockwool_control.csv",
    "yan2003_roots_dose6.csv",
    "yan2003_roots_dose7.csv",
    "yan2003_roots_dose8.csv",
]

def run_piecewise():
    rows = []
    for f in QUALIFYING:
        t, y = load_series(DATA_DIR + f, "day")
        delta, tb, post_slope = compare(t, y)
        rows.append({
            "file": f,
            "n": len(t),
            "delta_aicc": delta,
            "favored": delta > 4,
            "breakpoint_wk": tb,
            "post_slope": post_slope,
        })
    out = pd.DataFrame(rows)
    os.makedirs("results", exist_ok=True)
    out.to_csv("results/piecewise.csv", index=False)
    return out

if __name__ == "__main__":
    print(run_piecewise().to_string())
