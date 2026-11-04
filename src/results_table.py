import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"

SHOW_TAU2 = True 

def main():
    p = pd.read_csv("results/pooled.csv")
    rows = []
    for _, r in p.iterrows():
        if r["stratum"] == "solution":
            # one study, unpooled: use Li's own per-series interval
            ps = pd.read_csv("results/per_series.csv")
            li = ps[(ps["stratum"] == "solution") & (ps["role"] == "primary")].iloc[0]
            rows.append(["Solution", "1 (unpooled)", f"{li['loss']:.3f}",
                         f"[{li['low']:.3f}, {li['high']:.3f}]", "-", li["verdict"]])
        else:
            rows.append([r["stratum"].capitalize(), int(r["k"]), f"{r['loss']:.3f}",
                         f"[{r['low']:.3f}, {r['high']:.3f}]", f"{r['tau2']:.3f}", r["verdict"]])
    cols = ["Stratum", "Studies", "Pooled loss\n(log10/wk)", "90% CI", "tau^2", "Verdict"]
    if not SHOW_TAU2:
        cols.pop(4)
        rows = [r[:4] + r[5:] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 2.6))
    ax.axis("off")
    t = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="center")
    t.auto_set_font_size(False); t.set_fontsize(11); t.scale(1, 2)
    fig.text(0.01, 0.02,
             "Pre-registered primary analysis (Amendment 11): inverse-variance within study, "
             "DerSimonian-Laird + Hartung-Knapp across studies.\n"
             "Supported if upper bound < 0.1; rejected if lower bound > 0.1; else inconclusive.",
             fontsize=7, ha="left")
    fig.savefig("figures/results_table.png", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
