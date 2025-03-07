import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

nltk.download('vader_lexicon')

with open("results/rss_results.json", "r", encoding="utf-8") as f:
    news = json.load(f)

analyzer = SentimentIntensityAnalyzer()

results = []
for article in news:
    text = article["Title"] + " " + article["Summary"]
    sentiment_score = analyzer.polarity_scores(text)

    if sentiment_score["compound"] >= 0.05:
        sentiment = "positive"
    elif sentiment_score["compound"] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    results.append({
        "text": text,
        "datetime": article["Published"],
        "sentiment_scores": sentiment_score,
        "sentiment": sentiment
    })

# Display the results
for result in results:
    print(result)