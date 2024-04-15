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
DATA_FILE = DATA_PATH + "tmp/gpt_classifier_output.csv"
OUTPUT_FILE_PATH = DATA_PATH + "tmp/twitter_account_sample_10pct.csv"

cols = ['username', 'description']
df = pd.read_csv(DATA_FILE).sample(frac=.10)[cols]
df.to_csv(OUTPUT_FILE_PATH, index=False)

