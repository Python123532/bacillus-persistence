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

if __name__ == "__main__":
    main()
