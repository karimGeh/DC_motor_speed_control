import pandas as pd
import csv


# file = open(OUTPUT_FILE_PATH)
FIELD_NAMES = ["TIME", "REF_SPEED", "SPEED"]
OUTPUT_FIELD_NAMES = ["CMD", "SPEED"]

INPUT_FILE_PATH = "output.csv"
OUTPUT_FILE_PATH = "results.csv"

with open(OUTPUT_FILE_PATH, "w") as f:
    csvWriter = csv.DictWriter(f, fieldnames=OUTPUT_FIELD_NAMES)
    csvWriter.writeheader()

data = pd.read_csv(INPUT_FILE_PATH)
x = data["TIME"]
y0 = map(float, data["REF_SPEED"])
y = map(float, data["SPEED"])

d = {}

for a, b in zip(y0, y):
    if a > 255:
        break
    if a in d:
        d[a] += [b]
    else:
        d[a] = [b]

for i, v in d.items():
    mean_speed = sum(v) / len(v)
    with open(OUTPUT_FILE_PATH, "a") as f:
        csvWriter = csv.DictWriter(f, fieldnames=OUTPUT_FIELD_NAMES)
        info = {"CMD": i, "SPEED": round(mean_speed)}
        csvWriter.writerow(info)
