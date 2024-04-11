"""
This module interacts with chatGPT api to label descriptions based on the
task describted.
"""
import os
import time
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv(find_dotenv())


DATA_PATH = os.environ.get("DATA_PATH")
USER_FILE = os.environ.get("USER_FILE")
OUTPUT_FILE_PATH = DATA_PATH + "tmp/gpt_classifier_output.csv"


task_1 = """
You will be provided with a Twitter account name and its description written in French.
Your task is to classify the description into one of the following political ideologies within the context of French politics: left, center, right, or not applicable.

Your output should consist of the category followed by a semicolon and a brief, one-sentence justification in English.
"""


task_2 = """
You will be provided with a Twitter account name and its description written in French.
Your task is to classify the description into one of the following categories: 

- media (mainstream media or alternative media)
- party/politician
- Influencer (political influencer, non political influencer)

Your output should consist of the category followed by a semicolon and a brief, one-sentence justification.
"""


def make_task_3(media_type):
    media_dict = {
        'influencer': '1. political influencer OR 2. non-political influencer',
        'media': '1. mainstream media OR 2. alternative media',
        'political': '1. political party OR 2. politician',
    }
    return f"""You will be provided with a Twitter account name and its description written in French.
Your task is to choose a category best suited for the description based on the following two choices: 
- {media_dict[media_type]}
Your output consists only of the choosen category."""


def run_task(task, content):
    try:
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
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
          max_tokens=128,
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


task_dict = {
    # "ideology": task_1,
    # "media": task_2,
    "media_type": make_task_3,
}


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def main():
    try:
        tmp_df = pd.read_csv(OUTPUT_FILE_PATH, index_col='username')
        print("Resuming from previous file.")
    except FileNotFoundError:
        df = pd.read_csv(DATA_PATH+USER_FILE)
        df = df.dropna(subset=['username', 'description']).set_index('username')
        df['description'].to_csv(OUTPUT_FILE_PATH)
        tmp_df = df[['description']].copy()
        print("New output filed created!")

    for task in task_dict:
        newcol = f'task_{task}'

        if newcol not in tmp_df.columns:
            tmp_df[newcol] = "NONE"

        for i, j in tmp_df.iterrows():
            if tmp_df.loc[j.name, newcol] != "NONE":
                continue
            print(f"Running task for {j.name}")
            task_output = run_task(
                task_dict[task],  # Comment for task 3
                # task_dict[task](j['task_media']),  # Uncomment for Task 3
                make_content(j)
            )

            tmp_df.loc[j.name, newcol] = task_output

            tmp_df.to_csv(OUTPUT_FILE_PATH)
            print("Filed Saved")


if __name__ == "__main__":
    main()
