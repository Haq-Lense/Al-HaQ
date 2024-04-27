from snscrape.module import twitter
import json
queries=['residential proxies']
max = 1000
def scrap_id(query):
	scrap = twitter.twitterIdScraper(query)
	return scrap
for query in queries:
	output_filename = query.replace("","_"+".txt")
	with open(output_filename):
		scrap = scrap_id(query)
		i=0
		for i, tweet in enumerate(scrap.get_items(), start=1):
				tweet_json = json.loads(tweet.json())
				print(f"\nscraped tweet:{tweet_json['content']}")
				f.write(tweet.json)
				f.write("\n")
				f.flush()
				if max and i > max:
					break