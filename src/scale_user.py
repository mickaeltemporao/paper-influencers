import ast
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


load_dotenv(find_dotenv())


DATA_FILE_PATH = os.environ.get("USER_DATA_FILE_PATH")
OUTPUT_FILE_PATH=os.environ.get("OUTPUT_FILE_PATH")
df = pd.read_csv(DATA_FILE_PATH)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# df['description'] = df['description'].fillna("NOT AVAILABLE")
df = df.dropna(subset=['description'])

task_1 = """
You will receive a Twitter account description written in French. Your objective is to analyze the description and generate a Python list comprising 7 elements, with values between 0 to 1, which indicate the likelyhood of the description aligning with each of the specified political ideologies within the context of the French politics.

[Extreme left,Left,Center left ,Center,Center right ,Right,Extreme right]

Your output is a python list containing 7 elements that reflect the propabilities of the account description belonging to each of these.
"""

task_2 = """
You will receive a Twitter account description written in French. Your objective is to analyze the description and generate 3 Python lists comprising 3 elements each, with values between 0 to 1, which indicate the likelyhood of the description aligning with each of the specified types of political actors within the context of the French politics.

[mainstream media, alternative media, not applicable]
[political party, politician, not applicable]
[political influencer, non political influencer, not applicable]

"""

"""
If the account description is "NOT AVAILABLE", provide list with prediected probabilities of 0.
"""


def clean_output(text):
    text = text.replace(',,',',')
    return text


def scale_description(task, content):
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
    output = clean_output(output)
    return output


def main():

    cols = ['username', 'description', 'ideology', 'actor']
    tmp_df = pd.DataFrame(columns=cols)

    for i, j in df.iterrows():
        try:
            old_csv = pd.read_csv(OUTPUT_FILE_PATH)
        except FileNotFoundError:
            tmp_df.to_csv(OUTPUT_FILE_PATH, index=False)
            old_csv = pd.read_csv(OUTPUT_FILE_PATH)
            print("Starting Filed Saved!")

        if j['username'] in old_csv['username'].to_list():
            continue

        print(f"{j['username']} - {i} out of {len(df)}")

        task_1_output = scale_description(task_1, j['description'])
        task_2_output = scale_description(task_2, j['description'])

        tmp_out = {
            'username': j['username'],
            'description': j['description'],
            'ideology': [ast.literal_eval(task_1_output)],
            'actor': list(ast.literal_eval(task_2_output.replace("\n", ",")))
        }
        tmp_out_df = pd.DataFrame().from_dict(
            tmp_out, orient='index'
        ).transpose()

        tmp_df = pd.concat([old_csv, tmp_out_df])
        tmp_df.to_csv(OUTPUT_FILE_PATH, index=False)
        print("Filed Saved")


if __name__ == "__main__":
    main()
