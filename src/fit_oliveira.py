import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

PATH = "data/raw_yield/oliveira2023_fig2C_shoot_fresh_mass.csv"

def model(d, Y0, a, d_star):
    return Y0 + a * d * np.exp(-d / d_star)
    ...

def main():
    df = pd.read_csv(PATH, comment="#")
    d = df["dose_e3_cfu_per_ml"].to_numpy(dtype=float)
    y = df["shoot_fresh_mass_g"].to_numpy(dtype=float)
    popt, pcov = curve_fit(model, d, y, p0=[313, 5, 30])
    #p0 = starting guess for (Y0, a, d_star); curve_fit searches from there
    errs = np.sqrt(np.diag(pcov))   # standard error of each parameter
    Y0, a, d_star = popt
    print(f"Y0     = {Y0:.1f} +/- {errs[0]:.1f} g")
    print(f"a      = {a:.2f} +/- {errs[1]:.2f}")
    print(f"d_star = {d_star:.1f} +/- {errs[2]:.1f} (x10^3 CFU/mL)")
    peak = model(d_star, *popt)
    gain = (peak - Y0) / Y0 * 100
    print(f"peak yield = {peak:.1f} g at dose {d_star:.1f}, {gain:.0f}% over fitted Y0")
    print(f"gain over measured control = {(peak - y[0]) / y[0] * 100:.0f}%")
    rss = np.sum((y - model(d, *popt)) ** 2)
    print(f"RSS = {rss:.0f}")

if __name__ == "__main__":
    main()
    
