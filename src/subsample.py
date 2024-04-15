"""
This module generate the 10% sample to be coded by humans.
"""

import os
import random
import pandas as pd
from dotenv import find_dotenv, load_dotenv


random.seed(199)
load_dotenv(find_dotenv())


DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
OUTPUT_FILE_PATH = DATA_PATH + "tmp/twitter_account_sample_10pct.csv"

df = pd.read_csv(DATA_PATH+USER_FILE)
df

