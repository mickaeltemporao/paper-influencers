import requests
import os
import json
import time
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from tqdm import tqdm


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# Note : The use of next_token or pagination_token in the query depends on which API you are using. Eg "users" uses pagination_token where "tweets" uses "next_token".

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


def get_last_token():
    files = os.listdir(f'{data_path}raw/')
    files.sort()
    file = f"{data_path}raw/{files[0]}"
    with open(file) as f:
        d = json.load(f)
    return d['meta']['next_token']


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    new_id = json_response['meta']['newest_id']
    old_id = json_response['meta']['oldest_id']
    f'{data_path}raw/new-{new_id}_old-{old_id}.json'
    with open(f'{data_path}raw/new-{new_id}_old-{old_id}.json', 'w') as f:
        json.dump(json_response, f)
    if 'next_token' not in json_response['meta'].keys():
        return print("Tweet collection completed successfully! 🎉")
    update_query(json_response['meta']['next_token'])
    # print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    ntweets = 950000
    sleep_time = 15*60
    start_time = time.time()
    count = 1

    if len(os.listdir(f'{data_path}raw/')) > 0:
        try:
            update_query(get_last_token())
            for i in tqdm(range(int(ntweets/500))):
                main()
                count += 1
                end_time = time.time()
                execution_time = end_time - start_time
                if count > 295 and execution_time < sleep_time:  # 900 seconds = 15 minutes
                    time.sleep(sleep_time - execution_time + 120)
                    count = 1
                    start_time = time.time()
        except KeyError as e:
            print("Tweet collection completed successfully! 🎉")
            pass
            
