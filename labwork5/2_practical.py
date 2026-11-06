import pandas as pd

students = pd.read_csv('students.csv')
scores = pd.read_csv('scores.csv')

print("Missing in students.csv:\n", students.isnull().sum())
print("\nMissing in scores.csv:\n", scores.isnull().sum())

students['age'] = students['age'].fillna(students['age'].median())

students['GPA'] = students.groupby('major')['GPA'].transform(lambda x: x.fillna(x.mean()))

scores['math'] = scores['math'].fillna(scores['math'].mean())
scores['database'] = scores['database'].fillna(scores['database'].mean())

merged_df = pd.merge(students, scores, on='student_id')

merged_df['average_score'] = merged_df[['python', 'math', 'database']].mean(axis=1)

top_5_students = merged_df.sort_values(by='average_score', ascending=False).head(5)
print("\n--- Top 5 Students ---")
print(top_5_students[['student_id', 'name', 'major', 'average_score']])

avg_score_by_major = merged_df.groupby('major')['average_score'].mean()
print("\n--- Average Score by Major ---")
print(avg_score_by_major)