import h5py
import matplotlib.pyplot as plt
from analysis.fourier import fastfourier
import numpy as np

import os
# dat_files = filter(lambda x: x.endswith('.dat'), os.listdir('mydir'))
# dat_files.sort()
# dat_files[0]

PATH = '/home/y/Documents/officialresults/red3'

def read_files(folder):
    # filenames = []
    # dat_files = filter(lambda x: x.endswith('.hdf5'), os.listdir(folder))
    # dat_files.sort()
    # print(dat_files)

    files = []
    for file in os.listdir(folder):
        if file.endswith(".hdf5"):
            files.append(file)
    b = sorted(files)#, reverse=True)

    return b

def fetch_data(filenames):
    master_data = []
    for f in filenames:
        data = h5py.File(PATH+'/'+f,'r')
        dset = data['ev_data']
        master_data.append(dset[()])
        data.close()
    return master_data


if __name__ == "__main__":
    names = read_files(PATH)
    print(len(names),"this is the amount of files created")
    all_data = fetch_data(names)

    print(all_data[0])
    flat_list1 = [item for sublist in all_data for item in sublist]
    flat_list2 = [item for sublist in flat_list1 for item in sublist]
    print(len(flat_list2),"amount of data")
    volts = [x*0.256/32768 for x in flat_list2]
    # plt.plot(flat_list2)
    # plt.xlabel("samples")
    # plt.ylabel("bits")
    # plt.show()
    #
    # plt.plot(volts)
    # plt.xlabel("samples")
    # plt.ylabel("volts")
    # plt.show()

    xp,yp = fastfourier(len(volts),10,volts)
    plt.plot(xp, np.abs(yp))
    plt.xlabel("Hz")
    plt.ylabel("decibels")
    #plt.ylim()
    plt.show()
