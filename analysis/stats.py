import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.anova import AnovaRM
from statsmodels.tsa.stattools import adfuller

def mean_reading(color):
    all_means = []
    for x in color:
        all_means.append(np.mean(x))

    return all_means

def stationarity(plant):
    for x in plant:
        print(adfuller(x))


def mean_std(trial1, trial2, trial3,t_all):
    m1 = np.mean(trial1)
    m2 = np.mean(trial2)
    m3 = np.mean(trial3)

    std1 = np.std(m1)
    std2 = np.std(m2)
    std3 = np.std(m3)

    print("mean and std for trial 1:", m1, "+-", std1)
    print("mean and std for trial 2:", m2, "+-", std2)
    print("mean and std for trial 3:", m3, "+-", std3)

    #total_data = trial1 + trial2 + trial3 # concatenate all files
    m_all = np.mean(t_all)
    std_all = np.std(m_all)

    return m_all, std_all

def find_min_trials(t1,t2,t3):
    length_trials = [len(t1), len(t2), len(t3)]
    length_cutoff = min(length_trials)

    return length_cutoff

def find_min_reading(t):
    lengths = []
    for x in t:
        lengths.append(len(x))

    min_ = min(lengths)
    return min_

def sum_readings(data, cap_value):
    all_data = []
    for x in data:
        all_data.append(x[:cap_value])

    return all_data
def sum_trials(t1,t2,t3):
    t_all = t1+t2+t3
    return t_all
def sum_one_trial(r1,r2,r3,r4,r5):
    trial = r1+r2+r3+r4+r5
    return trial

def length_adjust(t1,t2,t3,min_val):
    t1_good = t1[:min_val]
    t2_good = t2[:min_val]
    t3_good = t3[:min_val]

    return t1_good, t2_good, t3_good

def all_data_colors(blue,red,amber):
    t_all_colors = blue+red+amber
    return t_all_colors

def anova_one_color(blue, red, amber):
    f_values = stats.f_oneway(blue,red,amber)
    return f_values

def anova_single_plant(color):
    f_values = stats.f_oneway(color[0],color[1],color[2],color[3],color[4])
    return f_values

def tukey_hsd_trial(all_data, sample_number):
    color_groups = np.repeat(['r1','r2','r3','r4','r5'], repeats=sample_number)
    tukey = pairwise_tukeyhsd(endog=all_data,
                              groups=color_groups,
                              alpha=0.05)
    return tukey


def tukey_hsd(all_data, sample_number):
    color_groups = np.repeat(['blue', 'red', 'amber'], repeats=sample_number)
    tukey = pairwise_tukeyhsd(endog=all_data,
                              groups=color_groups,
                              alpha=0.05)
    return tukey

