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
OUTPUT_FILE_PATH = DATA_PATH + "scaled_output.csv"
df = pd.read_csv(DATA_PATH+USER_FILE).dropna(subset=['description'])
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


OLD_TASK_IDEOLOGY = """
You will receive a Twitter account description written in French. Your objective is to analyze the description and generate a Python list comprising 7 elements, with values between 0 to 1, which indicate the likelyhood of the description aligning with each of the specified political ideologies within the context of the French politics.

[Extreme left,Left,Center left ,Center,Center right ,Right,Extreme right]

Your output is a python list containing 7 elements that reflect the propabilities of the account description belonging to each of these.
"""

OLD_TASK_MEDIA = """
You will receive a Twitter account description written in French. Your objective is to analyze the description and generate 3 Python lists comprising 3 elements each, with values between 0 to 1, which indicate the likelyhood of the description aligning with each of the specified types of political actors within the context of the French politics.

[mainstream media, alternative media, not applicable]
[political party, politician, not applicable]
[political influencer, non political influencer, not applicable]

Your output the python list containing 3 sublists that reflect the propabilities of the account description belonging to each of these categories. No other text, or description should be in the output.
"""


task_1 = """
You will be provided with a Twitter account description written in French.
Your task is to classify the description into one of the following political ideologies within the context of French politics: left, center, right, or not applicable.

Your output should consist of the category followed by a semicolon and a brief, one-sentence justification.
"""


task_2 = """
You will be provided with a Twitter account description written in French.
Your task is to classify the description into one of the following categories: 

- media (mainstream media or alternative media)
- party/politician
- Influencer (political influencer, non political influencer)

Your output should consist of the category followed by a semicolon and a brief, one-sentence justification.
"""


task_3 = """

- Media, mainstream or alternative
- party/politician
- Influencer, political influence, non political influencer

"""

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


def main():

    cols = ['username', 'output']
    tmp_df = pd.DataFrame(columns=cols)

    for i, j in df.iterrows():
        try:
            old_csv = pd.read_csv(OUTPUT_FILE_PATH)
        except FileNotFoundError:
            tmp_df.to_csv(OUTPUT_FILE_PATH, index=False)
            old_csv = tmp_df
            print("Starting Filed Saved!")

        if j['username'] in old_csv['username'].to_list():
            continue

        print(f"{j['username']} - {i} out of {len(df)}")

        task_output = run_task(task_2, j['description'])

        tmp_out = {
            'username': j['username'],
            'task_1': task_output,
        }
        tmp_out_df = pd.DataFrame().from_dict(
            tmp_out, orient='index'
        ).transpose()

        tmp_df = pd.concat([old_csv, tmp_out_df])
        tmp_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print("Filed Saved")


if __name__ == "__main__":
    main()
