import requests
import pandas as pd
from datetime import datetime

# specify topic in URL encoding
# %22 is "
# %20 is single space
topic = "(%22wildlife%20crime%22%20OR%20poaching%20OR%20%22illegal%20fishing%22%20OR%20%22wildlife%20trade%22)"
maxrecords = 100
url = "https://api.gdeltproject.org/api/v2/doc/doc?query="+topic+"&mode=artlist&maxrecords="+str(maxrecords)+"&timespan=1week&format=json"

# send request
response = requests.get(url)
data = response.json()

articles = data.get("articles", [])

df = pd.DataFrame(articles)


# process date to be more readable
def convert_seendate(x):
    try:
        return datetime.strptime(x, "%Y%m%d%H%M%S").strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(x, "%Y%m%dT%H%M%SZ").strftime('%Y-%m-%d %H:%M:%S UTC')
        except ValueError:
            return None

df["seendate"] = df["seendate"].apply(convert_seendate)

# Display relevant columns
print(df[["title", "url", "seendate", "domain", "language"]])

df[["title", "url", "seendate", "domain", "language"]].to_csv("gdelt_news.csv", index=True)