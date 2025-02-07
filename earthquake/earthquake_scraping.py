import requests # type: ignore
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# API for getting earthquakes in real-time
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# calculate time frame
current_date = datetime.today()
tomorrow_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
previous_month_date = current_date - relativedelta(months=1)

# convert format
current_date = datetime.today().strftime('%Y-%m-%d')
previous_month_date= previous_month_date.strftime('%Y-%m-%d')

# set start and end time for queries and the minimum magnitue of the earthquakes to be included
# here we use tomorrow's date to also include results that occured today
params = {
    "format": "geojson",
    "starttime": previous_month_date,
    "endtime": tomorrow_date,
    "minmagnitude": 1
}

# get
response = requests.get(url, params=params)
data = response.json()

# convert to pandas
earthquakes = [
    {
        "time": event["properties"]["time"],
        "magnitude": event["properties"]["mag"],
        "place": event["properties"]["place"],
        "latitude": event["geometry"]["coordinates"][1],
        "longitude": event["geometry"]["coordinates"][0],
        "depth": event["geometry"]["coordinates"][2],
    }
    for event in data["features"]
]

df = pd.DataFrame(earthquakes)
# interpret the time from epoch time to UTC
df["time"] = df["time"].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S UTC'))

print(df.head())
df.to_csv("earthquake_data.csv", index=False)