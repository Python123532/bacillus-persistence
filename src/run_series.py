import os
import pandas as pd
from scipy import stats
from src.equivalence import loss_rate, verdict

DATA_DIR = "data/raw/"
MANIFEST = "data/series_manifest.csv"

def load_series(path, time_unit):
    df = pd.read_csv(path, comment="#")
    t = df["time"].to_numpy()
    y = df["log10_value"].to_numpy()
    if time_unit == "day":
        t = t / 7
    return t, y

def run_all():
    manifest = pd.read_csv(MANIFEST, comment="#")
    rows = []
    for _, m in manifest.iterrows():
        row = {"file": m["file"], "stratum": m["stratum"],
               "tier": m["tier"], "role": m["role"],
               "study": m["file"].split("_")[0]}
        try:
            t, y = load_series(DATA_DIR + m["file"], m["time_unit"])
            loss, low, high = loss_rate(t, y, 0.90)
            t_crit = stats.t.ppf(0.95, len(t) - 2)
            row["n"] = len(t)
            row["loss"] = loss
            row["low"] = low
            row["high"] = high
            row["se"] = (high - low) / (2 * t_crit)
            row["verdict"] = verdict(low, high)
        except ValueError as e:
            row["error"] = str(e)
        rows.append(row)
    out = pd.DataFrame(rows)
    os.makedirs("results", exist_ok=True)
    out.to_csv("results/per_series.csv", index=False)
    return out

if __name__ == "__main__":
    print(run_all().to_string())
