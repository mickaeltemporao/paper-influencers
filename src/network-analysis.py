import pandas as pd
import igraph as ig
from matplotlib import pyplot as plt


df = pd.read_csv("data/tmp/network.csv")
g = ig.Graph.TupleList(df[['author_id', 'mentions']].itertuples(index=False), directed=True)

# We look at in degree centrality as we want to get the most retweeted users
estimate = g.degree(mode="in")

output = pd.DataFrame(
    {
        "author_id": g.vs["name"],
        "centrality": estimate,
     }
)

output['centrality'] = output['centrality']/(output.shape[0]-1)
mask = output['centrality'] > output['centrality'].quantile(0.99)
output[mask].sort_values(by='centrality', ascending=False).to_csv("data/tmp/indegree99.csv", index=False)

