import numpy as np
import h5py
import os
import os.path
from datetime import datetime
import time


def get_timestamp():
    current_timestamp = datetime.now()
    timestamp_string = str(current_timestamp).split('.')[0]
    return timestamp_string



def make_h5():
    tmp_files = sorted(os.listdir("./tmp"))
    tmp_get_npz = [x for x in tmp_files if ".npz" in x]
    
    nodes = []
    rh = []
    temp = []
    co2 = []
    voc = []
    timestamps = []

    for f in tmp_get_npz:
        data = np.load(f"./tmp/{f}")
        nodes.append(data["plant_ev_signals"])
        temp.append(data["temp"])
        rh.append(data["humidity"])
        co2.append(data["CO2"])
        voc.append(data["VOC"])
        timestamps.append(data["timestamp"])

    nodes = np.array(nodes)
    temp = np.array(temp)
    rh = np.array(rh)
    co2 = np.array(co2)
    voc = np.array(voc)
    timestamps = np.array(timestamps)
   
    #path = '/home/pi/Plant_eV/software/Plant_eV/data
    #os.path.dirname(
    timestamp_string = get_timestamp() 
    filename = f"/home/pi/long_apple_amp_run.hdf5"
    f = h5py.File(filename, "w")
    f.create_dataset("ev_data", data=nodes)
    f.create_dataset("temp", data=temp)
    f.create_dataset("rh", data=rh)
    f.create_dataset("CO2", data=co2)
    f.create_dataset("timestamp", data=timestamps)
    f.create_dataset("VOC", data=voc)
    f.flush() # write all this to disk
    f.close() # and close the file


        
        
if __name__=="__main__":
    make_h5()
