"""Run previous figs code"""
from src.analysis import main as dfs
import pandas as pd

df1, df2, df3, df4 = dfs()

def fropis_detected_by_method(): 
    df1 = pd.DataFrame({
        'task_ideology': ['1. Left', '2. Centre', '3. Right', '4. Non-Par.'],
        'I. Media': [7, 0, 3, 4],
        'II. Pol': [9, 13, 13, 0],
        'III. Other': [13, 3, 28, 8],
    })
    df1 = pd.DataFrame(df1).set_index('task_ideology').T
    df1['type'] = ['media', 'pol', 'other']
    df1 = df1.set_index('type').sum(axis=1)
    df1.name = 'M1'
    df = pd.concat([df2,df3,df4])
    return pd.concat([df1, pd.crosstab(df['type'], df['method'])], axis=1)

fropis_detected_by_method()

def overlap_table():
    return None

def ideology_table():
    return None

