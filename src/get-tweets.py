import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from tqdm import tqdm


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

load_dotenv(find_dotenv())

bearer_token = os.environ.get("BEARER_TOKEN")
data_path = os.environ.get("DATA_PATH")
search_url = "https://api.twitter.com/2/tweets/search/all"

query_params = {
    'query': '#Presidentielle2022',
    'tweet.fields': 'created_at,author_id,entities,conversation_id',
    'start_time': '2022-02-01T00:00:00+01:00',
    'end_time': '2022-04-30T00:00:00+02:00',
    'max_results': 500,
    'expansions': 'author_id,referenced_tweets.id',
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


def update_query(next_id=None):
    query_params.update(
        {
            'next_token': next_id,
        }
    )


# TODO: Add data folder check and start from last entry
def main():
    json_response = connect_to_endpoint(search_url, query_params)
    update_query(json_response['meta']['next_token'])
    new_id = json_response['meta']['newest_id']
    old_id = json_response['meta']['oldest_id']
    f'{data_path}raw/new-{new_id}_old-{old_id}.json'
    with open(f'{data_path}raw/new-{new_id}_old-{old_id}.json', 'w') as f:
        json.dump(json_response, f)
    # print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    ntweets = 950000
    for i in tqdm(range(int(ntweets/500))):
        main()
