#Imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.signal_processing import volts, moving_average
import numpy as np
import h5py

PATH = '/Users/yasmeen/Desktop/sig_results/blueamberblue/plant2'
PATHH = '/Users/yasmeen/Desktop/sig_results/blueamberblue/p1'
A1 = '/Users/yasmeen/Desktop/sig_results/officialresults/amber1'
A2 = '/Users/yasmeen/Desktop/sig_results/officialresults/amber2'
A3 = '/Users/yasmeen/Desktop/sig_results/officialresults/amber3'

R1 = '/Users/yasmeen/Desktop/sig_results/officialresults/red1'
R2 = '/Users/yasmeen/Desktop/sig_results/officialresults/red2'
R3 = '/Users/yasmeen/Desktop/sig_results/officialresults/red3'

B1 = '/Users/yasmeen/Desktop/sig_results/officialresults/blue1'
B2 = '/Users/yasmeen/Desktop/sig_results/officialresults/blue2'
B3 = '/Users/yasmeen/Desktop/sig_results/officialresults/p2blue'

def normalize(data):
    minz = min(data)
    maxz = max(data)
    normed = []
    for x in data:
        x = (x-minz)/(maxz-minz)
        normed.append(x)

    return normed
def read_files(n_points, filter, path, gain):
    # set path for files
    source_folder = os.chdir(path)

    # create empty dictionaries to grab files
    all_data_csv = {}

    # List file in directory and based off extension extract

    for file in os.listdir(source_folder):
        if file.endswith(".csv"):  # sanity check to only take csv in folder
            df = pd.read_csv(file)
            file = file[:-4]  # renamaining for key to work by gain
            first_column = df.iloc[:, 0]
            print("lenght of data:", len(first_column))
            data = first_column.iloc[:n_points]
            data_v, _ = volts(gain,data)
            if filter == None:
                z = normalize(data_v)
                all_data_csv[file] = z
            if filter == 'MA' :
                ma = moving_average(data_v,20)
                all_data_csv[file] = ma

    return all_data_csv

def read_hdf5(filter, path, gain):
    all_data_hdf5 = []
    length_hdf5 = []
    source_folder = os.chdir(path)

    for file in os.listdir(source_folder):
        if file.endswith(".hdf5"):
            data = h5py.File(file, 'r')
            dset = data['ev_data']
            flat_list = [item for sublist in dset for item in sublist]

            volts_data, _ = volts(gain,flat_list)
            if filter == 'MA':
                ma = moving_average(volts_data, 40)
                dd = normalize(volts_data)
                all_data_hdf5.append(dd)
                length_hdf5.append(len(dd))
            if filter == None:
                dd = normalize(volts_data)
                all_data_hdf5.append(dd)
                length_hdf5.append(len(dd))


    cutoff = min(length_hdf5)
    good_length = []
    for x in all_data_hdf5:
        good_length.append(x[:cutoff])

    return good_length

def df_hdf5_multi(p1,p2,p3):

    flat_list1 = [item for sublist in p1 for item in sublist]
    flat_list2 = [item for sublist in p2 for item in sublist]
    flat_list3 = [item for sublist in p3 for item in sublist]
    #print("cehck:", flat_list1)
    sizes = [len(flat_list1),len(flat_list2), len(flat_list3)]
    minima = min(sizes)
    flat_list1 = flat_list1[:minima]
    flat_list2 = flat_list2[:minima]
    flat_list3 = flat_list3[:minima]
    doc = {'plant1':flat_list1,'plant2':flat_list2,'plant3':flat_list3}
    #print(len(all_data_hdf5))
    #print(all_data_hdf5[0])
    #print(all_data_hdf5[1])
    df = pd.DataFrame(doc)
    print(df)
    return df.T

def df_hdf5_color(a1,a2,a3, r1,r2,r3,b1,b2,b3):

    alist1 = [item for sublist in a1 for item in sublist]
    alist2 = [item for sublist in a2 for item in sublist]
    alist3 = [item for sublist in a3 for item in sublist]

    rlist1 = [item for sublist in r1 for item in sublist]
    rlist2 = [item for sublist in r2 for item in sublist]
    rlist3 = [item for sublist in r3 for item in sublist]

    blist1 = [item for sublist in b1 for item in sublist]
    blist2 = [item for sublist in b2 for item in sublist]
    blist3 = [item for sublist in b3 for item in sublist]
    #print("cehck:", flat_list1)
    sizes = [len(alist1),len(alist2), len(alist3), len(rlist1), len(rlist2), len(rlist3),len(blist2), len(blist2), len(blist3)]
    minima = min(sizes)
    alist1 = alist1[:minima]
    alist2 = alist2[:minima]
    alist3 = alist3[:minima]
    rlist1 = rlist1[:minima]
    rlist2 = rlist2[:minima]
    rlist3 = rlist3[:minima]
    blist1 = blist1[:minima]
    blist2 = blist2[:minima]
    blist3 = blist3[:minima]
    doc = {'red1':rlist1,'red2':rlist2,'red3':rlist3,
           'blue1':blist1,'blue2':blist2,'blue3':blist3,'amber1':alist1,'amber2':alist2,'amber3':alist3}
    #print(len(all_data_hdf5))
    #print(all_data_hdf5[0])
    #print(all_data_hdf5[1])
    df = pd.DataFrame(doc)
    print(df)
    return df.T


def df_hdf5(good_length):

    doc = {'run1': good_length[0],'run2':good_length[1], 'run3':good_length[2], 'run4': good_length[3], 'run5': good_length[4]}
    df = pd.DataFrame(doc)
    print(df)

    return df.T

def make_multidf(p1,p2):
    #print(p1.values())
    flat_list1 = [item for sublist in p1.values() for item in sublist]
    flat_list2 = [item for sublist in p2.values() for item in sublist]
    sizes = [len(flat_list1),len(flat_list2)]
    minima = min(sizes)
    #print(flat_list1)
    flat_list1 = flat_list1[:minima]
    flat_list2 = flat_list2[:minima]

    doc = {'plant1':flat_list1,'plant2':flat_list2}
    df = pd.DataFrame(doc)
    print(df)
    return df.T



def make_dataframe(data, windowsize):
    df = pd.DataFrame(data)
    cols = ['run1','run2','run3','run4','run5','run6','run7','run8','run9','run10']

    #print(df)
    df= df[cols]
    #print(df)
    df.rename(columns={'run1': '0-5','run2':'5-10','run3':'10-15', 'run4':'15-20', 'run5':'20-25','run6': '25-30',
                       'run7':'30-35', 'run8':'35-40','run9':'40-45', 'run10':'45-50'}, inplace=True)
    #print(df)

    transposed = df.T
    #print(transposed)
    return transposed

def heatmap(data):
    sns.heatmap(data)
    #plt.ylabel("Minutes")
    plt.xlabel("Readings")
    plt.show()

if __name__ == "__main__":
    # master_data = read_files(3000, None)
    # data = make_dataframe(master_data,10)
    # heatmap(data)
    #
    master_data1 = read_files(3000, 'MA', PATHH, 8)
    master_data2 = read_files(3000, 'MA', PATH,8)
    data = make_multidf(master_data1,master_data2)
    heatmap(data)
    data1 = make_dataframe(master_data1,10)
    data2 = make_dataframe(master_data2,10)
    heatmap(data1)
    heatmap(data2)
    # df1 = read_hdf5('MA', PATH1)
    # d_1 = df_hdf5(df1)
    # heatmap(d_1)
    #
    #
    #
    # df2 = read_hdf5('MA', PATH2)
    # heatmap(df2)
    # df3 = read_hdf5('MA', PATH3)
    # d_all = df_hdf5_multi(df1,df2,df3)
    # heatmap(d_all)
    # heatmap(df3)

    # a1 = read_hdf5(None, A1, 8)
    # a1heat = df_hdf5(a1)
    # heatmap(a1heat)
    # a2 = read_hdf5(None, A2, 8)
    # a2heat = df_hdf5(a2)
    # heatmap(a2heat)
    # a3 = read_hdf5(None, A3,8)
    # a3heat = df_hdf5(a3)
    # heatmap(a3heat)
    # d_alla = df_hdf5_multi(a1,a2,a3)
    # heatmap(d_alla)

    # r1 = read_hdf5(None, R1,8)
    # r2 = read_hdf5(None, R2,8)
    # r3 = read_hdf5(None, R3,8)
    # d_allz = df_hdf5_multi(r1, r2, r3)
    # heatmap(d_allz)
    # b1 = read_hdf5(None, B1,8)
    # b2 = read_hdf5(None, B2,8)
    # b3 = read_hdf5(None, B3,8)
    # d_alls = df_hdf5_multi(b1, b2,b3)
    # heatmap(d_alls)
    #
    # d_all = df_hdf5_color(a1, a2, a3, r1,r2,r3,b1,b2,b3)
    # heatmap(d_all)