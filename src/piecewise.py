import numpy as np

def aicc(rss, n, k):
    return n*np.log(rss/n) + 2*k + 2*k*(k+1)/(n-k-1)

def fit_hinge(t, y, tb):
    col3 = np.maximum(0, t - tb)               # 0 before tb, ramps up after
    X = np.column_stack([np.ones(len(t)), t, col3])
    coefs = np.linalg.lstsq(X, y, rcond=None)[0]   # [a, b1, b2]
    resid = y - X @ coefs                          # X @ coefs = fitted values
    rss = np.sum(resid**2)
    return coefs, rss, X
   

def candidate_breaks(t):
    return np.linspace(t[1], t[-3], 200, endpoint=False)

def best_hinge(t, y):
    best = None
    for tb in candidate_breaks(t):
        coefs, rss, X = fit_hinge(t, y, tb)
        if best is None or rss < best[2]:
            best = (tb, coefs, rss, X)
    return best

def compare(t, y):
    n = len(t)

    # 1. Plain line: np.polyfit(t, y, 1) returns [slope, intercept]
    slope, intercept = np.polyfit(t, y, 1)
    fitted = slope * t + intercept          # predicted y for every t
    rss_line = np.sum((y - fitted) ** 2)    # same RSS idea as before

    tb, coefs, rss_hinge, X = best_hinge(t, y)

    aicc_line  = aicc(rss_line,  n, 2)
    aicc_hinge = aicc(rss_hinge, n, 4)
    delta = aicc_line - aicc_hinge

    return delta, tb, coefs[1] + coefs[2]

if __name__ == "__main__":
    from src.run_series import load_series
    t, y = load_series("data/raw/tetteh2026_peatmoss_control.csv", "day")
    print(compare(t, y))
