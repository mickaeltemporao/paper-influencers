# Twitter API
source .env

# Get Existing Rules
existing='https://api.twitter.com/2/tweets/search/stream/rules'
curl -v $existing -H "Authorization: Bearer $BEARER_TOKEN" | python -m json.tool

# Update Rules
update='https://api.twitter.com/2/tweets/search/stream/rules'
rules='{ "add": [ {"value": "arthaud OR poutou OR melenchon OR melanchon OR hidalgo OR toubira OR jadot OR macron OR pecresse OR pécresse OR #avecvalérie OR #avecvalerie OR asselineau OR zemmour OR zemour OR philippot OR le pen OR #mlafrance OR lassale OR dupont aigan", "tag": "dict 2022-02-10" } ] }'
curl -X POST $update -H "Content-type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -d "$rules"| python -m json.tool

# Setup Query
query="https://api.twitter.com/2/tweets/search/stream?
tweet.fields=created_at,lang&
expansions=author_id&
user.fields=username
"

# Get Tweets
curl $query -H "Authorization: Bearer $BEARER_TOKEN" >> output.txt

# Delete Rules
delete='https://api.twitter.com/2/tweets/search/stream/rules'
to_delete='{ "delete": { "ids": [ "1491712714120564736" ] } }'
curl -X POST $delete -H "Content-type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -d $to_delete
