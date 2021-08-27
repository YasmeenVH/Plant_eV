TIMER = 10  #Duration of the experiment in secondes
MEASURMENT_INTERVAL = 5  # seconds between each measurement, this can not be under 5 sencodes


import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import digitalio
import adafruit_tca9548a
from datetime import datetime
import numpy as np
from os.path import os
from os import path
import h5py


# 0. Function
# 0.1 Fucntion to get timestamp

def get_timestamp(strtofloat = "False"):
    current_timestamp = datetime.now()
    timestamp_string = str(current_timestamp).split('.')[0]
    timestamp_goodformat = ''
    for x in timestamp_string:
        if x is '-' or x is ' ' or x is ':' and strtofloat == "False":
            x = '_'
            timestamp_goodformat += x
        elif x is '-' or x is ' ' or x is ':' and strtofloat == "True":
            x = '_'
        else:
            timestamp_goodformat += x

    return timestamp_goodformat

# 0.2 Function to concatenate the npz file to get a big hdf5 file with all the data
def concatenate_files():
    tmp_files = sorted(os.listdir("./tmp"))
    tmp_files_filtered = [x for x in tmp_files if ".npz" in x]

    all_temp = []
    all_rh   = []
    all_pres = []
    all_time = []

    for x in tmp_files_filtered:
        data = np.load(f"./tmp/{x}")
        all_temp = np.append(all_temp,  data["temp"])
        all_rh.append(data["humidity"])
        all_pres.append(data["pressure"])
        all_time.append(data["timestamp"])

    all_temp = np.array(all_temp)
    all_rh   = np.array(all_rh)
    all_pres = np.array(all_pres)
    all_time = np.array(all_time)
    all_time = all_time.astype(np.float)

    timestamp_string = get_timestamp()
    filename = f"{timestamp_string}.hdf5"
    f = h5py.File(filename, "w")
    f.create_dataset("Temperature", data=all_temp)
    f.create_dataset("Humidity", data=all_rh)
    f.create_dataset("Pressure", data=all_pres)
    f.create_dataset("Timestamp", data=all_time)
    f.flush()
    f.close()

    for x in tmp_files_filtered:
        os.remove(f"./tmp/{x}")

    print(f"wrote new aggregate file: {filename}")


# 1. Create the folder to put data on npz format
if os.path.exists("./tmp"):
    print("dir already exists")
else:
    os.makedirs("./tmp")
    print("dir was created")

#
# 2. Create IC2 bus for the TCA9548A
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)


# 3. Loop for the acquisition of data
timer_start  = time.time()
timer_elapse = time.time()

while timer_elapse-timer_start < TIMER:
    timestamp_string = get_timestamp(strtofloat = "True")
    temp     = []
    Rh       = []
    pressure = []

    # Get sensors data
    for x in range(4):
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(tca[x])
        temp.append(bme280.temperature)
        Rh.append(bme280.relative_humidity)
        pressure.append(bme280.pressure)

    # Save data in npz files
    np.savez(f"./tmp/{timestamp_string}.npz",
         timestamp          = timestamp_string,
         temp               = temp,
         humidity           = Rh,
         pressure           = pressure)

    # Waiting time before another measurement
    time.sleep(MEASURMENT_INTERVAL-1.8)
    timer_elapse = time.time()

# 4. Concatenate file in a big hdf5 files
concatenate_files()
