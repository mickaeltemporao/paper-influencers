def make_task(task_text):
    return f"""
        You are an unbiased French politics expert.
        You will be provided with a Twitter account name and description written in French.
        Your task is to classify the account into one of the following numbered categories:
        {task_text}
        For each of these categories, I have provided a short description to help you with your choice. 
        Your output consists only of the number of the selected category, that is the number before the description provided.
    """


task_dict = {
    "type": make_task(
        """
        1. News media are providers of informational content and analysis on politics, current affairs in France and internationally;
        2. Political Actors are formal or officially registered candidates, elected politicians and organizations that compete in elections, official spokespersons and members of French government;
        3. Other persons and organizations of interest are all other accounts that are for individuals or personal use;
        """
    ),
    "ideology": make_task(
        """
        1. Left wing accounts are those that express political views and opinions or include content that focuses on issues of income equality, environmental protection, social justice, open borders, progressive policies to promote minority representation;
        2. Centre accounts are those that express political views that mix or combine left and right opinion and content such that one opinion or type of content does not dominate;
        3. Right wing accounts are those that express political views and opinions or include content that focuses on issues of economic liberalism, less state intervention in citizens lives, lower taxes, controlling borders and immigration);
        4. Non-partisan accounts are those that typically do not express political views or contain any political content;
        """
    ),
    "media": make_task(
        """
        1. Mainstream news media are accounts that are established news providers on the TV, newspapers, radio or current affairs magazines, and individual accounts of prominent current and former journalists that have worked for these outlets;
        2. Alternative news media are accounts that are online news sites that present viewpoints independent and also critical of the mainstream media and that have an online presence only;
        """
    ),
    "political": make_task(
        """
        1. Elected politicians and representatives holding office in France during 2022 at the national, regional or department and local level or a person that ran as an official candidate in the 2022 French parliamentary and Presidential election;
        2. Legally recognized and registered political parties in France, leaders of parties, official spokespersons of parties and political campaigns;
        3. Political influencer includes former NATIONAL elected politicians, people that have previously held some kind of a governmental office or role;
        4. Political influencer includes former INTERNATIONAL elected politicians, people that have previously held some kind of a governmental office or role;
        5. Government agencies, departments, civil servants i.e. non elected/non partisan official state actors;
        """
    ),
    "other": make_task(
        """
        1. Individuals and organizations that are not directly linked with politics or do not have a former political career, journalistic or media outlets but who are mainly focused on talking about politics, and all other people clearly seeking to influence political views and who regularly comment on the news and political matters;
        2. Celebrities sports people, groups and organizations that are not primarily concerned with politics but occasionally or frequently express political views, or have an obvious ideological standpoint and seek to influence opinions and votes;
        3. Individuals that are not directly linked with politics currently, do not have a former political career, they never or very rarely talk about politics and don’t have an obvious ideological or political views;
        4. Business organizations, companies and commercial vendors;
        """
    ),
}
