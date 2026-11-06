# Table 3 reconstruction verification

Verified on 6 November 2026 in the local Windows environment. Result: PASS for the reconstructed INEC cohort and the documented resident-population specification. The manuscript PDF remains unchanged.

## Source and calculation checks

The [bibliographic argument and decision register](reconstruction_rationale.md)
link the changes to source definitions, published statistical methods and
declared study choices. This verification establishes computational agreement;
it does not validate diagnoses, resolve patient identity or certify the
independence assumptions in the cited statistical models.

- Rebuilt the denominators and census weights from both SHA-256-verified official population workbooks; checked all 1,111 extracted population and census values against their recorded workbook cells.
- Confirmed 10,972 reconstructed admissions and 963 deaths; the primary resident population contains 10,969 admissions and 963 deaths. Three foreign-resident live discharges are excluded.
- Independently derived completed age, anatomical category, death and residence eligibility from preserved source fields, rather than using the corresponding derived cohort columns.
- Independently aggregated the five primary age groups and 18 narrower age groups; confirmed complete annual populations, positive denominators, and standard weights summing to one. The observed census standard totals 16,938,986; the 2022 annual denominator is 17,715,301.
- Independently reproduced all 400 annual standardized estimates, 80 mean/pooled summaries, 4,600 age-specific estimates and 110 fatality estimates, covering both residence policies and both age schemes.
- Recomputed Fay-Feuer intervals with chi-square quantiles independently of the production gamma-quantile function. Checked Wilson intervals against scipy.stats.binomtest.
- Maximum absolute difference across independently checked rates, limits and variances: 1.6e-14.
- Verified all 110 displayed annual and mean cells, including estimates and both confidence limits; the primary CSV matches its underlying rate evidence.
- All regenerated numeric evidence agrees with committed historical T03 results within relative tolerance 1e-11 and absolute tolerance 1e-12. Input fingerprints in run_metadata.json match the current files.

## Verified mean annual rates per 100,000 residents

| Measure | Estimate | 95% model-based interval |
|---|---:|---:|
| Age-adjusted hospitalization rate | 6.611238 | 6.487228 to 6.737258 |
| Age-adjusted in-hospital death rate | 0.598464 | 0.560971 to 0.638028 |

The mean is the arithmetic mean of ten annual standardized rates. Its interval is computed from the combined weighted counts; annual interval endpoints are not averaged. Pooled admission fatality is 8.779287% (95% Wilson interval 8.264023% to 9.323413%) and is a separate admission-denominator measure.

## Differences from the manuscript Table 3

Compared the actual table on PDF pages 11-12. These are reconstruction changes, not an exact reproduction of the legacy 8,249-admission analysis.

| Cell | Manuscript | Verified reconstruction |
|---|---:|---:|
| 2017 admissions, Total | 0.185 | 7.583 |
| 2017 deaths, Total | 0.060 | 0.758 |
| 2023 admissions, Total | 0.485 | 6.280 |
| 2023 deaths, Total | 0.485 | 0.586 |
| 2024 admissions, Total | 3.631 | 5.784 |
| 2024 admissions, Unspecified | 0.000 | 2.152 |
| Mean annual hospitalization rate | 4.859 | 6.611 |
| Mean annual in-hospital death rate | 0.461 | 0.598 |

The full comparison of 100 annual measure/category cells is in [table3_manuscript_comparison.csv](../outputs/reports/table3_manuscript_comparison.csv). The rebuilt primary table is [table3_rebuilt.md](../outputs/tables/table3_rebuilt.md).

## Interpretation and remaining work

No numerical discrepancy was found in the reconstruction under the documented specification. Its direct standardization follows the weighted age-specific-rate definition in [NCI SEER guidance](https://seer.cancer.gov/seerstat/tutorials/aarates/definition.html); intervals follow [Fay and Feuer (1997)](https://wonder.cdc.gov/controller/pdf/FayFeuerConfidenceIntervals.pdf).

These measure hospital-discharge burden and deaths during admissions, not unique-patient cancer incidence or overall cancer mortality. Intervals assume independent admissions and fixed denominators; repeat admissions, facility clustering and denominator uncertainty are not included. The five broad age groups match the manuscript methods; narrower-band sensitivity results remain available. Manuscript tables, narrative and Figure 1 still require coordinated replacement.
