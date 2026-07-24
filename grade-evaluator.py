import csv
import sys
import os


def load_csv_data():
    """Prompts user for filename, checks if it exists, extracts fields."""
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            if not rows:
                print("Error: The CSV file is empty. No grades to process.")
                sys.exit(1)

            for row in rows:
                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except ValueError:
                    print(f"Error: Invalid data in row: {row}")
                    sys.exit(1)

                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': score,
                    'weight': weight
                })
        return assignments
    except KeyError as e:
        print(f"Error: Missing expected column {e} in CSV file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """Evaluates grades, GPA, pass/fail, and resubmission logic."""
    print("\n--- Processing Grades ---")

    # a) Validate scores
    print("\n[Validation] Checking score ranges...")
    for item in data:
        if not (0 <= item['score'] <= 100):
            print(f"Error: Score for '{item['assignment']}' is {item['score']}, out of range (0-100).")
            sys.exit(1)
    print("All scores are within valid range (0-100).")

    # b) Validate weights
    print("\n[Validation] Checking weights...")
    total_weight = sum(item['weight'] for item in data)
    formative_weight = sum(item['weight'] for item in data if item['group'] == 'Formative')
    summative_weight = sum(item['weight'] for item in data if item['group'] == 'Summative')

    if total_weight != 100:
        print(f"Error: Total weights sum to {total_weight}, must equal 100.")
        sys.exit(1)
    if formative_weight != 60:
        print(f"Error: Formative weights sum to {formative_weight}, must equal 60.")
        sys.exit(1)
    if summative_weight != 40:
        print(f"Error: Summative weights sum to {summative_weight}, must equal 40.")
        sys.exit(1)
    print(f"Weights valid: Total={total_weight}, Formative={formative_weight}, Summative={summative_weight}.")

    # c) Calculate grades
    print("\n--- Grade Breakdown ---")
    total_grade = 0
    formative_score = 0
    formative_total_weight = 0
    summative_score = 0
    summative_total_weight = 0

    for item in data:
        weighted = (item['score'] / 100) * item['weight']
        total_grade += weighted
        print(f"  {item['assignment']} ({item['group']}): {item['score']}% x {item['weight']}% = {weighted:.2f}")
        if item['group'] == 'Formative':
            formative_score += weighted
            formative_total_weight += item['weight']
        else:
            summative_score += weighted
            summative_total_weight += item['weight']

    gpa = (total_grade / 100) * 5.0
    formative_percentage = (formative_score / formative_total_weight) * 100
    summative_percentage = (summative_score / summative_total_weight) * 100

    print(f"\n--- Results ---")
    print(f"Total Grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f} / 5.0")
    print(f"Formative Average: {formative_percentage:.2f}%")
    print(f"Summative Average: {summative_percentage:.2f}%")

    # d) Pass/Fail
    print(f"\n--- Final Decision ---")
    if formative_percentage >= 50 and summative_percentage >= 50:
        print("Status: PASSED")
    else:
        print("Status: FAILED")
        if formative_percentage < 50:
            print(f"  Reason: Formative average is {formative_percentage:.2f}% (below 50%)")
        if summative_percentage < 50:
            print(f"  Reason: Summative average is {summative_percentage:.2f}% (below 50%)")

    # e) Resubmission logic
    failed_formatives = [item for item in data
                         if item['group'] == 'Formative' and item['score'] < 50]

    if failed_formatives:
        max_weight = failed_formatives[0]['weight']
        for item in failed_formatives:
            if item['weight'] > max_weight:
                max_weight = item['weight']

        resubmit = [item for item in failed_formatives if item['weight'] == max_weight]

        print(f"\n--- Resubmission ---")
        print(f"Failed Formative assignments:")
        for item in failed_formatives:
            print(f"  - {item['assignment']}: {item['score']}% (weight: {item['weight']}%)")
        print(f"\nEligible for resubmission (highest weight = {max_weight}%):")
        for item in resubmit:
            print(f"  => {item['assignment']} (weight: {item['weight']}%)")
    else:
        print("\nNo failed formative assignments. No resubmission needed.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
