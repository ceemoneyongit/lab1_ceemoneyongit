import csv
import sys
import os

REQUIRED_COLUMNS = ['assignment', 'group', 'score', 'weight']
TOTAL_WEIGHT = 100
FORMATIVE_WEIGHT = 60
SUMMATIVE_WEIGHT = 40


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    Invalid rows are skipped and reported; fatal problems exit with a message.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        sys.exit(1)

    assignments = []
    skipped = 0

    try:
        with open(filename, mode='r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: The CSV file has no header row.")
                sys.exit(1)

            headers = [h.strip().lower() for h in reader.fieldnames if h]
            missing = [c for c in REQUIRED_COLUMNS if c not in headers]
            if missing:
                print(f"Error: Missing required column(s): {', '.join(missing)}")
                sys.exit(1)

            for line_no, raw in enumerate(reader, start=2):
                row = {(k or '').strip().lower(): (v or '').strip() for k, v in raw.items()}

                # Skip completely empty rows
                if not any(row.values()):
                    print(f"Warning: Line {line_no} is empty and was skipped.")
                    skipped += 1
                    continue

                # Required fields must all have a value
                if not all(row.get(c) for c in REQUIRED_COLUMNS):
                    print(f"Warning: Line {line_no} has missing value(s) and was skipped.")
                    skipped += 1
                    continue

                # Group must be Formative or Summative
                group = row['group'].lower()
                if group not in ('formative', 'summative'):
                    print(f"Warning: Line {line_no} has unknown group '{row['group']}' and was skipped.")
                    skipped += 1
                    continue

                # Numeric fields must be numbers
                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except ValueError:
                    print(f"Warning: Line {line_no} has a non-numeric score or weight and was skipped.")
                    skipped += 1
                    continue

                assignments.append({
                    'assignment': row['assignment'],
                    'group': group.capitalize(),
                    'score': score,
                    'weight': weight
                })
    except SystemExit:
        raise
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if skipped:
        print(f"Note: {skipped} invalid row(s) were skipped.")

    if not assignments:
        print("Error: No valid assignment records found in the file.")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    Validates the data, calculates the final grade and GPA,
    determines Pass/Fail and any resubmission options.
    """
    print("\n--- Processing Grades ---")

    # a) Check if all scores are percentage based (0-100)
    valid = True
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: Score {item['score']:g} for '{item['assignment']}' is outside the 0-100 range.")
            valid = False
    for item in data:
        if item['weight'] <= 0:
            print(f"Error: Weight {item['weight']:g} for '{item['assignment']}' must be greater than 0.")
            valid = False

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    formative_weight = 0.0
    summative_weight = 0.0
    for item in data:
        if item['group'] == 'Formative':
            formative_weight += item['weight']
        else:
            summative_weight += item['weight']
    total_weight = formative_weight + summative_weight

    if total_weight != TOTAL_WEIGHT:
        print(f"Error: Total weight is {total_weight:g}, but it must be exactly {TOTAL_WEIGHT}.")
        valid = False
    if formative_weight != FORMATIVE_WEIGHT:
        print(f"Error: Formative weight is {formative_weight:g}, but it must be {FORMATIVE_WEIGHT}.")
        valid = False
    if summative_weight != SUMMATIVE_WEIGHT:
        print(f"Error: Summative weight is {summative_weight:g}, but it must be {SUMMATIVE_WEIGHT}.")
        valid = False

    if not valid:
        print("\nValidation failed. Please fix the errors above and try again.")
        return

    # c) Calculate the Final Grade and GPA
    formative_earned = 0.0
    summative_earned = 0.0
    for item in data:
        points = item['score'] * item['weight'] / 100
        if item['group'] == 'Formative':
            formative_earned += points
        else:
            summative_earned += points

    final_grade = formative_earned + summative_earned      # out of 100
    gpa = (final_grade / 100) * 5.0

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_pct = formative_earned / formative_weight * 100
    summative_pct = summative_earned / summative_weight * 100
    passed = formative_pct >= 50 and summative_pct >= 50

    # e) Check for failed formative assignments (< 50%)
    #    and find the highest weight among them (ties included)
    failed_formative = []
    for item in data:
        if item['group'] == 'Formative' and item['score'] < 50:
            failed_formative.append(item)

    resubmit = []
    if failed_formative:
        highest = failed_formative[0]['weight']
        for item in failed_formative:
            if item['weight'] > highest:
                highest = item['weight']
        for item in failed_formative:
            if item['weight'] == highest:
                resubmit.append(item)

    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"\nFormative: {formative_earned:.2f}/{FORMATIVE_WEIGHT} ({formative_pct:.1f}%)")
    print(f"Summative: {summative_earned:.2f}/{SUMMATIVE_WEIGHT} ({summative_pct:.1f}%)")
    print(f"Final Grade: {final_grade:.2f} / 100")
    print(f"GPA: {gpa:.2f} / 5.0")
    print(f"\nFinal Decision: {'PASSED' if passed else 'FAILED'}")

    if resubmit:
        print("\nEligible for resubmission (failed formative with the highest weight):")
        for item in resubmit:
            print(f"  - {item['assignment']} (score {item['score']:g}, weight {item['weight']:g})")
    else:
        print("\nNo failed formative assignments: no resubmission needed.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
