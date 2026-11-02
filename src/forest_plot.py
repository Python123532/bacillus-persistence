import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"

def main():
    ps = pd.read_csv("results/per_series.csv")
    pooled = pd.read_csv("results/pooled.csv")
    prim = ps[ps["role"] == "primary"]

    fig, ax = plt.subplots(figsize=(8, 10))
    y = 0
    labels, positions = [], []

    for stratum in ["solution", "substrate", "roots"]:
        g = prim[prim["stratum"] == stratum].sort_values("study")
        for _, r in g.iterrows():
            
            ax.errorbar(r["loss"], y, xerr=[[r["loss"] - r["low"]], [r["high"] - r["loss"]]], fmt="o", color="black", capsize=3)
            labels.append(r["file"].replace(".csv", ""))
            positions.append(y)
            y += 1
        #the pooled row for this stratum (skip if loss is missing):
        p = pooled[pooled["stratum"] == stratum].iloc[0]
        if not np.isnan(p["loss"]):
          ax.errorbar(p["loss"], y, xerr=[[p["loss"] - p["low"]], [p["high"] - p["loss"]]],
          fmt="D", color="firebrick", capsize=4)
          labels.append(f"POOLED {stratum}"); positions.append(y)
        y += 2          # gap between strata

    ax.axvline(0.1, linestyle="--", color="gray")      # equivalence margin
    ax.axvline(0.0, color="lightgray", linewidth=0.8)
    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Loss rate (log10 per week), 90% interval")
    ax.set_xlim(-1.5, 4.5)
    fig.tight_layout()
    fig.savefig("figures/forest.png", dpi=300)

if __name__ == "__main__":
    main()
