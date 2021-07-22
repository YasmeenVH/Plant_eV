# RPi
import time
# import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import numpy as np
import datetime
import time
import h5py
import json
import os.path
from os import path
from datetime import datetime
from software.Plant_eV.env_conditions import Sensors

S=Sensors()

NODEMCU_SEND_TIME = 2  # seconds between Node broadcasts
TIMER_MAX         = 180 # time in seconds when the numpy files should be concatenated and stored as HDF5
TIMER_COND        = 10 # time in seconds when to get temp, rh, co2, voc sensors data
timer             = 0

# Setup callback functions that are called when MQTT events happen like
# connecting to the server or receiving data from a subscribed feed.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test")

    if os.path.exists("./tmp"):
        return print("dir already exists")
    else:
        os.makedirs("./tmp")
        return print("dir was created")

def payload_to_python(payload):
   ### example "[1,2,0.5,1,...,]", also don't forget `import json`
   return json.loads(payload) # http://docs.python.org/library/json.html#json.loads

def get_timestamp():
    current_timestamp = datetime.now()
    timestamp_string = str(current_timestamp).split('.')[0]
    return timestamp_string

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global timer
    plant_ev_signals = payload_to_python(msg.payload) # takes the payload and converts to numpy array or Py list

    if (timer * NODEMCU_SEND_TIME) % TIMER_COND == 0:
        rh, temp = S.rh_temp()
        co2, voc = S.gas()

        if temp == None or rh == None:
            temp = 1234
            rh   = 1234
        if co2 == None or voc == None:
            co2 = 1234
            voc = 1234

        timestamp_string = get_timestamp()
        np.savez(f"./tmp/{timestamp_string}.npz",
             temp               = temp,
             humidity           = rh,
             CO2                = co2,
             VOC                = voc,
             plant_ev_signals   = plant_ev_signals["data"],
             timestamp          = plant_ev_signals["timestamp"])
        print("ok")
    else:
        timestamp_string = get_timestamp()
        np.savez(f"./tmp/{timestamp_string}.npz",
             temp               = 1234,
             humidity           = 1234,
             CO2                = 1234,
             VOC                = 1234,
             plant_ev_signals   = plant_ev_signals["data"],
             timestamp          = plant_ev_signals["timestamp"])

    timer += 1
    print(timer)

    if timer * NODEMCU_SEND_TIME == TIMER_MAX:
        concatenate_files() # read all the small numpy files, write to one big HDF5, then delete all numpy files
        timer = 0

def concatenate_files():
    tmp_files = sorted(os.listdir("./tmp"))

    # ./.
    # ./..
    # ./.DS_STORE
    # ./20200714-045412.npz
    tmp_files_filtered = [x for x in tmp_files if ".npz" in x]

    # these will store all the data from the individual numpys
    all_the_nodemcu_data = []
    all_the_rh           = []
    all_the_temp         = []
    all_the_co2          = []
    all_the_voc          = []
    all_the_timestamp    = []

    for x in tmp_files_filtered:
        data = np.load(f"./tmp/{x}") # load a single numpy file
        all_the_nodemcu_data.append(data["plant_ev_signals"])
        all_the_temp.append(data["temp"])
        all_the_rh.append(data["humidity"])
        all_the_co2.append(data["CO2"])
        all_the_voc.append(data["VOC"])
        all_the_timestamp.append(data["timestamp"])

    # let's make all those buffers into numpy arrays
    all_the_nodemcu_data = np.array(all_the_nodemcu_data)
    all_the_temp         = np.array(all_the_temp)
    all_the_rh           = np.array(all_the_rh)
    all_the_co2          = np.array(all_the_co2)
    all_the_voc          = np.array(all_the_voc)
    all_the_timestamp    = np.array(all_the_timestamp)

#    print(all_the_nodemcu_data)
#    print(all_the_temp)
#    print(all_the_rh)
#    print(all_the_co2)
#    print(all_the_voc)

    #sanity check
    print (all_the_nodemcu_data.shape, all_the_nodemcu_data.dtype, all_the_nodemcu_data.min(), all_the_nodemcu_data.max(), all_the_nodemcu_data.mean())
    print (all_the_temp.shape, all_the_temp.dtype, all_the_temp.min(), all_the_temp.max(), all_the_temp.mean())
    print (all_the_rh.shape, all_the_rh.dtype, all_the_rh.min(), all_the_rh.max(), all_the_rh.mean())
    print (all_the_co2.shape, all_the_co2.dtype, all_the_co2.min(), all_the_co2.max(), all_the_co2.mean())
    print (all_the_voc.shape, all_the_voc.dtype, all_the_voc.min(), all_the_voc.max(), all_the_voc.mean())
    print (all_the_timestamp.shape, all_the_timestamp.dtype, all_the_timestamp.min(), all_the_timestamp.max(), all_the_timestamp.mean())

    timestamp_string = get_timestamp()
    filename = f"{timestamp_string}.hdf5"
    f = h5py.File(filename, "w")
    f.create_dataset("ev_data", data=all_the_nodemcu_data)
    f.create_dataset("temp", data=all_the_temp)
    f.create_dataset("rh", data=all_the_rh)
    f.create_dataset("CO2", data=all_the_co2)
#    f.create_dataset("timestamp", all_the_timestamp)
    f.create_dataset("VOC", data=all_the_voc)
    f.flush() # write all this to disk
    f.close() # and close the file

    # remove all the
    for x in tmp_files_filtered:
        os.remove(f"./tmp/{x}")

    print (f"wrote new aggregate file: {filename}")


# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running
# this script and the MQTT server.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('10.0.0.66', 1883, 60)
# Connect to the MQTT server and process messages in a background thread.
client.loop_forever()
#concatenate_files()
