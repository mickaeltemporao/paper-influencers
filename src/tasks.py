task_1 = """
You will be provided with a Twitter account name and its description written in French.
Your task is to classify the description into one of the following political ideologies within the context of French politics: left, center, right, or not applicable.

Your output should consist of the category followed by a semicolon and a brief, one-sentence justification in English.
"""

task_2 = """
You will be provided with a Twitter account name and its description written in French.
Your task is to classify the description into one of the following categories:

- media
- political
- influencer

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


"""
News media are providers of informational content and analysis on politics, current affairs in France and internationally

Subcategory i. Mainstream news media are established news providers on the TV, newspapers, radio or current affairs magazines, and individual accounts of prominent current and former journalists that have worked for these outlets

Subcategory ii. Alternative news media are online news sites that present viewpoints independent and also critical of the mainstream media and that have an online presence only.

 

Political Actors are formal or officially registered candidates, elected politicians and organizations that compete in elections, or are an official government agency or official spokespersons and members of French government

Subcategory i. Elected politicians and representatives holding office in France during 2022 at the national, regional or department and local level or a person that ran as an official candidate in the 2022 French parliamentary and Presidential election.

Subcategory ii. Legally recognized and registered political parties in France, leaders of parties, official spokespersons of parties and political campaigns

 

Influencer All other accounts that are for individuals or personal that are not classified in tasks XX  This excludes business organizations, companies and commercial vendors

Subcategory i. political influencer includes former elected politicians, people that have previously held some kind of a governmental office or role, and all other people clearly seeking to influence political views and who regularly comment on the news and political matters

Subcategory ii. non political influencers are individuals that are not directly linked with politics or do not have a former political career, they never or very rarely talk about politics and don’t have an obvious ideological or political views.

 

Left wing accounts are those that express political views and opinions or include content that focuses on issues of income equality, environmental protections, social justice, open borders, progressive policies to promote minority representation

Right wing accounts are those that express political views and opinions or include content that focuses on issues of economic liberalism, less state intervention in citizens lives, lower taxes, controlling borders and immigration

Centre accounts are those that express political views that mix or combine left and right opinion and content such that one opinion or type of content does not dominate.

Non-partisan accounts  are those that typically do not express political views or contain any political content.
"""


task_main = """
You will be provided with a Twitter account name and description written in French.
Your task is to classify the account into one of the following four categories:
- News media
- Political Actors
- Influencer
- Other 

Your output consists of only one of the four categories followed by a semicolon and a brief, one-sentence justification in English.

News media are providers of informational content and analysis on politics, current affairs in France and internationally.

Political Actors are formal or officially registered candidates, elected politicians and organizations that compete in elections, or are an official government agency or official spokespersons and members of French government.

Influencer are all other accounts that are for individuals or personal use that are not classified as news media or political actors. This excludes business organizations, companies and commercial vendors.

Other are business organizations, companies and commercial vendors.
"""

task_sub_media = """
Mainstream: Are Mainstream news media, established news providers on the TV, newspapers, radio or current affairs magazines, and individual accounts of prominent current and former journalists that have worked for these outlets.

Alternative: Are Alternative news media are online news sites that present viewpoints independent and also critical of the mainstream media and that have an online presence only.
"""

task_sub_pol = """
I. Elected politicians and representatives holding office in France during 2022 at the national, regional or department and local level or a person that ran as an official candidate in the 2022 French parliamentary and Presidential election.

II. Legally recognized and registered political parties in France, leaders of parties, official spokespersons of parties and political campaigns.
"""

task_sub_inf = """
Subcategory i. political influencer includes former elected politicians, people that have previously held some kind of a governmental office or role, and all other people clearly seeking to influence political views and who regularly comment on the news and political matters.

Subcategory ii. non political influencers are individuals that are not directly linked with politics or do not have a former political career, they never or very rarely talk about politics and don’t have an obvious ideological or political views.
"""

task_idl = """
Left wing accounts are those that express political views and opinions or include content that focuses on issues of income equality, environmental protections, social justice, open borders, progressive policies to promote minority representation.

Right wing accounts are those that express political views and opinions or include content that focuses on issues of economic liberalism, less state intervention in citizens lives, freedom of speech, lower taxes, controlling borders and immigration.

Centre accounts are those that express political views that mix or combine left and right opinion and content such that one opinion or type of content does not dominate.

Non-partisan accounts  are those that typically do not express political views or contain any political content.
"""
