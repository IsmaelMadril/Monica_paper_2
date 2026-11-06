"""Extract age-specific annual denominators and actual CPV2022 standard counts."""
import csv, hashlib, re
from pathlib import Path
import openpyxl
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / 'provenance/t03'

def group_age(age, scheme):
    if scheme == 'five_groups':
        return '0-17' if age <= 17 else '18-44' if age <= 44 else '45-64' if age <= 64 else '65-79' if age <= 79 else '80+'
    if scheme == 'five_years':
        return '85+' if age >= 85 else f'{int(age)//5*5}-{int(age)//5*5+4}'
    raise ValueError(scheme)

def main():
    with (PROV/'population_manifest.csv').open(encoding='utf-8', newline='') as stream:
        records = {r['role']: r for r in csv.DictReader(stream)}
    for row in records.values():
        with (ROOT/row['path']).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != row['sha256']:
                raise ValueError('Population source checksum mismatch')
    projection = openpyxl.load_workbook(ROOT/records['annual_denominators']['path'], read_only=True, data_only=True)
    sheet = list(projection['1.1'].values)
    assert 'Revisión 2024' in str(sheet[9][2])
    assert '30 de junio' in str(sheet[117][1])
    denominator = []
    for year in range(2015, 2025):
        starts = [i for i, v in enumerate(sheet[13]) if v == year]
        assert len(starts) == 1
        start = starts[0]
        assert sheet[14][start:start+3] == ('Hombre', 'Mujer', 'Total')
        for row_number, row in enumerate(sheet[15:116], start=16):
            text = str(row[1]).strip()
            age = 100 if text == '100 y más' else int(text)
            male, female, total = row[start:start+3]
            assert male + female == total and total > 0
            denominator.append(dict(year=year, age=age, population=total, source_sheet='1.1',
                                    source_cell=f'{openpyxl.utils.get_column_letter(start+3)}{row_number}'))
        assert sum(r['population'] for r in denominator if r['year'] == year) == sheet[116][start+2]
    census = openpyxl.load_workbook(ROOT/records['census_standard']['path'], read_only=True, data_only=True)
    standard = []
    total = None
    for row_number, row in enumerate(census['3'].values, start=1):
        if row[1] != 'Total Nacional':
            continue
        if row[2] == 'Total Nacional':
            total = row[3]
            continue
        match = re.match(r'^(\d+) años', str(row[2]))
        if match:
            age = int(match.group(1))
            assert row[4] + row[5] == row[3]
            standard.append(dict(age=age, standard_population=row[3], source_sheet='3', source_cell=f'D{row_number}'))
    pop, std = pd.DataFrame(denominator), pd.DataFrame(standard)
    assert set(std.age) == set(range(101)) and std.age.is_unique
    assert std.standard_population.sum() == total == 16938986
    assert all(set(g.age) == set(range(101)) for _, g in pop.groupby('year'))
    pop.to_csv(PROV/'population_single_age.csv', index=False)
    std.to_csv(PROV/'census_2022_single_age.csv', index=False)
    grouped_pop, grouped_std = [], []
    for scheme in ['five_groups', 'five_years']:
        p = pop.assign(age_group=pop.age.map(lambda a: group_age(a, scheme)))
        s = std.assign(age_group=std.age.map(lambda a: group_age(a, scheme)))
        pg = p.groupby(['year', 'age_group'], sort=False).population.sum().reset_index()
        sg = s.groupby('age_group', sort=False).standard_population.sum().reset_index()
        pg['scheme'] = scheme
        sg['scheme'] = scheme
        sg['standard_weight'] = sg.standard_population / total
        assert abs(sg.standard_weight.sum()-1) < 1e-12
        grouped_pop.append(pg)
        grouped_std.append(sg)
    pd.concat(grouped_pop).to_csv(PROV/'annual_population_by_age.csv', index=False)
    pd.concat(grouped_std).to_csv(PROV/'standard_weights_2022.csv', index=False)
    print('Extracted 101 ages for each of 10 denominator years; actual census standard:', total)
    print(pop.groupby('year').population.sum().to_string())
    print(pd.concat(grouped_std).query("scheme=='five_groups'").to_string(index=False))

if __name__ == '__main__':
    main()
