import feedparser
from bs4 import BeautifulSoup
import json

# Replace with your Google Alert RSS feed URL
rss_url = 'https://www.google.com/alerts/feeds/14821320735758315107/443672522669696169'
feed = feedparser.parse(rss_url)

def strip_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

results = []

for entry in feed.entries:
    # Remove HTML tags from title and summary
    clean_title = strip_html(entry.title)
    clean_summary = strip_html(entry.summary)
    
    results.append({
        'Title': strip_html(clean_title),
        'Link': entry.link,
        'Published': entry.published,
        'Summary': strip_html(clean_summary)
    })

with open('results/rss_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

