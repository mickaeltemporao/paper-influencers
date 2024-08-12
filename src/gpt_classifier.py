"""
This module interacts with chatGPT API to create labels based on a given task.
"""

import src.tasks

import os
import time
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv(find_dotenv())

# TODO: uniform file names, output-m[1-4]..., ids-m[1-4].csv etc
DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
# USER_FILE = 'tmp/inf-algo-ids.csv'
USER_FILE = 'tmp/m4-ids.csv'
# MODEL = "gpt-4o"
MODEL = "gpt-4o-mini-2024-07-18"
# OUTPUT_FILE_PATH = DATA_PATH + f"tmp/output_{MODEL}.csv"
# OUTPUT_FILE_PATH = DATA_PATH + f"tmp/output_{MODEL}_infalgo.csv"
OUTPUT_FILE_PATH = DATA_PATH + f"tmp/output_{MODEL}_networkalgo_m4.csv"
SUBTASK_LIST = list(src.tasks.task_sub.keys())


def run_task(task, content):
    try:
        response = client.chat.completions.create(
          model=MODEL,
          messages=[
            {
              "role": "system",
              "content": task
            },
            {
              "role": "user",
              "content": content
            }
          ],
          temperature=0.7,
          max_tokens=5,
          top_p=1
        )
        output = response.choices[0].message.content
        print(output)
        return output
    except RateLimitError:
        print("Reached RateLimit.")
        print(f"Sleeping for {60*5} seconds.")
        time.sleep(60*5)
        pass


def make_content(obs):
    return f"""Account name: {obs.name}
Account description: {obs['description']}
"""


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def find_file():
    try:
        tmp_df = pd.read_csv(OUTPUT_FILE_PATH, index_col='username')
        print("Resuming from previous file.")
    except FileNotFoundError:
        df = pd.read_csv(DATA_PATH+USER_FILE)
        df = df.dropna(subset=['username', 'description']).set_index('username')
        df['description'].to_csv(OUTPUT_FILE_PATH)
        tmp_df = df[['description']].copy()
        print("New output filed created!")
    return tmp_df


def main():
    tmp_df = find_file()

    for task in src.tasks.task_main:
        newcol = f'task_{task}'

        if newcol not in tmp_df.columns:
            tmp_df[newcol] = "NONE"

        for i, j in tmp_df.iterrows():
            if tmp_df.loc[j.name, newcol] != "NONE":
                continue
            print(f"Running task for {j.name}")
            task_output = run_task(
                src.tasks.task_main[task],
                make_content(j)
            )

            tmp_df.loc[j.name, newcol] = task_output

            tmp_df.to_csv(OUTPUT_FILE_PATH)
            print("Filed Saved")

def sub():
    tmp_df = find_file()
    newcol = 'task_sub'
    if newcol not in tmp_df.columns:
        tmp_df[newcol] = "NONE"

    for i, j in tmp_df.iterrows():
        if tmp_df.loc[j.name, newcol] != "NONE":
            continue
        print(f"Running task for {j.name}")
        current_type = int(j['task_type'] - 1)
        task_output = run_task(
            src.tasks.task_sub[SUBTASK_LIST[current_type]],
            make_content(j)
        )
        tmp_df.loc[j.name, newcol] = task_output
        tmp_df.to_csv(OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()
    sub()
