import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

# ---------------- CONFIG ----------------
PORT1 = "/dev/ttyUSB0"   # Master TX source
PORT2 = "/dev/ttyUSB0"   # Slave RX source
BAUD = 9600
WINDOW = 500             # number of points visible
# ----------------------------------------

# Open serial ports
ser1 = serial.Serial(PORT1, BAUD, timeout=0.01)
ser2 = serial.Serial(PORT2, BAUD, timeout=0.01)

# PyQtGraph window
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Dual Serial Scope (PyQtGraph)")
win.resize(900, 600)

# ----- TX Plot -----
tx_plot = win.addPlot(title="Master TX (USB0)")
tx_plot.setYRange(0, 255)
tx_curve = tx_plot.plot(pen='c')
tx_data = []

win.nextRow()

# ----- RX Plot -----
rx_plot = win.addPlot(title="Slave RX (USB1)")
rx_plot.setYRange(0, 255)
rx_curve = rx_plot.plot(pen='y')
rx_data = []

# ----- Update Loop -----
def update():
    global tx_data, rx_data

    # -------- USB0: Master TX --------
    if ser1.in_waiting:
        line1 = ser1.readline().decode(errors="ignore").strip()
        if line1.startswith("Master TX:"):
            try:
                v = int(line1.split(":")[1].strip())
                tx_data.append(v)
                tx_data = tx_data[-WINDOW:]
            except:
                pass

    # -------- USB1: Slave RX --------
    if ser2.in_waiting:
        line2 = ser2.readline().decode(errors="ignore").strip()
        if line2.startswith("Slave RX:"):
            try:
                v = int(line2.split(":")[1].strip())
                rx_data.append(v)
                rx_data = rx_data[-WINDOW:]
            except:
                pass

    # Update curves
    tx_curve.setData(tx_data)
    rx_curve.setData(rx_data)

    # 🔥 IMPORTANT: Force GUI refresh
    QtWidgets.QApplication.processEvents()


# Timer — smooth 100 FPS oscilloscope
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

# Exec (compatible with PyQt5 & PyQt6)
try:
    app.exec()      # PyQt6
except AttributeError:
    app.exec_()     # PyQt5
