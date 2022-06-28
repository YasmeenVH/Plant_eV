import pandas as pd
import numpy as np
import os
import config
import h5py

## results for true results for anova, in hdf5
OFFICIAL_PATH = config.path_official_results # in hdf5
BLUE_TRUE = config.official_blue # an array of 3 seperate plants
RED_TRUE = config.official_red
AMBER_TRUE = config.official_amber

## dc bias results
DC_BIAS = config.dcbias_results
BLUE_DC = config.dcbias_blue    # what gain is this
AMBER_DC = config.dcbias_amber
RED_DC = config.dcbias_red
R1 = config.res1 # 100Kohm
R2 = config.res2 # 1Mohm
R3 = config.res3 # 10Mohm

GAIN = [0,1,2,4,8,16]
##file_type stuff csv, hdf5
FILETYPE = config.file_type

N_POINTS = 3000
class DataLoader(object):
    def __init__(self, path=DC_BIAS,file_type=FILETYPE, blue=BLUE_DC,red = RED_DC, amber= AMBER_DC, res = True, gain= GAIN, n_points = N_POINTS):
        self.path = path
        self.file_type = file_type
        self.blue = blue
        self.red = red
        self.amber = amber
        self.res = res
        if self.res == True:
            self.r1 = R1
            self.r2 = R2
            self.r3 = R3
        self.gain = gain
        self.n_points = n_points


    def read_files(self,folder,n_points):

        # set path for files
        source_folder = os.chdir(self.path +'/'+ folder)

        # create empty dictionaries to grab files
        all_data_hdf5 = []
        all_data_csv = {}
        length_hdf5 = []

        # List file in directory and based off extension extract
        if self.file_type == "csv":
            for file in os.listdir(source_folder):
                if file.endswith(".csv"):    #sanity check to only take csv in folder
                    df = pd.read_csv(file)
                    file = file[:-4]  # renamaining for key to work by gain
                    first_column = df.iloc[:, 0]
                    data = first_column.iloc[:n_points]
                    all_data_csv[file] = data

            return all_data_csv

        if self.file_type == "hdf5":

            for file in os.listdir(source_folder):

                if file.endswith(".hdf5"):    #sanity check to only take hdf5 in folder
                    data = h5py.File(file, 'r')
                    dset = data['ev_data']
                    flat_list = [item for sublist in dset for item in sublist]
                    length_hdf5.append(len(flat_list))
                    all_data_hdf5.append(flat_list)

            min_val = min(length_hdf5)
            print(len(all_data_hdf5))
            master_hdf5 = []
            for x in all_data_hdf5:
                master_hdf5.append(x[:min_val])

            return master_hdf5

if __name__ == "__main__":
    Loader = DataLoader(path=DC_BIAS,file_type=FILETYPE[0], blue = BLUE_DC, red = RED_DC, amber=AMBER_DC,res= True)

    bluedc_file_names = Loader.read_files(Loader.blue+ '/'+ Loader.r1)
    print(bluedc_file_names)