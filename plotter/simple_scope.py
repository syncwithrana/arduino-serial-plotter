import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

# ---- CONFIG ----
PORT = "/dev/ttyUSB0"
BAUD = 9600
WINDOW = 500
# ----------------

ser = serial.Serial(PORT, BAUD, timeout=0.01)

app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Arduino Serial Oscilloscope")
win.resize(800, 500)

plot = win.addPlot(title="Serial Waveform")
plot.setYRange(0, 255)
curve = plot.plot(pen='y')

data = []

def update():
    global data

    while ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        if line.isdigit():  # expecting 0..255
            v = int(line)
            data.append(v)
            data = data[-WINDOW:]

    curve.setData(data)
    QtWidgets.QApplication.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)   # ~100 FPS

try:
    app.exec()
except AttributeError:
    app.exec_()
