import pandas as pd
import multiprocessing
from time import process_time


dtypes = {
    'id': 'int',
    'created_at': 'str',
    'author_id': 'int',
    'type': 'str',
    'ref_id': 'int',
}

HOURS = 48
QUANTILE = 95

# df = pd.read_csv("data/tmp/tweets-small-kfactor.csv", dtype=dtypes)
users = pd.read_csv("data/tmp/twitter-users.csv")
df = pd.read_csv("data/tmp/tweets.csv", dtype=dtypes)
df['created_at'] = pd.to_datetime(df['created_at'])

election_date = pd.to_datetime("2022-04-25").tz_localize('UTC')
df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
df = df[df['created_at'] <= election_date]
df['date'] = df['created_at'].dt.date

# Find Top 1% active accounts in the last 4 weeks 
group = ['date', 'author_id']
two_weeks = pd.to_datetime("2022-04-24") - pd.Timedelta('4w')
top_df = df.groupby(group).size().reset_index(name='msg_count')
mask = pd.to_datetime(top_df['date']) > two_weeks
top_df = top_df[mask]
top_df = top_df.set_index(group)
tmp_df = top_df.reset_index().groupby('author_id').size()
mask = tmp_df > tmp_df.quantile(QUANTILE/100)
top_authors = tmp_df[mask].index.values
print(len(top_authors))
del tmp_df

# TODO:
# Add momentum parameter: Sample top m days % change kfacotrs
# Add popularity parameter: threshold top p % accounts
# TESTS
# Sample top n% daily highest kfactors
# VS
# optimize N vs inductive

# Switch to CONVERSION RATE
def get_conversion_rate(df, author, date, hours=HOURS):
    # Find tweets from author
    mask1 = df['author_id'] == author
    # Get tweets from author up to date
    mask2 = df['date'] <= date
    # Get the list of ids for user on date
    user_tw_list = df.loc[(mask1 & mask2), 'id'].unique()
    # Conversion Date Range
    mask3 = df['date'] <= date + pd.Timedelta(f'{HOURS}h')
    # i = number of tweets sent by user
    i = len(user_tw_list)
    if i <= 0:
        return 0
    # n_int = number of interactions from other users
    n_interactions = df[(~mask1 & mask3)]['ref_id'].isin(user_tw_list).sum()
    # c = percent conversion of each tweet
    if n_interactions > 0:
        return n_interactions/i
    else:
        return 0


list_of_dates = df['date'].unique()
list_of_dates.sort()
k_factors_list = []
day = pd.to_datetime('2022-02-01').date()
user = 772215918868979712
get_conversion_rate(df, user, day)


def task(day):
    print(f"Starting task {day}.")
    tic = process_time()
    mask1 = df['date'] <= day
    mask2 = df['author_id'].isin(top_authors)
    list_of_users = df.loc[(mask1 & mask2), 'author_id'].unique()
    tmp_output = []
    for user in list_of_users:
        tmp_output.append({'author_id': user, 'date': day, 'k_factor': get_conversion_rate(df, user, day)})
    print(f"Day {day} completed in {process_time() - tic}!")
    return tmp_output


# create a process pool that uses all cpus -1
cpus = multiprocessing.cpu_count()-1
with multiprocessing.Pool(cpus) as pool:
    for result in pool.map(task, list_of_dates):
        k_factors_list.append(pd.DataFrame(result))

# Save the k-factors DataFrame to a CSV file
pd.concat(k_factors_list).to_csv(f'data/tmp/q{QUANTILE}_daily_conversions_{HOURS}.csv', index=False)
