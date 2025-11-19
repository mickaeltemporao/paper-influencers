"""Run previous figs code"""
from src.analysis import main as dfs
import pandas as pd

df = dfs()

freq_table = pd.crosstab(df['type'], df['method'])
pct_table = pd.crosstab(df['type'], df['method'], normalize='columns').round(2)
row_margins = freq_table.sum(axis=1)
col_margins = freq_table.sum()
combined_table = freq_table.astype(str) + ' (' + (pct_table * 100).astype(int).astype(str) + '%)'
print(combined_table)
combined_table.to_clipboard(excel=True)

freq_table = pd.crosstab(df['method'], df['idl'])
pct_table = pd.crosstab(df['method'], df['idl'], normalize='index').round(2)
row_margins = freq_table.sum(axis=1)
col_margins = freq_table.sum()
combined_table = freq_table.astype(str) + ' (' + (pct_table * 100).astype(int).astype(str) + '%)'
print(combined_table)
combined_table.to_clipboard(excel=True)

df2 = df[~(df['idl'] == "4. Non-Par.")]
freq_table = pd.crosstab(df2['method'], df2['idl'])
pct_table = pd.crosstab(df2['method'], df2['idl'], normalize='index').round(2)
row_margins = freq_table.sum(axis=1)
col_margins = freq_table.sum()
combined_table = freq_table.astype(str) + ' (' + (pct_table * 100).astype(int).astype(str) + '%)'
print(combined_table)
combined_table.to_clipboard(excel=True)

# Total N of each type of Fropi identified across all methods, with duplicates excluded
for i in df['type'].unique():
    mask = df['type'] == i
    n = len(df.loc[mask, 'username'].unique())
    ntot = 1369
    print(i, n, round(n/ntot, 2))

for i in df['idl'].unique():
    for j in df['method'].unique():

groups = ['idl', 'method', 'type']

df.groupby(groups)['username'].count()
df.groupby(['method', 'type'])['username'].count()
