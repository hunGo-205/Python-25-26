import pandas as po
import matplotlib.pyplot as mat

df = po.read_csv('scores.csv')
po.plotting.scatter_matrix(df[['math', 'python', 'database']], figsize=(8, 8), alpha=0.8)
mat.suptitle("Scatter Plot Matrix of Scores")
mat.tight_layout()
mat.savefig('scattered.png')
mat.close()

fig, axes = mat.subplots(1, 3, figsize=(12,4))
courses = ['math', 'python', 'database']

for ax,course in zip(axes, courses):
    df[course].plot.hist(ax=ax, bins=10, edgecolor='black', title=f'Histogram of {course.upper()}')
    ax.set_xlabel('Scores')
    ax.set_ylabel('Frequency')

mat.tight_layout()
mat.savefig('Histo.png')
mat.close()
            
mat.figure(figsize=(8,6))
df[['math', 'python','database']].plot.box()
mat.title('Box Plot of Math, Python, and DB Scores')
mat.ylabel('Score')
mat.tight_layout()
mat.savefig('box.png')
mat.close()