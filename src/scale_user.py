import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


load_dotenv(find_dotenv())


data_path = 'data/frml_user_details.csv'
df = pd.read_csv(data_path)
df.head()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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

content = df['description'][25]
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": task_2
    },
    {
      "role": "user",
      "content": content
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)
print(content)
print(response.choices[0].message.content)



task = """
You will be provided with a Twitter account description.
Solely based on the description, your task is to return two python lists of propabilities, ranging from 0 to 100 of the account belonging each of the follwoing political ideologies and types of political actors.

Political Ideologies 
[Extreme left,Left,Center left ,Center,Center right ,Right,Extreme right]

Type of actor
[mainstream media, alternative media, political party, politician, political influencer, non political influencer]

Your output is two python list containing 7 and 6 elements that reflect the propabilities of the account description belonging to each of these.
"""


