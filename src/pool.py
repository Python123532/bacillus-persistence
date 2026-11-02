import numpy as np
import pandas as pd
from scipy import stats
from src.equivalence import verdict

def combine_within(df):
    """df = primary rows for ONE study in ONE stratum.
    Return (loss, se) for the study."""
    w = 1 / df["se"]**2
    loss = sum(w * df["loss"]) / sum(w)
    se = 1 / np.sqrt(sum(w))
    return loss, se

def study_table(per_series):
    primary = per_series[per_series["role"] == "primary"]
    rows = []
    for (stratum, study), g in primary.groupby(["stratum", "study"]):
      loss, se = combine_within(g)
      rows.append({"stratum": stratum, "study": study,
      "n_series": len(g), "loss": loss, "se": se})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    per_series = pd.read_csv("results/per_series.csv")
    print(per_series["se"].isna().sum())            # optional check, can keep
    out = pool_strata(study_table(per_series))      # replaces the old print line
    out.to_csv("results/pooled.csv", index=False)
    print(out.to_string())
  
def dl_pool(x, se, level=0.90):
    """x, se = NumPy arrays, one entry per study.
    Return (mu, low, high, tau2) or None if fewer than 2 studies."""
    k = len(x)
    if k < 2:
        return None
    v = se ** 2
    w = 1 / v
    x_fe = np.sum(w * x) / np.sum(w)
    Q = np.sum(w * (x - x_fe) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0, (Q - (k - 1)) / C)
    w_star = 1 / (v + tau2)
    mu = np.sum(w_star * x) / np.sum(w_star)
    q = np.sum(w_star * (x - mu) ** 2) / (k - 1)
    se_hk = np.sqrt(q / np.sum(w_star))
    t_crit = stats.t.ppf(1 - (1 - level) / 2, k - 1)
    return mu, mu - t_crit * se_hk, mu + t_crit * se_hk, tau2

def pool_strata(studies):
    rows = []
    for stratum, g in studies.groupby("stratum"):
        res = dl_pool(g["loss"].to_numpy(), g["se"].to_numpy())
        if res is None:
            rows.append({"stratum": stratum, "k": len(g), "note": "unpooled (1 study)"})
        else:
            mu, low, high, tau2 = res
            rows.append({"stratum": stratum, "k": len(g), "loss": mu,
                         "low": low, "high": high, "tau2": tau2,
                         "verdict": verdict(low, high)})
    return pd.DataFrame(rows)
