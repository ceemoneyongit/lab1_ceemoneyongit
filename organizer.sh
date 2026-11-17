#!/bin/bash
# Archives grades.csv with a timestamp, creates a new empty grades.csv,
# and appends the details to organizer.log.

CSV="grades.csv"
ARCHIVE_DIR="archive"
LOG="organizer.log"

# Create the archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

if [ ! -f "$CSV" ]; then
    echo "Error: $CSV not found in $(pwd). Nothing to archive."
    echo "$TIMESTAMP | ERROR: $CSV not found, nothing archived" >> "$LOG"
    exit 1
fi

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

# Rename (move) the existing file into the archive with the timestamp
mv "$CSV" "$ARCHIVE_DIR/$ARCHIVED_NAME"

# Workspace reset: create a new, empty grades.csv
: > "$CSV"

# Log: timestamp, original filename, new archived filename
echo "$TIMESTAMP | original: $CSV | archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG"

echo "Archived $CSV -> $ARCHIVE_DIR/$ARCHIVED_NAME"
echo "New empty $CSV created. Logged to $LOG."
