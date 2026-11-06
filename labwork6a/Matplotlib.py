import matplotlib.pyplot as go
import math
num_points = 500
x = [-5.0 + i * (10.0 / (num_points - 1) ) for i in range (num_points)]

y =[ 2 *xi + math.sin(xi) **2 +3 for xi in x ]

go.figure(figsize=(8,6))
go.plot(x, y, label=r"$y = 2x + \sin^2(x) + 3$")
go.title("Hello, po!")
go.grid(True)
go.xlabel("x")
go.ylabel("y")

go.xticks(range(-5,6))
go.legend()


go.savefig("Po.pdf")
go.show()
go.close()