import json
import os
import pandas as pd

from tqdm import tqdm


def main():
    path_to_json = 'data/raw/tweets-Presidentielle2022/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    cols = ['id', 'created_at', 'author_id', 'referenced_tweets']
    new_cols = ['id', 'created_at', 'author_id', 'referenced_tweets', 'type', 'ref_id']
    keep_cols = ['id', 'created_at', 'author_id', 'type', 'ref_id']

    all_dfs = []
    all_users = []
    for file in tqdm(json_files):
        with open(path_to_json+file) as f:
            d = json.load(f)
        df = pd.json_normalize(d['data'], max_level=2)
        users_df = pd.json_normalize(d['includes']['users'])
        df = df[cols]

        mask = df['referenced_tweets'].isna()
        df['referenced_tweets'] = df['referenced_tweets'].ffill()
        df['referenced_tweets'] = df['referenced_tweets'].bfill()
        df['referenced_tweets'] = df['referenced_tweets'].apply(lambda x: x[0])
        df = pd.concat([df, df['referenced_tweets'].apply(pd.Series)], axis=1)
        df.columns = new_cols
        df = df[keep_cols]
        df.loc[mask, 'type'] = 'tweet'
        df.loc[mask, 'ref_id'] = 0
        all_dfs.append(df)
        all_users.append(users_df)
    pd.concat(all_dfs).to_csv('data/tmp/tweets.csv', index=False)
    pd.concat(all_users)[['id', 'name', 'username']].drop_duplicates().to_csv(
        'data/tmp/twitter-users.csv',
        index=False,
        escapechar='\\'
    )


if __name__ == "__main__":
    main()
