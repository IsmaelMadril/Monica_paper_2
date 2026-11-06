# T04 mortality association specification

Specified 6 November 2026, before fitting the rebuilt-cohort models.

The outcome is death during a recorded C71 admission (`death=1`), with live discharge
as zero. The unit is a discharge record, not a unique patient. The aim is descriptive
adjusted association, not causal effects or a clinical prediction tool.

## Primary analysis

Use all 10,972 audited admissions and all ten years, including foreign residents:
this is an admission-level outcome model, not a resident-population rate. Unknown
outcomes or missing required covariates must be reported and cannot be silently
removed. Use age group, sex, source ethnicity code, public/private sector, corrected
anatomy and categorical discharge year. No automated significance-based selection
or interactions. Anatomical category and calendar year are recorded at discharge;
this is not a claim that every adjustment variable was measured at admission.
Reference categories: age 0–17, male, Mestizo ethnicity (source
code 6), private sector, supratentorial anatomy, and year 2015. Source ethnicity code
9 remains an explicit unknown category; codes 2/3/4 remain distinct, with sparse
estimates flagged. Reference selection does not imply a normative clinical baseline.

Exclude final length of stay from the primary model because death/discharge
contributes to determining its duration. Exclude rural/urban residence from the
all-year primary model because 2015–2017 labels are provisional. Include residence
only in a verified-year sensitivity model. Do not infer baseline disease severity
from final stay length or recorded anatomical specificity.

Fit unpenalized logistic maximum likelihood if the data support a finite solution.
Check design rank, complete/quasi separation via linear programming, coefficient
convergence, score and observed information. If separation or unresolved fit failure
occurs, stop primary output and report it before selecting a justified penalized
alternative; never conceal a warning or simply raise the iteration cap. Report
conventional observed-information Wald intervals, with record-level independence
assumed. Robust single-record HC0 covariance is a sensitivity check, not a remedy
for unobserved repeated-patient clustering. Do not fabricate unique facility or
patient identifiers from institutional descriptors or province.

## Predefined sensitivities

1. Resident-only cohort, comparable to the T03 resident population.
2. Exclude 2017 and 2023 together as a legacy-year stress test, not the primary
   analysis: the reconstructed source records do not justify deleting them.
3. Verified years 2018–2024: fit the core covariates, then add residence area on
   the same rows to distinguish year restriction from the residence adjustment.
4. Add final LOS categories to the full cohort only as a post-outcome descriptive
   model; no protective or causal interpretation.
5. Restrict to known ethnicity, preserving source categories; compare with the
   explicit unknown-category primary analysis.
6. Record-level HC0 covariance for the same primary fit; cannot address dependence
   by patient/facility. No province clustering is presented as facility clustering.

Produce marginal outcome counts, crude odds ratios, adjusted ORs, intervals,
diagnostics, fit warnings and model sample sizes. Quantify coefficient shifts across
sensitivities. Do not judge model quality or effects solely by statistical significance.
No train/test split, AUC target or claim of predictive validation is part of T04.

The supplied original SAV/SPV/XLSX package is complete. Legacy output examination is
separate from reconstruction and must distinguish decoded evidence from inference.

## Supplementary sparse-level interval check

After the planned sparse-level checks identified six levels with fewer than ten
deaths, supplementary profile-likelihood intervals were calculated for those
levels. The primary table retains consistently labelled Wald intervals; profile
intervals are supplied separately. This changes the uncertainty assessment, not
the selected predictors or source categories.
