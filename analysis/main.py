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
from statsmodels.tsa.stattools import adfuller

def blanks(path):
    source_folder = os.chdir(path)
    all_data_csv = {}

    # List file in directory and based off extension extract

    for file in os.listdir(source_folder):
        if file.endswith(".csv"):  # sanity check to only take csv in folder
            df = pd.read_csv(file)
            file = file[:-4]  # renamaining for key to work by gain
            first_column = df.iloc[:, 0]
            data = first_column.iloc[:3000]
            all_data_csv[file] = data

    return all_data_csv

def dc_bias_analysis():
    ## LOADING ALL CSV FILE FOR DC BIASING
    Loader_DC = DataLoader(path=config.dcbias_results,file_type=config.file_type[0], blue = config.dcbias_blue, red = config.dcbias_red, amber= config.dcbias_amber, res= True, n_points = config.n_points, material = False)

    bluedc_r1 = Loader_DC.read_files(Loader_DC.blue + '/'+ Loader_DC.r1, Loader_DC.n_points)
    bluedc_r2 = Loader_DC.read_files(Loader_DC.blue + '/' + Loader_DC.r2, Loader_DC.n_points)
    bluedc_r3 = Loader_DC.read_files(Loader_DC.blue + '/' + Loader_DC.r3, Loader_DC.n_points)

    reddc_r1 = Loader_DC.read_files(Loader_DC.red + '/'+ Loader_DC.r1, Loader_DC.n_points)
    reddc_r2 = Loader_DC.read_files(Loader_DC.red + '/' + Loader_DC.r2, Loader_DC.n_points)
    reddc_r3 = Loader_DC.read_files(Loader_DC.red + '/' + Loader_DC.r3, Loader_DC.n_points)

    amberdc_r1 = Loader_DC.read_files(Loader_DC.amber + '/'+ Loader_DC.r1, Loader_DC.n_points)
    amberdc_r2 = Loader_DC.read_files(Loader_DC.amber + '/' + Loader_DC.r2, Loader_DC.n_points)
    amberdc_r3 = Loader_DC.read_files(Loader_DC.amber + '/' + Loader_DC.r3, Loader_DC.n_points)
    #print(bluedc_file_names['gain0'])
    return bluedc_r1,bluedc_r2,bluedc_r3,reddc_r1,reddc_r2,reddc_r3,amberdc_r1,amberdc_r2,amberdc_r3

def load_colors():
    # First trial for blue, red, amber

    Loader_HDF5_1 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=False)
    blue_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.blue, Loader_HDF5_1.n_points)
    red_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.red, Loader_HDF5_1.n_points)
    amber_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.amber, Loader_HDF5_1.n_points)

    # Second trial for blue, red, amber
    Loader_HDF5_2 = DataLoader(path=config.path_official_results, file_type=config.file_type[1],
                             blue=config.official_blue[1], red=config.official_red[1], amber=config.official_amber[1],
                             res=False, n_points=config.n_points, material = False)
    blue_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.blue, Loader_HDF5_1.n_points)
    red_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.red, Loader_HDF5_1.n_points)
    amber_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.amber, Loader_HDF5_1.n_points)

    # Third trial for blue, red, amber
    Loader_HDF5_3 = DataLoader(path=config.path_official_results, file_type=config.file_type[1],
                             blue=config.official_blue[2], red=config.official_red[2], amber=config.official_amber[2],
                             res=False, n_points=config.n_points, material = False)
    blue_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.blue, Loader_HDF5_1.n_points)
    red_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.red, Loader_HDF5_1.n_points)
    amber_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.amber, Loader_HDF5_1.n_points)

    return blue_official_p1,blue_official_p2,blue_official_p3,red_official_p1,red_official_p2,red_official_p3,amber_official_p1,amber_official_p2,amber_official_p3

def load_materials():
    # First trial for wg, al, alg

    Loader_HDF5_1 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    wg_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.wg, Loader_HDF5_1.n_points)
    al_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.al, Loader_HDF5_1.n_points)
    alg_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.alg, Loader_HDF5_1.n_points)

    # Second trial for wg, al, alg

    Loader_HDF5_2 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    wg_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.wg, Loader_HDF5_2.n_points)
    al_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.al, Loader_HDF5_2.n_points)
    alg_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.alg, Loader_HDF5_2.n_points)

    # Third trial for wg, al, alg

    Loader_HDF5_3 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points, material=True)
    wg_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.wg, Loader_HDF5_3.n_points)
    # al_official_p2 = Loader_HDF5_1.read_files(Loader_HDF5_2.al, Loader_HDF5_2.n_points)
    alg_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.alg, Loader_HDF5_3.n_points)

    return wg_official_p1,wg_official_p2,wg_official_p3,al_official_p1,al_official_p2,alg_official_p1,alg_official_p2,alg_official_p3

def plots_asabe():
    b1,b2,b3,r1,r2,r3,a1,a2,a3 = load_colors()


def signal_type(plant):
    return stationarity(plant)
def volts_(p1,p2,p3, color):

    if color == "red":
        pv1, _ = volts(8,p1)
        pv2, _ = volts(16,p2)
        pv3, _ = volts(16,p3)

    if color == "blue":
        pv1, _ = volts(8,p1)
        pv2, _ = volts(8,p2)
        pv3, _ = volts(8,p3)

    if color == "amber":
        pv1, _ = volts(4,p1)
        pv2, _ = volts(4,p2)
        pv3, _ = volts(4,p3)



# def clean_sig(plant):
#     for x in plant:


def define_box_properties(plot_name, color_code, label):
    for k, v in plot_name.items():
        plt.setp(plot_name.get(k), color=color_code)

    # use plot function to draw a small line to name the legend.
    plt.plot([], c=color_code, label=label)
    plt.legend()


def analysis_single_trial(t1,t2,t3, color):
    t1_min = find_min_reading(t1)
    t2_min = find_min_reading(t2)
    t3_min = find_min_reading(t3)

    t1_final = sum_readings(t1,t1_min)
    t2_final = sum_readings(t2,t2_min)
    t3_final = sum_readings(t3,t3_min)
    #print(len(t1_final), "check that we still have 5 lists")
    #print(t1_final)
    ticks = ['r1', 'r2', 'r3', 'r4', 'r5']
    if color == "red":
        t1_f, center1 = volts(8,t1_final)
        t2_f, center2 = volts(16,t2_final)
        t3_f, center3 = volts(16,t3_final)


        # Python program to illustrate
        # boxplot using inbuilt data-set
        # given in seaborn
        plant_1 = plt.boxplot(t1_f,
                                       positions=np.array(
                                           np.arange(len(t1_f))) * 2.0 - 0.5,
                                       widths=0.3)

        plant_2 = plt.boxplot(t2_f,
                                       positions=np.array(
                                           np.arange(len(t2_f))) * 2.0,
                                       widths=0.3)
        plant_3 = plt.boxplot(t3_f,
                                       positions=np.array(
                                           np.arange(len(t3_f))) * 2.0 + 0.5,
                                       widths=0.3)

        define_box_properties(plant_1, 'red', 'plant1')
        define_box_properties(plant_2, 'maroon', 'plant2')
        define_box_properties(plant_3, 'firebrick', 'plant3')
        # set the x label values
        plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)

        # set the limit for x axis
        plt.xlim(-2, len(ticks) * 2)

        # set the limit for y axis
        #plt.ylim(0, 50)

        # set the title
        plt.title('Repeated readings per plant')
        # sns.boxplot(data=t1_f,color="red")
        # sns.boxplot(data=t2_f, color = 'maroon')
        # sns.boxplot(data=t3_f, color='firebrick')
        plt.xlabel('Repeated Readings')
        plt.ylabel('Volts (V)')
        plt.show()
        c='red'

    if color == "blue":
        t1_f, center1 = volts(8,t1_final)
        t2_f, center2 = volts(8,t2_final)
        t3_f, center3 = volts(8,t3_final)
        plant_1 = plt.boxplot(t1_f,
                              positions=np.array(
                                  np.arange(len(t1_f))) * 2.0 - 0.5,
                              widths=0.3)

        plant_2 = plt.boxplot(t2_f,
                              positions=np.array(
                                  np.arange(len(t2_f))) * 2.0,
                              widths=0.3)
        plant_3 = plt.boxplot(t3_f,
                              positions=np.array(
                                  np.arange(len(t3_f))) * 2.0 + 0.5,
                              widths=0.3)

        define_box_properties(plant_1, 'lightsteelblue', 'plant1')
        define_box_properties(plant_2, 'blue', 'plant2')
        define_box_properties(plant_3, 'midnightblue', 'plant3')
        # set the x label values
        plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)

        # set the limit for x axis
        plt.xlim(-2, len(ticks) * 2)

        # set the limit for y axis
        # plt.ylim(0, 50)

        # set the title
        plt.title('Repeated readings per plant')
        plt.xlabel('Repeated Readings')
        plt.ylabel('Volts (V)')
        # sns.boxplot(data=t1_f,color="red")
        # sns.boxplot(data=t2_f, color = 'maroon')
        # sns.boxplot(data=t3_f, color='firebrick')
        plt.show()
        c = 'blue'
    if color == "amber":
        t1_f, center1 = volts(4,t1_final)
        t2_f, center2 = volts(4,t2_final)
        t3_f, center3 = volts(4,t3_final)

        plant_1 = plt.boxplot(t1_f,
                              positions=np.array(
                                  np.arange(len(t1_f))) * 2.0 - 0.5,
                              widths=0.3)

        plant_2 = plt.boxplot(t2_f,
                              positions=np.array(
                                  np.arange(len(t2_f))) * 2.0,
                              widths=0.3)
        plant_3 = plt.boxplot(t3_f,
                              positions=np.array(
                                  np.arange(len(t3_f))) * 2.0 + 0.5,
                              widths=0.3)

        define_box_properties(plant_1, 'yellow', 'plant1')
        define_box_properties(plant_2, 'orange', 'plant2')
        define_box_properties(plant_3, 'chocolate', 'plant3')
        # set the x label values
        plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)

        # set the limit for x axis
        plt.xlim(-2, len(ticks) * 2)

        # set the limit for y axis
        # plt.ylim(0, 50)

        # set the title
        plt.xlabel('Repeated Readings')
        plt.ylabel('Volts (V)')
        plt.title('Repeated readings per plant')
        # sns.boxplot(data=t1_f,color="red")
        # sns.boxplot(data=t2_f, color = 'maroon')
        # sns.boxplot(data=t3_f, color='firebrick')
        plt.show()
        c='gold'
    #positions = np.array(xrange(len(data_a))) * 2.0 - 0.4, sym = '', widths = 0.6
    # plt.boxplot(t1_f, positions=np.array(range(len(t1_f)))*2.0-0.4, sym='', widths=0.6)
    # plt.boxplot(t2_f,positions=np.array(range(len(t2_f)))*2.0+0.4, sym='', widths=0.6)
    # plt.boxplot(t3_f,positions=np.array(range(len(t3_f)) )* 2.0 + 0.8, sym = '', widths = 0.6)
    std_1 = []
    std_2 = []
    std_3 = []
    for x in t1_f:
        std_1.append(np.std(x))
    for x in t2_f:
        std_2.append(np.std(x))
    for x in t3_f:
        std_3.append(np.std(x))
    print(std_1, "std for plant 1")
    print(std_2, "std for plant 2")
    print(std_3, "std for plant 3")
    m1 = mean_reading(t1_f)
    m2 = mean_reading(t2_f)
    m3 = mean_reading(t3_f)

    # plt.plot(std_1)
    # plt.plot(std_2)
    # plt.plot(std_3)
    plt.show()
    #plt.boxplot
    #plt.show()

    p1 = anova_single_plant(t1_f)
    p2 = anova_single_plant(t2_f)
    p3 = anova_single_plant(t3_f)

    t1_flat = [item for sublist in t1_f for item in sublist]
    t2_flat = [item for sublist in t2_f for item in sublist]
    t3_flat = [item for sublist in t3_f for item in sublist]
    t1_flat_std = np.std(t1_flat)
    t2_flat_std = np.std(t2_flat)
    t3_flat_std = np.std(t3_flat)
    all_flat = [t1_flat,t2_flat,t3_flat]
    plt.boxplot(all_flat)
    plt.title("Reproducibility"+" "+c)
    plt.xlabel("plants")
    plt.ylabel("volts (v)")
    plt.show()
    print('std for p1, p2, p3:',t1_flat_std,t2_flat_std,t3_flat_std)

    return p1, p2, p3
def anova_color_compare():
    pass
def mean_anova(trial):
    means = []
    for x in trial:
        means.append(np.mean(x))
    return means
def length_fix_sumtrials(b1,b2,b3,r1,r2,r3,a1,a2,a3):
    ## Processing to find the length that will suite all colors and trials
    blue_min = find_min_trials(b1,b2,b3)
    red_min = find_min_trials(r1,r2,r3)
    amber_min = find_min_trials(a1,a2,a3)

    min_all_colors = min(blue_min,red_min,amber_min)

    ## Adjusting length
    b1_, b2_, b3_ = length_adjust(b1,b2,b3,min_all_colors)
    r1_, r2_, r3_ = length_adjust(r1,r2,r3,min_all_colors)
    a1_, a2_, a3_ = length_adjust(a1,a2,a3,min_all_colors)
    print("b1_",len(b1_))

    b1v, _ = volts(8,b1_)
    b2v, _ = volts(8,b2_)
    b3v, _ = volts(8, b3_)
    b1vmean = mean_anova(b1v)
    b2vmean = mean_anova(b2v)
    b3vmean = mean_anova(b3v)
    


    #print('BITS BLUE',b1_)
    #print("VOLTS BLUE", b1v)
    ## Summing trials
    all_blue = sum_trials(b1_,b2_,b3_)
    all_red = sum_trials(r1_,r2_,r3_)
    all_amber = sum_trials(a1_,a2_,a3_)
    print(len(all_blue), "what is len all trials")
    #print("allblue",all_blue)

    ## Make into volts
    amber_v , amber_center_line = volts(4, all_amber)
    blue_v, blue_center_line = volts(8,all_blue)
    red_v_p1, red_center_p1 = volts(8,r1_)
    red_v_p2, red_center_p2 = volts(16,r2_)
    red_v_p3, red_center_p3 = volts(16, r3_)

    all_red_v = sum_trials(red_v_p1,red_v_p2,red_v_p3)#, min_all_colors)

    ## Filtering
    #blue_filter = butter_filter(blue_v,10,2.2,3.2,10).tolist()
    #red_filter = butter_filter(all_red_v,10,2.2,3.2,10).tolist()
    #amber_filter = butter_filter(amber_v,10,2.2,3.2,10).tolist()
    #print("data points after fitlering length:",type(blue_filter),len(red_filter),len(amber_filter))

    #plot_box_color(all_blue, all_red, all_amber)
    #plot_box_color(blue_v, all_red_v, amber_v)
    #plot_box_color(blue_filter,red_filter,amber_filter)

    print("all length of all trials should be the same in bits:", type(all_blue),len(all_red),len(all_amber))
    print("all length of all trials should be the same in volts:", len(blue_v), len(all_red_v), len(amber_v))
    ## Perform Anova
    anova_results = anova_one(all_blue,all_red,all_amber)
    print("anova results in bits:", anova_results)

    anova_volts = anova_one(blue_v,all_red_v,amber_v)
    print("anova results in volts:", anova_volts)

    anova_filter = anova_one(blue_filter,red_filter,amber_filter)
    print("anova results for filtered :", anova_filter)
    ## Perform Tukey
    #all_data = all_blue+all_red+all_amber
    all_data_volts = blue_v + all_red_v + amber_v
    all_data_filter = blue_filter + red_filter + amber_filter
    print(len(all_data_filter))
    print("data length before tukey",len(all_data_filter),len(all_data_volts))
    tukey = tukey_hsd(all_data_volts,len(all_blue))
    print("tukey pairwise comparison_volts:", tukey)

    tukey_filt = tukey_hsd(all_data_filter, len(blue_filter))
    print("tukey pairwise comparison_filter:", tukey_filt)
    #plot_box_color(all_blue,all_red,all_amber)
def mean_of_trial(trial):
    trial_mean = []

    for x in trial:
        trial_mean.append(np.mean(x))
    return trial_mean
def makefourier(data):
    xs = []
    ys = []

    for x in data:
        xf, yf = fast_fourier(len(x),10,x)
        xs.append(xf)
        ys.append(yf)
    return xs, ys
def main_materials(analysis):
    wg1,wg2,wg3,al1,al2,alg1,alg2,alg3 = load_materials()

    voltswg1, _ = volts(4,wg1)
    voltswg2, _ = volts(4, wg2)
    voltswg3, _ = volts(4, wg3)

    voltsal1, _ = volts(4, al1)
    voltsal2, _ = volts(4, al2)

    voltsalg1, _ = volts(4, alg1)
    voltsalg2, _ = volts(4, alg2)
    voltsalg3, _ = volts(4, alg3)

    if analysis == 'filtered':

        #len_voltswg1 = [len(x) for x in voltswg1]
        #len_voltswg2 = [len(x) for x in voltswg2]
        #len_voltswg3 = [len(x) for x in voltswg3]
        len_r1 = [len(x) for x in r1v]
        len_r2 = [len(x) for x in r2v]
        len_r3 = [len(x) for x in r3v]
        len_a1 = [len(x) for x in a1v]
        len_a2 = [len(x) for x in a2v]
        len_a3 = [len(x) for x in a3v]

        mins = [min(len_b1),min(len_b2),min(len_b3),min(len_r1),min(len_r2),min(len_r3),min(len_a1),min(len_a2),min(len_a3)]
        themin= min(mins)
        print(themin)

        bb1 = [x[:themin] for x in b1v]
        bb2 = [x[:themin] for x in b2v]
        bb3 = [x[:themin] for x in b3v]

        rr1 = [x[:themin] for x in r1v]
        rr2 = [x[:themin] for x in r2v]
        rr3 = [x[:themin] for x in r3v]

        aa1 = [x[:themin] for x in a1v]
        aa2 = [x[:themin] for x in a2v]
        aa3 = [x[:themin] for x in a3v]

        reds = rr1 + rr2 + rr3
        blues = bb1 + bb2+bb3
        ambers = aa1 + aa2+aa3
        redmean = []
        bluemean = []
        ambermean = []
        for x in reds:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            redmean.append(m)
        for x in blues:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            bluemean.append(m)
        for x in ambers:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            ambermean.append(m)
        print("redmeans:",redmean)
        print("red min:", min(redmean),"red max:", max(redmean))
        #redmean = [x for x in redmean if x < 0.2]
        print("bluemeans:", bluemean)
        print("blue min:", min(bluemean), "blue max:", max(bluemean))
        bluemean = [x for x in bluemean if x <0.2]
        print(len(bluemean))
        print("ambermeans:", ambermean)
        print("amber min:", min(ambermean), "amber max:", max(ambermean))

        results = anova_one_color(bluemean,redmean,ambermean)
        print(results)
        flat_red = [item for sublist in rr3 for item in sublist]
        flat_blue = [item for sublist in bb3 for item in sublist]
        flat_amber = [item for sublist in aa3 for item in sublist]
        #data = [flat_red, flat_blue, flat_amber]
        data = [redmean, bluemean,ambermean]
        bplot = plt.boxplot(data,patch_artist=True)
        plt.xticks([1, 2, 3], ['red', 'blue', 'amber'])
        colors = ['red', 'blue', 'orange']
        #
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
        plt.xlabel("Wavelength", fontsize=20)
        plt.ylabel("Volts (V)", fontsize = 20)
        #plt.legend()
        plt.show()


        clean_sig = moving_average(lowpass(rr1[0]), 5)
        clean_red2 = moving_average(lowpass(rr1[1]), 5)
        clean_red3 = moving_average(lowpass(rr1[2]), 5)
        clean_blue1 = moving_average(lowpass(bb1[0]), 5)
        clean_blue2 = moving_average(lowpass(bb1[1]), 5)
        clean_blue3 = moving_average(lowpass(bb1[2]), 5)
        clean_a1 = moving_average(lowpass(aa1[0]), 5)
        clean_a2 = moving_average(lowpass(aa1[1]), 5)
        clean_a3 = moving_average(lowpass(aa1[2]), 5)

        x = np.linspace(0, 300, num=len(clean_sig))
        xx = np.linspace(0,300, num=len(rr1[0]))
def main(analysis):
    #color_analysis()
    b1,b2,b3,r1,r2,r3,a1,a2,a3 = load_colors()
    print(len(b1), "what is len of b1")
    print(len(r1), "what is len of r1")
    #b1m = mean_of_trial(b1)
    #b2m = mean_of_trial(b2)
    #b3m = mean_of_trial(b3)
    volts_blue = []
    print(type(b1[0]))
    if analysis == "volts":
        b1v, _ = volts(8,b1)
        b2v,_ = volts(8,b2)
        b3v,_ = volts(8,b3)

        r1v, _ = volts(8, r1)
        r2v, _ = volts(16, r2)
        r3v, _ = volts(16, r3)

        a1v, _ = volts(4, a1)
        a2v, _ = volts(4, a2)
        a3v, _ = volts(4, a3)

        return b1v,b2v,b3v,r1v,r2v,r3v,a1v,a2v,a3v

    if analysis == 'raw':
        b1v, _ = volts(8,b1)
        b2v,_ = volts(8,b2)
        b3v,_ = volts(8,b3)

        r1v, _ = volts(8, r1)
        r2v, _ = volts(16, r2)
        r3v, _ = volts(16, r3)

        a1v, _ = volts(8, a1)
        a2v, _ = volts(8, a2)
        a3v, _ = volts(8, a3)

        plt.plot(b1v[0], label='blue1', color="blue")
        # plt.plot(b1v[1], label= 'blue2')
        # plt.plot(b1v[2], label = 'blue3')
        # plt.plot(b1v[3], label = 'blue4')
        # plt.plot(b1v[4], label = 'blue5')

        plt.plot(r1v[0], label='red1', color="red")
        # plt.plot(r1v[1], label= 'red2')
        # plt.plot(r1v[2], label = 'red3')
        # plt.plot(r1v[3], label = 'red4')
        # plt.plot(r1v[4], label = 'red5')

        plt.plot(a1v[0], label='amber1', color="orange")
        plt.plot(a1v[1], label= 'amber2', color ='orange')
        plt.plot(a1v[2], label = 'amber3',color ='orange')
        plt.plot(a1v[3], label = 'amber4',color ='orange')
        plt.plot(a1v[4], label = 'amber5',color ='orange')

        plt.legend()
        plt.show()
    if analysis == 'filtered':
        b1v, _ = volts(8,b1)
        b2v,_ = volts(8,b2)
        b3v,_ = volts(8,b3)

        r1v, _ = volts(8, r1)
        r2v, _ = volts(8, r2)
        r3v, _ = volts(8, r3)

        a1v, _ = volts(8, a1)
        a2v, _ = volts(8, a2)
        a3v, _ = volts(8, a3)

        len_b1 = [len(x) for x in b1v]
        len_b2 = [len(x) for x in b2v]
        len_b3 = [len(x) for x in b3v]
        len_r1 = [len(x) for x in r1v]
        len_r2 = [len(x) for x in r2v]
        len_r3 = [len(x) for x in r3v]
        len_a1 = [len(x) for x in a1v]
        len_a2 = [len(x) for x in a2v]
        len_a3 = [len(x) for x in a3v]

        mins = [min(len_b1),min(len_b2),min(len_b3),min(len_r1),min(len_r2),min(len_r3),min(len_a1),min(len_a2),min(len_a3)]
        themin= min(mins)
        print(themin)

        bb1 = [x[:themin] for x in b1v]
        bb2 = [x[:themin] for x in b2v]
        bb3 = [x[:themin] for x in b3v]

        rr1 = [x[:themin] for x in r1v]
        rr2 = [x[:themin] for x in r2v]
        rr3 = [x[:themin] for x in r3v]

        aa1 = [x[:themin] for x in a1v]
        aa2 = [x[:themin] for x in a2v]
        aa3 = [x[:themin] for x in a3v]

        reds = rr1 + rr2 + rr3
        print(len(rr1), len(reds), "what are dimensions")
        blues = bb1 + bb2+bb3
        ambers = aa1 + aa2+aa3
        flat_reds = [item for sublist in reds for item in sublist]
        flat_blues = [item for sublist in blues for item in sublist]
        flat_ambers = [item for sublist in ambers for item in sublist]


        plt.hist(flat_blues, color='blue', edgecolor='black',
                 bins=100)
        # plt.title("distribution of data for blue")
        # plt.xlabel("Volts(V)")
        # plt.ylabel("samples")
        #plt.show()

        plt.hist(flat_reds, color='red', edgecolor='black',
                 bins=100)
        # plt.title("distribution of data for red")
        # plt.xlabel("Volts(V)")
        # plt.ylabel("samples")
        #plt.show()

        plt.hist(flat_ambers, color='orange', edgecolor='black',
                 bins=100)
        plt.title("distribution of data for all colors")
        plt.xlabel("Volts(V)")
        plt.ylabel("samples")

        plt.show()

        redmean = []
        bluemean = []
        ambermean = []
        for x in reds:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            redmean.append(m)
        for x in blues:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            bluemean.append(m)
        for x in ambers:
            z = lowpass(x)
            m = np.mean(z)
            s = np.std(x)
            ambermean.append(m)
        print("redmeans:",redmean)
        print("red min:", min(redmean),"red max:", max(redmean))
        #redmean = [x for x in redmean if x < 0.2]
        print("bluemeans:", bluemean)
        print("blue min:", min(bluemean), "blue max:", max(bluemean))
        bluemean = [x for x in bluemean if x <0.2]
        print(len(bluemean))
        print("ambermeans:", ambermean)
        print("amber min:", min(ambermean), "amber max:", max(ambermean))

        results = anova_one_color(bluemean,redmean,ambermean)
        print(results)
        # flat_red = [item for sublist in rr3 for item in sublist]
        # flat_blue = [item for sublist in bb3 for item in sublist]
        # flat_amber = [item for sublist in aa3 for item in sublist]
        #data = [flat_red, flat_blue, flat_amber]
        data = [redmean,bluemean,ambermean]
        bplot = plt.boxplot(data,patch_artist=True)
        plt.xticks([1, 2, 3], ['red', 'blue', 'amber'])
        colors = ['red', 'blue', 'orange']
        #
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
        plt.xlabel("Wavelength", fontsize=20)
        plt.ylabel("Volts (V)", fontsize = 20)
        #plt.legend()
        plt.show()

        print("what is rr1", rr1[0])
        clean_sig = moving_average(lowpass(rr1[0]), 5)
        clean_red2 = moving_average(lowpass(rr1[1]), 5)
        clean_red3 = moving_average(lowpass(rr1[2]), 5)
        clean_blue1 = moving_average(lowpass(bb1[0]), 5)
        clean_blue2 = moving_average(lowpass(bb1[1]), 5)
        clean_blue3 = moving_average(lowpass(bb1[2]), 5)
        clean_a1 = moving_average(lowpass(aa1[0]), 5)
        clean_a2 = moving_average(lowpass(aa1[1]), 5)
        clean_a3 = moving_average(lowpass(aa1[2]), 5)

        x = np.linspace(0, 300, num=len(clean_sig))
        xx = np.linspace(0,300, num=len(rr1[0]))

        plt.plot(xx,rr1[0], color = 'red', label='Raw Signal')
        plt.xlabel("Time (s)", fontsize=20)
        plt.ylabel("Volts (V)", fontsize=20)
        plt.legend()
        plt.show()
        plt.plot(x, clean_sig, color='red', label='red1')
        plt.plot(np.linspace(0,300,num=len(clean_red2)),clean_red2, color = 'red',label='red2')
        plt.plot(np.linspace(0, 300, num=len(clean_red3)), clean_red3,color='red', label='red3')
        plt.plot(np.linspace(0, 300, num=len(clean_blue1)), clean_blue1,color='blue', label='blue1')
        plt.plot(np.linspace(0, 300, num=len(clean_blue2)),clean_blue2, color='blue', label='blue2')
        plt.plot(np.linspace(0, 300, num=len(clean_blue3)), clean_blue3,color='blue', label='blue3')
        plt.plot(np.linspace(0, 300, num=len(clean_a1)), clean_a1, color='orange', label='amber1')
        plt.plot(np.linspace(0, 300, num=len(clean_a2)), clean_a2, color='orange', label='amber2')
        plt.plot(np.linspace(0, 300, num=len(clean_a3)), clean_a3, color='orange', label='amber3')
        plt.legend()
        plt.xlabel("Time (s)", fontsize=20)
        plt.ylabel("Volts (V)", fontsize=20)
        plt.show()

    if analysis == 'fourier':
        b1v, _ = volts(8,b1)
        b2v,_ = volts(8,b2)
        b3v,_ = volts(8,b3)

        r1v, _ = volts(8, r1)
        r2v, _ = volts(8, r2)
        r3v, _ = volts(8, r3)

        a1v, _ = volts(8, a1)
        a2v, _ = volts(8, a2)
        a3v, _ = volts(8, a3)
        # fig, axs = plt.subplots(len(labels))
        # custom_xlim = (0, 5)
        # custom_ylim = (0, 35)
        #
        # # Setting the values for all axes.
        # plt.setp(axs, xlim=custom_xlim, ylim=custom_ylim)
        #
        # for i in range(len(xs)):
        #     # plot_fourier(x[i],y[i])
        #     # plt.plot(xs[i],np.abs(ys[i]), label=labels[i])
        #     axs[i].plot(xs[i], np.abs(ys[i]), color="red")
        #     axs[i].set_title(labels[i])
        # # plt.xlabel('Hertz (Hz)', fontsize=30)
        # # plt.ylabel('Power (dB)', fontsize=30)
        # # fig.suptitle("Signal with gain 1 testing resistor impacts on signal", fontsize=30)
        # fig.text(0.51, 0.04, 'Hertz (Hz)', ha='center', fontsize=20)
        # fig.text(0.04, 0.5, 'Power (dB)', va='center', rotation='vertical', fontsize=20)
        # # fig.tight_layout()
        # # plt.legend()
        # plt.subplots_adjust(hspace=0.6)
        # plt.show()

        xb1,yb1 = makefourier(b1v)
        xb2,yb2 = makefourier(b2v)
        plt.plot(xb2[0],np.abs(yb2[0]), label='blue1',color="blue")
        #plt.plot(xb1[1], np.abs(yb1[1]),label='blue2')
        #plt.plot(xb1[2],np.abs(yb1[2]), label='blue3')
        #plt.plot(xb1[3], np.abs(yb1[3]),label='blue4')
        #plt.plot(b1v[4], label='blue5')

        #plt.plot(xb2[0],np.abs(yb2[0]), label='blue1')
        #plt.plot(xb2[1], np.abs(yb2[1]),label='blue2')
        #plt.plot(xb2[2],np.abs(yb2[2]), label='blue3')
        #plt.plot(xb2[3], np.abs(yb2[3]),label='blue4')

        xr1,yr1 = makefourier(r1v)
        plt.plot(xr1[0],np.abs(yr1[0]), label='red1',color="red")
        # plt.plot(r1v[1], label='red2')
        # plt.plot(r1v[2], label='red3')
        # plt.plot(r1v[3], label='red4')
        #plt.plot(r1v[4], label='red5')

        xa1,ya1 = makefourier(a1v)
        xa3,ya3 = makefourier(a3v)
        plt.plot(xa3[0],np.abs(ya3[0]), label='amber1', color="orange")
        # plt.plot(a1v[1], label='amber2')
        # plt.plot(a1v[2], label='amber3')
        # plt.plot(a1v[3], label='amber4')
        # plt.plot(a1v[4], label='amber5')
        plt.ylim(0,100)
        plt.legend()
        plt.show()

    #blue_f1_t1, blue_f2_t2, blue_f3_t3 = analysis_single_trial(b1,b2,b3,"blue")

    #red_f1_t1, red_f2_t2, red_f3_t3 = analysis_single_trial(r1, r2, r3,"red")

    #amber_f1_t1, amber_f2_t2,amber_f3_t3 = analysis_single_trial(a1,a2,a3,"amber")
    #length_fix_sumtrials(b1,b2,b3,r1,r2,r3,a1,a2,a3)
    # print("red")
    # print(red_f1_t1)
    # print(red_f2_t2)
    # print(red_f3_t3)
    # print("blue")
    # print(blue_f1_t1)
    # print(blue_f2_t2)
    # print(blue_f3_t3)
    # print("amber")
    # print(amber_f1_t1)
    # print(amber_f2_t2)
    # print(amber_f3_t3)
def run_fourier_dc(dict, labels):
    xs = []
    ys = []
    # for k,v in dict.items():
    #     x, y = fast_fourier(3000,10,v)
    #     xs.append(x)
    #     ys.append(y)
    colors = ['red','crimson','firebrick']
    for k in range(len(dict)):
        x, y = fast_fourier(3000,10,dict[k])
        xs.append(x)
        ys.append(y)
    for i in range(len(xs)):
        #plot_fourier(x[i],y[i])
        plt.plot(xs[i],np.abs(ys[i]), label=labels[i], color=colors[i])
    plt.xlabel('Hertz (Hz)', fontsize=30)
    plt.ylabel('Power (dB)', fontsize=30)
    plt.legend()
    plt.show()

def blank_dc():
    ## path for blanks
    path_red = '/home/y/blanks/red'
    path_amber = '/home/y/blanks/amber'

    red_b = blanks(path_red)
    r_gains = list(red_b.keys())
    red_volts = []
    red_v_gain16, _ = volts(16,red_b[r_gains[0]])
    red_v_gain4, _ = volts(4, red_b[r_gains[1]])
    red_v_gain1, _ = volts(1, red_b[r_gains[2]])
    red_volts.append(red_v_gain16)
    red_volts.append(red_v_gain4)
    red_volts.append(red_v_gain1)
    red_labels = ["gain 16", "gain 4", "gain 1"]

    amber_b = blanks(path_amber)
    a_gains = list(amber_b.keys())
    amber_volts = []
    amber_v_gain2, _ = volts(2,amber_b[a_gains[0]])
    amber_v_gain1, _ = volts(4, amber_b[a_gains[1]])
    amber_v_gain8, _ = volts(1, amber_b[a_gains[2]])
    amber_volts.append(amber_v_gain8)
    amber_volts.append(amber_v_gain2)
    amber_volts.append(amber_v_gain1)
    amber_labels = ["gain8", "gain2", "gain1"]
    #print(amber_b.keys())
    run_fourier_dc(red_volts, red_labels)
    return red_volts[2]

def gain_errplot(br,rr,ar,resistor):

    brmeans, brtop, brbottom = std_mean_err(br)
    rrmeans, rrtop, rrbottom = std_mean_err(rr)
    armeans, artop, arbottom = std_mean_err(ar)
    gains = ['raw', 'gain1', 'gain2', 'gain4', 'gain8', 'gain16']

    gains2 = ['raw', 'gain1', 'gain2', 'gain4', 'gain8']
    gains3 = ['raw', 'gain1', 'gain2']
    #plt.plot(gains,dashline, color="black",linestyle="--")
    #print("test:",test)
    plt.plot(gains3,armeans, color="orange",marker='o')
    plt.fill_between(gains3, arbottom, artop, alpha=0.3, color="orange",label="Amber")

    plt.plot(gains3, rrmeans,color="crimson",marker='o')
    plt.fill_between(gains3, rrbottom, rrtop, alpha=0.3,color="crimson",label="Red")

    plt.plot(gains3, brmeans,color="blue",marker='o')
    plt.fill_between(gains3, brbottom, brtop, alpha=0.3,color="blue",label="Blue")

    plt.xlabel("Gains")
    plt.ylabel("Voltage (V)")
    plt.title("DC biaising for different wavelengths for R = " + resistor)
    plt.legend()
    #plt.plot(gains, mean2)
    #plt.plot(gains, mean3)
    #plt.plot(gains, mean4)

    plt.show()

def fourier_plot(data,labels,colors):
    xs = []
    ys = []
    # for k,v in dict.items():
    #     x, y = fast_fourier(3000,10,v)
    #     xs.append(x)
    #     ys.append(y)
    for k in range(len(data)):
        x, y = fast_fourier(len(data[k]),10,data[k])
        xs.append(x)
        ys.append(y)

    fig, axs = plt.subplots(len(labels))
    custom_xlim = (0, 5)
    custom_ylim = (0, 20)

    # Setting the values for all axes.
    plt.setp(axs, xlim=custom_xlim, ylim=custom_ylim)

    for i in range(len(xs)):
        #plot_fourier(x[i],y[i])
        #plt.plot(xs[i],np.abs(ys[i]), label=labels[i])
        axs[i].plot(xs[i],np.abs(ys[i]), color=colors[i])
        axs[i].set_title(labels[i])
    #plt.xlabel('Hertz (Hz)', fontsize=30)
    #plt.ylabel('Power (dB)', fontsize=30)
    #fig.suptitle("Signal with gain 1 testing resistor impacts on signal", fontsize=30)
    fig.text(0.51, 0.04, 'Hertz (Hz)', ha='center', fontsize=20)
    fig.text(0.04, 0.5, 'Power (dB)', va='center', rotation='vertical', fontsize=20)
    #fig.tight_layout()
    #plt.legend()
    plt.subplots_adjust(hspace=0.6)
    plt.show()

def main_dc():
    br1,br2,br3,rr1,rr2,rr3,ar1,ar2,ar3 = dc_bias_analysis()
    #####################list blanks################
    all_blue_r1 = []
    all_blue_r2 = []
    all_blue_r3 = []

    all_red_r1 = []
    all_red_r2 = []
    all_red_r3 = []

    all_amber_r1 = []
    all_amber_r2 = []
    all_amber_r3 = []

    ##############################BLUE#################
    br1_gains = list(br1.keys())
    br2_gains = list(br2.keys())
    br3_gains = list(br3.keys())
    #print(br1_gains, br2_gains, br3_gains)
    ##################BLUE R1###################
    br1_v_gain8, _ = volts(8,br1[br1_gains[0]])
    br1_v_gain16, _ = volts(16, br1[br1_gains[1]])
    br1_v_gain2, _ = volts(2, br1[br1_gains[2]])
    br1_v_gain0, _ = volts(0, br1[br1_gains[3]])
    br1_v_gain1, _ = volts(1, br1[br1_gains[4]])
    br1_v_gain4, _ = volts(4, br1[br1_gains[5]])
    all_blue_r1.append(br1_v_gain0)
    all_blue_r1.append(br1_v_gain1)
    all_blue_r1.append(br1_v_gain2)
    all_blue_r1.append(br1_v_gain4)
    all_blue_r1.append(br1_v_gain8)
    all_blue_r1.append(br1_v_gain16)

    ########################BLUE R2#######################
    br2_v_gain2, _ = volts(2, br2[br2_gains[0]])
    br2_v_gain0, _ = volts(0, br2[br2_gains[1]])
    br2_v_gain1, _ = volts(1, br2[br2_gains[2]])
    br2_v_gain4, _ = volts(4, br2[br2_gains[3]])
    all_blue_r2.append(br2_v_gain0)
    all_blue_r2.append(br2_v_gain1)
    all_blue_r2.append(br2_v_gain2)
    all_blue_r2.append(br2_v_gain4)
    ############################BLUE r3#####################
    br3_v_gain2, _ = volts(2, br3[br3_gains[0]])
    br3_v_gain0, _ = volts(0, br3[br3_gains[1]])
    br3_v_gain1, _ = volts(1, br3[br3_gains[2]])
    all_blue_r3.append(br3_v_gain0)
    all_blue_r3.append(br3_v_gain1)
    all_blue_r3.append(br3_v_gain2)
    ###################RED###############################
    #####################################################

    rr1_gains = list(rr1.keys())
    rr2_gains = list(rr2.keys())
    rr3_gains = list(rr3.keys())
    #print("here",rr1_gains, rr2_gains, rr3_gains)
  #############################RED R1##################################################
    rr1_v_gain8, _ = volts(8,rr1[rr1_gains[0]])
    rr1_v_gain16, _ = volts(16, rr1[rr1_gains[1]])
    rr1_v_gain2, _ = volts(2, rr1[rr1_gains[2]])
    rr1_v_gain0, _ = volts(0, rr1[rr1_gains[3]])
    rr1_v_gain1, _ = volts(1, rr1[rr1_gains[4]])
    rr1_v_gain4, _ = volts(4, rr1[rr1_gains[5]])
    all_red_r1.append(rr1_v_gain0)
    all_red_r1.append(rr1_v_gain1)
    all_red_r1.append(rr1_v_gain2)
    all_red_r1.append(rr1_v_gain4)
    all_red_r1.append(rr1_v_gain8)
    all_red_r1.append(rr1_v_gain16)
    ############################RED R2#############################################
    rr2_v_gain8, _ = volts(8,rr2[rr2_gains[0]])
    rr2_v_gain2, _ = volts(2, rr2[rr2_gains[1]])
    rr2_v_gain0, _ = volts(0, rr2[rr2_gains[2]])
    rr2_v_gain1, _ = volts(1, rr2[rr2_gains[3]])
    rr2_v_gain4, _ = volts(4, rr2[rr2_gains[4]])
    all_red_r2.append(rr2_v_gain0)
    all_red_r2.append(rr2_v_gain1)
    all_red_r2.append(rr2_v_gain2)
    all_red_r2.append(rr2_v_gain4)
    all_red_r2.append(rr2_v_gain8)
    ############################RED R3#############################################
    rr3_v_gain2, _ = volts(2, rr3[rr3_gains[0]])
    rr3_v_gain0, _ = volts(0, rr3[rr3_gains[1]])
    rr3_v_gain1, _ = volts(1, rr3[rr3_gains[2]])
    all_red_r3.append(rr3_v_gain0)
    all_red_r3.append(rr3_v_gain1)
    all_red_r3.append(rr3_v_gain2)

    ##############AMBER################################################################
    ar1_gains = list(ar1.keys())
    ar2_gains = list(ar2.keys())
    ar3_gains = list(ar3.keys())
    print(ar1_gains, ar2_gains, ar3_gains)
    ########### AMBER R1#############################################################
    ar1_v_gain8, _ = volts(8,ar1[ar1_gains[0]])
    ar1_v_gain16, _ = volts(16, ar1[ar1_gains[1]])
    ar1_v_gain2, _ = volts(2, ar1[ar1_gains[2]])
    ar1_v_gain0, _ = volts(0, ar1[ar1_gains[3]])
    ar1_v_gain1, _ = volts(1, ar1[ar1_gains[4]])
    ar1_v_gain4, _ = volts(4, ar1[ar1_gains[5]])
    all_amber_r1.append(ar1_v_gain0)
    all_amber_r1.append(ar1_v_gain1)
    all_amber_r1.append(ar1_v_gain2)
    all_amber_r1.append(ar1_v_gain4)
    all_amber_r1.append(ar1_v_gain8)
    all_amber_r1.append(ar1_v_gain16)
    ############################## AMBER R2###########################
    ar2_v_gain2, _ = volts(2, ar2[ar2_gains[0]])
    ar2_v_gain0, _ = volts(0, ar2[ar2_gains[1]])
    ar2_v_gain1, _ = volts(1, ar2[ar2_gains[2]])
    ar2_v_gain4, _ = volts(4, ar2[ar2_gains[3]])
    all_amber_r2.append(ar2_v_gain0)
    all_amber_r2.append(ar2_v_gain1)
    all_amber_r2.append(ar2_v_gain2)
    all_amber_r2.append(ar2_v_gain4)
    #############################AMBER R3############################
    ar3_v_gain2, _ = volts(2, ar3[ar3_gains[0]])
    ar3_v_gain0, _ = volts(0, ar3[ar3_gains[1]])
    ar3_v_gain1, _ = volts(1, ar3[ar3_gains[2]])
    all_amber_r3.append(ar3_v_gain0)
    all_amber_r3.append(ar3_v_gain1)
    all_amber_r3.append(ar3_v_gain2)

    return all_blue_r1, all_blue_r2, all_blue_r3, all_red_r1,all_red_r2,all_red_r3,all_amber_r1,all_amber_r2,all_amber_r3


if __name__ == "__main__":
    #main()
    #b1,b2,b3,r1,r2,r3,a1,a2,a3 = main_dc()
    #b1,b2,b3,r1,r2,r3,a1,a2,a3 = main("filtered")
    b1, b2, b3, r1, r2, r3, a1, a2, a3 = main("fourier")
    #gain_errplot(b1,r1,a1,"100Kohm")
    #gain_errplot(b2,r2,a2, "1Mohm")
    #gain_errplot(b3, r3, a3, "10Mohm")
    # lengths = [len(b1[1]),len(r1[1]),len(a1[1])]
    # min_ = min(lengths)
    # bb = b1[1][:min_]
    # rr = r1[1][:min_]
    # aa = a1[1][:min_]
    # all_colors = [bb,rr,aa]
    # color_labs = ["blue","red","amber"]
    # colors = ["blue","red","orange"]
    # fourier_plot(all_colors,color_labs,colors)
    # gains = ['raw', 'gain1', 'gain2', 'gain4', 'gain8','gain16'] #, 'gain16']
    # gains2 = ['raw', 'gain1', 'gain2', 'gain4', 'gain8']
    # gains3 = ['raw', 'gain1', 'gain2']
    # resistors = ['100Kohm','1Mohm','10Mohm']
    # x = np.linspace(0, 300, num=3000)
    # plt.plot(x,b1[0][:3000], label='raw')
    # plt.plot(x,b1[1][:3000],label = 'gain1')
    # plt.plot(x,b1[2][:3000], label = 'gain2')
    # plt.plot(x,b1[3][:3000], label = 'gain4')
    # plt.plot(x,b1[4][:3000], label = 'gain8')
    # plt.plot(x,b1[5][:3000],label = 'gain16')
    # x = np.linspace(0, 300, num=3000)
    # plt.legend()
    # plt.ylabel("Volts (V)",fontsize = 20)
    # plt.xlabel("Time (s)",fontsize = 20)
    # plt.show()
    # rawforgain0 = [r1[0],r2[0],r3[0]]
    # resforgain1 = [r1[1],r2[1],r3[1]]
    # print(b3)
    # fourier_plot(r2,gains2)
    # red_gain1_blank = blank_dc()
    # #xs, ys = fast_fourier(len(r1[1]), 10, r1[1])
    # blank_vsnot = [red_gain1_blank,r1[1]]
    # labs = ['blank','plant']
    # fourier_plot(blank_vsnot,labs)
    #
    #
    # x = np.linspace(0,300,num=3000)
    # x2 = np.linspace(0,len(r2[1])/10, num=len(r2[1]))
    # #x2 = np.linspace(0, 300, num=len(r1[1]))
    # #print(x)
    # # print(leplt.plot(a1v[1], label='amber2')
    # #     plt.plot(a1v[2], label='amber3')
    # #     plt.plot(a1v[3], label='amber4')
    # #     plt.plot(a1v[4], label='amber5')n(blank_vsnot[0]), len(x))
    # plt.plot(x,blank_vsnot[0], color='crimson',label='blank')
    # plt.plot(x2,r2[1],color='firebrick',label='plant')
    # plt.xlabel("Time (s)",fontsize=30)
    # plt.ylabel("Volts (V)",fontsize=30)
    # plt.legend()
    # plt.show()
    # print(adfuller(r2[1]))
    # #main("fourier")