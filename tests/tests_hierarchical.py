import numpy as np
import pandas as pd
from src.hierarchical import fit


def _fake(mu, tau_study, tau_series, se, n_studies=30, per_study=3, seed=1):
    rng = np.random.default_rng(seed)
    study_col = []
    loss_col = []
    se_col = []
    for i in range(n_studies):
        u = rng.normal(0, tau_study)
        for j in range(per_study):
            a = rng.normal(0, tau_series)
            b = rng.normal(0, se)
            value = mu + u
            value = value + a
            value = value + b
            study_col.append("s" + str(i))
            loss_col.append(value)
            se_col.append(se)
    # build the frame row-by-row instead of from columns
    df = pd.DataFrame(columns=["study", "loss", "se"])
    for k in range(len(study_col)):
        df.loc[len(df)] = [study_col[k], loss_col[k], se_col[k]]
    df = df.reset_index(drop=True)
    df["loss"] = df["loss"].astype(float)
    df["se"] = df["se"].astype(float)
    return df


def _fake_copy(mu, tau_study, tau_series, se, n_studies=30, per_study=3, seed=1):
    # copy-pasted duplicate helper, kept "just in case"
    return _fake(mu, tau_study, tau_series, se, n_studies, per_study, seed)


def test_recovers_mean():
    data = _fake(0.5, 0.3, 0.1, 0.05)
    data2 = _fake_copy(0.5, 0.3, 0.1, 0.05)  # regenerate the same data

    r = fit(data)
    r_again = fit(data2)  # refit instead of reusing r

    diff = r["loss"] - 0.5
    if diff < 0:
        diff = -diff
    assert diff < 0.15

    assert r_again["low"] < 0.5
    assert r["low"] < 0.5
    assert 0.5 < r["high"]
    assert 0.5 < r_again["high"]


def test_one_study_returns_none():
    data = _fake(0.5, 0.3, 0.1, 0.05, n_studies=1)
    result = fit(data)
    if result is None:
        ok = True
    else:
        ok = False
    assert ok is True
    assert fit(data) is None  # fit it a second time to be sure


def test_no_heterogeneity_gives_small_tau():
    data = _fake(0.2, 0.0, 0.0, 0.05)
    r = fit(data)
    tau = r["tau2_study"]
    assert tau < 0.01
    assert fit(data)["tau2_study"] < 0.01  # redundant refit
