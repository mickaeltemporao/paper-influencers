import random
import pandas as pd


def generate_text(k=3):
    return ''.join(random.choices('abcdefgh', k=k))


def generate_date(date=None):
    # Generate a random date within the last year
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.Timedelta(days=30)
    new_date = start_date + pd.Timedelta(
        seconds=random.randint(
            0, int((end_date - start_date).total_seconds())
        )
    )
    if date is not None:
        random_days = random.randint(1, 30)  
        new_date = pd.to_datetime(date) + pd.Timedelta(random_days)
    return new_date.strftime("%Y-%m-%d")

def make_data(n=100):
    # Generate a sample dataframe
    df = pd.DataFrame(
        {'user-uid': [f'u{random.randint(0, 9)}' for i in range(n)],
         'tweet': [generate_text() for i in range(n)],
         'tweet-uid': [f't{random.randint(0,100**5)}' for i in range(n)],
         'retweet': [0 for i in range(n)],
         'timestamp': [generate_date() for i in range(n)],
         },
    )
    retweets = df.sample(n**2, replace=True)
    retweets['retweet'] = 1
    retweets['timestamp'] = retweets['timestamp'].apply(
        lambda x: generate_date(x)
    )
    retweets['user-uid'] = retweets['user-uid'].apply(
        lambda x: f'u{random.randint(10, 100)}'
    )
    output = pd.concat([df, retweets])
    output['timestamp'] = pd.to_datetime(output['timestamp'])
    return output


def get_k_factor(user_name, date):
    mask = df['user-uid'] == user_name
    mask2 = df['timestamp'] < date
    tweets = df[mask]
    user_tw_list = tweets['tweet-uid'].unique()
    # i = number of tweets sent by user
    i = len(user_tw_list)
    # c = percent conversion of each tweet
    if df[~mask]['tweet-uid'].isin(user_tw_list).sum() > 0:
        c = df[~mask]['tweet-uid'].isin(user_tw_list).sum()
    else:
        c = 1
    # k-factor
    k = i * c
    return k


# TODO:
# Add momentum parameter: Sample top m days % change kfacotrs
# Add popularity parameter: threshold top p % accounts
# daily k-factor
# TESTS
# Sample top n% daily highest kfactors
# VS
# optimize N vs inductive

df = make_data(10)
df
df['retweet'].value_counts()
df['tweet-uid'].value_counts()
df['user-uid'].value_counts()

# STREAMING ALTERNATIVE with SIMULATED DATA

user_name = 'u18'
date = pd.to_datetime('today')

get_k_factor('u82', 'random')

def main():
    pass


def calculate_k_factor(initial_tweets, new_tweets, time_period):
    k_factor = (new_tweets / initial_tweets) ** (1 / time_period) - 1
    return k_factor

initial_tweets = int(input("Enter the initial number of customers: "))
new_tweets = int(input("Enter the number of new customers acquired: "))
time_period = int(input("Enter the time period (in days): "))

k_factor = calculate_k_factor(initial_tweets, new_tweets, time_period)
print("The K-factor is: ", k_factor)


if __name__ == "__main__":
    main()
