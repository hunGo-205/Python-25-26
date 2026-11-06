import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
students = pd.read_csv("students.csv")
scores = pd.read_csv("scores.csv")
df = pd.merge(students, scores, on="student_id")
df["average_score"] = df[["python", "math",
"database"]].mean(axis=1)
sns.barplot( data=df,
x="major",
y="average_score",
errorbar=None
)
plt.title("Average Score by Major")
plt.xticks(rotation=25)
plt.show()