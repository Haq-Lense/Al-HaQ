#!/bin/bash

# Define queries
queries=("residential proxies")

# Define maximum number of tweets
max_tweets=1000

# Function to scrape tweet IDs
function scrap_id() {
    local query="$1"
    scrap=$(snscrape --jsonl --max-results $max_tweets twitter-search "$query")
    echo "$scrap"
}

# Loop over queries
for query in "${queries[@]}"; do
    output_filename="${query// /_}.txt"
    touch "$output_filename"
    scrap=$(scrap_id "$query")
    i=0
    while IFS= read -r tweet; do
        i=$((i+1))
        tweet_content=$(jq -r '.content' <<< "$tweet")
        echo -e "\nScraped tweet $i: $tweet_content"
        echo "$tweet" >> "$output_filename"
        if [ "$max_tweets" ] && [ "$i" -gt "$max_tweets" ]; then
            break
        fi
    done <<< "$scrap"
done
