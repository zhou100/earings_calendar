# earings_calendar

Personal earnings calendar: next earnings dates for my watchlist, regenerated daily from Yahoo Finance.

## Subscribe

Google Calendar -> Other calendars -> From URL, paste:

```
https://zhou100.github.io/earings_calendar/earnings.ics
```

## How it works

`.github/workflows/update.yml` runs `generate.py` every morning (~06:00 PT) and commits the refreshed `earnings.ics`. The file is served via GitHub Pages.
