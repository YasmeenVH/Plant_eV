# RPi
import time 
# import RPi.GPIO as GPIO 
import paho.mqtt.client as mqtt 
import numpy as np
import datetime
import time
import h5py

NODEMCU_SEND_TIME = 2 # seconds between Node broadcasts
# time in seconds when the numpy files should be concatenated and stored as HDF5
TIMER_MAX = 10 # every 10 seconds
# TIMER_MAX = 10 * 60 # every 10 minutes

# TODO: once this is tested, crank this up to every hour, then every day.

timer = 0

# Setup callback functions that are called when MQTT events happen like 
# connecting to the server or receiving data from a subscribed feed. 
def on_connect(client, userdata, flags, rc): 
   
   print("Connected with result code " + str(rc)) 
   # Subscribing in on_connect() means that if we lose the connection and 
   # reconnect then subscriptions will be renewed. 
   client.subscribe("test")
   ev_data = -1  
   os.makedirs("./tmp") # this fails if directory exists

def payload_to_python(payload)
   ### example "[1,2,0.5,1,...,]", also don't forget `import json`
   return json.loads(payload) # http://docs.python.org/library/json.html#json.loads

def get_timestamp():
   current_timestamp = time.time() 
   timestamp_string = datetime.datetime.fromtimestamp(current_timestamp).strftime("%Y%m%d-%H%M%S')
   return timestamp_string

# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
   globals timer
   print(msg.topic+" "+str(msg.payload)) 
   # Check if this is a message for the Pi LED. 
   plant_ev_signals = payload_to_python(msg.payload) # takes the payload and converts to numpy array or Py list
   hum_temp = read_dht()
   compounds = read_comp_sensor()
   picture = read_camera()

   timestamp_string = get_timestamp()
   np.savez(f"./tmp/{timestamp_string}.npz", 
            hum_temp=hum_temp, 
            compounds=compounds,
            picture=picture,
            plant_ev_signals=plant_ev_signals)

   timer += 1                                                                                   
                                                                                  
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
   all_the_images = []
   all_the_dhts = []
   all_the_compounds = []

   for x in tmp_files_filtered:
      data = np.load(f"./tmp/{x}") # load a single numpy file
      all_the_nodemcu_data.append(data["plant_ev_signals"])
      all_the_images.append(data["picture"])
      all_the_dhts.append(data["hum_temp"])
      all_the_compounds.append(data["compounds"])

   # let's make all those buffers into numpy arrays
   all_the_nodemcu_data = np.array(all_the_nodemcu_data)                                                                               
   all_the_images = np.array(all_the_images)
   all_the_dhts = np.array(all_the_dhts)                                                                               
   all_the_compounds = np.array(all_the_compounds)

   # sanity check
   print (all_the_nodemcu_data.shape, all_the_nodemcu_data.dtype, all_the_nodemcu_data.min(), all_the_nodemcu_data.max(), all_the_nodemcu_data.mean())
   print (all_the_images.shape, all_the_images.dtype, all_the_images.min(), all_the_images.max(), all_the_images.mean())
   print (all_the_dhts.shape, all_the_dhts.dtype, all_the_dhts.min(), all_the_dhts.max(), all_the_dhts.mean())
   print (all_the_compounds.shape, all_the_compounds.dtype, all_the_compounds.min(), all_the_compounds.max(), all_the_compounds.mean())
                                                                                  
   timestamp_string = get_timestamp()
   filename = f"{timestamp_string}.hdf5"
   f = h5py.File(filename, "w")
   f.create_dataset("ev_data", all_the_nodemcu_data)
   f.create_dataset("images", all_the_images)
   f.create_dataset("dht", all_the_dhts)
   f.create_dataset("compounds", all_the_compounds)
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
client.connect('192.168.0.106', 1883, 60) 
# Connect to the MQTT server and process messages in a background thread. 
client.loop_forever() 
