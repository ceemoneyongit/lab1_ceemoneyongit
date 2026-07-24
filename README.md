# lab1_ceemoneyongit - Grade Evaluator & Archiver

## How to Run

### Python Script
```bash
python3 grade-evaluator.py
```
When prompted, enter: `grades.csv`

### Shell Script
```bash
chmod +x organizer.sh
./organizer.sh
```

## What it does
- Validates scores (0-100) and weights (Total=100, Formative=60, Summative=40)
- Calculates GPA using formula: GPA = (Total Grade / 100) * 5.0
- Determines Pass/Fail (must score >= 50% in BOTH Formative and Summative)
- Shows which failed formative assignments are eligible for resubmission
- Shell script archives grades.csv with timestamp and logs the action
