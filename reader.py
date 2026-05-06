import json
import pandas as pd

with open("log.json", "r", encoding="utf-8") as log_file:
    weekly_data = json.load(log_file)

all_events = [event for week in weekly_data for event in week]

df = pd.json_normalize(all_events)

df["fromdate"] = pd.to_datetime(df["fromdate"], errors="coerce")
df["todate"] = pd.to_datetime(df["todate"], errors="coerce")

df["country"] = df["country"].str.split(", ")
df = df.explode("country").reset_index(drop=True)

country_counts = df["country"].value_counts()
df["longitude"] = df["coordinates"].str[0]
df["latitude"] = df["coordinates"].str[1]
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1100)

df["duration"] = (df["todate"] - df["fromdate"]).dt.days

sample_rows_output = "Sample event rows:\n" + df.head().to_string(index=False)
country_counts_output = "Country counts:\n" + country_counts.to_frame("count").to_string()
event_type_counts_output = "Event type counts:\n" + df["eventtype"].value_counts().to_frame("count").to_string()
alert_level_counts_output = "Alert level counts:\n" + df["alertlevel"].value_counts().to_frame("count").to_string()
avg_duration_by_country_output = (
    "Average event duration by country (days):\n"
    + df.groupby("country")["duration"]
    .mean()
    .sort_values(ascending=False)
    .round(1)
    .to_frame("avg_duration")
    .to_string()
)
avg_duration_by_event_type_output = (
    "Average event duration by event type (days):\n"
    + df.groupby("eventtype")["duration"]
    .mean()
    .sort_values(ascending=False)
    .round(1)
    .to_frame("avg_duration")
    .to_string()
)

output_text = "\n\n".join(
    [
        sample_rows_output,
        country_counts_output,
        event_type_counts_output,
        alert_level_counts_output,
        avg_duration_by_country_output,
        avg_duration_by_event_type_output,
    ]
)

print(output_text)

with open("log_analysis.txt", "w") as f:
    f.write(output_text)
