# Twitter API

# Get Existing Rules
curl -v https://api.twitter.com/2/tweets/search/stream/rules -H "Authorization: Bearer $BEARER_TOKEN" | python -m json.tool

# Update Rules
curl -X POST 'https://api.twitter.com/2/tweets/search/stream/rules' -H "Content-type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -d '{ "add": [ {"value": "zemmour OR macron OR pecresse", "tag": "Mention Candidat"} ] }' | python -m json.tool

# Delete Rules
curl -X POST 'https://api.twitter.com/2/tweets/search/stream/rules'
  -H "Content-type: application/json"
  -H "Authorization: Bearer $BEARER_TOKEN" -d
  '{
    "delete": {
      "ids": [
        "1491049415108349952"
      ]
    }
  }'

# Get Tweets
curl https://api.twitter.com/2/tweets/search/stream -H "Authorization: Bearer $BEARER_TOKEN"

curl "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at" -H "Authorization: Bearer $BEARER_TOKEN"

# Capture stderr and output displayed on the console and in a file
command |& tee -a output.txt

curl "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at" -H "Authorization: Bearer $BEARER_TOKEN" 2>&1 |& tee -a output.txt

