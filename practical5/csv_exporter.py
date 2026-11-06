import csv
import pandas as pd


def export_to_csv(students, courses):
    with open("students.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "dob", "gpa"])
        for s in students:
            writer.writerow([s.id, s.name, s.dob, s.gpa])

    with open("courses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "credit"])
        for c in courses.values():
            writer.writerow([c.id, c.name, c.credit])

    with open("marks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "course_id", "mark"])
        for s in students:
            for cid, mark in s.marks.items():
                writer.writerow([s.id, cid, mark])


def load_dataframes():
    df_students = pd.read_csv("students.csv")
    df_courses = pd.read_csv("courses.csv")
    df_marks = pd.read_csv("marks.csv")
    return df_students, df_courses, df_marks


def query_students_dataframe(condition):
    try:
        df_students, _, _ = load_dataframes()
        if df_students.empty:
            return "No student data available in DataFrame."
        result = df_students.query(condition)
        return result
    except Exception as e:
        return f"Query Error: {e}"