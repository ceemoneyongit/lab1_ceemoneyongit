#!/bin/bash
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory."
fi
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found."
    exit 1
fi
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
NEW_NAME="grades_${TIMESTAMP}.csv"
cp grades.csv "archive/${NEW_NAME}"
rm grades.csv
echo "Archived grades.csv as archive/${NEW_NAME}"
touch grades.csv
echo "Created fresh grades.csv"
echo "[${TIMESTAMP}] Archived: grades.csv -> archive/${NEW_NAME}" >> organizer.log
echo "Logged to organizer.log"
