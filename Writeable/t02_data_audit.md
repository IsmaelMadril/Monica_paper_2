# T02 — Admission reconstruction and data audit

Audit date: 23 October 2026. **The cohort has been rebuilt from official annual INEC SPSS releases, rather than repaired by editing the supplied SAV.** The reconstructed C71.0–C71.9 cohort contains **10,972 discharge records: 963 deaths and 10,009 live discharges**. These supersede the legacy dataset counts for the next analysis stage; they are not yet replacement manuscript results. Rates and regressions must be recalculated in T03–T05.

## Inputs and reproducibility

Official SPSS files were obtained for every year 2015–2024. The download URLs, access timestamps, byte sizes and SHA-256 hashes are in [the source manifest](../provenance/inec_download_manifest.csv). Archived release pages are stored locally under `data/raw/inec_discovery_2026-10-23/`. Releases for 2015–2023 are linked from their annual INEC pages; 2024 is linked from the [current operation page](https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios/). Separate dictionary archives were downloaded for 2018–2024; the annual SAV variable and value labels provide additional codebook evidence for all years. Early-year official syntax archives are recorded separately in `provenance/inec_syntax_manifest.csv`.

The annual files contain 1,161,044; 1,128,004; 1,143,765; 1,164,659; 1,195,311; 907,515; 1,038,235; 1,130,603; 1,170,813; and 1,132,667 national records, respectively. These are source-file row counts, not C71 admissions.

Run, in order:

```sh
source .venv/bin/activate
pip install -r requirements.txt
python scripts/freeze_inputs.py --verify
# Only needed when restoring source downloads on a new machine:
python scripts/acquire_inec.py
python scripts/acquire_early_dictionaries.py
python scripts/extract_inec.py
python scripts/audit_admissions.py
python -m unittest discover -s tests -v
```

The generated extract is `data/processed/admissions_c71_audited.csv`. Each admission has a source-year/source-row key that identifies its position in the downloaded national file; this is not a patient identifier. Inputs, extracted annual SAV files and individual-level outputs remain ignored by Git. Aggregate audit tables and schemas are under `provenance/t02/` and can be version controlled.

## Selection and retention decisions

1. Read the official raw `cau_cie10` discharge-diagnosis code, without converting it to its value label. Trim surrounding whitespace, uppercase it and remove the decimal point.
2. Retain only a full match to `C71[0-9]`: C710 through C719. Do not include C79 secondary brain lesions, benign/uncertain neoplasms or broader CNS codes. No age or sex restriction is applied.
3. Preserve every eligible record, including repeated or identical observed attributes. No patient-level deduplication is possible. Missing covariates do not remove an otherwise eligible discharge.
4. Preserve source fields and add explicitly coded derived variables. Retain unknown ethnicity, foreign residence and any invalid covariate as flags rather than inventing values.
5. Retain all ten years in the reconstructed cohort. The source records do not support removing 2017/2023 as unusually incomplete national years on the basis of the supplied subset.

[Selection flow](../provenance/t02/selection_flow.csv) reports national input rows, C71-prefix rows, eligible codes, missing diagnoses, other diagnoses and exclusions after selection. There were no post-selection exclusions. This is a fresh source-file flow; the historical flow into the supplied 8,249-record dataset is unavailable.

## Annual reconciliation

| Year | Legacy admissions | Reconstructed admissions | Legacy deaths | Reconstructed deaths | Reconstructed live discharges |
|---|---:|---:|---:|---:|---:|
| 2015 | 1,013 | 1,073 | 91 | 97 | 976 |
| 2016 | 982 | 1,057 | 88 | 95 | 962 |
| 2017 | 31 | 1,221 | 10 | 113 | 1,108 |
| 2018 | 1,044 | 1,148 | 95 | 104 | 1,044 |
| 2019 | 1,096 | 1,239 | 92 | 103 | 1,136 |
| 2020 | 932 | 942 | 75 | 75 | 867 |
| 2021 | 1,059 | 1,080 | 83 | 87 | 993 |
| 2022 | 1,002 | 1,098 | 91 | 101 | 997 |
| 2023 | 83 | 1,095 | 83 | 101 | 994 |
| 2024 | 1,007 | 1,019 | 85 | 87 | 932 |
| **Total** | **8,249** | **10,972** | **793** | **963** | **10,009** |

Machine-readable results: [annual reconciliation](../provenance/t02/annual_reconciliation.csv) and [year/code/outcome counts](../provenance/t02/year_code_outcome.csv).

**2017:** the source contains 1,221 eligible discharges, including 1,108 live discharges. The legacy count of 31 is not an accurate count of all eligible records in this release.

**2023:** the source contains 1,095 eligible discharges, including 994 live discharges. The legacy all-death subset is contradicted by the national release. Its apparent perfect separation is therefore not evidence that all eligible admissions died nationally. Refit the mortality model using the explicit death indicator in the rebuilt cohort.

**2024:** there are two separate discrepancies. Within the legacy data, the SAV and both workbook `Hoja3` sheets contain 1,007 admissions, 85 deaths and **922** live discharges. The manuscript's 895 live discharges are a transcription error. Independently, the official release contains **1,019** eligible records, 87 deaths and 932 live discharges. It would be insufficient to correct only the manuscript cell while retaining the incomplete legacy extract.

Both legacy and reconstructed 2024 data contain **379 C719 discharges**. Consequently, a zero unspecified hospitalization rate is not supported. The precise spreadsheet/rate calculation that produced zero has not been recovered; T03 must regenerate the rate from the verified numerator.

## Anatomical classification errors

The legacy SAV assigns **127 C714 (occipital-lobe) records to infratentorial/midline**, and **82 C717 (brainstem) records to unspecified**. These 209 classifications contradict the manuscript's stated grouping. The saved derived CIE10 group must not be reused.

The reconstructed mapping is C710–C714 → supratentorial; C715–C717 → infratentorial/midline; C718 → overlapping; C719 → unspecified. This produces 4,669; 1,523; 112; and 4,668 admissions, respectively. The ventricular/midline combination remains an operational anatomical grouping, not a histological classification. [Legacy classification audit](../provenance/t02/legacy_anatomy_audit.csv) preserves the evidence.

## Outcome, age and stay rules

- **Outcome:** source codes 1=live; 2=death under 48 hours; 3=death at 48 hours or more. The new `death` variable is 0 for code 1 and 1 for codes 2/3; unexpected values become missing. Annual metadata were checked against these meanings. All 10,972 selected records have a recognized outcome. This does not settle which event the old SPSS regression modelled; T04 must still inspect/refit that model.
- **Age:** preserve `cod_edad` and raw `edad`. There are 90 subyear records: 3 coded in hours, 3 in days and 84 in months; they belong to the pediatric group and have completed age zero. A number of months is never treated as that many years. Valid year ages are 1–115; age group boundaries are 0–17, 18–44, 45–64, 65–79 and 80+. Unknown/invalid units or values are missing rather than assigned to 80+. No selected record has an unclassifiable age under these rules.
- **Stay:** use recorded `dia_estad`, with categories 0 days, 1–3, 4–14, 15–30 and **31+**, preserving invalid or missing values as unknown. Day 30 belongs only to 15–30. There are 68 day-30 records in the reconstructed cohort. No selected record has zero, negative, missing or noninteger recorded stay.
- **Dates:** all selected discharges have valid parsed admission/discharge dates, no negative date interval and no discharge-year mismatch. There are 827 same-calendar-day admissions with recorded stay 1. Every other recorded stay equals the calendar-day difference. This is consistent with a minimum-one-day recorded-stay convention; the recorded variable is retained, and both date-derived duration and their difference are preserved. Do not convert these 827 records to missing or silently replace their stay.

These rules are defined in `scripts/audit_admissions.py` and covered by boundary tests. The longest recorded stay is 1,684 days; the dates support this interval, so it was retained rather than arbitrarily capped.

## Missingness, geography and dependence

[Missingness by year and variable](../provenance/t02/missingness_by_year.csv) distinguishes blanks/nulls from source-coded unknowns summarized in [quality by year](../provenance/t02/quality_by_year.csv).

- **Ethnicity:** 1,290 records have code 9 (ignored/no information). The source also distinguishes Afrodescendant, Negro, Mulato, White, Indigenous, Mestizo, Montubio and Other. Preserve these source meanings; do not merge unknown ethnicity into Other. No model-specific complete-case exclusion or imputation has been selected in T02.
- **Residence:** three records indicate foreign residence (one in 2018 and two in 2019). They remain in the discharge cohort, explicitly flagged. A resident-population rate analysis must address these three records in T03; foreign residence is not missing province information.
- **Geography:** retain both `prov_ubi` (facility province) and `prov_res` (residence province), and both location/residence area fields. No patient identifier or stable unique facility identifier has been established. `entidad`, `clase` and `tipo` describe institutions but are not identifiers. Do not infer province-based disease risk from facility counts. The legacy field `Prob` has no metadata establishing which province field was used; its lineage remains unverified.
- **Residence-area limitation:** 2015–2017 SAVs lack area-residence value labels. The working mapping 1=urban, 2=rural is marked **provisional** for those years (`residence_area_mapping_verified=False`), based on later official labels and dictionaries. Later-year mappings are supported by SAV labels or the 2019/2020 dictionaries. Those dictionaries contain a copied location-description phrase in the `area_res` row, although the variable name/title identifies residence. The early syntax archives did not independently resolve the missing labels. Preserve the early raw codes; confirm those labels before modelling rural/urban associations.
- **Sector:** retain public, private for profit and private nonprofit, plus a separately documented public/private aggregation. Social-security institutions are retained under the official public-sector code rather than treated as a fourth mutually exclusive sector.
- **Duplicates:** the legacy SAV has 714 repeated projections beyond the first, but its coarse attributes cannot prove duplicate hospitalizations. The rebuilt selected records include 12 records in groups identical on the retained raw audit fields, each with a distinct source-row key. None was removed. Dates and additional source fields help audit records but do not establish unique patients or admissions across institutions.

## Workbook findings and historical limits

Each workbook's `Hoja3` contains the same 8,249 records and 12 original fields as the SAV, in the same order after normalizing integer-versus-float display. They are therefore copies of the same legacy analytic extract for these fields, not independent evidence of national completeness. The plotting workbook additionally includes provincial count tables. Their production history remains unavailable.

The original extraction/cleaning script is not available for this audit; the author may supply it later. The exact historical filters, joins or recodes responsible for the reductions in every year and differences in ethnicity cannot be established from the final extract alone. Do not present these as INEC registration failures. The supplied source release versions may also differ from those originally used. The new pipeline avoids relying on the unknown historical processing, preserves current release hashes and explicitly defines selection and recoding.

## Verification and task status

Verified: six preserved inputs unchanged; all downloaded archives hashed; ten annual source files read; source selection flow reconciled; audited admission keys unique; outcome totals reconcile; all selected codes have one anatomical group; ages and stays have explicit bounds; original/projected repeats retained; workbooks reconciled; recoding boundary tests pass.

**T02 reconstruction is implemented. G1 remains pending confirmation of early-year residence-area labels and review of the recorded inclusion/geography decisions before association modelling.** Historical processing remains an open provenance question, not a reason to silently reuse the legacy cohort. Independent replication and any later discovery of earlier source versions should be recorded before manuscript numbers are finalized.

Next: T03 should use the rebuilt cohort and original annual population denominators to regenerate every standardized rate. T04/T05 must rebuild models; none of the old aORs/aRRRs should be transferred to this cohort.
