## **1\. Hypotheses (unchanged)**

H1 (persistence): after a single application, the net loss rate of Bacillus in a hydroponic reservoir is practically zero. H2 (mechanism): published data will not clearly separate the dose-driven model (A) from the maintained-level model (B).

## **2\. Scope**

> * Organisms: genus Bacillus only. Relevance tiers: Tier 1, B. velezensis and B. amyloliquefaciens; Tier 2, other members of the B. subtilis group; Tier 3, B. cereus group and other Bacillus. Primary analysis uses Tiers 1 and 2; Tier 3 is added in a labeled secondary analysis.  
> * Systems: hydroponic nutrient solution (NFT, DWC, aquaponics, static), soilless substrates (rockwool, peat, coir), and hydroponic root colonization. Substrate and sterile-solution studies form labeled strata.  
> * Persistence series: counts of an added Bacillus at three or more time points after inoculation. Yield series: plant yield at three or more inoculum doses, or single versus repeated inoculation.  
> * A series is one organism by one system by one sample type (for example reservoir total, reservoir spores, roots) by one treatment arm.  
> * Target: at least 10 persistence series, 20 or more preferred. If fewer qualify after the search is exhausted, all qualifying series are reported and pooled estimates are labeled exploratory.

## **3\. Data quality score (0 to 7, one point each)**

Five or more time points; error reported with n; values from a table or raw data; strain-specific counting (marker, qPCR or strain-selective medium); planted, non-sterile system; known dose with a sample within 24 h of dosing; Tier 1 or 2\. Analyses are repeated on series scoring 4 or more.

## **4\. Models**

Persistence: constant, log-linear, Weibull, log-linear with tail, biphasic, logistic with loss, two-pool, never more than n minus 2 parameters for n points. Plant side: Model A, yield as a function of peak concentration; Model B, yield as a function of time above a threshold; Model C (new), yield as a function of cumulative dose.

## **5\. Decision rules (unchanged)**

H1 supported only if the upper bound of the 90% confidence interval of the net loss rate is below 0.1 log CFU/mL per week (equivalence test); rejected if the interval lies entirely above 0.1; otherwise inconclusive. A model is favored only if its AICc is lower than the next by more than 4\. The verdict is reported for the primary set, the secondary set, and the high-quality subset, whatever its direction.

## **6\. Search**

PubMed, Europe PMC, and Google Scholar, with the search strings recorded in the Dataset Log. Every record found, screened, excluded (with reason) and included is logged for a PRISMA 2020 flow diagram. Studies are included or excluded only by the criteria above, regardless of the direction of their results.

## Amendments (append only)

### Amendment 1 (Decided 2026-10-29, committed 2026-10-31): Piecewise model for rise-then-fall series

- **Problem:** Some series boom, then bust(Tetteh's rockwool was up about 1.5 log, then down about 2 log). A straight line averages growth and loss, losing data validity.
- **Changes:** A broken-stick model will be added, and for series that rise first, H1 uses the slope after the peak.
- **Sensitivity:** I'll also report the standard log-linear slope. 'Rises first' will be defined objectively, through the fitted breakpoint as an example, but definitely not through pure eyeballing.

### Amendment 2 (2026-10-31): H1 applied per system stratum

- **Problem:** H1 is worded for a hydroponic reservoir, which doesn't reflect all the data(some of it comes from solution, substrate, and roots). Pooling lets a very precise potting-mix series(Yan) dominate.
- **Changes:** H1 is tested separately per stratum, with each verdict being reported. This is because different things happen in each place, like water washout and root growth diluting counts.
- **Sensitivity:** Also report a pooled estimate, labeled as pooled.

### Amendment 3 (2026-10-31): MBI600 tier

- **Problem:** Samaras' genome analysis says *Bacillus subtilis*, but the *Bacillus velezensis* reclassification isn't verified.
- **Changes:** tier it 2. The primary analysis relies on Tiers 1 and 2 anyway, so quality point 7 counts both. This choice barely moves the primary set, and only really matters for a Tier-1-only check.
- **Sensitivity:** re-run with MBI600 as Tier 1.
  
### Amendment 4 (2026-10-31): Xu 2022 arm selection

- **Problem:** One unplanted lab study has about 20 arms(pH levels, nutrient additions), that aren't independent, so they'd swamp the substrate stratum.
- **Changes:** Only the control arm(CK) will be used.
- **Sensitivity:** All arms, with a random effect by study.
  
### Amendment 5 (2026-10-31): Jin 2026 repeated dosing

- **Problem:** H1 concerns a *single* application, but Jin gave 3 drenches 2 days apart, with an ambiguous time zero.
- **Changes:** It's excluded from H1 pooling and reported separately.
- **Sensitivity:** I'll report its own post-peak slope.

### Amendment 6 (2026-10-31): Tetteh 2026 arm selection

- **Problem:** There are 6 arms in Table 3-3, with 4 of them showing how *Bacillus subtilis* recovers in an environment exposed to other bacteria, like Salmonella. Only 2 of them are controls(pathogen arms measure Bacillus under competition, a different question from pure inoculant persistence), so only *Bacillus subtilis* is included. Counting all 6 confounds the data by introducing competition with other bacteria present in the rockwool/peat.
- **Changes:** Only the 2 control arms (rockwool and peat moss, no pathogen) are used in the primary analysis.
- **Sensitivity:** Report the other 4 pathogen arms separately.

### Amendment 7 (2026-10-31): Xu 2022 measurement method

- **Problem:** Table 6 gives two measurements of the same sample, and they measure different things (viable cells vs DNA copies, which can include dead cells). The other series is of a viable count, so the plate counts are comparable measurements, with a goal being not to pool them both together.
- **Changes:** Plate counts will be used as the primary series, using the CK row from Table 6. All other arms are to be excluded from this. Plate counts is chosen because it matches the unit in the other series.
- **Sensitivity:** I'll also report the measurements from qPCR, and if the 2 disagree on the H1 verdict, I'll report both verdicts and say the result depends on the method.

### Amendment 8 (2026-10-31): Pasura 2008 GB03 Classification

- **Problem:** The thesis calls GB03 *Bacillus subtilis*, but the 2026 *J Bacteriol* review classes it as *Bacillus velezensis*. The tier matters since if its Tier 1 it'll be part of the Tier 1 only robustness check.
- **Changes:** It will be reclassified to *Bacillus velezensis* following the review, especially since both use the exact same strain name which had not been changed. This differs from the MBI600 amendment because GB03’s reclassification is documented in a dedicated review, while MBI600’s was not verified.
- **Sensitivity:** I'll also report the measurements if it is treated as Tier 2, going with how the thesis names it. Then, I'll report whether the Tier-1-only result differs between the two tierings.

### Amendment 9 (2026-11-1): Tetteh 2026 QST 713 Classification

- **Problem:** The paper calls QST 713 *Bacillus subtilis*, but as per a later genome sequencing paper, it is now *Bacillus velezensis*. The tier matters since if it is Tier 1 it'll be part of the Tier 1 only robustness check.
- **Changes:** It will be reclassified to *Bacillus velezensis* following a later paper, Pandin 2018, which uses the same designation. This differs from the MBI600 amendment because QST 713’s reclassification is documented in a later paper, while MBI600’s was not verified.
- **Sensitivity:** I'll also report the measurements if it is treated as Tier 2, going with how the dissertation names it. Then, I'll report whether the Tier-1-only result differs between the two tierings.

### Amendment 10 (2026-11-01): Piecewise model application (refines Amendment 1)

- **Problem:** Amendment 1 says the piecewise model is "defined objectively through the fitted breakpoint", but it does not give the exact criterion.
- **Changes:** The piecewise model is used only if the series has at least 6 points and the piecewise model is favored over log-linear by AICc > 4. The model has 4 parameters, so it needs at least 6 points under the n - 2 rule, which makes the Tetteh and Yan root series the only ones that qualify by size. For these series, H1 uses the post-peak slope. Breakpoints may only fall where each segment has enough points, like at least 2 up to and including the breakpoint and 3 after it. If this isn't the case, the search will be restricted and will revert to log-linear. All series that do not meet the criterion use the plain log-linear slope over the whole series, even if they appear to rise first.
- **Sensitivity:** For every series, I will also report the plain log-linear slope and the verdict it gives. If the two verdicts differ, I will report both and state that the result depends on the model.

### Amendment 11 (2026-11-01): Series pooling within a stratum

- **Problem:** Amendment 2 says verdicts are per stratum, but not how the series combine into one estimate.
- **Changes:**
  - Series included: Primary role in the manifest csv only.
  - Unit of analysis: One paper or thesis, for Samaras they will be weighed as 2 individual papers.
  - Within a study: Series from one study are combined before pooling via inverse-variance weighting.
  - Across studies: Random effects model, DerSimonian-Laird variance, Hartung-Knapp intervals, confidence level about 90%
  - Fewer than 2 studies in a stratum:
  - Verdict: upper bound below 0.1 means supported, whole interval above means rejected, otherwise inconclusive. Keeps everything consistent.
  - Per-series verdicts are recorded regardless.
  - Limitation: The pooled estimate is exploratory because not all series within a study are independent. A study-level model fitted at the regional stage is an added analysis and does not replace this rule.
- **Sensitivity:** For each stratum, a leave-one-out study analysis and unweighted mean of series slopes will be reported. If either of these diverge from the main pooled verdict, I'll report all verdicts and state the result depends on how it's pooled.
