import json
import os
import numpy as np
import pandas as pd


path_to_json = 'data/tweets-Presidentielle2022/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

with open(path_to_json+json_files[0]) as f:
    d = json.load(f)

df = pd.json_normalize(d['data'], max_level=2)
cols = ['id', 'created_at', 'author_id', 'referenced_tweets']
df = df[cols]

mask = df['referenced_tweets'].isna()
df['referenced_tweets'] = df['referenced_tweets'].ffill()
df['referenced_tweets'] = df['referenced_tweets'].apply(lambda x: x[0])
df = pd.concat([df, df['referenced_tweets'].apply(pd.Series)], axis=1)
df.columns = ['id', 'created_at', 'author_id', 'referenced_tweets', 'type', 'ref_id']
df.loc[mask, 'type'] = 'tweet'
df.loc[mask, 'ref_id'] = np.nan

