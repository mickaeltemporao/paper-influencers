
"""
This module runs a quick analysis to overview the results.
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
MODEL = "gpt-4o"
OUTPUT_FILE_PATH = DATA_PATH + f"tmp/output_{MODEL}.csv"

type_values = {1: "media", 2: "pol", 3: "other"}
sub_values_1 = {1: "alt", 2: "msm"}
sub_values_2 = {1: "current", 2: "party", 3: "nat", 4: "int", 5: "gov"}
sub_values_3 = {1: "pol", 2: "socpol", 3: "soc", 4: "com"}
idl_values = {1: "1. left", 2: "2. centre", 3: "3. right", 4: "np"}
types = ['task_type', 'task_sub']

df = pd.read_csv(OUTPUT_FILE_PATH).drop(columns=['description'])
df = df[['username', 'task_type', 'task_sub', 'task_ideology']]
df.info()


mask = df['task_type'] == 1
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_1)
mask = df['task_type'] == 2
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_2)
mask = df['task_type'] == 3
df.loc[mask, 'task_sub'] = df.loc[mask, 'task_sub'].replace(sub_values_3)

df['task_ideology'] = df['task_ideology'].replace(idl_values)
df['task_type'] = df['task_type'].replace(type_values)

df.head()

df[types].groupby('task_type').value_counts(normalize=True).sort_index()
df[types].groupby('task_type').value_counts().sort_index()
df['task_ideology'].value_counts().sort_index()
df['task_ideology'].value_counts(normalize=True).sort_index()

"""
type                    n      %
media      alt         55   0.65
           msm         30   0.35
other      com        115   0.36
           pol         61   0.19
           soc        115   0.36
           socpol      31   0.10
pol        current     38   0.54
           gov          6   0.09
           int          3   0.04
           nat          5   0.07
           party       18   0.26

ideology      n     %
1. left      49  0.10
2. centre    14  0.03
3. right     36  0.08
np          378  0.79
"""
