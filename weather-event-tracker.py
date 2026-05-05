import requests
import datetime
import json

log_path = "log.json"
weekly_logs = []
weather_data_last_week = []

try:
    with open(log_path, "r", encoding="utf-8") as log_file:
        weekly_logs = json.load(log_file)
        if weekly_logs:
            weather_data_last_week = weekly_logs[-1]
        print(f"Loaded {len(weekly_logs)} weeks of data from {log_path}.")
except FileNotFoundError:
    print(f"Warning: {log_path} not found, starting new log.")
except json.JSONDecodeError as exc:
    print(f"Error reading {log_path}: {exc}")

past_eventids = set()
for week in weekly_logs:
    for event in week:
        eventid = event.get("properties", {}).get("eventid")
        if eventid:
            past_eventids.add(eventid)

current_date = datetime.datetime.now().date()
date_week_ago = current_date - datetime.timedelta(days=7)
all_events = []
page = 1

while True:
    response = requests.get(
        "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH",
        params={
            "eventlist": "EQ;TC;FL;VO;WF;DR",
            "alertlevel": "red;orange;green",
            "fromdate": date_week_ago.strftime("%Y-%m-%d"),
            "todate": current_date.strftime("%Y-%m-%d"),
            "pagenumber": page
        }
    )

    if not response.text.strip():
        print(f"Finished! Got {len(all_events)} total events across {page - 1} pages.")
        break

    data = response.json()
    events = data.get("features", [])

    if not events:
        print(f"Finished! Got {len(all_events)} total events across {page - 1} pages.")
        break

    all_events.extend(events)
    print(f"Page {page}: got {len(events)} events")
    page += 1

filtered_events = []
skipped_count = 0
for event in all_events:
    eventid = event.get("properties", {}).get("eventid")
    if eventid and eventid not in past_eventids:
        filtered_events.append(event)
    else:
        skipped_count += 1
        print(f"Skipping duplicate event: {eventid}")

print(f"Fetched {len(all_events)} events, {skipped_count} duplicates skipped, {len(filtered_events)} new events.")

for event in filtered_events:
    props = event["properties"]
    print(props.get("eventtype"), props.get("country"), props.get("alertlevel"))


weekly_logs.append(filtered_events)
with open(log_path, "w", encoding="utf-8") as log_file:
    json.dump(weekly_logs, log_file, indent=4)
    print(f"Saved new week with {len(filtered_events)} events to {log_path}.")
