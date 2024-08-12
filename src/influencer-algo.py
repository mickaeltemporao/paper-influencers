"""
This module outputs a csv containing the username and descriptions for M3.
"""
import os
import pandas as pd
import requests

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


df = pd.read_csv("data/tmp/q95_daily_conversions_48.csv")

timeframe = pd.to_datetime("2022-04-24") - pd.Timedelta('4w')
mask = pd.to_datetime(df['date']) > timeframe
df = df[mask]

mask = df.groupby('author_id')['k_factor'].mean() > 1
ids = mask[mask].reset_index()['author_id'].values

users = pd.read_csv("data/tmp/twitter-users.csv")
users = users[~users['id'].duplicated()].set_index('id').loc[ids]


bearer_token = os.environ.get("BEARER_TOKEN")
data_path = os.environ.get("DATA_PATH")
search_url = "https://api.twitter.com/2/users/"

query_params = {
    'ids': ','.join(map(str, ids)),
    'user.fields': 'username,description',
}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request(
        "GET",
        search_url,
        auth=bearer_oauth,
        params=params
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    df = pd.json_normalize(json_response['data'])
    df['author_id'] = ids
    df.to_csv('data/tmp/q95-inf-algo-ids.csv', index=False)


if __name__ == "__main__":
    main()
