"""
This module runs a quick analysis to overview the results.
"""


import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.metrics import cohen_kappa_score


load_dotenv(find_dotenv())


DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
MODEL = "gpt-4o"
OUTPUT_FILE_PATH = DATA_PATH + f"tmp/output_{MODEL}.csv"
SAMPLE = DATA_PATH + "raw/twitter_10pct_fg.csv"

type_values = {1: "media", 2: "pol", 3: "other"}
sub_values_1 = {1: "alt", 2: "msm"}
sub_values_2 = {1: "current", 2: "party", 3: "nat", 4: "int", 5: "gov"}
sub_values_3 = {1: "pol", 2: "socpol", 3: "soc", 4: "com"}
idl_values = {1: "1. left", 2: "2. centre", 3: "3. right", 4: "4. non partisan"}
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

sample_idl_values = {"left": "1. left", "centre": "2. centre", "right": "3. right", "non partisan": "4. non partisan"}


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


# Prep GPT Coded Data
df = pd.read_csv(OUTPUT_FILE_PATH).drop(columns=['description'])
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


df = df.set_index('username')
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
df_algo = pd.read_csv("data/tmp/output_gpt-4o_infalgo.csv")
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

