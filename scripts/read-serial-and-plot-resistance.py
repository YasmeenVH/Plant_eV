### to install the dependencies for this:
## conda install -c conda-forge pyqtgraph pyqt


from collections import deque
import serial
from serial.tools import list_ports
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

## replace this with whatever port the Arduino/NodeMCU is on (check in Arduino IDE)
PORT = "/dev/cu.usbserial-0001"
## replace this with whatever baudrate you have in the reading script on the Arduino/NodeMCU
BAUDRATE = 115_200

## maximum number of datapoints to hold in memory at any point in time
MAX_DATAPOINTS = 10_000

ports_available = [tuple(p) for p in list(list_ports.comports())]
print("available ports:")
print("LOCATION,\tDEVICE,\tMISC")
for port in ports_available:
    print(port)

if PORT not in [x[0] for x in ports_available]:
    print("ERR: Couldn't find user-specified serial port in available serial ports")

ser = serial.Serial(PORT, BAUDRATE, timeout=10)


def get_serial_val():
    try:
        line = ser.readline().decode("UTF-8")
    except UnicodeDecodeError:
        return None

    # this is looking for a specific sctring in the serial connection,
    # so if you're not using my INO NodeMCU/Arduino firmware,
    # then adjust this to extract whatever format you have it in
    if line[:5] == "AIN0:":
        parts = line[:-2].split(" ")
        # print(parts)
        raw_val = int(parts[1])
        return raw_val
    else:
        return None


while True:
    val = get_serial_val()
    if val is not None:
        print("received a reading, good to start plotting")
        break

data_storage = deque(maxlen=MAX_DATAPOINTS)

app = pg.mkQApp("Plotting Example")
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle("pyqtgraph example: Plotting")
pg.setConfigOptions(antialias=True)

plot_container = win.addPlot(title="Updating plot")
curve = plot_container.plot(pen="y")  # yellow pen


def update():
    global curve, plot_container, data_storage
    reading = get_serial_val()
    if reading is not None:
        data_storage.append(reading)
    else:
        print("WARN: got empty reading - something is not working right")

    curve.setData(data_storage)


timer = QtCore.QTimer()
timer.timeout.connect(update)  # call the update function on a regular timer
timer.start(1)  # call this every millisecond (the `get_serial_val()` above will cause delays in the readings anyway)

app.exec_()
