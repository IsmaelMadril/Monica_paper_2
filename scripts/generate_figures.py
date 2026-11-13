"""T09: exact Table3 rate figures and explicit province-count geography."""
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'provenance/t09'
FIGURES=ROOT/'outputs/figures'
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'outputs/reports/matplotlib_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import Normalize
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
import numpy as np
import pandas as pd

YEARS=list(range(2015,2025))
PROVINCES=dict(zip([f'{n:02}' for n in range(1,25)],[
    'Azuay','Bolívar','Cañar','Carchi','Cotopaxi','Chimborazo','El Oro','Esmeraldas',
    'Guayas','Imbabura','Loja','Los Ríos','Manabí','Morona Santiago','Napo','Pastaza',
    'Pichincha','Tungurahua','Zamora Chinchipe','Galápagos','Sucumbíos','Orellana',
    'Santo Domingo de los Tsáchilas','Santa Elena']))
ANATOMY=['Total','Supratentorial','Unspecified','Infratentorial/midline','Overlapping']
COLOURS=['#222222','#0072B2','#009E73','#D55E00','#CC79A7']
MARKERS=['o','s','^','D','v']
MM=1/25.4


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_name(value):
    return ''.join(c for c in unicodedata.normalize('NFKD',value).casefold() if not unicodedata.combining(c)).strip()


def validate_province_fields(data,field,label_field,allow_foreign):
    codes=data[field].astype('string').str.zfill(2)
    allowed=set(PROVINCES)|({'88'} if allow_foreign else set())
    if codes.isna().any() or not codes.isin(allowed).all():
        raise ValueError('Missing/unrecognized province code in '+field)
    expected={**PROVINCES,**({'88':'Exterior'} if allow_foreign else {})}
    for code,group in data.groupby(codes):
        labels=set(group[label_field].dropna().map(normalized_name))
        if group[label_field].isna().any() or labels!={normalized_name(expected[code])}:
            raise ValueError('Province code/name mismatch in '+field+': '+code)
    return codes


def province_grid(data,field,label_field,allow_foreign=False):
    """Zeros require a present audited year; unknown codes are errors, never zero."""
    if set(data.source_year)!=set(YEARS):
        raise ValueError('All ten audited source years must be present before interpreting zeros')
    codes=validate_province_fields(data,field,label_field,allow_foreign)
    included=data.loc[codes.ne('88')].copy()
    included['province_code']=codes.loc[included.index]
    grouped=included.groupby(['province_code','source_year']).size()
    grid=pd.MultiIndex.from_product([list(PROVINCES),YEARS],names=['province_code','source_year'])
    counts=grouped.reindex(grid,fill_value=0).rename('admissions').reset_index()
    counts['province']=counts.province_code.map(PROVINCES)
    counts['status']=np.where(counts.admissions.eq(0),'observed_zero','observed_count')
    counts['assignment']=field
    if int(counts.admissions.sum())!=len(included):raise ValueError('Province count sum mismatch')
    return counts


def validate_rates(table,evidence):
    keys=['policy','scheme','year','anatomy','measure']
    expected=evidence.loc[evidence.policy.eq('resident') & evidence.scheme.eq('five_groups')]
    if table.duplicated(keys).any() or len(table)!=100:
        raise ValueError('Table3 must have exactly100 unique primary rate rows')
    a=table.set_index(keys).sort_index();b=expected.set_index(keys).sort_index()
    if not a.index.equals(b.index):raise ValueError('Table3 does not match primary T03 keys')
    for name in ['events','rate_per_100k','lower_95','upper_95']:
        if not np.allclose(a[name],b[name],rtol=1e-12,atol=1e-12):
            raise ValueError('Table3 differs from executed T03 evidence: '+name)
    if not np.isfinite(a[['rate_per_100k','lower_95','upper_95']]).all().all():raise ValueError('Nonfinite rate/interval')
    if ((a.lower_95<0)|(a.lower_95>a.rate_per_100k)|(a.upper_95<a.rate_per_100k)).any():raise ValueError('Invalid rate interval')
    for (year,measure),part in table.groupby(['year','measure']):
        if not math.isclose(part.loc[part.anatomy.eq('Total'),'rate_per_100k'].iloc[0],part.loc[part.anatomy.ne('Total'),'rate_per_100k'].sum(),abs_tol=1e-12):
            raise ValueError('Nonadditive anatomical rates')
    return table.sort_values(['measure','anatomy','year']).reset_index(drop=True)


def join_boundaries(geo):
    if geo.get('type')!='FeatureCollection' or len(geo['features'])!=24:raise ValueError('Expected24 boundary features')
    if geo.get('crs',{}).get('properties',{}).get('name') not in ['urn:ogc:def:crs:OGC:1.3:CRS84','urn:ogc:def:crs:EPSG::4326']:
        raise ValueError('Unexpected geometry CRS')
    lookup={normalized_name(name):code for code,name in PROVINCES.items()}
    features={};crosswalk=[]
    for feature in geo['features']:
        prop=feature['properties'];name=normalized_name(prop['shapeName'])
        if name not in lookup:raise ValueError('Unmatched boundary name: '+name)
        code=lookup[name]
        if code in features:raise ValueError('Duplicate boundary province: '+code)
        if feature['geometry']['type'] not in ['Polygon','MultiPolygon']:raise ValueError('Nonpolygon province')
        features[code]=feature
        crosswalk.append(dict(province_code=code,province=PROVINCES[code],boundary_name=prop['shapeName'],
                              boundary_id=prop['shapeID'],source_ISO_not_used=prop['shapeISO']))
    if set(features)!=set(PROVINCES):raise ValueError('Incomplete province boundary join')
    return features,pd.DataFrame(crosswalk).sort_values('province_code')


def ring_area(points):
    points=np.asarray(points,float)
    return .5*np.sum(points[:-1,0]*points[1:,1]-points[1:,0]*points[:-1,1])


def polygon_path(rings):
    vertices=[];codes=[]
    for index,ring in enumerate(rings):
        points=np.asarray(ring,float)[:,:2]
        if len(points)<4 or not np.isfinite(points).all() or not np.array_equal(points[0],points[-1]):
            raise ValueError('Invalid polygon ring')
        # Nonzero winding: exterior counterclockwise, holes clockwise.
        if (ring_area(points)>0)!=(index==0):points=points[::-1]
        vertices.extend(points);codes.extend([MplPath.MOVETO]+[MplPath.LINETO]*(len(points)-2)+[MplPath.CLOSEPOLY])
    return MplPath(vertices,codes)


def polygons(feature):
    g=feature['geometry']
    return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']


def label_point(feature):
    """Choose an interior point on the largest polygon, away from its vertices."""
    ring=max(polygons(feature),key=lambda p:abs(ring_area(p[0])))[0]
    points=np.asarray(ring,float)[:,:2];path=polygon_path([ring])
    x=np.linspace(points[:,0].min(),points[:,0].max(),35)
    y=np.linspace(points[:,1].min(),points[:,1].max(),35)
    candidates=np.array(np.meshgrid(x,y)).reshape(2,-1).T
    candidates=candidates[path.contains_points(candidates)]
    if not len(candidates):raise ValueError('No interior label point')
    distances=((candidates[:,None,:]-points[None,:,:])**2).sum(2).min(1)
    return candidates[distances.argmax()]


def save_figure(fig,name,preview=True):
    for suffix in ['pdf','svg','png']:
        options={'dpi':600} if suffix=='png' else {}
        fig.savefig(FIGURES/f'{name}.{suffix}',**options)
    if preview:
        shutil.copyfile(FIGURES/f'{name}.png',OUT/f'{name}_preview.png')


def rate_figure(rates):
    fig,axes=plt.subplots(2,1,figsize=(180*MM,165*MM),sharex=True)
    fig.subplots_adjust(left=.14,right=.98,bottom=.10,top=.84,hspace=.27)
    for ax,measure,title in zip(axes,['admissions','deaths'],['A  Hospitalizations','B  In-hospital deaths']):
        for anatomy,colour,marker in zip(ANATOMY,COLOURS,MARKERS):
            part=rates.loc[rates.measure.eq(measure)&rates.anatomy.eq(anatomy)].sort_values('year')
            ax.plot(part.year,part.rate_per_100k,label=anatomy,color=colour,marker=marker,markersize=3.5,
                    linewidth=1.4 if anatomy=='Total' else 1.0)
            if anatomy=='Total':
                ax.fill_between(part.year,part.lower_95,part.upper_95,color=colour,alpha=.12,linewidth=0)
        ax.set_title(title,loc='left',fontsize=10,fontweight='bold')
        ax.set_ylabel('Rate per 100,000 residents',fontsize=8.5)
        ax.set_ylim(bottom=0);ax.set_xlim(2014.75,2024.25)
        ax.grid(axis='y',color='#dddddd',linewidth=.5)
        ax.spines[['right','top']].set_visible(False)
    axes[1].set_xticks(YEARS);axes[1].set_xlabel('Discharge year',fontsize=9)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.55,.98),ncol=3,frameon=False,fontsize=8)
    fig.text(.55,.875,'Shading: total 95% interval; all component intervals in companion table',ha='center',fontsize=7.3)
    save_figure(fig,'figure1_rates');plt.close(fig)


def heatmap(counts,name,title,vmax):
    frame=counts.pivot(index='province_code',columns='source_year',values='admissions').reindex(index=PROVINCES,columns=YEARS)
    values=frame.to_numpy(dtype=float)
    fig,ax=plt.subplots(figsize=(180*MM,185*MM))
    fig.subplots_adjust(left=.325,right=.975,top=.88,bottom=.18)
    cmap=plt.get_cmap('YlOrBr').copy();cmap.set_bad('#bdbdbd')
    norm=Normalize(0,vmax)
    mesh=ax.pcolormesh(np.ma.masked_invalid(values),cmap=cmap,norm=norm,edgecolors='white',linewidth=.35,rasterized=False)
    ax.set_ylim(24,0);ax.set_xlim(0,10)
    ax.set_xticks(np.arange(10)+.5,YEARS);ax.xaxis.tick_top()
    ax.set_yticks(np.arange(24)+.5,[f'{code}  {PROVINCES[code]}' for code in PROVINCES])
    ax.tick_params(length=0,pad=4,labelsize=7.5)
    for i in range(24):
        for j in range(10):
            value=values[i,j]
            rgba=cmap(norm(value)) if np.isfinite(value) else (.7,.7,.7,1)
            luminance=.2126*rgba[0]+.7152*rgba[1]+.0722*rgba[2]
            ax.text(j+.5,i+.5,str(int(value)) if np.isfinite(value) else 'NA',ha='center',va='center',fontsize=7.2,
                    color='white' if luminance<.48 else 'black')
    for spine in ax.spines.values():spine.set_visible(False)
    fig.suptitle(title,fontsize=11,y=.97)
    fig.text(.65,.925,f'N={int(counts.admissions.sum()):,} admission records | discharge year',ha='center',fontsize=8.2)
    cax=fig.add_axes([.38,.113,.55,.018]);bar=fig.colorbar(mesh,cax=cax,orientation='horizontal');bar.solids.set_rasterized(False)
    cax.set_xlabel('Admission counts (same scale for all years)',fontsize=7.5)
    cax.tick_params(labelsize=7.5)
    fig.text(.325,.022,'0 = no matching records in the audited release; grey/NA = unavailable\nCounts describe recorded admissions, not population incidence or risk.',fontsize=7.2)
    save_figure(fig,name);plt.close(fig)


def atlas(features,counts,vmax):
    cmap=plt.get_cmap('YlOrBr');norm=Normalize(0,vmax)
    positions={code:label_point(feature) for code,feature in features.items()}
    with PdfPages(FIGURES/'figureS1_residence_atlas.pdf') as pdf:
        for year in YEARS:
            values=counts.loc[counts.source_year.eq(year)].set_index('province_code').admissions
            fig=plt.figure(figsize=(180*MM,180*MM))
            main=fig.add_axes([.035,.34,.62,.56]);inset=fig.add_axes([.08,.205,.23,.125])
            for code,feature in features.items():
                ax=inset if code=='20' else main
                for polygon in polygons(feature):
                    ax.add_patch(PathPatch(polygon_path(polygon),facecolor=cmap(norm(values[code])),edgecolor='#555555',linewidth=.4))
                point=positions[code]
                ax.text(*point,code,ha='center',va='center',fontsize=7.5,
                        bbox=dict(boxstyle='round,pad=.08',facecolor='white',edgecolor='none',alpha=.85))
            main.set_xlim(-81.5,-75.0);main.set_ylim(-5.2,1.6)
            islands=np.concatenate([np.asarray(p[0])[:,:2] for p in polygons(features['20'])])
            inset.set_xlim(islands[:,0].min()-.1,islands[:,0].max()+.1)
            inset.set_ylim(islands[:,1].min()-.1,islands[:,1].max()+.1)
            main.set_aspect('equal');main.set_axis_off()
            inset.set_aspect('equal');inset.set_xticks([]);inset.set_yticks([])
            for spine in inset.spines.values():spine.set_edgecolor('#cccccc');spine.set_linewidth(.4)
            inset.set_title('Galápagos inset',fontsize=7.5,pad=1)
            fig.text(.68,.865,'INEC province codes',fontsize=8.5,fontweight='bold')
            for index,(code,province) in enumerate(PROVINCES.items()):
                label=province
                fig.text(.68,.832-index*.0235,f'{code}  {label}',fontsize=7.5,va='top',linespacing=1.0)
            fig.suptitle(f'{year}  Admissions by province of residence',fontsize=11,y=.975)
            fig.text(.5,.931,f'N={int(values.sum()):,} resident admission records | shared count scale',ha='center',fontsize=8)
            sm=matplotlib.cm.ScalarMappable(norm=norm,cmap=cmap)
            cax=fig.add_axes([.12,.14,.70,.018]);bar=fig.colorbar(sm,cax=cax,orientation='horizontal');bar.solids.set_rasterized(False)
            cax.set_xlabel('Admission counts (not population rates)',fontsize=8);cax.tick_params(labelsize=7.5)
            fig.text(.05,.035,'Fixed geoBoundaries ECU ADM1 (2011 representation); Wikimedia Commons source.\n'
                     'geoBoundaries / William & Mary geoLab. Lon/lat view; Galápagos repositioned at a different scale.\n'
                     'Zeros are observed records absent from that province/year; no annual boundary/completeness validation.',fontsize=7)
            pdf.savefig(fig)
            fig.savefig(FIGURES/f'figureS1_{year}.svg')
            fig.savefig(FIGURES/f'figureS1_{year}.png',dpi=300)
            plt.close(fig)


def main():
    OUT.mkdir(parents=True,exist_ok=True);FIGURES.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.titlesize':10,
                         'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'svg.fonttype':'none'})
    metadata=json.loads((ROOT/'provenance/t03/run_metadata.json').read_text())
    checks={}
    for name,expected in metadata['inputs_sha256'].items():
        path=ROOT/name;content=path.read_bytes().replace(b'\r\n',b'\n')
        alternatives={hashlib.sha256(content).hexdigest(),hashlib.sha256(content.replace(b'\n',b'\r\n')).hexdigest()}
        if expected not in alternatives:raise ValueError('T03 input changed beyond line endings: '+name)
        checks[name]=dict(expected_sha256=expected,current_sha256=digest(path),exact_or_line_ending_equivalent=True)
    cohort_path=ROOT/'data/processed/admissions_c71_audited.csv'
    data=pd.read_csv(cohort_path,dtype={'prov_res':'string','prov_ubi':'string'})
    if not data.admission_id.is_unique or not data.death.isin([0,1]).all():raise ValueError('Invalid cohort keys/outcomes')
    annual=data.groupby('source_year').size()
    flow=pd.read_csv(ROOT/'provenance/t02/selection_flow.csv').set_index('year')
    if set(annual.index)!=set(YEARS) or not annual.eq(flow.eligible_c710_c719).all():raise ValueError('Annual cohort/selection mismatch')
    table_path=ROOT/'outputs/tables/table3_rebuilt.csv'
    if not table_path.exists():raise FileNotFoundError('Run scripts/calculate_rates.py to generate Table3 before T09')
    rates=validate_rates(pd.read_csv(table_path),pd.read_csv(ROOT/'provenance/t03/annual_standardized_rates.csv'))
    residence=province_grid(data,'prov_res','residence_province',True)
    facility=province_grid(data,'prov_ubi','facility_province')
    excluded=data.loc[data.prov_res.str.zfill(2).eq('88')]
    if len(excluded)!=3 or int(excluded.death.sum())!=0:raise ValueError('Foreign-resident geography exclusions changed')
    manifest=json.loads((OUT/'boundary_manifest.json').read_text())
    for item in manifest['files']:
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('Boundary hash changed')
    features,crosswalk=join_boundaries(json.loads((OUT/'ecuador_adm1.geojson').read_text()))
    for name,frame in [('figure1_rates',rates),('figure2_residence_counts',residence),('facility_counts',facility),('province_boundary_crosswalk',crosswalk)]:
        frame.to_csv(OUT/f'{name}.csv',index=False)
    margins=[]
    for year in YEARS:
        r=int(residence.loc[residence.source_year.eq(year),'admissions'].sum())
        f=int(facility.loc[facility.source_year.eq(year),'admissions'].sum())
        foreign=int(excluded.source_year.eq(year).sum())
        if f!=int(annual[year]) or r+foreign!=f:raise ValueError('Geographic annual margins fail')
        margins.append(dict(year=year,residence_admissions=r,foreign_excluded=foreign,facility_admissions=f,source_admissions=int(annual[year]),passed=True))
    pd.DataFrame(margins).to_csv(OUT/'geography_reconciliation.csv',index=False)
    controls={}
    for year,group,measure,key in [(2017,'Total','deaths','2017_total_death_rate'),(2024,'Total','admissions','2024_total_admission_rate'),(2024,'Unspecified','admissions','2024_unspecified_admission_rate')]:
        row=rates.loc[rates.year.eq(year)&rates.anatomy.eq(group)&rates.measure.eq(measure)].iloc[0]
        controls[key]={k:float(row[k]) for k in ['events','rate_per_100k','lower_95','upper_95']}
    vmax=int(math.ceil(max(residence.admissions.max(),facility.admissions.max())/50)*50)
    rate_figure(rates)
    heatmap(residence,'figure2_residence_counts','Admissions by province of residence',vmax)
    heatmap(facility,'figureS2_facility_counts','Admissions by treating-facility province',vmax)
    atlas(features,residence,vmax)
    inputs=[cohort_path,table_path,ROOT/'provenance/t03/annual_standardized_rates.csv',ROOT/'provenance/t02/selection_flow.csv',
            OUT/'boundary_manifest.json',OUT/'ecuador_adm1.geojson',OUT/'analysis_specification.md',
            ROOT/'scripts/generate_figures.py',ROOT/'requirements-figures.txt']
    result=dict(prepared_date='2026-11-13',recorded_utc=datetime.now(timezone.utc).isoformat(),
                inputs_sha256={p.relative_to(ROOT).as_posix():digest(p) for p in inputs},t03_input_checks=checks,
                matplotlib=matplotlib.__version__,numpy=np.__version__,pandas=pd.__version__,
                rate_points=100,residence_cells=240,facility_cells=240,residence_admissions=int(residence.admissions.sum()),
                facility_admissions=int(facility.admissions.sum()),foreign_exclusions=3,unknown_province_exclusions=0,
                count_scale_min=0,count_scale_max=vmax,count_scale_type='shared linear',
                rate_controls=controls,boundary_join='24-to-24 by explicit province name/code crosswalk, accent normalization only',
                source_ISO_not_used_duplicates=crosswalk.loc[crosswalk.source_ISO_not_used.duplicated(False),'source_ISO_not_used'].unique().tolist(),
                geography='residence primary; facility separate; both count admission records',
                rendering='180mm width main figures; PDF/SVG;600dpi PNG; ten-page atlas PDF and annual SVG/300dpi preview',
                outputs_sha256={p.name:digest(p) for p in FIGURES.glob('*') if p.suffix in ['.pdf','.svg','.png']})
    (OUT/'run_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['rate_points','residence_admissions','facility_admissions','count_scale_max','rate_controls']},indent=2))


if __name__=='__main__':main()
