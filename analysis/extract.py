import h5py
import numpy as np
import os
import re

PATH = '/data/plantppl/experiment1-preliminary'
VARIABLES = ['CO2', 'VOC', 'ev_data', 'rh', 'temp']

def get_variable(data):
    '''Function that returns one array with all the data from one file '''
    all_var = []
    for i in range(len(hdfid[data])):
        all_var.append(hdfid[data][i])

    all_clean = np.concatenate(all_var).ravel()

    return all_clean

def find_newest():
    r = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.hdf5$')
    latest_file = max(filter(r.search, os.listdir(PATH)))
    
    return latest_file

def open_files():
    os.chdir(PATH)  # change working directory
    files = os.listdir(PATH)
    for f in files:


