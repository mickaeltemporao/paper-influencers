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

task = "You will be provided with a tweet, and your task is to classify its sentiment as positive, neutral, or negative."


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": task
    },
    {
      "role": "user",
      "content": "I loved the new Batman movie!"
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)

type(response)

response
response.choices[0].message.content

