# Bacillus persistence in soilless and hydroponic systems: a computational analysis of published data

The cartridge project assumes that a maintained Bacillus population in the reservoir is needed. This analysis screens that assumption: if published data show that the population persists after a single dose, or that the benefit does not require a maintained level, a cartridge may not be justified.

**Status:** preliminary, school fair version. Results below are exploratory until the regional-fair analysis.

## Pre-registration

Hypotheses, scope, models and decision rules are in `prereg/`, with 13 dated amendments appended. The dataset was frozen on 2026-11-01 at 02:11 (before any model was fitted to the real data); see the commit history.

## Repository layout

| Path | Contents |
|---|---|
| `prereg/` | Pre-registration v2 and the amendments (append-only) |
| `data/raw/` | One CSV per persistence series (38 files) |
| `data/series_manifest.csv` | Stratum, tier, role and time unit for each series |
| `data/raw_yield/` | Yield (dose-response) data, not persistence series |
| `data/digitization/` | Raw WebPlotDigitizer exports and calibration screenshots |
| `data/checks/` | Published values used only to check my pipeline |
| `src/` | Analysis code |
| `tests/` | Tests, run on synthetic data |

## Data format

Each series file starts with `#` header lines (source, strain and tier, system, unit, design, notes), then the columns:

`time, time_unit, value_raw, log10_value, sd, n`

Values come from a table (typed) or a figure (digitized with WebPlotDigitizer, error about +/-0.1-0.2 log). `sd` and `n` are blank unless the paper reports them. Units differ between series (per g substrate, per g root, per cm root, per mL solution), so slopes are compared only within a stratum.

## Manifest columns

- `stratum`: solution, substrate or roots (analyzed separately)
- `tier`: 1 (B. velezensis / amyloliquefaciens), 2 (rest of the B. subtilis group), 3 (B. cereus group and other Bacillus)
- `role`: primary, secondary (Tier 3) or sensitivity
- `time_unit`: day or week

## Decision rules (summary)

In general, a cartridge is justified only if the population declines after one dose (H1 rejected) and the benefit needs a maintained level (Model B favored). If H1 is supported, or Model B isn’t favored, the cartridge isn’t justified by these data

***H1(persistence): does the population stay put after one dose?***

- For each series, a log-linear model will be applied, counted against time in weeks. The loss rate would be -*b*, with *b* being the slope in **log10** units
- A confidence interval of 90% will be calculated
- This criterion is satisfied if the interval's upper bound is   0.1 log per week. The loss is practically zero, and the interval has to *prove* it’s small
- Rejected if the whole interval is above 0.1
- Inconclusive otherwise, including when the interval just includes 0 but is wide

***Model comparison (H2): does yield follow the initial dose or the maintained level?***

- Models A (peak concentration), B (time above a threshold), C (cumulative dose)
- A model is only favored if its AICc is lower than the others’ by more than 4. Otherwise, you say the data can’t separate them

***Amendments***

- H1 is tested per stratum (solution, substrate, roots), and pooled by study with random effects
- For series that rise first, the loss rate uses the post-peak slope (piecewise model), if the criterion in Amendment 10 is met
- Series are primary, secondary or sensitivity, and the sensitivity results are reported either way

## How to run

TBD

## Limitations

- Thin solution stratum: only one primary series (Li), so H1 for hydroponic reservoirs can’t be settled
- Few studies per stratum (about 4), so pooled intervals are wide and verdicts are often inconclusive
- Heterogeneous measurements: plating versus qPCR, per mL, per g and per cm, and some series with only 3 or 4 points and no day-0 sample
- Digitization error: about ±0.1–0.2 log for figure data. The table series are exact
- Incomplete search: several databases weren’t reachable (Web of Science, Scopus, CAB Abstracts, ProQuest, CNKI), so the set is “studies found in the databases searched”.
- Strain classification choices: MBI600, GB03 and QST 713 tiers rest on documented but debatable taxonomy, with sensitivity runs
- Published data only: no new measurements, so it’s a screen and not a test
