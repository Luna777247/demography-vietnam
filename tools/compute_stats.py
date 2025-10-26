import pandas as pd
from pathlib import Path

p = Path(__file__).parents[1]/'raw'/'vietnam.csv'
# read, handle weird unicode minus and percent columns
s = p.read_text(encoding='utf-8')
s = s.replace('\u2212', '-')
with p.open('w', encoding='utf-8') as f:
    f.write(s)

df = pd.read_csv(p, encoding='utf-8')
# clean columns
# Population as numeric
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
# Yearly % Change remove %
df['Yearly % Change'] = df['Yearly % Change'].astype(str).str.replace('%','').astype(float)
# Migrants (net)
# some values might include commas — remove commas
for col in ['Migrants (net)','Yearly Change','Urban Population','Country\'s Share of World Pop']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',','')
# Migrants numeric
if 'Migrants (net)' in df.columns:
    df['Migrants (net)'] = pd.to_numeric(df['Migrants (net)'].str.replace(' ','').replace('', '0'), errors='coerce')
# Median Age
if 'Median Age' in df.columns:
    df['Median Age'] = pd.to_numeric(df['Median Age'], errors='coerce')
# Fertility Rate
if 'Fertility Rate' in df.columns:
    df['Fertility Rate'] = pd.to_numeric(df['Fertility Rate'], errors='coerce')
# Density
if 'Density (P/Km\u00b2)' in df.columns:
    df['Density (P/Km²)'] = pd.to_numeric(df['Density (P/Km\u00b2)'], errors='coerce')
# Urban Pop %
if 'Urban Pop %' in df.columns:
    df['Urban Pop %'] = df['Urban Pop %'].astype(str).str.replace('%','').astype(float)

cols = [
    ('Population','Population'),
    ('Yearly % Change','Yearly % Change'),
    ('Median Age','Median Age'),
    ('Fertility Rate','Fertility Rate'),
    ('Urban Pop %','Urban Pop %'),
    ('Density (P/Km²)','Density (P/Km²)'),
    ('Migrants (net)','Migrants (net)')
]

import numpy as np

def stats(series):
    s = series.dropna()
    return dict(
        mean = s.mean(),
        std = s.std(ddof=1),
        mn = s.min(),
        q25 = s.quantile(0.25),
        q75 = s.quantile(0.75),
        mx = s.max(),
        n = len(s)
    )

results = {}
for name,col in cols:
    if col in df.columns:
        results[name] = stats(df[col])
    else:
        results[name] = None

# Print results nicely
for name in results:
    r = results[name]
    if r is None:
        print(f"{name}: column not found")
    else:
        if name == 'Population':
            # convert to millions for display
            print(name)
            print({k:(v/1e6 if k in ['mean','std','mn','q25','q75','mx'] else v) for k,v in r.items()})
        else:
            print(name, r)

# Also produce LaTeX table with Population in millions and Migrants formatted

def fmt(x, pop=False):
    if pop:
        return f"{x/1e6:.2f}"
    if isinstance(x, (int,)):
        return f"{x:,}"
    return f"{x:.2f}"

print('\nLaTeX table row values:')
rows = []
for name in ['Population','Yearly % Change','Median Age','Fertility Rate','Urban Pop %','Density (P/Km²)','Migrants (net)']:
    r = results[name]
    if name=='Population':
        row = [fmt(r['mean'],pop=True), fmt(r['std'],pop=True), fmt(r['mn'],pop=True), fmt(r['q25'],pop=True), fmt(r['q75'],pop=True), fmt(r['mx'],pop=True)]
    elif name=='Migrants (net)':
        row = [fmt(r['mean']), fmt(r['std']), fmt(int(r['mn'])), fmt(int(r['q25'])), fmt(int(r['q75'])), fmt(int(r['mx']))]
    else:
        row = [fmt(r['mean']), fmt(r['std']), fmt(r['mn']), fmt(r['q25']), fmt(r['q75']), fmt(r['mx'])]
    print(name, ' & '.join(row))
    rows.append((name,row))

# Save a CSV summary
out = pd.DataFrame({name:pd.Series(results[name]) if results[name] else None for name in results})
out.to_csv(Path(__file__).parents[1]/'analysis'/'summary_stats.csv')
print('\nSaved analysis/summary_stats.csv')
