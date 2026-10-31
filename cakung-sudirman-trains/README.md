# Cakung ⇄ Sudirman Trains

A small departure board for the KRL Commuter Line (Bekasi line) commute between Cakung and Sudirman.

- Shows the next train with a countdown, in Jakarta time (WIB)
- Switches direction on its own: Cakung → Sudirman before noon, Sudirman → Cakung after
- Covers both routes: direct via Manggarai (about 25–35 min) and the loop via Pasar Senen and Kampung Bandan (about 60–75 min)
- Tells you when waiting for a later train gets you there sooner

## Data

Times come from the KRL Commuter Line Jabodetabek timetable effective 1 February 2025. Check the KRL Access app for delays or timetable changes.

## Updating the timetable

`tools/parse.py` reads the Bekasi line tables from the timetable PDF. `tools/build.py` turns them into Cakung–Sudirman trips. You need Python with `pdfplumber` installed.

```
python3 tools/parse.py timetable.pdf
python3 tools/build.py
```

Then replace the `const DATA=...` line in `index.html` with the line written to `data.js`.
