"""Build T07 section text and an exact numeric source ledger; optionally export Word."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t07'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(name):
    with (ROOT/name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def select(rows, **filters):
    selected = [r for r in rows if all(r.get(k)==str(v) for k,v in filters.items())]
    if len(selected)!=1:
        raise ValueError(f'Expected one source row for {filters}, found {len(selected)}')
    return selected[0]


def export_docx(text, path):
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin = section.bottom_margin = Inches(.7)
    section.left_margin = section.right_margin = Inches(.8)
    normal = document.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.03
    normal.paragraph_format.space_after = Pt(7)
    for name, size in [('Title',19),('Heading 1',13),('Heading 2',12)]:
        style = document.styles[name]
        style.font.name = 'Times New Roman'
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0,0,0)
        style.paragraph_format.space_before = Pt(9)
        style.paragraph_format.space_after = Pt(7)
    for style in document.styles:
        for border in list(style.element.iter(qn('w:pBdr'))):
            border.getparent().remove(border)
        if style.name in ['Normal','Title','Heading 1','Heading 2']:
            fonts = style.element.get_or_add_rPr().find(qn('w:rFonts'))
            if fonts is not None:
                for attribute in list(fonts.attrib):
                    if attribute.endswith('Theme'):
                        del fonts.attrib[attribute]
    for line in text.splitlines():
        if not line.strip():
            continue
        if line=='<!-- PAGE -->':
            document.add_page_break()
            continue
        style = 'Title' if line.startswith('# ') else 'Heading 1' if line.startswith('## ') else None
        value = re.sub(r'^#{1,2} ', '', line)
        paragraph = document.add_paragraph(style=style)
        for index, part in enumerate(re.split(r'\*\*(.*?)\*\*',value)):
            run = paragraph.add_run(part)
            run.bold = bool(index%2)
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    run = footer.add_run()
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'),'PAGE')
    run._r.addnext(field)
    document.core_properties.title = text.splitlines()[0].removeprefix('# ')
    document.core_properties.author = ''
    document.save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--docx',action='store_true',help='Requires optional python-docx; does not change analysis dependencies')
    args = parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    ledger = {}
    inputs = {}

    def source(name):
        inputs[name] = digest(ROOT/name)
        return read_rows(name)

    def value(key, raw, name, locator, precision=None, count=False):
        shown = f'{int(raw):,}' if count else f'{float(raw):.{precision}f}' if precision is not None else str(raw)
        ledger[key] = dict(source=name, locator=locator, field=key, raw_value=raw, displayed=shown)
        return shown

    cohort = ROOT/'data/processed/admissions_c71_audited.csv'
    cohort_sha = digest(cohort)
    inputs[cohort.relative_to(ROOT).as_posix()] = cohort_sha
    for stage in ['t04','t05','t06']:
        name = f'provenance/{stage}/run_metadata.json'
        metadata = json.loads((ROOT/name).read_text())
        if metadata['inputs_sha256'][cohort.relative_to(ROOT).as_posix()]!=cohort_sha:
            raise ValueError(f'{stage} cohort differs; rebuild before generating manuscript numbers')
        inputs[name] = digest(ROOT/name)
    # T03 was run on Windows: accept only its exact bytes or the exact LF->CRLF transform.
    name = 'provenance/t03/run_metadata.json'
    metadata = json.loads((ROOT/name).read_text())
    expected = metadata['inputs_sha256'][cohort.relative_to(ROOT).as_posix()]
    normalized = cohort.read_bytes().replace(b'\r\n',b'\n')
    variants = {hashlib.sha256(normalized).hexdigest(),hashlib.sha256(normalized.replace(b'\n',b'\r\n')).hexdigest()}
    if expected not in variants:
        raise ValueError('T03 cohort differs beyond exact line endings')
    line_ending_checks = {}
    for name, expected in metadata['inputs_sha256'].items():
        content = (ROOT/name).read_bytes().replace(b'\r\n',b'\n')
        alternatives = {hashlib.sha256(content).hexdigest(),hashlib.sha256(content.replace(b'\n',b'\r\n')).hexdigest()}
        if expected not in alternatives:
            raise ValueError('T03 input fingerprint changed beyond line endings: '+name)
        line_ending_checks[name] = dict(recorded_sha256=expected,current_sha256=digest(ROOT/name),
                                        exact_or_exact_line_ending_equivalence=True)
        inputs[name] = digest(ROOT/name)
    inputs['provenance/t03/run_metadata.json'] = digest(ROOT/'provenance/t03/run_metadata.json')
    flow_name = 'provenance/t02/selection_flow.csv'
    flow = source(flow_name)
    for key, raw, locator in [
        ('source_records',sum(int(r['source_records']) for r in flow),'sum source_records'),
        ('admissions',sum(int(r['eligible_c710_c719']) for r in flow),'sum eligible_c710_c719'),
        ('prefix_records',sum(int(r['c71_prefix_records']) for r in flow),'sum c71_prefix_records'),
        ('prefix_rejected',sum(int(r['c71_prefix_records'])-int(r['eligible_c710_c719']) for r in flow),'sum prefix minus eligible'),
        ('other_records',sum(int(r['other_or_unknown_diagnosis']) for r in flow),'sum other_or_unknown_diagnosis')]:
        value(key,raw,flow_name,locator,count=True)
    fatality_name = 'provenance/t03/admission_fatality.csv'
    fatality = select(source(fatality_name),policy='all_discharges',period='2015-2024',anatomy='Total')
    for key, field, precision, count in [('deaths','deaths',None,True),('fatality','percent',2,False),
                                         ('fatality_lo','lower_95',2,False),('fatality_hi','upper_95',2,False)]:
        value(key,fatality[field],fatality_name,'all_discharges / 2015-2024 / Total / '+field,precision,count)
    rate_name = 'provenance/t03/period_summary_rates.csv'
    rates = source(rate_name)
    for measure,prefix in [('admissions','aahr'),('deaths','death_rate')]:
        row = select(rates,policy='resident',scheme='five_groups',anatomy='Total',measure=measure,
                     estimator='arithmetic_mean_of_10_annual_standardized_rates')
        for suffix,field in [('', 'rate_per_100k'),('_lo','lower_95'),('_hi','upper_95')]:
            value(prefix+suffix,row[field],rate_name,f'resident / five_groups / Total / {measure} / arithmetic mean / {field}',3)
        if measure=='admissions':
            value('resident_admissions',row['events'],rate_name,'resident admission count',count=True)
            value('foreign',int(fatality['admissions'])-int(row['events']),rate_name,'all minus resident admissions',count=True)
    name = 'provenance/t04/all_model_coefficients.csv'
    row = select(source(name),model='primary',variable='age_group',level='80+')
    for key,field in [('age_or','aor'),('age_lo','lower_95'),('age_hi','upper_95')]:
        value(key,row[field],name,'primary / 80+ vs 0-17 / '+field,3)
    name = 'provenance/t05/all_model_coefficients.csv'
    row = select(source(name),panel='site',model='primary',variable='age_group',level='0-17')
    for key,field in [('site_or','aor'),('site_lo','lower_95'),('site_hi','upper_95')]:
        value(key,row[field],name,'site / primary / 0-17 vs 18-44 / '+field,3)
    name = 'provenance/t05/anatomy_descriptive.csv'
    row = select(source(name),anatomy='Unspecified')
    value('unspecified',row['admissions'],name,'Unspecified / admissions',count=True)
    value('unspecified_pct',row['percent'],name,'Unspecified / percent',2)
    name = 'provenance/t05/model_flow.csv'
    flows = source(name)
    for panel,field,key in [('coding','events','coding_events'),('site','included_admissions','site_admissions'),
                            ('site','events','site_events'),('site','excluded_c718','overlapping')]:
        row = select(flows,panel=panel)
        value(key,row[field],name,panel+' / '+field,count=True)
    name = 'provenance/t06/table_scopes.csv'
    row = select(source(name),table=1,variable='residence_area')
    for key,field in [('verified_admissions','included'),('early_admissions','excluded')]:
        value(key,row[field],name,'Table1 / residence / '+field,count=True)
    name = 'provenance/t06/missingness.csv'
    row = select(source(name),table=1,variable='ethnicity')
    value('unknown_ethnicity',row['source_unknown_count'],name,'Table1 / ethnicity / source_unknown_count',count=True)
    template = ROOT/'Writeable/t07_sections_template.md'
    text = template.read_text(encoding='utf-8')
    for key, item in ledger.items():
        text = text.replace('{{'+key+'}}',item['displayed'])
    if re.search(r'\{\{.*?\}\}',text):
        raise ValueError('Unresolved manuscript value placeholder')
    path = ROOT/'Writeable/t07_manuscript_sections.md'
    path.write_text(text,encoding='utf-8')
    (OUT/'numeric_traceability.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
    baseline = ROOT/'data/raw/baseline_2026-10-23/Writeable/tumores encefalo Monica art completo.docx'
    if baseline.exists():
        inputs[baseline.relative_to(ROOT).as_posix()] = digest(baseline)
    inputs[template.relative_to(ROOT).as_posix()] = digest(template)
    inputs['scripts/prepare_t07_sections.py'] = digest(Path(__file__))
    result = dict(prepared_date='2026-11-10',recorded_utc=datetime.now(timezone.utc).isoformat(),
                  inputs_sha256=inputs,section_text_sha256=digest(path),
                  baseline_docx_note='Present at T07 inspection; absent from six-input T01 manifest; origin/version equivalence not established',
                  scope='Replacement title, abstract, framing and Methods; not an integrated submission manuscript',
                  t03_cohort_exact_line_ending_equivalence=True,t03_input_checks=line_ending_checks,number_entries=len(ledger))
    if args.docx:
        docx_path = ROOT/'Writeable/t07_manuscript_sections.docx'
        export_docx(text,docx_path)
        result['docx_sha256'] = digest(docx_path)
    (OUT/'run_metadata.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Prepared {len(ledger)} traceable numeric entries and {len(text.split("<!-- PAGE -->"))} planned pages.')


if __name__=='__main__':
    main()
