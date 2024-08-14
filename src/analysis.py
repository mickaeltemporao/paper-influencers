"""
This module runs a quick analysis to overview the results.
"""


import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from dotenv import find_dotenv, load_dotenv
from sklearn.metrics import cohen_kappa_score

load_dotenv(find_dotenv())


# TODO: Check account descriptions used are the ones from election camapaign!
DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
SAMPLE = DATA_PATH + "raw/twitter_10pct_fg.csv"
DATA_M2 = DATA_PATH + "tmp/output_gpt-4o.csv"
DATA_M3 = DATA_PATH + "tmp/output_gpt-4o-mini-2024-07-18_infalgo.csv"
DATA_M4 = DATA_PATH + "tmp/output_gpt-4o-mini-2024-07-18_networkalgo.csv"

type_values = {1: "I. Media", 2: "II. Pol", 3: "III. Other"}
sub_values_1 = {1: "alt", 2: "msm"}
sub_values_2 = {1: "current", 2: "party", 3: "nat", 4: "int", 5: "gov"}
sub_values_3 = {1: "pol", 2: "socpol", 3: "soc", 4: "com"}
idl_values = {1: "1. Left", 2: "2. Centre", 3: "3. Right", 4: "4. Non-Par."}
types = ['task_type', 'task_sub']
type_desc = {
    'media/msm': 'I.1. media/msm',
    'media/alt': 'I.2. media/alt',
    'pol/current': 'II.1. pol/current',
    'pol/party': 'II.2. pol/party',
    'pol/nat': 'II.3. pol/nat',
    'pol/int': 'II.4. pol/int',
    'pol/gov': 'II.5. pol/gov',
    'other/pol': 'III.1. other/pol',
    'other/socpol': 'III.2. other/socpol',
    'other/soc': 'III.3. other/soc',
    'other/com': 'III.4. other/com',
}

sample_idl_values = {"left": "1. Left", "centre": "2. Centre", "right": "3. Right", "non partisan": "4. Non-Par."}


# Prep Human Coded Sample
df_sample = pd.read_csv(SAMPLE)
df_sample['fg_type'] = df_sample['fg_type'].str.lower()
df_sample['fg_idl'] = df_sample['fg_idl'].str.lower()
df_sample[['fg_type', 'fg_sub']] = df_sample['fg_type'].str.split("/", expand=True)
vars = ["username", "fg_type", "fg_sub", "fg_idl"]
df_sample = df_sample[vars]

# WARNING: THERE ARE MISSING VALUES -> RECODED NON PARTISAN : OK with FG
mask = df_sample['fg_idl'].isna()
df_sample.loc[mask, 'fg_idl'] = "non partisan"
df_sample['fg_idl'] = df_sample['fg_idl'].replace(sample_idl_values)


# WARNING: THERE ARE MISSING VALUES OBS bernard_montiel
# WE CODED IT TOGETHER WITH FG bernard_montiel,MEDIA/MSM,NON PARTISAN
mask = df_sample['fg_type'].str.contains("media", na=False)
df_sample.loc[mask, 'fg_type'] = 1
mask = df_sample['fg_type'].str.contains("pol", na=False)
df_sample.loc[mask, 'fg_type'] = 2
mask = df_sample['fg_type'].str.contains("opooi", na=False)
df_sample.loc[mask, 'fg_type'] = 3
df_sample['fg_type'] = df_sample['fg_type'].replace(type_values)

# """TODO: Check with FG if former = nat (subcat 3 of pols)
# 1: "current", 2: "party", 3: "nat", 4: "int", 5: "gov"}
# OK WITH FG
mask = df_sample['fg_sub'] == 'former'
df_sample.loc[mask, 'fg_sub'] = 'nat'

# TODO: Check with FG if recode is correct espectially for social and social2
# Seems ok!
mask = df_sample['fg_type'] == "other"
sample_sub_values_3 = {
    "pol": "pol",
    "social": "socpol",
    "social2": "soc",
    "market": "com"
}

df_sample.loc[mask, 'fg_sub'] = df_sample.loc[mask, 'fg_sub'].replace(sample_sub_values_3)

df_sample = df_sample.dropna()
accounts = df_sample['username']


# Prep M2 Data
df2 = pd.read_csv(DATA_M2).drop(columns=['description'])
vars = ['username', 'task_type', 'task_sub', 'task_ideology']
df2 = df2[vars]
df2.info()

mask = df2['task_type'] == 1
df2.loc[mask, 'task_sub'] = df2.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df2['task_type'] == 2
df2.loc[mask, 'task_sub'] = df2.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df2['task_type'] == 3
df2.loc[mask, 'task_sub'] = df2.loc[mask, 'task_sub'].replace(sub_values_3)

df2['task_ideology'] = df2['task_ideology'].replace(idl_values)
df2['task_type'] = df2['task_type'].replace(type_values)

df2['type'] = df2['task_type'] + "/" + df2['task_sub']


df2['username'] = df2['username'].str.lower()
df2 = df2.set_index('username')
df_sample['username'] = df_sample['username'].str.lower()
df_sample = df_sample.set_index('username')
df_sample = df_sample.join(df2)
df_sample['human_type'] = df_sample['fg_type'] + "/" + df_sample['fg_sub']
df_sample['ai_type'] = df_sample['task_type'] + "/" + df_sample['task_sub']
df_sample['ai_type'] = df_sample['ai_type'].replace(type_desc)
df_sample['human_type'] = df_sample['human_type'].replace(type_desc)

vars_fg = df_sample.columns[df_sample.columns.str.contains('fg')]
vars_task = df_sample.columns[df_sample.columns.str.contains('task')]

# Make table
df2['type'] = df2['task_type'] + "/" + df2['task_sub']

# Method 2 Table
df2['type'] = df2['type'].replace(type_desc)
pd.crosstab(df2['type'],df2['task_ideology'], margins=True)

# Method 2 Broad categories
pd.crosstab(df2['task_type'],df2['task_ideology'], margins=True).round(2)

# Method 2 Broad categories sample
pd.crosstab(df_sample['ai_type'],df_sample['task_ideology'], margins=True).round(2)
# Method 2 Broad categories sample
pd.crosstab(df_sample['human_type'],df_sample['fg_idl'], margins=True)

cohen_kappa_score(df_sample['fg_type'], df_sample['task_type'])
cohen_kappa_score(df_sample['fg_sub'], df_sample['task_sub'])
cohen_kappa_score(df_sample['fg_idl'], df_sample['task_ideology'])

test = df_sample['fg_type'] == df_sample['task_type']
test.mean()
test = df_sample['fg_sub'] == df_sample['task_sub']
test.mean()
test = df_sample['fg_idl'] == df_sample['task_ideology']
test.mean()


# Method 3: Analyasis of influencers based on ALGO Method (3)
df3 = pd.read_csv(DATA_M3)
df3
mask = df3['task_type'] == 1
df3.loc[mask, 'task_sub'] = df3.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df3['task_type'] == 2
df3.loc[mask, 'task_sub'] = df3.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df3['task_type'] == 3
df3.loc[mask, 'task_sub'] = df3.loc[mask, 'task_sub'].replace(sub_values_3)

df3['task_ideology'] = df3['task_ideology'].replace(idl_values)
df3['task_type'] = df3['task_type'].replace(type_values)
df3

df3[types].groupby('task_type').value_counts().sort_index()
df3[types].groupby('task_type').value_counts(normalize=True).sort_index()
df3['task_ideology'].value_counts().sort_index()
df3['task_ideology'].value_counts(normalize=True).sort_index()

df3['type'] = df3['task_type'] + "/" + df3['task_sub']
df3['type'] = df3['type'].replace(type_desc)

pd.crosstab(df3['type'], df3['task_ideology'], margins=True)

# Method 4 - Network
DATA_M4 = DATA_PATH + "tmp/output_gpt-4o-mini-2024-07-18_networkalgo_m4.csv"
df4 = pd.read_csv(DATA_M4).drop(columns=['description'])
mask = df4['task_type'] == 1
df4.loc[mask, 'task_sub'] = df4.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df4['task_type'] == 2
df4.loc[mask, 'task_sub'] = df4.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df4['task_type'] == 3
df4.loc[mask, 'task_sub'] = df4.loc[mask, 'task_sub'].replace(sub_values_3)

df4['task_ideology'] = df4['task_ideology'].replace(idl_values)
df4['task_type'] = df4['task_type'].replace(type_values)
df4['type'] = df4['task_type'] + "/" + df4['task_sub']
df4['type'] = df4['type'].replace(type_desc)

pd.crosstab(df4['type'], df4['task_ideology'], margins=True)

df4.columns =  ['username', 'type', 'idl', 'age', 'gender', 'education', 'background', 'sub', 'mix']

# Get proportion of accounts in list of 66 & 477
usr66 = pd.read_table('data/raw/acc_tw_66.txt')['username'].str.lower()
usr66
usr66

pd.Series(df3['username'].str.lower().unique()).isin(usr66).sum()
pd.Series(df3['username'].str.lower().unique()).isin(df2.index.str.lower()).sum()
pd.Series(df3['username'].str.lower().unique()).isin(df4['username'].str.lower().unique()).sum()
pd.Series(df4['username'].str.lower().unique()).isin(df2.index.str.lower()).sum()

# Prepare Figures

# Creating the dataframe
df1 = pd.DataFrame({
    'task_ideology': ['1. Left', '2. Centre', '3. Right', '4. Non-Par.'],
    'I. Media': [7, 0, 3, 4],
    'II. Pol': [9, 13, 13, 0],
    'III. Other': [13, 3, 28, 8],
})
df1 = pd.DataFrame(df1).set_index('task_ideology').T
df1

vars = ['type', 'sub', 'idl', 'mix']
df2.columns = vars
df2['method'] = 'M2'

df_fg = df_sample[df_sample.columns[df_sample.columns.str.contains('fg|human')]]
df_fg
df_fg.columns = vars
df_fg['method'] = 'M2 Sample HM'

df_ai = df_sample[df_sample.columns[~df_sample.columns.str.contains('fg|human')]]
df_ai = df_ai.drop(columns = ['ai_type'])
df_ai
df_ai.columns = vars
df_ai
df_ai['method'] = 'M2 Sample IA'

df3['username'] = df3['username'].str.lower()
df3 = df3.set_index('username')
df3.columns =  ['description', 'type', 'idl', 'age', 'gender', 'education', 'background', 'sub', 'mix']
df3['method'] = 'M3'
pd.crosstab(df3['type'], df3['idl'])

def make_fig(df, title='Method 1 (n=101)', output='heatmap_square.png'):
# Plotting the heatmap
    plt.figure(figsize=(10, 10))
    sns.heatmap(df, annot=True, cmap='Blues', linewidths=3, annot_kws={"size": 40}, cbar=False, square=True, fmt=".0f")
    plt.title(title, fontsize=26)
    plt.xlabel('Ideology', fontsize=24)
    plt.ylabel('Type', fontsize=24)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig(output, bbox_inches='tight', pad_inches=0.1)


n1 = df1.sum().sum()
make_fig(df1, title=f'Method 1 | Expert Evaluation \nn={n1}', output='figures/fig_m1.png')
plot = pd.crosstab(df2['type'], df2['idl'])
n2 = plot.sum().sum()
make_fig(plot, title=f'Method 2 | Hybrid Evaluation \nn={n2}', output='figures/fig_m2.png')
plot = pd.crosstab(df_fg['type'], df_fg['idl'])
nsample = plot.sum().sum()
make_fig(plot, title=f'M2 Human Sample \nn={nsample}', output='figures/fig_m2hm.png')
plot = pd.crosstab(df_ai['type'], df_ai['idl'])
plot['3. Right'] = [0, 0, 0]
plot = plot[["1. Left", "2. Centre", "3. Right", "4. Non-Par."]]
make_fig(plot, title=f'M2 AI Sample \nn={nsample}', output='figures/fig_m2ai.png')
plot = pd.crosstab(df3['type'], df3['idl'])
n3 = plot.sum().sum()
make_fig(plot, title=f'Method 3 | Algorithmic Evaluation \nn={n3}', output='figures/fig_m3.png')
plot = pd.crosstab(df4['type'], df4['idl'])
n4 = plot.sum().sum()
make_fig(plot, title=f'Method 4 | Centrality - Indegree \nn={n4}', output='figures/fig_m4.png')




def make_fig(df, title='Method 1 (n=101)', output='heatmap_square.png'):
# Plotting the heatmap
    plt.figure(figsize=(10, 10))
    sns.heatmap(df, annot=True, cmap='Blues', linewidths=3, annot_kws={"size": 40}, cbar=False, fmt=".2f")
    plt.title(title, fontsize=26)
    plt.xlabel('Ideology', fontsize=24)
    plt.ylabel('Type', fontsize=24)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig(output, bbox_inches='tight', pad_inches=0.1)

plot = df1/n1
make_fig(plot.round(2), title=f'Method 1 | Expert Evaluation \nn={n1}', output='figures/fig_m1_prop.png')
plot = pd.crosstab(df2['type'], df2['idl'])
plot = plot/n2
make_fig(plot.round(2), title=f'Method 2 | Hybrid Evaluation \nn={n2}', output='figures/fig_m2_prop.png')
plot = pd.crosstab(df3['type'], df3['idl'])
plot = plot/n3
make_fig(plot.round(2), title=f'Method 3 | Algorithmic Evaluation \nn={n3}', output='figures/fig_m3_prop.png')
plot = pd.crosstab(df4['type'], df4['idl'])
plot = plot/n4
make_fig(plot.round(2), title=f'Method 4 | Centrality - Indegree \nn={n4}', output='figures/fig_m4_prop.png')

