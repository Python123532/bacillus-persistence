import numpy as np
from scipy import stats
from src.run_series import load_series, DATA_DIR

FILES = [
    "pasura2008_gb03_2004_premier_brk.csv",
    "pasura2008_gb03_2004_premier_hp.csv",
]

def main():
    ts, ys = [], []
    for f in FILES:
        t, y = load_series(DATA_DIR + f, "week")   # TODO: confirm unit (check the manifest)
        ts.append(t)
        ys.append(y)
    t_all = np.concatenate(ts)
    y_all = np.concatenate(ys)
    fit = stats.linregress(t_all, y_all)
    print(f"slope = {fit.slope:.3f} log10/wk")
    print(f"R^2   = {fit.rvalue ** 2:.2f}")
    print(f"n     = {len(t_all)}")

if __name__ == "__main__":
    main()
