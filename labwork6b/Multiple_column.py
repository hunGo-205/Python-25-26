import pandas as pd
import matplotlib.pyplot as plt
df = pd.DataFrame({
"python": [70, 73, 75, 78, 82, 85, 88],
"math": [68, 71, 74, 77, 79, 84, 86]
}, index=[1, 2, 3, 4, 5, 6, 7])
df[["python", "math"]].plot(marker="o")
plt.title("Scores over Time")
plt.xlabel("Week")
plt.ylabel("Score")
plt.show()