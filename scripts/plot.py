import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.fft import rfft, rfftfreq
import seaborn as sns

R1 = '100Kohm'
R2 = '1Mohm'
R3 = '10Mohm'
PATH1 = '/home/y/Documents/nov21/lighton/' + R1
PATH2 = '/home/y/Documents/nov21/lighton/' + R2
PATH3 = '/home/y/Documents/nov21/lighton/' + R3

PATH4 = '/home/y/Documents/nov21/lightoff/' + R1
PATH5 = '/home/y/Documents/nov21/lightoff/' + R2
PATH6 = '/home/y/Documents/nov21/lightoff/' + R3

def load_files(PATH):
    os.chdir(PATH)
    file_names = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".csv"):
                file_names.append(file)

    return file_names

def get_data(file_names):
    """['10hz_260umol_gain1.csv', '10hz_260umol_gain2.csv', '10hz_260umol_gain16.csv',
    '10hz_260umol_gain8.csv', '10hz_260umol_gain4.csv', '10hz_260umol_nogain.csv']"""
    all_data = []
    for f in file_names:
        df = pd.read_csv(f)
        first_column = df.iloc[:, 0]
        data = first_column.iloc[:3001]
        all_data.append(data)

    return all_data

def fourier_(data):
    #import scipy.fftpack
    N = len(data)
    T = 1.0/11.0
    print(N)
    print(type(data))
    yf = rfft(data)
    #xf = np.linspace(0.0,1.0/(2.0*T), int(N/2.0))
    xf = rfftfreq(N,T)
    plt.plot(xf,np.abs(yf))
    #plt.plot(xf,2.0/N* np.abs(yf[:N//2]))
    plt.xlabel('Hertz (Hz)', fontsize=30)
    plt.ylabel('Power (dB)', fontsize=30)
    plt.show()

def distance_from

def plot_box(r1,r2,r3):
    x_ = [0, 3000]
    y_ = [16384, 16384]
    #fig, ax = plt.subplots()

    #plt.xlabel("Sample")
    #plt.ylabel("Bit")

    # plt.boxplot(g0)
    # plt.boxplot(g1)
    # plt.boxplot(g2)
    # plt.boxplot(g4)
    # plt.boxplot(g8)
    # plt.boxplot(g16)
    r1pos = [-0.3,0.7,1.7,2.7,3.7,4.7]
    r2pos = [0,1,2]
    r3pos = [0.3,1.3,2.3]
    labs = ['Raw Signal', 'Gain 1', 'Gain 2','Gain 4', 'Gain 8', 'Gain 16']
    #bplot1 = sns.swarmplot(x='gains',y='bits', data = r1)#,positions = r1pos,patch_artist=True) #,widths = 0.1)
    #bplot2 = sns.swarmplot(x='gains',y='bits',data = r2)#,positions = r2pos,patch_artist=True) #,widths = 0.1)
    #plot3 = sns.swarmplot(x='gains',y='bits',data = r3)#,positions = r3pos,patch_artist=True) #,widths = 0.1)
    #plt.plot(r1['bits'][3], label='r1 Gain4')
    #plt.plot(r1['bits'][1],label='r1 Gain1')
    #plt.plot(r1['bits'][2],label='r1 Gain2')

    ##plt.plot(r1['bits'][4],label='r1 Gain8')

    #plt.plot(r1['bits'][5],label='r1 Gain16')
    #plt.plot(r1['bits'][0],label='r1 No Gain')

    #plt.plot(r2['bits'][0],label='r2 No Gain')
    #plt.plot(r2['bits'][1],label='r2 Gain1')
    #plt.plot(r2['bits'][2],label='r2 Gain2')
    #plt.plot(r2['bits'][3],label='r2 Gain4')
    #plt.plot(r2['bits'][4],label='r2 Gain8')
    #plt.plot(r2['bits'][5],label='r2 Gain16')

    #plt.plot(r3['bits'][0],label='r3 No Gain')

    ##plt.plot(r3['bits'][1],label='r3 Gain1')

    #plt.plot(r3['bits'][2],label='r3 Gain2')
    #plt.plot(r3['bits'][3],label='r3 Gain4')
    #plt.plot(r3['bits'][4],label='r3 Gain8')
    #plt.plot(r3['bits'][5],label='r3 Gain16')
    #plt.plot(x_, y_, 'r', linestyle='dashed', linewidth=2)

    #plt.legend()
    # colors = ['pink', 'lightblue', 'lightgreen']
    # for bplot in (bplot1, bplot2,bplot3):
    #     for patch, color in zip(bplot['boxes'], colors):
    #         patch.set_facecolor(color)


    #plt.xticks([0,1,2,3,4,5],['Raw Signal', 'Gain 1', 'Gain 2','Gain 4', 'Gain 8', 'Gain 16'])
    #plt.show()
    fourier_(r3['bits'][1])


if __name__ == "__main__":

    #######  light on
    r1_100k = load_files(PATH1)
    d1 = get_data(r1_100k)
    print(r1_100k)

    r2_1M = load_files(PATH2)
    d2 = get_data(r2_1M)
    print(r2_1M)

    r3_10M = load_files(PATH3)
    d3 = get_data(r3_10M)
    print(r3_10M)

    ##### Light off
    r1_100k = load_files(PATH4)
    d4 = get_data(r1_100k)
    print(r1_100k)

    r2_1M = load_files(PATH5)
    d5 = get_data(r2_1M)
    print(r2_1M)

    r3_10M = load_files(PATH6)
    d6 = get_data(r3_10M)
    print(r3_10M)

    ### GENERAL
    max_bit = [32768]*3001
    maxd = pd.DataFrame(max_bit)

    d1r1 = [d1[5],d1[0],d1[1],d1[4],d1[3],d1[2]]
    d2r2 = [d2[4],d2[1],d2[0],maxd, maxd, maxd]
    d3r3 = [d3[3],d3[0], d3[1],maxd,maxd,maxd]

    d4r1 = [d4[5],d4[0],d4[1],d4[2],d4[3],d4[4]]
    d5r2 = [d5[3],d5[0],d5[1],d5[2],maxd,maxd]
    d6r3 = [d6[2],d6[0],d6[1],maxd,maxd, maxd]

    # nogain = [d1r1[0],d2r2[0],d3r3[0]]
    # gain1 = [d1r1[1],d2r2[1],d3r3[1]]
    # gain2 = [d1r1[2], d2r2[2], d3r3[2]]
    # gain4 = [d1r1[3], d2r2[3], d3r3[3]]
    # gain8 = [d1r1[4], d2r2[4], d3r3[4]]
    # gain16 = [d1r1[5]]#, d2r2[5], d3r3[5]]
    nogain = np.asarray(['nogain']*3001)
    gain1 = np.asarray(['gain1']*3001)
    gain2 = np.asarray(['gain2']*3001)
    gain4 = np.asarray(['gain4'] * 3001)
    gain8 = np.asarray(['gain8'] * 3001)
    gain16 = np.asarray(['gain16'] * 3001)


    dfr1 = {'bits': [d1[5],d1[0],d1[1],d1[4],d1[3],d1[2]], 'gains': [nogain,gain1,gain2,gain4,gain8,gain16]}
    dfr2 = {'bits': [d2[4],d2[1],d2[0],maxd, maxd, maxd], 'gains': [nogain, gain1, gain2, gain4, gain8, gain16]}
    dfr3 = {'bits': [d3[3],d3[0], d3[1],maxd,maxd,maxd], 'gains': [nogain, gain1, gain2, gain4, gain8, gain16]}
    dfr1=pd.DataFrame(dfr1)
    dfr2=pd.DataFrame(dfr2)
    dfr3=pd.DataFrame(dfr3)


    print(dfr3['bits'])
    plot_box(dfr1,dfr2,dfr3)
