# src/run_series.py
import pandas as pd
import os
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
    rows = []  # like an ArrayList<Map<String,Object>>
    for _, m in manifest.iterrows():
        row = {"file": m["file"], "stratum": m["stratum"],
               "tier": m["tier"], "role": m["role"]}
        try:
            t, y = load_series(DATA_DIR + m["file"], m["time_unit"])
            loss, low, high = loss_rate(t, y, 0.90)
            row["n"] = len(t)
            row["loss"] = loss
            row["low"] = low
            row["high"] = high
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
