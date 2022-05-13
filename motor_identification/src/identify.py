import serial
import _thread
import csv
import time as timeModule

FIELD_NAMES = ["TIME", "REF_SPEED", "SPEED"]

OUTPUT_FILE_PATH = "output.csv"

with open(OUTPUT_FILE_PATH, "w") as f:
    csvWriter = csv.DictWriter(f, fieldnames=FIELD_NAMES)
    csvWriter.writeheader()

ser = serial.Serial("COM3", 9600)
ser.close()
ser.open()


def incrementSpeed():
    i = 0
    while i := i + 1:
        if i * 5 == 260:
            exit()
        print(i * 5)
        ser.write(b"1")
        timeModule.sleep(3)


try:
    _thread.start_new_thread(incrementSpeed, ())

    while True:
        if not ser.inWaiting():
            pass

        data = ser.readline().decode()
        time, ref_speed, speed = map(float, data.split(","))
        with open(OUTPUT_FILE_PATH, "a") as f:
            csvWriter = csv.DictWriter(f, fieldnames=FIELD_NAMES)

            info = {"TIME": time, "REF_SPEED": ref_speed, "SPEED": speed}

            csvWriter.writerow(info)

except Exception as e:
    ser.close()
    print(e)
    print("Error: unable to start thread")
