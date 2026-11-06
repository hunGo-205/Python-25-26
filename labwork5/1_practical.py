import pandas as pd

df_students = pd.read_csv('students.csv')

print("--- First 5 Rows ---")
print(df_students.head())

rows, cols = df_students.shape
print(f"\nDataset shape: {rows} rows, {cols} columns")

name_gpa = df_students[['name', 'GPA']]
print("\n--- Name and GPA ---")
print(name_gpa.head())

high_gpa = df_students[df_students['GPA'] >= 3.5]
print("\n--- Students with GPA >= 3.5 ---")
print(high_gpa[['student_id', 'name', 'major', 'GPA']])

sorted_students = df_students.sort_values(by='GPA', ascending=False)
print("\n--- Sorted by GPA (Descending) ---")
print(sorted_students[['name', 'major', 'GPA']].head(10))

avg_gpa_by_major = df_students.groupby('major')['GPA'].mean()
print("\n--- Average GPA by Major ---")
print(avg_gpa_by_major)