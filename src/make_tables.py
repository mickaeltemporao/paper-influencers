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

def overlap_table():
    return None

