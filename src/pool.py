import numpy as np
import pandas as pd
from scipy import stats
from src.equivalence import verdict

def combine_within(df):
    """df = primary rows for ONE study in ONE stratum.
    Return (loss, se) for the study."""
    w = 1 / df["se"]**2
    loss = sum(w * df["loss"]) / sum(w)
    se = 1 / sqrt(sum(w))

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
    print(per_series["se"].isna().sum())     # how many NaN standard errors?
    print(study_table(per_series).to_string())
  
