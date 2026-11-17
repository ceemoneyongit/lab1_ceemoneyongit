# Lab 2: ALU Transcript Generator

Python app and Bash organizer for evaluating a student's course grades.

## Files
- `grade-evaluator.py` - validates grades.csv, calculates GPA, prints PASSED/FAILED and resubmission options
- `organizer.sh` - archives grades.csv with a timestamp, creates a new empty grades.csv, logs to organizer.log
- `grades.csv` - course data (`assignment,group,score,weight`)

## How to run
```
python3 grade-evaluator.py     # when prompted, type: grades.csv
bash organizer.sh
```

## What the Python app does
- Grade validation: every score must be between 0 and 100
- Weight validation: total = 100, Summative = 40, Formative = 60
- GPA = (Total Grade / 100) * 5.0, where Total Grade = sum(score * weight / 100)
- PASSED only if >= 50% in BOTH Formative and Summative
- Resubmission: failed formative assignment(s) (< 50) with the highest weight; all tied ones are listed

## Error handling
Missing or empty file, missing header/columns, empty rows, missing values, unknown group,
non-numeric values, out-of-range scores and wrong weights each print a clear message instead of crashing.

## Libraries
Only Python standard-library modules `csv`, `sys` and `os` are used, for reading the CSV
(provided in the starter template), exiting with an error code and checking the file exists.
No external libraries. `sort()`, `sorted()` and `max()` are not used.

## organizer.sh
1. Creates `archive/` if missing
2. Renames grades.csv to `grades_YYYYMMDD-HHMMSS.csv` inside `archive/`
3. Creates a new empty `grades.csv`
4. Appends timestamp, original filename and archived filename to `organizer.log` (entries accumulate)
