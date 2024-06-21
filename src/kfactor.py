import pandas as pd
import multiprocessing
from time import process_time

from tqdm import tqdm


dtypes = {
    'id': 'int',
    'created_at': 'str',
    'author_id': 'int',
    'type': 'str',
    'ref_id': 'int',
}

# df = pd.read_csv("data/tmp/tweets-small-kfactor.csv", dtype=dtypes)
users = pd.read_csv("data/tmp/twitter-users.csv")
df = pd.read_csv("data/tmp/tweets.csv", dtype=dtypes)
df['created_at'] = pd.to_datetime(df['created_at'])
df['date'] = df['created_at'].dt.date
df

# TODO:
# Add momentum parameter: Sample top m days % change kfacotrs
# Add popularity parameter: threshold top p % accounts
# TESTS
# Sample top n% daily highest kfactors
# VS
# optimize N vs inductive

# Switch to CONVERSION RATE
def get_k_factor(df, author, date):
    # Find tweets from author
    mask1 = df['author_id'] == author
    # Filter before date
    mask2 = df['date'] <= date
    # Get the list of ids for user until date
    user_tw_list = df.loc[(mask1 & mask2), 'id'].unique()
    # i = number of tweets sent by user
    i = len(user_tw_list)
    # n_int = number of interactions from other users
    n_interactions = df[(~mask1 & mask2)]['ref_id'].isin(user_tw_list).sum()
    # c = percent conversion of each tweet
    if n_interactions > 0:
        c = n_interactions/i
    else:
        c = 0
    # k-factor
    return c


list_of_dates = df['date'].unique().sort()
k_factors_list = []
day = pd.to_datetime('2022-03-10').date()
user = 772215918868979712
get_k_factor(df, user, day)


def task(day):
    print(f"Starting task {day}.")
    tic = process_time()
    mask = df['date'] <= day
    list_of_users = df.loc[df['date'] == day, 'author_id'].unique()
    tmp_output = []
    for user in list_of_users:
        tmp_output.append({'author_id': user, 'date': day, 'k_factor': get_k_factor(df, user, day)})
    print(f"Day {day} completed in {process_time() - tic}!")
    return tmp_output


# create a process pool that uses all cpus -1
cpus = multiprocessing.cpu_count()-1
with multiprocessing.Pool(cpus) as pool:
    for result in pool.map(task, list_of_dates[0:2]):
        k_factors_list.append(result)

# Save the k-factors DataFrame to a CSV file
k_factors_df = pd.DataFrame(k_factors_list)
k_factors_df.to_csv('daily_k_factors.csv', index=False)

