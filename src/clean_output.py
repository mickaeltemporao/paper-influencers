import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


DATA_PATH = os.environ.get("DATA_PATH")
OUTPUT_FILE_PATH = DATA_PATH + "tmp/gpt_classifier_output.csv"


df = pd.read_csv(OUTPUT_FILE_PATH)


def task_recode(var_name, data):
    data[var_name] = data[var_name].sort_values().str.replace("Category: ", "")
    data[var_name] = data[var_name].str.replace(":", ";")
    data[var_name+'_desc'] = data[var_name].apply(lambda x: x.split(";")[1])
    data[var_name] = data[var_name].apply(lambda x: x.split(";")[0])
    data[var_name] = data[var_name].str.lower()
    return data.copy()


df = task_recode('task_media', df)
df = task_recode('task_ideology', df)


# Specific Media Task Clanup | CAREFUL OUTPUTS WILL VARY BETWEEN RUNS
df.loc[df['task_media'].str.contains("influencer"), 'task_media'] = 'influencer'
df.loc[df['task_media'].str.contains("party|politi"), 'task_media'] = 'political'
df.loc[df['task_media'].str.contains("media"), 'task_media'] = 'media'
df['task_media_type'] = df['task_media_type'].str.lower()
df.loc[df['task_media_type'].str.contains("non-pol"), 'task_media_type'] = 'non-political influencer'
df.loc[df['task_media_type'].str.contains("mainstream"), 'task_media_type'] = 'mainstream media'
df.loc[df['task_media_type'].str.contains("alternative"), 'task_media_type'] = 'alternative media'
df.loc[df['task_media_type'].str.contains("party"), 'task_media_type'] = 'party'
df.loc[df['task_media_type'].str.contains("non-political"), 'task_media_type'] = 'non-political'
df.loc[df['task_media_type'].str.contains("politician"), 'task_media_type'] = 'politician'
df.loc[df['task_media_type'].str.contains("political inf"), 'task_media_type'] = 'political'


# Specific Ideology Task Clanup
df.loc[df['task_ideology'].str.contains("not app"), 'task_ideology'] = 'not applicable'
df.loc[df['task_ideology'].str.contains("left"), 'task_ideology'] = 'left'
df.loc[df['task_ideology'].str.contains("center"), 'task_ideology'] = 'center'
df.loc[df['task_ideology'].str.contains("right"), 'task_ideology'] = 'right'

# Reorder columns
newcols = [
    'username',
    'description',
    'task_media',
    'task_media_type',
    'task_media_desc',
    'task_ideology',
    'task_ideology_desc'
]

df[newcols].to_csv(OUTPUT_FILE_PATH, index=False)
