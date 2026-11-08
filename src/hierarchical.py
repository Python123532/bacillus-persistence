"""Three-level random-effects model (addition to Amendment 11): series within study within stratum.
loss_ij = mu + u_i + e_ij + sampling error,  u_i ~ N(0, tau2_study),  e_ij ~ N(0, tau2_series).
Fitted by REML. Interval: mu +/- t(k-1) * SE, k = number of studies, 90%."""
import numpy as np
import pandas as pd
from scipy import stats, optimize
from src.equivalence import verdict

def _blocks(df):
    return [(g["loss"].to_numpy(), g["se"].to_numpy() ** 2) for _, g in df.groupby("study")]

def _gls(blocks, t_study, t_series):
    """Generalized least squares mean. Returns (mu, sum of 1'V^-1 1, log det V, residual term)."""
    w = wy = logdet = 0.0
    inv = []
    for y, v in blocks:
        Vi = np.linalg.inv(np.diag(v + t_series) + t_study)
        w += Vi.sum()                    # 1' V^-1 1
        wy += (Vi @ y).sum()             # 1' V^-1 y
        logdet -= np.linalg.slogdet(Vi)[1]
        inv.append((y, Vi))
    mu = wy / w
    rss = sum((y - mu) @ Vi @ (y - mu) for y, Vi in inv)
    return mu, w, logdet, rss

def _neg_reml(log_taus, blocks):
    mu, w, logdet, rss = _gls(blocks, *np.exp(log_taus))
    return 0.5 * (logdet + np.log(w) + rss)

def fit(df, level=0.90):
    """df: one stratum, columns study, loss, se. Returns dict or None if < 2 studies."""
    blocks = _blocks(df)
    k = len(blocks)
    if k < 2:
        return None
    starts = ([-2, -2], [0, -4], [-4, 0])
    best = min((optimize.minimize(_neg_reml, x0, args=(blocks,), method="Nelder-Mead") for x0 in starts),
               key=lambda r: r.fun)
    t_study, t_series = np.exp(best.x)
    mu, w, _, _ = _gls(blocks, t_study, t_series)
    half = stats.t.ppf(1 - (1 - level) / 2, k - 1) / np.sqrt(w)
    return {"k": k, "m": len(df), "loss": mu, "low": mu - half, "high": mu + half,
            "tau2_study": t_study, "tau2_series": t_series, "verdict": verdict(mu - half, mu + half)}

def run(per_series):
    prim = per_series[per_series["role"] == "primary"]
    rows = []
    for stratum, g in prim.groupby("stratum"):
        r = fit(g)
        rows.append({"stratum": stratum, **(r or {"k": g["study"].nunique(), "note": "unpooled (1 study)"})})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    out = run(pd.read_csv("results/per_series.csv"))
    out.to_csv("results/pooled_hierarchical.csv", index=False)
    print(out.to_string())
