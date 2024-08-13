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


DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
SAMPLE = DATA_PATH + "raw/twitter_10pct_fg.csv"
DATA_M2 = DATA_PATH + "tmp/output_gpt-4o.csv"
DATA_M3 = DATA_PATH + "tmp/output_gpt-4o-mini-2024-07-18_infalgo.csv"

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
df = pd.read_csv(DATA_M2).drop(columns=['description'])
vars = ['username', 'task_type', 'task_sub', 'task_ideology']
df = df[vars]
df.info()

mask = df['task_type'] == 1
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df['task_type'] == 2
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df['task_type'] == 3
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_3)

df['task_ideology'] = df['task_ideology'].replace(idl_values)
df['task_type'] = df['task_type'].replace(type_values)

df['type'] = df['task_type'] + "/" + df['task_sub']


df['username'] = df['username'].str.lower()
df = df.set_index('username')
df_sample['username'] = df_sample['username'].str.lower()
df_sample = df_sample.set_index('username')
df_sample = df_sample.join(df)
df_sample['human_type'] = df_sample['fg_type'] + "/" + df_sample['fg_sub']
df_sample['ai_type'] = df_sample['task_type'] + "/" + df_sample['task_sub']
df_sample['ai_type'] = df_sample['ai_type'].replace(type_desc)
df_sample['human_type'] = df_sample['human_type'].replace(type_desc)

vars_fg = df_sample.columns[df_sample.columns.str.contains('fg')]
vars_task = df_sample.columns[df_sample.columns.str.contains('task')]

# Make table
df['type'] = df['task_type'] + "/" + df['task_sub']

# Method 2 Table
df['type'] = df['type'].replace(type_desc)
pd.crosstab(df['type'],df['task_ideology'], margins=True)

# Method 2 Broad categories
pd.crosstab(df['task_type'],df['task_ideology'], margins=True).round(2)

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
df_algo = pd.read_csv(DATA_M3)
df_algo
mask = df_algo['task_type'] == 1
df_algo.loc[mask, 'task_sub'] = df_algo.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df_algo['task_type'] == 2
df_algo.loc[mask, 'task_sub'] = df_algo.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df_algo['task_type'] == 3
df_algo.loc[mask, 'task_sub'] = df_algo.loc[mask, 'task_sub'].replace(sub_values_3)

df_algo['task_ideology'] = df_algo['task_ideology'].replace(idl_values)
df_algo['task_type'] = df_algo['task_type'].replace(type_values)
df_algo

df_algo[types].groupby('task_type').value_counts().sort_index()
df_algo[types].groupby('task_type').value_counts(normalize=True).sort_index()
df_algo['task_ideology'].value_counts().sort_index()
df_algo['task_ideology'].value_counts(normalize=True).sort_index()

df_algo['type'] = df_algo['task_type'] + "/" + df_algo['task_sub']
df_algo['type'] = df_algo['type'].replace(type_desc)

pd.crosstab(df_algo['type'], df_algo['task_ideology'], margins=True)

# Get proportion of accounts in list of 66 & 477
usr66 = pd.read_table('data/raw/acc_tw_66.txt')['username'].str.lower()
pd.Series(df_algo['username'].str.lower().unique()).isin(usr66).sum()
pd.Series(df_algo['username'].str.lower().unique()).isin(df.index.str.lower()).sum()

# Prepare Figures

# Creating the dataframe
df_66 = pd.DataFrame({
    'task_ideology': ['1. Left', '2. Centre', '3. Right', '4. Non-Par.'],
    'I. Media': [7, 0, 3, 4],
    'II. Pol': [9, 13, 13, 0],
    'III. Other': [13, 3, 28, 8],
})
df_66 = pd.DataFrame(df_66).set_index('task_ideology').T
df_66

vars = ['type', 'sub', 'idl', 'mix']
df.columns = vars
df['method'] = 'M1'

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

df_algo['username'] = df_algo['username'].str.lower()
df_algo = df_algo.set_index('username')
df_algo.columns =  ['description', 'type', 'idl', 'age', 'gender', 'education', 'background', 'sub', 'mix']

df_algo = df_algo[vars].copy()
df_algo['method'] = 'M3'
df_algo

pd.crosstab(df_algo['type'], df_algo['idl'])

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

make_fig(df_66, title='Method 1 | Expert Evaluation \nn=101', output='figures/fig_m1.png')
plot = pd.crosstab(df['type'], df['idl'])
make_fig(plot, title='Method 2 | Hybrid Evaluation \nn=477', output='figures/fig_m2.png')
plot = pd.crosstab(df_fg['type'], df_fg['idl'])
make_fig(plot, title='M2 Human Sample \nn=48', output='figures/fig_m2hm.png')
plot = pd.crosstab(df_ai['type'], df_ai['idl'])
plot['3. Right'] = [0, 0, 0]
plot = plot[["1. Left", "2. Centre", "3. Right", "4. Non-Par."]]
make_fig(plot, title='M2 AI Sample \nn=48', output='figures/fig_m2ai.png')
plot = pd.crosstab(df_algo['type'], df_algo['idl'])
make_fig(plot, title='Method 3 | Algorithmic Evaluation \nn=40', output='figures/fig_m3.png')


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

n1 = df_66.sum().sum()
plot = df_66/n1
make_fig(plot.round(2), title=f'Method 1 | Expert Evaluation \nn={n1}', output='figures/fig_m1_prop.png')
plot = pd.crosstab(df['type'], df['idl'])
n2 = plot.sum().sum()
plot = plot/n2
make_fig(plot.round(2), title=f'Method 2 | Hybrid Evaluation \nn={n2}', output='figures/fig_m2_prop.png')
plot = pd.crosstab(df_algo['type'], df_algo['idl'])
n3 = plot.sum().sum()
plot = plot/n3
make_fig(plot.round(2), title=f'Method 3 | Algorithmic Evaluation \nn={n3}', output='figures/fig_m3_prop.png')

