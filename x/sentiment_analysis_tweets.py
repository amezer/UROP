import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

nltk.download('vader_lexicon')

with open("results/parsed_tweets.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

analyzer = SentimentIntensityAnalyzer()

results = []
for tweet in tweets:
    text = tweet["text"]
    sentiment_score = analyzer.polarity_scores(text)

    if sentiment_score["compound"] >= 0.05:
        sentiment = "positive"
    elif sentiment_score["compound"] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    results.append({
        "text": text,
        "datetime": tweet["datetime"],
        "sentiment_scores": sentiment_score,
        "sentiment": sentiment
    })

# Display the results
for result in results:
    print(result)


df = pd.DataFrame(results)

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['compound'] = df['sentiment_scores'].apply(lambda score: score['compound'])


daily_sentiment = df.groupby('date')['compound'].mean()

output_dir = "results/plots"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10,6))
plt.plot(daily_sentiment.index, daily_sentiment.values, marker='o', color='purple')
plt.title("Average Daily Compound Sentiment")
plt.xlabel("Date")
plt.ylabel("Average Compound Score")
plt.xticks(rotation=45)

plot_filename = os.path.join(output_dir, "daily_sentiment.png")
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
plt.show()