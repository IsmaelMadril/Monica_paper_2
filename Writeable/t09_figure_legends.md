# T09 figure legends

Prepared 13 November 2026. These captions accompany the rebuilt figures, not the
historical manuscript images. PDF/SVG versions are vector exports; main PNGs are
600 dpi at 180 mm width. Keep this width, or recheck label readability after resizing.

## Figure 1

**Age-adjusted hospitalization and in-hospital death rates associated with C71-coded admissions in Ecuador, 2015–2024.** Panel A shows hospitalizations and panel B deaths during included admissions, per 100,000 residents. The primary rate population comprises 10,969 resident discharge records and 963 deaths; three foreign-resident live discharges are excluded (one in 2018, two in 2019). Rates are directly standardized using ages 0–17, 18–44, 45–64, 65–79 and 80+ to the observed Ecuador 2022 census distribution. Annual national INEC midyear population estimates supply the denominators. Lines/markers show total and the operational anatomical groups: supratentorial C71.0–C71.4; infratentorial/midline C71.5–C71.7; overlapping C71.8; unspecified C71.9. C71.5 is an operational midline assignment, not universally infratentorial.

Shading gives the total 95% Fay–Feuer interval. All component intervals are supplied in Table 3 and the companion `provenance/t09/figure1_rates.csv`, which preserves the 100 plotted estimates and intervals. Figure values come from the exact Table 3 primary-rate rows, checked against the T03 evidence. Panels have different vertical scales. Intervals condition on fixed population denominators/weights and independent events; repeated admissions, facility dependence, capture error and miscoding are not included. These are recorded service-event rates, not cancer incidence or overall cancer mortality. No formal trend or causal COVID-effect test is shown.

Files: `outputs/figures/figure1_rates.pdf`, `.svg`, `.png`.

## Figure 2

**C71-coded admission counts by province of residence and discharge year, Ecuador, 2015–2024.** Cells show 10,969 domestic-resident discharge records assigned using the INEC province-of-residence code (`prov_res`), not the location of the treating facility. All 24 provinces and ten years are displayed, with numeric counts and a shared linear colour scale of 0–500. Province codes identify the INEC province categories. Three foreign-resident live discharges are excluded; no unknown residence-province code occurs in the included cohort. Code 20 unifies the Galapagos/Galápagos label variants. Early-year rural/urban label uncertainty is not used to assign provinces.

A zero denotes no matching admission record in that province/year in the audited release; it does not establish absence of disease or complete capture of all care. Unavailable values are distinguished by grey/NA rather than zero; none occurs in the current audited grid. The reconstructed 2017 and 2023 releases are included and are not marked incomplete on the basis of historical extract losses. Counts represent admissions, possibly repeated for a person, and are not population rates, incidence, risk, referral severity or measures of access. No provincial population denominator is applied. This heatmap uses administrative categories, not polygon geometry; the cartographic version is supplied in Figure S1.

Files: `outputs/figures/figure2_residence_counts.pdf`, `.svg`, `.png`.

## Figure S1

**Annual province-of-residence admission-count atlas for C71-coded admissions, Ecuador, 2015–2024.** The ten pages reproduce the same 240 province-year counts as Figure 2, with one map per discharge year, province-code key, annual resident-record total and identical 0–500 linear count scale. The three foreign-resident live discharges are excluded and all domestic province-year cells are available. Counts are admissions, not unique persons or population rates. A zero means no matching record in the audited release, not absence of cancer.

Cartography uses the simplified geoBoundaries gbOpen ECU ADM1 layer, boundary ID `ECU-ADM1-780006`, pinned repository commit `9469f09592ced973a3448cf66b6100b741b64c0d`, accessed 13 November 2026. Metadata identify a 2011 boundary representation, with geoBoundaries/Wikimedia Commons source and source licence CC0 1.0; attribution is to geoBoundaries and William & Mary geoLab. Geometry and metadata are archived with hashes. Coordinates are WGS84 longitude/latitude displayed with equal angular aspect; the framed Galápagos inset is repositioned at a different display scale. No distance or area inference is intended. A fixed layer is used throughout; historical annual boundary changes and complete registration coverage were not independently validated.

The join uses an explicit source-name-to-INEC-code crosswalk, with accent normalization only. The boundary file's duplicate `EC-H` ISO value for Cotopaxi/Chimborazo is preserved but not used for joining. All 24 province features match one-to-one. Neither polygon area nor colour identifies population cancer risk or care quality. All anatomical and age groups are combined in these count maps.

Files: `outputs/figures/figureS1_residence_atlas.pdf` (ten pages); individual annual SVG files `figureS1_2015.svg` through `figureS1_2024.svg`. Annual PNGs are 300 dpi previews.

## Figure S2

**C71-coded admission counts by treating-facility province and discharge year, Ecuador, 2015–2024.** This supplementary heatmap assigns all 10,972 discharge records using the INEC location code of the institution (`prov_ubi`), not residence. It includes the three foreign-resident admissions because their facilities are domestic. No unknown facility-province code occurs. The same 24-province ordering, numeric counts and 0–500 linear colour scale as Figure 2 permit comparison of the two recorded assignments. Such comparisons do not identify individual referral pathways: residence and institution are distinct recorded variables, and the figure supplies no linked transfer history.

Zeros mean no matching recorded C71 admission at a facility assigned to that province/year, not absence of residents with disease. Grey/NA denotes unavailable data and is unused in the current audited grid. Repeated admissions may be included. Counts describe recorded service location, not population incidence, risk, institutional complexity or performance. No provincial resident-population denominator or rural/urban mapping is used.

Files: `outputs/figures/figureS2_facility_counts.pdf`, `.svg`, `.png`.
