# T05 anatomical coding and recorded site: analysis specification

Specified 9 November 2026 after cell-count inspection, before adjusted fitting.

## Decision and estimands

Do not retain the old four-outcome model as an anatomy model: C71.9 is unspecified
coding, C71.8 overlaps sites, and neither is an alternative single anatomical
compartment. Preserve all four groups descriptively. Rebuilt records also have
zero overlapping-lesion outcomes for several nonreference ethnicity categories,
which yields a direction of strictly increasing multinomial likelihood with a
coefficient tending to minus infinity. Record these certificates rather than
pretend a conventional finite maximum exists or increase iterations.

Replace the old Table5 with two explicitly different, exploratory logistic panels:

A. All 10,972 discharges: event1 = non-C719 coding (C710-C718); event0 = C719.
   This is a recorded code-detail contrast, not diagnostic accuracy or a biological
   site model. It includes C718 and does not imply those records have a single site.
B. Only the two operational single-compartment groups: event1 = infratentorial/
   midline C715-C717; event0 = supratentorial C710-C714. Exclude C718 and C719
   explicitly (112 and 4668 records). Expected n6192 with1523 events. This is
   conditional on recorded group availability, not an incidence risk or a correction
   for nonrandom missing site information. C715 is a study-defined midline grouping;
   it is not universally infratentorial.

Both primary models use age group, sex, public/private sector and categorical year.
References: age18-44 (explicit adult reference for pediatric/adult comparisons),
male, private sector, year2015. This differs from the old Table5 age80+ reference
and from T04 age0-17; the reference change must not be hidden. No interactions,
automated variable selection or significance-driven pooling. Ethnicity is omitted
from primary adjustment because sparse source categories undermine uniform site
comparisons; all source levels are preserved descriptively and added in separate
extended full-cohort sensitivity models (Mestizo code6 reference, unknown code9
retained). The smaller primary model is an explicit exploratory specification,
not a claim of adequate causal confounding control.

Do not use death or final LOS to explain recorded anatomy in these models. Do not
use provisional early-year rural/urban labels. Institutional sector and finalized
diagnosis are record attributes; their temporal relation is not established by
these analyses. No causal institutional or biological ethnicity claim follows.

## Predefined sensitivities for both panels

- Resident-only observations, without altering the admission-level primary target.
- Exclude2017/2023 as a legacy-error stress test, not a claim those source years
  are incomplete.
- Restrict to2018-2024; fit core model and then add verified residence on the same
  observations. Reference year becomes2018; do not compare year contrasts as if
  the reference stayed2015.
- Same primary point estimates with record-level HC0 covariance; not patient or
  facility clustering correction.
- Add all source ethnicity categories to the full panel cohort; report sparse
  cells and supplementary profile-likelihood intervals where appropriate. No
  ethnic category is merged to obtain significance or removed based on its OR.
- For panelB only, exclude C715 to assess the operational ventricular/midline
  grouping. Compare C716/C717 with C710-C714; report the changed population.

Check explicit outcome mapping, sample flow, all outcome/predictor marginal cells,
rank, LP complete/quasi separation, fit convergence/warnings, score and observed
information. Any failing model must be labelled invalid/not estimated; do not
publish finite Wald estimates from a failed fit. Binary Firth methods are not
applied to the original unchanged multinomial outcome. If the supported binary
fits are finite, no penalty is required merely to recreate the old procedure.

Report aORs (not aRRRs), conditional Wald intervals, sample/event counts and all
reference categories. No multiplicity correction or confirmatory hypotheses;
comparisons are exploratory. Repeated admissions, unidentified facility dependence,
missing severity/treatment and nonrandom coding remain limitations. No published
multinomial estimate is automatically transferable to either new estimand.

## Reference and precision checks

Re-express the two primary age contrasts as0-17 versus80+ using the fitted covariance
matrix, solely to make the old Table5 reference issue explicit. Those remain new
binary outcome contrasts, not the old aRRRs. Supplementary profile intervals for
sparse extended ethnicity coefficients assess uncertainty; they do not change the
primary predictor specification or the estimand.
