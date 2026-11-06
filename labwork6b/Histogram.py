import pandas as po
import matplotlib.pyplot as plt
df = po.read_csv("students.csv")
plt.hist(df["GPA"].dropna(), bins = 8, edgecolor="black")

plt.title("Distribute of GPA")
plt.xlabel("GPA")
plt.ylabel("Number of Students")
plt.savefig("Histogram.png")
plt.show()