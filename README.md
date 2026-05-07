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
| `weather-event-tracker.py` | Fetches extreme weather events from the API and saves them to `log.json` |
| `log.json` | The raw event data, saved week by week |
| `reader.py` | Reads `log.json`, analyses the data using pandas, and writes the results to `log_analysis.txt` |
| `log_analysis.txt` | The human-readable analysis output produced by `reader.py` |
| `.github/workflows/` | GitHub Actions config (runs everything automatically on a schedule) |

---

## How the analysis works

`reader.py` reads the raw data from `log.json` and processes it using **pandas** (a Python data analysis library). Here's what it does step by step:

1. **Loads all events** from every week in `log.json` into a single flat table
2. **Parses the dates** so they can be used for calculations
3. **Splits countries** — since one event can affect multiple countries (e.g. "Argentina, Brazil"), it creates a separate row for each country so they can be counted individually
4. **Calculates duration** — works out how many days each event lasted (end date minus start date)
5. **Extracts coordinates** — pulls longitude and latitude out into their own columns
6. **Writes `log_analysis.txt`** with three sections:
   - **Sample event rows** — a table of the first few events with all their details
   - **Country counts** — how many events affected each country
   - **Event type counts** — totals for each disaster type (flood, drought, etc.)

This runs automatically via GitHub Actions every week, so `log_analysis.txt` is always kept up to date.

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
