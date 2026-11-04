import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"

STRATA = ["solution", "substrate", "roots"]

def main():
    ps = pd.read_csv("results/per_series.csv")
    is_prim = ps["role"] == "primary"
    prim = ps[is_prim].groupby(["study", "stratum"]).size()
    other = ps[~is_prim].groupby(["study", "stratum"]).size()   # sensitivity + secondary
    studies = sorted(ps["study"].unique())

    fig, ax = plt.subplots(figsize=(6, 0.5 * len(studies) + 1.5))
    for i, s in enumerate(studies):
        for j, st in enumerate(STRATA):
            n1, n2 = prim.get((s, st), 0), other.get((s, st), 0)
            if n1 or n2:
                color = "steelblue" if n1 else "lightgray" 
                ax.add_patch(plt.Rectangle((j - 0.45, i - 0.4), 0.9, 0.8,
                                           color=color, alpha=0.8 if n1 else 0.6))
                ax.text(j, i, f"{n1}" + (f" (+{n2})" if n2 else ""),
                        ha="center", va="center", fontsize=10)
    ax.set_xticks(range(len(STRATA)))
    ax.set_xticklabels([s.capitalize() for s in STRATA])
    ax.set_yticks(range(len(studies))); ax.set_yticklabels(studies)
    ax.set_xlim(-0.5, len(STRATA) - 0.5); ax.set_ylim(len(studies) - 0.5, -0.5)
    ax.xaxis.tick_top()
    ax.set_title("Primary series per study (+ sensitivity/secondary)", fontsize=10, pad=24)
    fig.tight_layout()
    fig.savefig("figures/evidence_map.png", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
