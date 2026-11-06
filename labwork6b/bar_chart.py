import pandas as po 
import matplotlib.pyplot as plt

df = po.read_csv("students.csv")
average_gpa = df.groupby("major")["GPA"].mean()
average_gpa.plot(kind="bar")

plt.xlabel("Major")
plt.ylabel("Average GPA")
plt.title("Average GPA by Major")
plt.xticks(rotation=25)
plt.savefig("BarChart.pdf")
plt.savefig("BarChart.png")
plt.show()

plt.close()