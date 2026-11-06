import pandas as po
import matplotlib.pyplot as plt

students = po.read_csv("students.csv")
scores = po.read_csv("scores.csv")
df = po.merge(students, scores, on="student_id")
df ["average_score"] = df[["python", "math", "database"]].mean(axis=1)
plot_data = df[["GPA", "average_score"]].dropna()

plt.scatter(
    plot_data["GPA"],
    plot_data["average_score"]
)

plt.xlabel("GPA")
plt.ylabel("Average Score")
plt.title("GPA and Average score")
plt.savefig("LinePlot.png")
plt.show()
plt.close()