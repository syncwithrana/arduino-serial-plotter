import serial
import matplotlib.pyplot as plt

# ---- CONFIG ----
PORT = "/dev/ttyUSB0"  # change if needed
BAUD = 9600
WINDOW = 300           # number of points visible on screen
# -----------------

ser = serial.Serial(PORT, BAUD)

plt.ion()
fig, ax = plt.subplots()
data = []

while True:
    try:
        line = ser.readline().decode().strip()
        value = int(line)         # expecting Arduino to send "0", "1", ...
        data.append(value)

        if len(data) > WINDOW:
            data.pop(0)

        ax.clear()
        ax.plot(data)
        ax.set_ylim(0, 255)
        ax.set_title("Serial Live Plot")
        plt.pause(0.001)

    except Exception as e:
        print("Error:", e)
        continue
