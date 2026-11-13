# T09 figures and geographic reporting

Completed 13 November 2026 for the reconstructed-cohort figure specification.
Figure 1 and Figure 2 are rebuilt; detailed annual maps are in a supplementary
atlas, and treating-facility counts have a separate supplementary view. Read the
[self-contained figure legends](t09_figure_legends.md). The historical PDF is
preserved; figure insertion and whole-paper consistency remain T07 integration.

## Figures and review copies

| Product | Purpose | Export |
|---|---|---|
| [Figure 1](../outputs/figures/figure1_rates.pdf) | Same primary-rate rows as Table 3; total uncertainty shown | PDF, SVG, 600 dpi PNG; 180 × 165 mm |
| [Figure 2](../outputs/figures/figure2_residence_counts.pdf) | All 24 residence provinces × ten years with full names and numeric counts | PDF, SVG, 600 dpi PNG; 180 × 185 mm |
| [Figure S1](../outputs/figures/figureS1_residence_atlas.pdf) | Ten annual residence maps with fixed shared count scale and framed island inset | Ten-page vector PDF; annual SVG and 300 dpi PNG previews; 180 × 180 mm/page |
| [Figure S2](../outputs/figures/figureS2_facility_counts.pdf) | Treating-facility province counts, explicitly distinct from residence | PDF, SVG, 600 dpi PNG; 180 × 185 mm |

Generated exports are ignored by Git and recreated with the script. Tracked PNG
review copies of the main figures/facility heatmap are in `provenance/t09/` for
inspection from a fresh checkout. Use PDF/SVG for journal layout, not those review
copies or a screenshot. All main labels are at least 7.2 pt at the stated size;
atlas attribution is 7 pt. Recheck after any journal-specific resizing.

## Figure 1 reconciliation

The builder reads `outputs/tables/table3_rebuilt.csv` and requires its 100 unique
resident/five-group rows to agree with `provenance/t03/annual_standardized_rates.csv`.
Keys, counts, rates and intervals are checked before rendering. Float comparisons
allow 1e-12 numerical precision; no rounded-text matching is used. The plotted
rows and all confidence intervals are copied to `provenance/t09/figure1_rates.csv`.
Two panels share calendar years but have separate hospitalization/death scales.
Total and components use consistent colours and distinct marker shapes.

| Previously problematic point | Verified estimate per 100,000 residents | 95% Fay–Feuer interval | Events |
|---|---:|---|---:|
| 2017 total in-hospital deaths | 0.758166 | 0.623834–0.913891 | 113 |
| 2024 total hospitalizations | 5.783973 | 5.433951–6.151412 | 1,019 |
| 2024 unspecified hospitalizations | 2.152234 | 1.940812–2.381219 | 379 |

These correct the near-zero 2017 death point and zero 2024 unspecified series in
the old figure. The 2024 total is generated from the same component rows as the
table. Only the total interval is shaded to keep the five series readable;
component uncertainty remains in the companion data and Table 3. No smoothing,
trend/stability test or COVID intervention effect was introduced. Rate intervals
retain T03's independent-event/fixed-denominator assumptions and limitations.

## Geographic definition and denominators

Primary Figure 2 and the atlas use **province of residence**, source `prov_res`.
They count **10,969 admissions** after excluding exactly **three foreign-resident
live discharges** (one in 2018 and two in 2019). There are no unknown domestic
province codes. Figure S2 instead uses **treating-facility province**, `prov_ubi`,
and counts all **10,972 admissions**, including the three foreign-resident records
whose hospitals are domestic. Neither assignment uses the provisional 2015–2017
rural/urban mapping. Province code 20 resolves the Galapagos/Galápagos spelling
variants; label-only grouping would split the same province.

Every province/year is present in a 240-cell grid. Counts are records, not distinct
people, cancer incidence, population risk, severity, access or institutional
performance. No provincial population rates were added because matched provincial
denominators and an appropriate geographic-rate specification were not established
in this task. The national population rates in Figure 1 are a separate estimand.
An observed zero is not an unavailable value. Missing/unknown province codes and
missing entire years make generation fail instead of silently producing zeros.
Grey/NA is reserved for unavailable display cells and does not occur in the current
audited grid. Reconstructed annual margins reconcile, without claiming that every
cancer admission nationally was registered.

All years are retained. The historical 2017/2023 low-count problem was not
reproduced in official-source reconstruction, so those years are not labelled as
incomplete national releases. Source rows, annual geography margins and the
three exclusions are auditable in `geography_reconciliation.csv` and the two
numeric province-count files. The boundary join does not drive the count
aggregation: source administrative codes do.

## Boundary source and map limitations

The supplementary maps use a fixed simplified geoBoundaries gbOpen ECU ADM1 layer,
ID `ECU-ADM1-780006`, repository commit
`9469f09592ced973a3448cf66b6100b741b64c0d`. The API metadata identify **2011** as
the represented year, 24 provinces, geoBoundaries/Wikimedia Commons as source and
CC0 1.0 as the source licence. The API documentation requests attribution; both
the figure and legends credit geoBoundaries and William & Mary geoLab. Geometry,
metadata, URLs, access date and SHA-256 hashes are tracked under `provenance/t09/`.
The published Git LFS object digest is also checked at first acquisition; a pointer
file is not accepted as GeoJSON.

A one-to-one crosswalk matches normalized source names to explicit INEC province
codes. Diacritics are normalized, with no fuzzy matching. The source metadata
contain duplicate ISO value `EC-H` for Cotopaxi and Chimborazo. That value is
preserved in the crosswalk for transparency and **not used for joining**; the
features' names map to codes 05 and 06 respectively. This does not constitute an
independent ground-truth validation of all geometry. Unexpected names, duplicates,
invalid rings, wrong CRS, missing provinces or changed hashes stop generation.

Maps use longitude/latitude WGS84 with equal angular aspect, not an equal-area
projection. Galápagos has a separate framed inset and different display scale,
including the layer's northern islands. No distance/area inference is made. One
fixed layer across years provides cartographic context; year-specific historical
boundary changes were not validated. The primary heatmap avoids dependence on
geometry and preserves readable province names. All count figures use the same
linear range **0–500**, including the facility comparison and all atlas years.

## Validation and reproduction

**All 72 project tests pass, no skips**, including 11 new T09 controls. Tests
independently compare all 480 geography cells to cohort filters, check annual
margins/exclusions, require all source years before creating zeros, unify accented
province labels by code, reject unknown/inconsistent geography and corrupted rate
points, verify the province-name boundary join despite duplicate source ISO,
check polygon-hole winding and assert flagged rate values. All 100 plotted rate
rows match Table 3. Dependency integrity (`pip check`) passed.

Visual QA inspected the two main figures, facility heatmap and every one of the
ten atlas pages at the intended 180 mm width, using print-size previews. Initial
footer/key/inset collisions were corrected before final review. PDF/SVG exports,
600 dpi main PNG dimensions, atlas page counts and figure hashes are recorded in
`render_verification.json`. This checks presentation and data consistency, not
clinical validity, clustering or national registration completeness.

With T02/T03 outputs available and the local environment active, the same commands
work in macOS shells or Windows PowerShell:

```sh
python -m pip install -r requirements.txt
python -m pip install -r requirements-figures.txt
python -X utf8 scripts/generate_figures.py
python -X utf8 -m unittest discover -s tests -v
```

The optional plotting requirements are separate from the core analysis. Source
geometry/metadata are tracked, so normal plotting needs **no network access**.
If those tracked files are absent, first restore them with their manifest intact:

```sh
python -X utf8 scripts/acquire_figure_boundaries.py
```

The acquisition script verifies existing hashes and never replaces an established
expected manifest. Do not reacquire a new current boundary release and silently
substitute it for this one. Cached restoration uses recorded URLs and digests.
Matplotlib uses a repository-local cache and a headless backend; it does not need
GUI/desktop access. Figure generation was verified on macOS; new Windows execution
remains unverified. Exact environment versions and input/code/output fingerprints
are preserved. No rate/model refits or changes to existing INEC/population manifests were required.

T09's figure deliverables are complete for the stated specification. T07's
whole-manuscript integration criterion remains open, and T10 must verify author
ethics/declarations and final journal/submission requirements. Coauthors should
review the geographic definition and final journal-sized layout before submission.

## Primary sources

INEC variable metadata and audited source records establish residence versus
facility meanings (R01); T03 sources/methods establish rates and conditional
uncertainty (R03–R07). The exact boundary API metadata and archived geometry are
[R21](reconstruction_rationale.md#r21), and the export implementation is supported
by [Matplotlib documentation R22](reconstruction_rationale.md#r22). Those references
do not validate this study's counts, geography matching or final layout: the local
reconciliation, tests and visual review provide that evidence.
