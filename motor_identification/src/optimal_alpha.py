import pandas as pd
import math
import matplotlib.pyplot as plt


STARTING_POINT = 6
X0 = 30
MAX_SPEED = 4200
INPUT_FILE_PATH = "results.csv"

F = lambda x, alpha: MAX_SPEED * (1 - math.exp(-(x - X0) * alpha))
data = pd.read_csv(INPUT_FILE_PATH)
X = [*map(float, data["CMD"])]
Y = [*map(float, data["SPEED"])]

X = X[STARTING_POINT:]
Y = Y[STARTING_POINT:]


number_of_points = len(X)


def meanError(alpha):
    Y2 = [*map(lambda x: F(x, alpha), X)]
    # print(Y2)
    s = 0
    for a, b in zip(Y, Y2):
        s += abs(a - b) / max(a, 1)
    return s / number_of_points


errors = []
alphaList = []

alpha = 0.001

i = 0.01
while i < 0.05:
    alphaList += [i]
    errors += [meanError(i)]
    i += 0.0001


plt.plot(alphaList, errors, label="errors")
plt.legend("Error", loc="lower right")
plt.show()

print("MINIMAL ERROR :", min(errors) * 100)
print("OPTIMAL ALPHA :", round(alphaList[errors.index(min(errors))], 6))
