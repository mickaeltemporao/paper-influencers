import pandas as pd

from tqdm import tqdm


dtypes = {
    'id': 'int',
    'created_at': 'str',
    'author_id': 'int',
    'type': 'str',
    'ref_id': 'int',
}

# df = pd.read_csv("data/tmp/tweets-small-kfactor.csv", dtype=dtypes)
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
    return i * c


list_of_dates = df['date'].unique()
k_factors_list = []

for day in tqdm(list_of_dates[0:5]):
    mask = df['date'] <= day
    list_of_users = df.loc[mask, 'author_id'].unique()
    for user in list_of_users:
        k_factors_list.append({'author_id': user, 'date': day, 'k_factor': get_k_factor(df, user, day)})

k_factors_df = pd.DataFrame(k_factors_list)
# Print the k-factors DataFrame
k_factors_df
# Save the k-factors DataFrame to a CSV file
k_factors_df.to_csv('daily_k_factors.csv', index=False)

