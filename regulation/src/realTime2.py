from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

FIELD_NAMES = ["TIME", "REF_SPEED", "SPEED"]

INPUT_FILE_PATH = "output.csv"
maxPointsInGraph = 30000

plt.style.use("fivethirtyeight")
index = count()


def animate(i):
    # global X, Y
    data = pd.read_csv(INPUT_FILE_PATH)
    x = data["TIME"]
    y0 = data["REF_SPEED"]
    y = data["SPEED"]
    if len(x) > maxPointsInGraph:
        x = x[-maxPointsInGraph:]
        y0 = y0[-maxPointsInGraph:]
        y = y[-maxPointsInGraph:]
    # X.append(next(index))
    # Y.append(random.randint(0, 5))
    plt.cla()
    plt.ylim(0, 4000)
    plt.plot(
        x,
        y,
        label="speed",
    )
    plt.plot(
        x,
        y0,
        label="ref",
    )
    plt.legend(loc="lower right")
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)
# animate(0)
plt.tight_layout()
plt.show()
