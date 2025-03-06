import glob
import json
from bs4 import BeautifulSoup

tweets = []

# Use glob to find all HTML files from each scroll iteration
for filename in glob.glob("scrolls/page_scroll_*.html"):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # Extract tweets from each article element
    for article in soup.find_all("article"):
        tweet_div = article.find("div", {"data-testid": "tweetText"})
        if tweet_div:
            tweet_text = tweet_div.get_text(separator=" ", strip=True)
        else:
            continue

        time_tag = article.find("time")
        tweet_time = time_tag["datetime"] if time_tag and time_tag.has_attr("datetime") else None

        tweets.append({
            "text": tweet_text,
            "datetime": tweet_time,
        })

# Remove duplicates based on tweet text
unique_tweets = []
seen_texts = set()
for tweet in tweets:
    # Normalize the tweet text: lower-case and strip extra spaces
    normalized_text = tweet["text"].lower().strip()
    if normalized_text not in seen_texts:
        unique_tweets.append(tweet)
        seen_texts.add(normalized_text)

# Output the unique tweets to the console
for tweet in unique_tweets:
    print(f"Time: {tweet['datetime']}")
    print(f"Tweet: {tweet['text']}\n")

# Save all unique tweets to a JSON file
with open("parsed_tweets.json", "w", encoding="utf-8") as outfile:
    json.dump(unique_tweets, outfile, indent=4)