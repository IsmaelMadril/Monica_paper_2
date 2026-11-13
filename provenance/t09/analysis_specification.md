# T09 figure specification — 13 November 2026

Figure1 uses the exact resident/five_groups annual rows used for Table3, including
all anatomical components and total. No smoothing or trend test. Two panels show
hospitalizations and in-hospital deaths per100,000 residents, 2015–2024, with a
shared year axis and separate measure scales. Colours/shapes are consistent;
shade total95% Fay–Feuer intervals only to avoid overlapping five bands. Provide
all100 component/measure/year estimates and intervals in a companion table.
Explicitly control 2017 death, 2024 total and2024 unspecified series. Verify current
Table3 against tracked T03 evidence with floating-point tolerance, not rounded text.

Figure2 is a 24-province by10-year residence-admission count heatmap, with source
INEC province codes and full province names. Count source records, not people.
Exclude exactly three foreign-resident live discharges from residence geography;
no unknown domestic residence code occurs. A separate facility heatmap counts all
10,972 records by treating-facility province; it is not patient origin. Use one
shared linear colour range across all years and both heatmaps. Print numeric
counts; distinguish observed zero from unavailable (grey/NA) data. No provincial
population rate, mortality risk or incidence inference. Geographic counts do not
use the provisional early rural/urban labels. Source code20 unifies accent variants
Galapagos/Galápagos; no fuzzy geographic matching or label-only join.

SupplementS1 contains one residence-count map per year with mainland and separate
Galápagos inset and a province-code key. The same count scale as the heatmaps is
used on every page. Archive fixed geoBoundaries gbOpen ECU ADM1 geometry commit
9469f09, boundaryID ECU-ADM1-780006, represented year2011; exactly24features.
Archive current metadata and hashes. Attribute geoBoundaries/geoLab and metadata
source Wikimedia Commons. Source metadata states CC0; repository API requests
attribution. Geometry is cartographic context, not validated annual boundaries.
Use longitude/latitude equirectangular axes with equal angular aspect; inset is
repositioned and not at the mainland display scale. No area/distance inference.

Keep all ten official reconstructed years. Historical 2017/2023 deficits were not
reproduced; do not shade them as incomplete official years. Release-year totals
reconcile to the audited cohort; this is not an independent completeness audit of
all hospital capture. Include interval, coverage, numerator/denominator and geography
limits in self-contained legends. Produce fixed-width180mm PDF/SVG and600dpi PNG
main figures; an atlas PDF plus individual annual SVG maps is supplementary.
Minimum intended figure label size7pt; full province names belong in heatmaps/key.
Do not use colour alone for rate-series identification or imply choropleth counts
measure province risk. Inspect main figures and every atlas page at intended size.

Local checks: all plotted points/counts match source outputs; all240 province-year
cells have unique keys, status and provenance; every annual margin reconciles;
24-feature join is one-to-one with no missing/duplicate/unmatched provinces; current
T03 inputs match recorded bytes or exact LF/CRLF variants. Rendering must reject
unexpected geography, invalid counts or invalid/changed boundaries. Add meaningful
controls for code joins, zero/missing handling and the flagged historical figures.
