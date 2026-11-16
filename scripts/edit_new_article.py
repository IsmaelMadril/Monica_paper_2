"""Apply the 16 November editing checklist to the supplied draft; retain a backup."""
from pathlib import Path
import re,json,hashlib,shutil
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/raw/baseline_2026-10-23/Writeable/New_article.docx'
backup=ROOT/'outputs/reports/article_edit/New_article_before_edit.docx'
if not backup.exists():shutil.copy2(path,backup)
doc=Document(backup);ps=list(doc.paragraphs);changes=[]
def replace(i,text):
 old=ps[i].text;ps[i].text=text;changes.append({'paragraph':i,'before':old,'after':text})
def after(anchor,text,style=None):
 p=doc.add_paragraph(text,style);anchor._p.addnext(p._p);return p
def section_text(name):
 text=(ROOT/'Writeable/t07_manuscript_sections.md').read_text()
 return text.split('## '+name+'\n')[1].split('\n## ')[0].replace('<!-- PAGE -->','').strip()
def clean(s):
 return re.sub(r'\[R(\d+)([^\]]*)\]',lambda m:'['+str(int(m[1]))+re.sub(r'R0?(\d+)',lambda n:str(int(n[1])),m[2])+']',s).replace('**','')
replacements={
0:'Hospitalizations and In Hospital Deaths Associated With Malignant Brain Neoplasms in Ecuador From 2015 to 2024',
22:'This study describes nationwide hospitalizations, anatomical coding and in-hospital deaths associated with malignant brain neoplasm discharge diagnoses in Ecuador during 2015–2024. We analyzed annual INEC discharge records with primary diagnosis C71.0–C71.9. Resident-population rates were directly standardized to the observed 2022 Ecuadorian census age distribution using annual population estimates. Binary logistic models estimated adjusted odds ratios (aORs) and 95% confidence intervals (CIs) for death, coding detail and conditional anatomical group. The reconstruction included 10,972 admissions and 963 deaths; admission fatality was 8.78% (95% CI 8.26–9.32). Resident rates excluded three foreign-resident live discharges. The mean annual age-adjusted hospitalization rate (AAHR) was 6.611 per 100,000 residents (95% CI 6.487–6.737), and the corresponding in-hospital death rate (AAIMR) was 0.598 (0.561–0.638).',
24:'Older age was associated with higher adjusted death odds: ages ≥80 versus 0–17 had an aOR of 2.631 (95% CI 1.864–3.715). Unspecified C71.9 coding accounted for 4,668 admissions (42.54%), including 379 in 2024. Among 6,192 records assigned to either anatomical group, ages 0–17 versus 18–44 had an aOR of 1.141 (0.985–1.320) for infratentorial/midline versus supratentorial coding; estimates varied by period. These results describe hospital service events and deaths during admission. Unspecified coding, selected inpatient populations and unresolved repeat-admission dependence limit interpretation.',
26:'Keywords: Malignant brain neoplasms; Hospital discharge records; Ecuador; Hospitalization; In-hospital death; Administrative health data.',
28:'Malignant brain tumors comprise a heterogeneous group of central nervous system neoplasms. Histological and molecular characterization informs their classification and clinical interpretation. Administrative discharge codes describe anatomical sites but do not provide the integrated histological and molecular classification used in neuro-oncology [19]. This analysis concerns diagnoses coded C71.0–C71.9; neither histological confirmation nor primary tumor origin can be established from a primary discharge diagnosis alone [2].',
29:'',
30:'Hospital-discharge records provide a complementary description of inpatient care and outcomes during admission. They do not identify incident cancers, unique patients or deaths outside the included hospital stays. Distinguishing these endpoints is essential when interpreting hospitalization rates alongside cancer incidence and mortality estimates [1,8].',
31:'In Latin America, regional research has described brain and central nervous system cancer incidence using cancer registries and mortality using WHO data, with world-standardized rates [20]. Those endpoints and standards differ from the admission-based measures examined here; direct numerical comparison requires matched definitions and populations.',
32:'According to the archived GLOBOCAN 2024 estimates, version 1.0, 561 new brain and central nervous system cancer cases and 463 related deaths were estimated in Ecuador, both sexes and all ages [18]. These are modeled cancer estimates, not observed hospital admissions. Hospital-discharge analysis can complement this context by describing recorded inpatient activity and deaths during admission.',
33:'Accordingly, this study aimed to characterize the hospitalization burden associated with malignant brain neoplasm discharge codes in Ecuador from 2015 to 2024 by examining age-adjusted hospitalization and in-hospital death rates, geographic distribution, anatomical coding, and sociodemographic and institutional associations with hospital outcomes. Coding detail and conditional anatomical group were analyzed as separate exploratory questions.',
36:clean(section_text('Study design and data sources')),
40:'Infratentorial and midline: C71.5 (brain ventricles), C71.6 (cerebellum), and C71.7 (brainstem). This is an operational grouping: C71.5 is not universally infratentorial. A sensitivity analysis excluded C71.5 [2].',
41:'Overlapping lesions: C71.8. These records were retained descriptively and in the coding-detail panel, without assignment to a single anatomical compartment [2].',
42:'Unspecified: C71.9 (malignant neoplasm of the brain, unspecified). This is a documentation category, not a biological anatomical site [2].',
44:'The primary outcome was death during the recorded admission, explicitly coded as death=1 for source discharge codes 2/3 and live discharge=0 for source code 1. Observation ended at discharge; there was no postdischarge survival follow-up. Separate binary outcomes represented non-C71.9 coding versus C71.9 and infratentorial/midline versus supratentorial coding in the eligible subset.',
45:'Recorded covariates encompassed demographic, institutional and temporal characteristics:',
46:'Demographic characteristics: age in completed years, accounting for source age units, grouped as 0–17, 18–44, 45–64, 65–79 and ≥80; sex; and all recorded ethnicity categories. Source unknown ethnicity (code 9; 1,290 records) was retained separately from Other. No clinical validation or imputation was performed.',
47:'Geographic and structural factors: recorded rural/urban residence and public/private sector. Rural/urban labels were verified only for 2018–2024, so those comparisons used 7,621 admissions. Early labels were excluded from all-year adjustment. Main geography used province of residence; a supplementary comparison used treating-facility province. Province counts are admission counts without population denominators.',
48:'Clinical and temporal variables: recorded length of stay (1–3, 4–14, 15–30 and 31+ days) and discharge year (2015–2024). No selected record had zero, negative, missing or noninteger recorded stay. Final stay duration was excluded from primary adjustment because it is partly determined by discharge/death timing.',
50:'Categorical variables were summarized using counts and column percentages; within-category fatality used deaths divided by admissions in that category. One exploratory omnibus comparison was performed per characteristic. Pearson chi-square without continuity correction was used when every active observed and expected cell was at least five. Sparse 2×2 tables used two-sided Fisher exact; other sparse tables used fixed-margin Monte Carlo Pearson tests with 99,999 draws and deterministic seeds. The simulated p-value was (exceedances+1)/(draws+1), including ties. No multiplicity adjustment or significance highlighting was used [17].',
55:'In these formulas, i denotes age group, H the number of hospitalizations, D the number of deaths during admission, P the annual resident population, and w the fixed proportion of age group i in the observed 2022 census standard. Annual denominators were INEC midyear population estimates, Revisión 2024; the fixed census standard summed to 16,938,986. Source workbooks, age counts and exact weights are supplied with the reproducibility materials [3,4].',
60:'Multivariable modeling addressed three separately defined admission-level outcomes:',
61:clean(section_text('Primary regression models').split('\n\n')[0]),
62:clean(section_text('Primary regression models').split('\n\n')[1]),
63:'Covariates provided limited descriptive adjustment, not complete confounding control. No significance-based selection or interaction search was performed. Models were checked for full rank, separation, convergence, finite estimates, score residuals and positive information eigenvalues. All eight death-model and 15 coding/site fits passed these checks. Primary intervals and p-values were Wald-based; sparse contrasts were supplemented with profile-likelihood intervals. The revised analysis used Python 3.14.7, pandas 3.1.0, SciPy 1.18.1 and statsmodels 0.15.0. The historical SPSS output was audited but was not reused as a validated estimate [13–16].',
65:'This study analyzed publicly released secondary hospital-discharge records from INEC. No clinical records or restricted patient-identification database were accessed.',
67:'Between 2015 and 2024, the reconstructed cohort included 10,972 hospital admissions with a primary C71 diagnosis, of which 963 ended in death and 10,009 in live discharge. Overall admission fatality was 8.78% (95% CI 8.26–9.32). Ages 45–64 accounted for 294 deaths (30.53% of deaths); ages 0–44 accounted for 5,694 live discharges (56.89% of live discharges). Crude fatality was 9.36% in the public sector and 7.89% in the private sector. These descriptive comparisons do not establish institutional performance or access barriers. Counts, explicit denominators and exploratory comparisons are shown in Table 1.',
72:'Recorded anatomical groups comprised 4,669 supratentorial, 1,523 infratentorial/midline, 112 overlapping and 4,668 unspecified admissions. Table 2 presents the distributions by age, sex, ethnicity, sector, recorded stay, year and verified residence period. These are recorded code groups; differences do not establish biological site propensity or diagnostic accuracy.',
77:'Between 2015 and 2024, the mean annual AAHR was 6.611 per 100,000 residents (95% CI 6.487–6.737). All ten years were retained. The highest total rate occurred in 2017 (7.583), and the lowest in 2020 (5.540). The 2024 total was 5.784, including an unspecified rate of 2.152 from 379 admissions. Supratentorial hospitalization rates peaked in 2019 (3.470), not 2024. These changes describe timing, without a formal trend or causal pandemic analysis.',
78:'The mean annual AAIMR was 0.598 per 100,000 residents (95% CI 0.561–0.638), with its highest value in 2017 (0.758) and lowest in 2020 (0.454). Unspecified and supratentorial components together accounted for 86.157% of the mean standardized in-hospital death rate. This is a standardized rate contribution, not the raw proportion of deaths. Table 3 provides the annual estimates and intervals.',
82:'Age-adjusted hospitalization and in-hospital death rates varied over the study period (Figure 1). Supratentorial and unspecified codes contributed the largest hospitalization-rate components. The severe 2017 and 2023 deficits in the historical extract were not reproduced by the official-source reconstruction; these years were retained without labeling them registration failures.',
87:'After adjustment for recorded covariates, older age groups had higher odds of death during admission than ages 0–17: aOR 1.593 (95% CI 1.312–1.934) for ages 45–64, 2.153 (1.742–2.661) for 65–79, and 2.631 (1.864–3.715) for ≥80. The public/private aOR was 1.201 (1.035–1.394), while 2023 versus 2015 was 1.034 (0.768–1.391). These are conditional associations, not causal effects or survival probabilities (Table 4). Final stay was excluded from the primary model.',
92:'The coding-detail model included 10,972 admissions, with 6,304 non-C71.9 events. The conditional anatomical model included 6,192 admissions, with 1,523 infratentorial/midline events, after excluding 112 overlapping and 4,668 unspecified records. In the latter model, ages 0–17 versus 18–44 had an aOR of 1.141 (95% CI 0.985–1.320). Table 5 presents the two separate binary panels, with age 18–44, male, private sector and 2015 as references. These aORs do not reproduce the former multinomial estimand.',
97:'Figure 2 displays admission counts for all 24 provinces of residence and ten discharge years, comprising 10,969 resident records. Three foreign-resident live discharges were excluded; no unknown residence-province codes occurred. The annual cartographic presentation is supplied in Figure S1; Figure S2 separately assigns all 10,972 records to treating-facility province. These counts describe recorded service events, not provincial cancer incidence, population risk, referral severity or access. The early rural/urban label uncertainty does not determine province assignment.',
101:'This study provides a nationwide evaluation of recorded C71-coded hospitalizations and in-hospital deaths during 2015–2024. The mean annual standardized hospitalization rate was 6.611 per 100,000 residents and the corresponding in-hospital death rate was 0.598. Unspecified coding remained frequent, including 379 admissions in 2024. These findings describe inpatient activity and documentation, without establishing cancer incidence, overall cancer mortality or improved diagnostic accuracy.',
102:'Our multivariable model identified higher adjusted death odds in older age groups relative to pediatric admissions. This association remains conditional on admission and the recorded adjustment set. Histology, grade, comorbidity, treatment, referral severity and palliative intent were unavailable; selection into inpatient care and unmeasured case mix may affect these associations. The estimates do not establish a causal age effect or validate a prediction model.',
103:'During the first year of the COVID-19 pandemic, 2020, total hospitalization and in-hospital death rates were the lowest in the observed series. This timing does not establish a pandemic effect. The data cannot distinguish changes in presentation, admission practice, care availability or recording, and do not demonstrate emergency prioritization. The reconstructed 2017 and 2023 counts do not support the historical extract-based claims of national registry disruptions.',
104:'International comparison requires compatible endpoints, diagnosis definitions and standard populations. Cancer-incidence and population-mortality estimates are not direct benchmarks for hospitalization rates [18,20]. Similarly, the observed public/private association cannot establish hospital quality, access barriers or tertiary case complexity, because clinical severity and referral pathways were not measured adequately.',
105:'This investigation has several limitations inherent to secondary administrative health datasets. Because the INEC records do not allow longitudinal identification of unique individuals, the unit of analysis was the hospitalization rather than the patient; repeated admissions may appear as separate records. Patient and facility clustering could not be resolved with validated identifiers, so reported intervals condition on independent records and may understate uncertainty. Discharge diagnoses were not clinically validated and may be misclassified. ICD-10 codes do not provide integrated WHO histological/molecular classification [19]. The dataset captures deaths during admission, excluding postdischarge and out-of-hospital deaths.',
106:'Despite these constraints, the study’s strengths include its ten-year national scope, explicit age standardization and reproducible selection and analysis. The coding-detail and conditional-site models answer distinct questions; exclusion of unspecified and overlapping codes from the site model does not correct nonrandom selection. Sparse categories and multiple exploratory comparisons limit interpretation. These results provide a descriptive basis for future clinical validation and linkage research rather than demonstrated effects of resource allocation or care policies.',
108:'This ten-year nationwide analysis describes C71-coded hospital admissions and deaths during admission in Ecuador. Older age was associated with higher adjusted death odds, while frequent unspecified coding and period-sensitive anatomical associations limit interpretation. Final length of stay is outcome-dependent and should not be interpreted as a protective or harmful baseline exposure.',
109:'These findings provide a reproducible description of recorded inpatient activity. They do not estimate cancer incidence or overall cancer mortality, validate diagnostic accuracy, or establish public/private differences in care quality. Future work linking clinical information and longitudinal outcomes could address these limitations.'}
for i,s in replacements.items():replace(i,s)
# Retain correct selection statement and anatomical list, adding audited flow.
a=ps[38]
a=after(a,'Across 11,172,616 source records, exact normalized C710–C719 selection retained 10,972 admissions. Seventeen C71-prefix records failed the exact subcode rule. All eligible records were retained without person deduplication or postselection covariate exclusions. All-admission descriptive and primary regression analyses used 10,972 records; population rates used 10,969 resident records after excluding three foreign-resident live discharges. Annual selection flow and code definitions accompany the reproducibility materials [1,2,8].')
after(ps[57],'Annual-rate intervals used the Fay–Feuer gamma method and admission-fatality intervals the Wilson method [6,7]. The ten-year summary is the arithmetic mean of annual rates; its interval was calculated from the weighted count sum. Annual denominators and census weights were treated as fixed. These intervals do not incorporate clustering, undercapture, miscoding or population-estimation error. Narrower age bands and all-discharge rate calculations were examined as sensitivities.')
after(ps[63],clean(section_text('Sensitivity analyses and descriptive comparisons').split('\n\n')[0]))
after(ps[87],'Resident-only mortality estimates changed little. Age ≥80 estimates were lower in the verified-year subset, while adding final stay descriptively changed the public-sector estimate from 1.201 to 1.066. The verified-year rural/urban aOR was 1.119 (95% CI 0.900–1.392). These sensitivity results do not establish equivalence or causal mediation; sparse profile intervals and full alternative fits accompany the analysis.')
after(ps[92],'All primary fits converged without detected separation. Coding/site estimates varied by period, and the primary conditional pediatric interval included one. Time-restricted fits were not selected to replace the primary model. C71.5-exclusion, resident-only, residence-adjusted and extended-ethnicity sensitivities are provided with the model outputs.')
after(ps[105],'Rural/urban comparisons were limited to verified 2018–2024 labels. Unknown ethnicity was retained explicitly. Rate intervals condition on fixed denominator estimates and census weights; narrower age bands changed overall mean rates by less than 0.5%, without eliminating residual age differences. No formal temporal stability or causal pandemic analysis was conducted.')
# Remove historical table objects and orphaned captions/notes.
for t in list(doc.tables):t._tbl.getparent().remove(t._tbl)
for i in [69,70,71,74,75,76,80,81,89,90,94,95,96,59]:
 ps[i]._p.getparent().remove(ps[i]._p)
# Native tables rebuilt from verified Markdown; narrative remains in original order.
def markdown_blocks(anchor,text):
 lines=text.splitlines();i=0
 while i<len(lines):
  s=lines[i].strip()
  if not s or s.startswith('# ') or re.match(r'^\[(Specification|Model)',s):i+=1;continue
  s=re.sub(r'`?provenance/[^\s`;,]+`?', 'the supplementary analysis files', s)
  s=s.replace('T03 CSV outputs','supplementary rate outputs').replace('CSV retains full numerical p-values','Supplementary data retain full numerical p-values')
  if s.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    vals=[clean(x.strip()) for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[:\- ]+',x) for x in vals):rows.append(vals)
    i+=1
   t=doc.add_table(rows=1,cols=len(rows[0]));t.autofit=False
   width=6.75;first=1.55 if len(rows[0])>4 else 2.1
   widths=([.85,1.8,.65,.6,.55,1.0,.65,.65] if len(rows[0])==8 else [first]+[(width-first)/(len(rows[0])-1)]*(len(rows[0])-1))
   for j,c in enumerate(t.columns):c.width=Inches(widths[j])
   for n,vals in enumerate(rows):
    cells=t.rows[0].cells if n==0 else t.add_row().cells
    for j,(c,v) in enumerate(zip(cells,vals)):
     c.width=Inches(widths[j]);c.text=v
     for p in c.paragraphs:
      p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
      p.paragraph_format.line_spacing=1
      for r in p.runs:r.font.size=Pt(8);r.font.name='Times New Roman';r.bold=n==0
    pr=t.rows[n]._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
    if n==0:pr.append(OxmlElement('w:tblHeader'))
   borders=OxmlElement('w:tblBorders')
   for edge in ['top','left','bottom','right','insideH','insideV']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
   t._tbl.tblPr.append(borders)
   anchor._p.addnext(t._tbl)
   p=doc.add_paragraph();t._tbl.addnext(p._p);anchor=p
   continue
  p=after(anchor,clean(s.lstrip('# ')), 'Heading 3' if s.startswith('##') else None)
  if s.startswith('##'):p.paragraph_format.keep_with_next=True
  else:
   for r in p.runs:r.font.size=Pt(9)
  anchor=p;i+=1
 return anchor
for num,idx in [(1,68),(2,73),(3,79),(4,88),(5,93)]:
 replace(idx,{'1':'','2':''}.get('x',f'Table {num} ')+['','Characteristics by discharge outcome','Characteristics by recorded anatomical group','Age adjusted hospitalization and in hospital death rates','Adjusted associations with death during admission','Adjusted associations with coding detail and conditional anatomical group'][num])
 ps[idx].style='Heading 2'
 markdown_blocks(ps[idx],(ROOT/f'outputs/tables/table{num}_rebuilt.md').read_text())
# Replace embedded figure paragraphs and captions.
for idx,stem in [(85,'figure1_rates'),(98,'figure2_residence_counts')]:
 ps[idx].clear();ps[idx].add_run().add_picture(str(ROOT/f'outputs/figures/{stem}.png'),width=Inches(6.7))
 ps[idx].paragraph_format.keep_with_next=True
leg=(ROOT/'Writeable/t09_figure_legends.md').read_text()
for idx,num in [(86,1),(99,2)]:
 block=leg.split(f'## Figure {num}\n')[1].split('\n## ')[0].split('\nFiles:')[0]
 replace(idx,f'Figure {num}. '+clean(block.strip()))
 for r in ps[idx].runs:r.font.size=Pt(9)
# Remove old bibliography field/content controls after REFERENCES.
body=doc._element.body;start=list(body).index(ps[110]._p)
for el in list(body)[start+1:]:
 if el.tag!=qn('w:sectPr'):body.remove(el)
# Verified source notes supply human-readable references; map IDs to numeric citations.
refs={}
for filename in ['t07_manuscript_sections.md','t08_interpretation_sections.md']:
 for line in (ROOT/'Writeable'/filename).read_text().splitlines():
  m=re.match(r'R(\d+)\.\s*(.*)',line)
  if m:refs[int(m[1])]=m[2]
# Source notes omitted from T08 builder are available in BibTeX; parse nested braces.
bib=(ROOT/'references/reconstruction.bib').read_text()
for entry in re.split(r'\n(?=@)',bib):
 m=re.search(r'R(\d+)\.',entry)
 if not m:continue
 n=int(m[1]);fields={}
 for field in ['author','title','journal','year','volume','pages','doi','url']:
  fm=re.search(r'\b'+field+r'\s*=\s*\{',entry)
  if fm:
   pos=fm.end();depth=1;end=pos
   while depth and end<len(entry):
    depth+=(entry[end]=='{')-(entry[end]=='}');end+=1
   fields[field]=entry[pos:end-1].replace('{','').replace('}','').replace('--','–')
 if n not in refs:refs[n]='. '.join(fields[x] for x in ['author','title','journal','year','volume','pages'] if x in fields)+'. '+('https://doi.org/'+fields['doi'] if 'doi' in fields else fields.get('url',''))
# Numeric bibliography keeps verified source numbering; cite remaining methods refs explicitly.
after(ps[63],'Model diagnostics and likelihood-based inference followed the recorded statistical implementation and methodological sources [13–16]. Direct standardization and uncertainty methods are documented in the source materials [5–7,12]. Reporting follows the applicable STROBE and RECORD items, without claiming that a checklist validates the analysis [8,9]. Reproducibility materials preserve source fingerprints and analytical decisions [10,11].')
for n in range(1,21):
 if n not in refs:raise RuntimeError(f'Missing reference {n}')
 doc.add_paragraph(f'{n}. {refs[n]}')
# Clear existing section breaks to avoid inherited blank pages; preserve portrait dimensions.
for p in doc.paragraphs:
 for br in p._p.xpath('./w:pPr/w:sectPr'):br.getparent().remove(br)
for sec in doc.sections:
 sec.left_margin=Inches(.8);sec.right_margin=Inches(.8);sec.top_margin=Inches(.75);sec.bottom_margin=Inches(.75)
for p in doc.paragraphs:
 p.paragraph_format.widow_control=True
 if p.text and not p.style.name.startswith(('Heading','Title')):
  p.paragraph_format.space_after=Pt(6);p.paragraph_format.line_spacing=1.08
  for r in p.runs:
   r.font.name='Times New Roman'
   if r.font.size is None or r.font.size.pt>14:r.font.size=Pt(11)
for sty in ['Title','Heading 1','Heading 2','Heading 3']:
 doc.styles[sty].font.color.rgb=RGBColor(0,0,0);doc.styles[sty].font.name='Times New Roman'
ps[0].style='Title'
# Author-only questions are comments, not fabricated declarations.
for idx,msg in [(8,'Please supply affiliation 6 for Aline Siteneski, or confirm that superscript 6 should be removed.'),(65,'Author confirmation required: provide the documented ethics review/exemption basis, consent determination and identifier if applicable. Also supply funding/funder role, competing interests, contributions, and final data/code availability statements. These cannot be inferred from public data access.')]:
 if ps[idx].runs:doc.add_comment(ps[idx].runs[0],text=msg,author='Editorial review',initials='ER')
# Final editorial and layout cleanup.
for p in list(doc.paragraphs):
 if not p.text.strip() and not p._p.xpath('.//w:drawing|.//m:oMath'):
  p._p.getparent().remove(p._p)
for p in doc.paragraphs:
 if p.text.startswith('Figure '):
  p.alignment=0
  for r in p.runs:
   r.text=r.text.replace('`provenance/t09/figure1_rates.csv`','supplementary figure data').replace('checked against the T03 evidence','verified against the rate calculations')
 if p.style.name.startswith('Heading'):
  for r in p.runs:r.font.size=Pt(12);r.bold=True
for sec in doc.sections:
 for p in sec.footer.paragraphs:
  pr=p._p.get_or_add_pPr();pr.append(OxmlElement('w:suppressLineNumbers'))
# Numerical citations in order of first appearance; retain each verified identity once.
reference_paragraphs={int(m[1]):p for p in doc.paragraphs if (m:=re.match(r'^(\d+)\. ',p.text)) and int(m[1]) in refs}
order=[]
def cite(m):
 ids=[]
 for part in m[1].split(','):
  part=part.strip()
  if '–' in part or '-' in part:
   a,b=re.split('[–-]',part);ids.extend(range(int(a),int(b)+1))
  else:ids.append(int(part))
 for n in ids:
  if n not in order:order.append(n)
 return '['+', '.join(str(n) for n in sorted({order.index(n)+1 for n in ids}))+']'
for p in doc.paragraphs:
 if p not in reference_paragraphs.values():
  for r in p.runs:
   if re.search(r'\[([0-9, –-]+)\]',r.text):r.text=re.sub(r'\[([0-9, –-]+)\]',cite,r.text)
for p in reference_paragraphs.values():p._p.getparent().remove(p._p)
for new,old in enumerate(order,1):
 p=doc.add_paragraph(f'{new}. {refs[old]}')
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(10)
for p in doc.paragraphs:
 if p.text.startswith('A. Non-C719'):p.paragraph_format.page_break_before=True
 for r in p.runs:
  if 'supplementary analysis files Full' in r.text:r.text=r.text.replace('supplementary analysis files Full','supplementary analysis files. Full')
  if r.text.endswith('supplementary analysis files'):r.text+='.'
for t in doc.tables:
 if len(t.columns)==8:
  t.cell(0,2).text='Admissions\n(n)';t.cell(0,3).text='Deaths\n(n)'
  for c in [t.cell(0,2),t.cell(0,3)]:
   for p in c.paragraphs:
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(8);r.bold=True
for node in doc._element.xpath('.//m:t'):
 if node.text:node.text=node.text.replace('100.000','100,000')
doc.save(path)
(ROOT/'provenance/article_edit/paragraph_changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
print(path)
