from analysis.dataloader import DataLoader
import config
from analysis.stats import find_min_trials, sum_trials, anova_one_color, tukey_hsd, length_adjust, find_min_reading, sum_readings, anova_single_plant, mean_reading, stationarity
from scripts.plot import plot_box_color, plot_fourier
from analysis.signal_processing import volts, butter_filter, fast_fourier
from scripts.plot import plot_trials_box, std_mean_err
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os
from analysis.fourier import lowpass, moving_average


def load_materials():
    # First trial for wg, al, alg

    Loader_HDF5_1 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    #print(Loader_HDF5_1.wg[0])
    wg_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.wg[0], Loader_HDF5_1.n_points)
    al_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.al[0], Loader_HDF5_1.n_points)
    alg_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.alg[0], Loader_HDF5_1.n_points)
    #print()
    # Second trial for wg, al, alg

    Loader_HDF5_2 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    wg_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.wg[1], Loader_HDF5_2.n_points)
    al_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.al[1], Loader_HDF5_2.n_points)
    alg_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.alg[1], Loader_HDF5_2.n_points)

    # Third trial for wg, al, alg

    Loader_HDF5_3 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    wg_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.wg[2], Loader_HDF5_3.n_points)
    # al_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.al, Loader_HDF5_2.n_points)
    alg_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.alg[2], Loader_HDF5_3.n_points)

    return wg_official_p1,wg_official_p2,wg_official_p3,al_official_p1,al_official_p2,alg_official_p1,alg_official_p2,alg_official_p3

def directions():
    Loader_HDF5_1 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    #print(Loader_HDF5_1.wg[0])
    notinverse = Loader_HDF5_1.read_files(Loader_HDF5_1.notinverse, Loader_HDF5_1.n_points)
    inverse = Loader_HDF5_1.read_files(Loader_HDF5_1.inverse, Loader_HDF5_1.n_points)

    return notinverse, inverse
def volts_(p1,p2,p3, material):

    if material == "wg":
        pv1, _ = volts(8,p1)
        pv2, _ = volts(8,p2)
        pv3, _ = volts(8,p3)
        return pv1, pv2, pv3

    if material == "al":
        pv1, _ = volts(8,p1)
        pv2, _ = volts(8,p2)
        #pv3, _ = volts(8,p3)
        return pv1, pv2

    if material == "alg":
        pv1, _ = volts(8,p1)
        pv2, _ = volts(8,p2)
        pv3, _ = volts(8,p3)
        return pv1, pv2, pv3
def volts_direction(d1,d2):


    pv1, _ = volts(8,d1)
    pv2, _ = volts(8,d2)

    return pv1, pv2



def find_length(trials):
    i=0
    for t in trials:
        for seq in t:
            i+=1
            #print(i)
            smallest = len(seq)
            if i == 1:
                smol = smallest
            if smol > smallest:
                smol = smallest


        return smol
def same_length(trials, minimum):
    all_trials = []
    for t in trials:
        tt = [x[:minimum] for x in t]
        all_trials.append(tt)
    return all_trials

def plot_mean_material(trials, pltlabels, title):

    print(len(trials))
    all_xs = []
    for x in range(len(trials)):
        x_flat = [item for sublist in trials[x] for item in sublist]
        mean = np.mean(trials[x])
        std = np.std(trials[x])
        top_error = np.add(mean,std)
        bottom_error = np.subtract(mean,std)
        print("Mean:", mean, "std:", std)
        print(len(x_flat), "what is thi slen")
        all_xs.append(x_flat)
    plt.boxplot(all_xs, labels=pltlabels)
    plt.title(title + " probe")
    plt.ylabel("Volts (V)")

    #plt.show()
    flatxs = [item for sublist in all_xs for item in sublist]
    return all_xs, flatxs

def histograms(material,title_material):
    plt.hist(material, color='blue', edgecolor='black',bins=40)
    plt.title("distribution of data for " + title_material)
    plt.xlabel("Volts(V)")
    plt.ylabel("samples")
    plt.show()

def amplitude(material, title_material):

    for x in range(len(material)):
        m = min(material[x])
        mm = max(material[x])
        amp = mm-np.abs(m)

        print(title_material[x], " min:",m, " max:", mm, " amplitude:", amp)
def makefourier(data):
    xs = []
    ys = []

    for x in data:
        xf, yf = fast_fourier(len(x),10,x)
        xs.append(xf)
        ys.append(yf)
    return xs, ys

def get_data():
    ##load material
    wg1, wg2, wg3, al1, al2, alg1, alg2, alg3 = load_materials()

    volt1_wg, volt2_wg, volt3_wg = volts_(wg1, wg2, wg3, "wg")
    volt1_al, volt2_al = volts_(al1, al2, wg3, "al")
    volt1_alg, volt2_alg, volt3_alg = volts_(alg1, alg2, alg3, "alg")

    ## all trials for materials
    trialswg = [volt1_wg, volt2_wg, volt3_wg]
    trialsal = [volt1_al, volt2_al]
    trialsalg = [volt1_alg, volt2_alg, volt3_alg]

    ## WG
    min_wg = find_length(trialswg)
    wg_volts = same_length(trialswg, min_wg)
    print(len(wg_volts), 'len of wg')
    alltrials = ['plant 1', 'plant 2', 'plant 3']
    print("this is wg")
    wg_lists, flat_wg = plot_mean_material(wg_volts, alltrials, "Wire and gel")

    ## AL
    min_al = find_length(trialsal)
    al_volts = same_length(trialsal, min_al)
    alltrials = ['plant 1', 'plant 2']  # , 'plant 3']
    print("this is al")
    al_lists, flat_al = plot_mean_material(al_volts, alltrials, "Aluminum ")
    # print(min_al)

    ## AG
    min_alg = find_length(trialsalg)
    alg_volts = same_length(trialsalg, min_alg)
    alltrials = ['plant 1', 'plant 2', 'plant 3']
    print("this is alg")
    alg_lists, flat_alg = plot_mean_material(alg_volts, alltrials, "Aluminum and gel")
    # print(min_alg)
    return flat_wg,wg_lists, flat_al, al_lists, flat_alg, alg_lists

def plotfourier(wg_lists,al_lists,alg_lists):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Fourier transform of materials')
    wgx, wgy = makefourier(wg_lists)
    for x in range(len(wgx)):
        ax1.plot(wgx[x], np.abs(wgy[x]))
    ax1.set_title('fourier of wire gel trials')
    # plt.title("fourier of wire gel trials")
    # ax1.set_xlabel('frequency (Hz)')
    ax1.set_ylabel('Power (dB)')
    # plt.ylabel("Power (dB)")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylim(0,100)
    ax1.set_ylim([0, 100])
    # plt.show()

    wgx, wgy = makefourier(al_lists)
    for x in range(len(wgx)):
        ax2.plot(wgx[x], np.abs(wgy[x]))
    ax2.set_title("fourier of aluminum trials")
    # ax2.set_xlabel('frequency (Hz)')
    ax2.set_ylabel('Power (dB)')
    # plt.ylabel("Power (dB)")
    # plt.xlabel("Frequency (Hz)")
    ax2.set_ylim([0, 200])
    # plt.ylim(0,200)
    # plt.show()

    wgx, wgy = makefourier(alg_lists)
    for x in range(len(wgx)):
        ax3.plot(wgx[x], np.abs(wgy[x]))
    ax3.set_title("fourier of aluminum gel trials")
    ax3.set_xlabel('frequency (Hz)')
    ax3.set_ylabel('Power (dB)')
    # plt.ylabel("Power (dB)")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylim(0,250)
    ax3.set_ylim([0, 250])
    plt.show()


if __name__ == "__main__":

    #flat_wg, wg_lists, flat_al,al_lists, flat_alg, alg_lists= get_data()
    notinverse, inverse = directions()
    volt_good, volt_inverse = volts_direction(notinverse,inverse)
    plt.plot(volt_good[2],label="normal direction")
    plt.plot(volt_inverse[2],label="inverse")
    plt.ylabel("Volts(V)")
    plt.xlabel("Samples")
    plt.legend()
    plt.show()

    flat_normal = [item for sublist in volt_good for item in sublist]
    flat_inverse = [item for sublist in volt_inverse for item in sublist]
    plt.hist(flat_normal, color='blue', edgecolor='black',bins=100, label="normal")
    plt.hist(flat_inverse, color='red', edgecolor='black',bins=100,label="inverse")
    plt.legend()
    plt.xlabel("volts(V)")
    plt.ylabel("samples")
    plt.show()

    plt.hist(flat_normal, color='blue', edgecolor='black',bins=100, label="normal")
    plt.xlabel("volts(V)")
    plt.ylabel("samples")
    plt.legend()
    plt.show()

    plt.hist(flat_inverse, color='red', edgecolor='black',bins=100,label="inverse")

    all_data = [flat_wg, flat_al, flat_alg]
    all_materials = ["wire and gel", "aluminum", "aluminum and gel"]
    plt.boxplot(all_data,labels=all_materials)
    plt.title("Probe material comparison")
    plt.ylabel("Volts(V)")
    plt.show()

    histograms(flat_wg,"wire and gel")
    histograms(flat_al,"aluminum")
    histograms(flat_alg,"aluminum and gel")

    print("WG:",np.mean(flat_wg),np.std(flat_wg))
    print("AL:", np.mean(flat_al), np.std(flat_al))
    print("ALG:", np.mean(flat_alg), np.std(flat_alg))

    amplitude(all_data,all_materials)
    #plot_fourier(wg_lists,al_lists,alg_lists)

