import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from src.fit_oliveira import model, PATH

plt.rcParams["font.family"] = "Arial"

def main():
    df = pd.read_csv(PATH, comment="#")
    d = df["dose_e3_cfu_per_ml"].to_numpy(dtype=float)
    y = df["shoot_fresh_mass_g"].to_numpy(dtype=float)
    popt, pcov = curve_fit(model, d, y, p0=[313, 5, 30])
    Y0, a, d_star = popt
    dd = np.linspace(0, 70, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(dd, model(dd, *popt), color="firebrick", label="Fitted curve")
    ax.scatter(d, y, color="black", zorder=3, label="Digitized data (Oliveira 2023)")
    ax.axvline(d_star, linestyle="--", color="gray")
    peak_y = model(d_star, *popt)
    ax.annotate(f"peak ~ {d_star:.0f} x10$^3$ CFU/mL",
                xy=(d_star, peak_y), xytext=(d_star + 12, peak_y - 25),
                arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("Dose (x10$^3$ CFU/mL)")
    ax.set_ylabel("Shoot fresh mass (g per plant)")
    ax.legend()
    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/oliveira.png", dpi=300)

if __name__ == "__main__":
    main()
