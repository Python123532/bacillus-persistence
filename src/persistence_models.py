"""Fit the pre-registered persistence model set (section 4, Amendments 1/10) to every series.
A model is fitted only if its parameter count k <= n - 2. AICc uses k without the variance
term, as in piecewise.py. A model is 'favored' over log-linear only if dAICc > 4.
All models are written for y = log10 count, t = weeks."""
import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from src.run_series import load_series

def constant(t, a):
    return np.full_like(t, a, dtype=float)

def log_linear(t, y0, b):
    return y0 + b * t

def weibull(t, y0, delta, p):                     # Mafart 2002
    return y0 - (t / delta) ** p

def log_linear_tail(t, y0, k, yres):              # Geeraerd 2000, no shoulder
    n0, nres = 10 ** y0, 10 ** yres
    return np.log10((n0 - nres) * np.exp(-k * t) + nres)

def logistic_loss(t, y0, r, yk):                  # dC/dt = rC(1 - C/K'), r = mu - k
    c0, kp = 10 ** y0, 10 ** yk
    return np.log10(kp / (1 + (kp / c0 - 1) * np.exp(-r * t)))

def biphasic(t, y0, f, k1, k2):                   # Cerf 1977
    return y0 + np.log10(f * np.exp(-k1 * t) + (1 - f) * np.exp(-k2 * t))

def two_pool(t, y0, k1, m, k2):                   # active cells die (k1) or form spores (m); spores decay (k2)
    a = k1 + m
    if abs(a - k2) < 1e-9:
        k2 = k2 + 1e-9
    n0 = 10 ** y0
    active = n0 * np.exp(-a * t)
    spores = m * n0 / (a - k2) * (np.exp(-k2 * t) - np.exp(-a * t))
    return np.log10(np.clip(active + spores, 1e-300, None))

def models(t, y):
    span = max(t.max(), 1e-6)
    y0, ymin, ymax = y[0], y.min(), y.max()
    # name: (function, start values, lower bounds, upper bounds)
    return {
        "constant": (constant, [y.mean()], [-np.inf], [np.inf]),
        "log_linear": (log_linear, [y0, 0.0], [-np.inf, -np.inf], [np.inf, np.inf]),
        "weibull": (weibull, [y0, span / 2, 1.0], [-np.inf, 1e-6, 0.05], [np.inf, 1e3, 10]),
        "log_linear_tail": (log_linear_tail, [y0, 0.5, ymin - 0.1], [ymin - 1, 0, -5], [ymax + 5, 50, ymax]),
        "logistic_loss": (logistic_loss, [y0, -0.5, ymax], [-5, -20, -5], [20, 20, 20]),
        "biphasic": (biphasic, [y0, 0.9, 1.0, 0.05], [-np.inf, 1e-6, 0, 0], [np.inf, 1 - 1e-6, 50, 50]),
        "two_pool": (two_pool, [y0, 0.5, 0.1, 0.05], [-np.inf, 0, 0, 0], [np.inf, 50, 50, 50]),
    }

def aicc(rss, n, k):
    if n - k - 1 <= 0:
        return np.nan                              # correction undefined
    return n * np.log(rss / n) + 2 * k + 2 * k * (k + 1) / (n - k - 1)

def fit_series(t, y):
    n = len(t)
    out = {}
    for name, (f, p0, lo, hi) in models(t, y).items():
        k = len(p0)
        if k > n - 2:
            continue
        try:
            p, _ = curve_fit(f, t, y, p0=p0, bounds=(lo, hi), maxfev=20000)
            rss = max(np.sum((y - f(t, *p)) ** 2), 1e-12)
            out[name] = (k, rss, aicc(rss, n, k))
        except (RuntimeError, ValueError):
            out[name] = (k, np.nan, np.nan)
    return out

def run_all():
    manifest = pd.read_csv("data/series_manifest.csv", comment="#")
    rows = []
    for _, m in manifest.iterrows():
        t, y = load_series("data/raw/" + m["file"], m["time_unit"])
        fits = fit_series(t, y)
        base = fits["log_linear"][2] if "log_linear" in fits else np.nan
        row = {"file": m["file"], "stratum": m["stratum"], "role": m["role"], "n": len(t),
               "models_fitted": ";".join(fits)}
        for name, (k, rss, a) in fits.items():
            row[f"aicc_{name}"] = a
        valid = {k_: v[2] for k_, v in fits.items() if not np.isnan(v[2])}
        if valid:
            best = min(valid, key=valid.get)
            row["best"] = best
            row["dAICc_vs_log_linear"] = base - valid[best] if best != "log_linear" else 0.0
            row["favored_over_log_linear"] = bool(best != "log_linear" and base - valid[best] > 4)
        rows.append(row)
    out = pd.DataFrame(rows)
    os.makedirs("results", exist_ok=True)
    out.to_csv("results/persistence_models.csv", index=False)
    return out

if __name__ == "__main__":
    r = run_all()
    print(r[["file", "role", "n", "models_fitted", "best", "dAICc_vs_log_linear", "favored_over_log_linear"]].to_string())
