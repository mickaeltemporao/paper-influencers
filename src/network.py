import json
import os
import pandas as pd

from tqdm import tqdm


def get_rt_user(x):
    if isinstance(x, list) and len(x) > 0:
        return x[0]['username']
    else:
        return None

def get_tw_type(x):
    if isinstance(x, list) and len(x) > 0:
        return x[0]['type']
    else:
        return None

def main():
    path_to_json = 'data/raw/tweets-Presidentielle2022/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    keep_cols = ['created_at', 'author_id', 'entities.mentions']
    col_names = ['created_at', 'author_id', 'mentions']

    all_dfs = []
    for file in tqdm(json_files):
        with open(path_to_json+file) as f:
            d = json.load(f)

        df = pd.json_normalize(d['data'])
        users_df = pd.json_normalize(d['includes']['users'])
        mask = df['referenced_tweets'].isna()
        df = df[~mask]
        df['referenced_tweets'] = df['referenced_tweets'].apply(get_tw_type)
        mask = df['referenced_tweets'] == 'retweeted'
        df = df[mask]
        df['entities.mentions'] = df['entities.mentions'].apply(get_rt_user)
        df = df[keep_cols]
        df.columns = col_names
        df['author_id'] = df['author_id'].replace(users_df.set_index('id')['username'])
        all_dfs.append(df)

    all_dfs = pd.concat(all_dfs).to_csv('data/tmp/network.csv', index=False)

if __name__ == "__main__":
    main()

# TODO:
# network
# analysis from last round of eletions
# remove ideology? 
# focus on identification instead of soliving 2 problems identification and classification

