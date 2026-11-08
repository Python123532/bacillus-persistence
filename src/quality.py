"""Quality score (pre-registration section 3) and the pre-registered re-run on series scoring >= 4.
Run only after every 'check' cell in data/quality_scores.csv has been verified against the paper."""
import os
import pandas as pd
from src.pool import study_table, pool_strata

THRESHOLD = 4

def load_scores():
    q = pd.read_csv("data/quality_scores.csv", comment="#")
    q["score"] = q[[f"q{i}" for i in range(1, 8)]].sum(axis=1)
    return q

def main():
    q = load_scores()
    ps = pd.read_csv("results/per_series.csv")
    missing = set(ps["file"]) - set(q["file"])
    if missing:
        raise ValueError(f"no score for: {missing}")
    ps = ps.merge(q[["file", "score"]], on="file")
    os.makedirs("results", exist_ok=True)
    ps[["file", "stratum", "role", "score"]].to_csv("results/quality_scores.csv", index=False)
    high = ps[ps["score"] >= THRESHOLD]
    res = pool_strata(study_table(high))
    res.to_csv("results/pooled_high_quality.csv", index=False)
    print(ps[["file", "role", "score"]].to_string())
    print("\nPRIMARY SERIES WITH SCORE >= 4, POOLED\n", res.to_string())

if __name__ == "__main__":
    main()
