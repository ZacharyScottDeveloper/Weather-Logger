# 🌩️ Weather Logger

A Python script that automatically fetches extreme weather events from around the world and saves them to a JSON file for later analysis.

---

## What does it do?

Every time you run it, the script:

1. **Loads any existing data** from `log.json` so it knows what events it has already seen.
2. **Calls the GDACS API** — a real disaster alert service run by the EU — to grab all major weather events from the past 7 days.
3. **Filters out duplicates** so the same event never gets logged twice.
4. **Saves the new events** as a new "week" entry in `log.json`.

---

## What events does it track?

It only captures serious (red or orange alert level) events, including:

| Code | Event Type |
|------|------------|
| EQ | Earthquake |
| TC | Tropical Cyclone |
| FL | Flood |
| VO | Volcano |
| WF | Wildfire |
| DR | Drought |

---

## What gets saved?

For each event, the script saves:

- **Event ID** — a unique identifier
- **Event type** — e.g. flood, earthquake
- **Alert level** — red or orange
- **Country** — where it happened
- **Headline** — a short description
- **From/To dates** — when it occurred
- **Coordinates** — the location on a map

---

## Files in this repo

| File | Description |
|------|-------------|
| `weather-event-tracker.py` | The main script |
| `log.json` | Where all the event data gets saved |
| `.github/workflows/` | GitHub Actions config (for running the script automatically) |

---

## How to run it

**Requirements:** Python 3 and the `requests` library.

Install the dependency:
```bash
pip install requests
```

Then run the script:
```bash
python weather-event-tracker.py
```

The results will be saved to `log.json` in the same folder.

---

## Data source

Event data comes from the [GDACS API](https://www.gdacs.org/) (Global Disaster Alert and Coordination System), a free public service provided by the European Commission.
