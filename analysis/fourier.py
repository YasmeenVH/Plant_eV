from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq, irfft
from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import os
from statsmodels.graphics.tsaplots import plot_acf
#from scipy.signal import butter, lfilter

def load_files(PATH):
    os.chdir(PATH)
    file_names = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".csv"):
                file_names.append(file)

    file_names.sort()
    return file_names

def get_data(file_names):
    """['10hz_260umol_gain1.csv', '10hz_260umol_gain2.csv', '10hz_260umol_gain16.csv',
    '10hz_260umol_gain8.csv', '10hz_260umol_gain4.csv', '10hz_260umol_nogain.csv']"""
    all_data = []
    file_name = []
    for f in file_names:
        df = pd.read_csv(f)
        file_name.append(f)
        first_column = df.iloc[:, 0]
        data = first_column.iloc[:3000]
        all_data.append(data)

    #all_data = [all_data[3],all_data[4],all_data[2],all_data[5],all_data[0],all_data[1]]
    return all_data

def fastfourier(n,freq,data):
    """n = number of sample points
    freq = sampling frequency of the time series, needs to be in Hz

    Return will be a plotand values with dB intensity """

    yf = rfft(data)
    xf = rfftfreq(n, 1/freq)

    return xf, yf

def lowpass(sig):#, order, lowcut, highcut, freq): #,order,lowfreq,sample_freq):
    """sig = signal to analyze
       order = order of the filter, the higher the more sever the dropoff
       lowfreq =  cutoff frequency that is included. Beyond this one it fades out
       sample freq = number of sample points
       freq = sampling frequency of the time series, needs to be in Hz
       Return will be a plotand values with dB intensity """
    lowcut = 2.2
    highcut = 3.2
    order = 10
    freq = 10 #hz

    sos = signal.butter(order,[lowcut,highcut],btype='bandstop',output='sos',fs=freq)
    filtered = signal.sosfilt(sos, sig)

    return filtered

def highpass(sig):
    """n = number of sample points
    freq = sampling frequency of the time series, needs to be in Hz

    Return will be a plotand values with dB intensity """


def noise_removal(x,y):
    cut_f_signal = np.abs(y.copy())
    print("what are peaks", cut_f_signal)
    #cut_f_signal[(x > 2.2 )] = 0
    #cut_f_signal[( x>3.2)] = 0
    #cut_f_signal[(x > 2.2)] = 0

    indices = 3 > cut_f_signal
    cut_f_signal = indices* cut_f_signal

    clean_sig = irfft(cut_f_signal)
    return x, clean_sig, cut_f_signal

def norma(data, gain):
    norm_data = []

    if gain == 0:
        ##dif resolution
        for x in data:
            b = x - 16384
            bb = b*3.3/32768
            norm_data.append(bb)

    if gain == 1:
        for x in data:
            b = x - 16384
            bb = b*4.096/32768
            norm_data.append(bb)

    if gain == 2:
        for x in data:
            b = x - 16384
            bb = b*2.048/32768
            norm_data.append(bb)

    if gain == 4:
        for x in data:
            b = x - 16384
            bb = b*1.024/32768
            norm_data.append(bb)

    if gain == 8:
        for x in data:
            b = x - 16384
            bb = b*0.512/32768
            norm_data.append(bb)

    if gain == 16:
        for x in data:
            b = x - 16384
            bb = b*0.256/32768
            norm_data.append(bb)

    return norm_data

def multiplot(x1,y1,x2,y2,x3,y3,x4,y4):
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(x1, np.abs(y1),color="grey")
    axs[0,0].set_ylim(0,85)
    axs[0, 0].set_title('white')
    axs[0, 1].plot(x2, np.abs(y2), color="orange")
    axs[0, 1].set_ylim(0, 85)
    axs[0, 1].set_title('amber')
    axs[1, 0].plot(x3, np.abs(y3), color="crimson")
    axs[1, 0].set_ylim(0, 85)
    axs[1, 0].set_title('red')
    axs[1, 1].plot(x4, np.abs(y4), color="blue")
    axs[1, 1].set_ylim(0, 85)
    axs[1, 1].set_title('blue')
    for ax in axs.flat:
        ax.set(xlabel='Frequency (Hz)', ylabel='Power (dB)')
    for ax in axs.flat:
        ax.label_outer()

    plt.show()

def multiplot_pos(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6):
    fig, axs = plt.subplots(2, 3)
    axs[0, 0].plot(x1, np.abs(y1))
    axs[0,0].set_ylim(0,85)
    axs[0, 0].set_title('position1')

    axs[0, 1].plot(x2, np.abs(y2))
    axs[0, 1].set_ylim(0, 85)
    axs[0, 1].set_title('position2')

    axs[0, 2].plot(x3, np.abs(y3))
    axs[0, 2].set_ylim(0, 85)
    axs[0, 2].set_title('position3')


    axs[0, 2].plot(x3, np.abs(y3))
    axs[0, 2].set_ylim(0, 85)
    axs[0, 2].set_title('position3')

    axs[1, 0].plot(x4, np.abs(y4))
    axs[1, 0].set_ylim(0, 85)
    axs[1, 0].set_title('position4')

    axs[1, 1].plot(x5, np.abs(y5))
    axs[1, 1].set_ylim(0, 85)
    axs[1, 1].set_title('position5')

    axs[1, 2].plot(x6, np.abs(y6))
    axs[1, 2].set_ylim(0, 85)
    axs[1, 2].set_title('position6')

    for ax in axs.flat:
        ax.set(xlabel='Frequency (Hz)', ylabel='Power (dB)')
    for ax in axs.flat:
        ax.label_outer()

    plt.show()

def multiplot_time_pos(y1,y2,y3,y4,y5,y6):
    fig, axs = plt.subplots(2, 3)
    axs[0, 0].plot(y1)

    axs[0, 0].set_title('position1')

    axs[0, 1].plot(y2)

    axs[0, 1].set_title('position2')

    axs[0, 2].plot(y3)

    axs[0, 2].set_title('position3')

    axs[1, 0].plot(y4)

    axs[1, 0].set_title('position4')

    axs[1, 1].plot(y5)

    axs[1, 1].set_title('position5')

    axs[1, 2].plot(y6)

    axs[1, 2].set_title('position6')

    for ax in axs.flat:
        ax.set(xlabel='sample points', ylabel='Voltage (V)')
    for ax in axs.flat:
        ax.label_outer()

    plt.show()

def multiplot_time(y1,y2,y3,y4):
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(y1,color="grey")
    axs[0, 0].set_title('white')
    axs[0, 1].plot(y2, color="orange")
    axs[0, 1].set_title('amber')
    axs[1, 0].plot(y3, color="crimson")
    axs[1, 0].set_title('red')
    axs[1, 1].plot(y4, color="blue")
    axs[1, 1].set_title('blue')
    for ax in axs.flat:
        ax.set(xlabel='sample points', ylabel='voltage (V)')
    for ax in axs.flat:
        ax.label_outer()

    plt.suptitle('100Kohm signal without noise and smoothed')

    plt.show()

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def main():
    PATH = '/home/y/white150umol/100Kohm/gain8.csv'
    df = pd.read_csv(PATH)
    first_column = df.iloc[:, 0]
    data = first_column.iloc[:3000]
    datanorm_w = norma(data)
    # print("data",len(data))
    xwhite, ywhite = fastfourier(len(datanorm_w), 10, datanorm_w)
    #
    # xclean_w, yclean_w, clean_f_w = noise_removal(xwhite,ywhite)
    # #yclean_white = butter_bandpass_filter(ywhite,2.5,3.5,10,5)
    #
    #ATH2 = '/home/y/amber150umol/100Kohm/gain8.csv'
    PATH2 = '/home/y/amber150umol/100Kohm/gain8.csv'
    df2 = pd.read_csv(PATH2)
    first_column = df2.iloc[:, 0]
    data_a = first_column.iloc[:3000]
    datanorm_a = norma(data_a)
    xamber, yamber = fastfourier(len(datanorm_a), 10, datanorm_a)
    #
    # xclean_a, yclean_a, clean_f_a = noise_removal(xamber, yamber)
    # #yclean_amber = butter_bandpass_filter(yamber, 2.5, 3.5, 10, 5)
    #
    PATH3 = '/home/y/red150umol/100Kohm/gain16.csv'
    df3 = pd.read_csv(PATH3)
    first_column = df3.iloc[:, 0]
    data_r = first_column.iloc[:3000]
    datanorm_r = norma(data_r)
    xred, yred = fastfourier(len(datanorm_r), 10, datanorm_r)
    #
    # xclean_r, yclean_r, clean_f_r = noise_removal(xred, yred)
    # #yclean_red = butter_bandpass_filter(yred, 2.5, 3.5, 10, 5)
    #
    PATH4 = '/home/y/blue150umol/100Kohm/gain16.csv'
    df4 = pd.read_csv(PATH4)
    first_column = df4.iloc[:, 0]
    data_b = first_column.iloc[:3000]
    datanorm_b = norma(data_b)
    xblue, yblue = fastfourier(len(datanorm_b), 10, datanorm_b)
    #
    PLANT1 = '/home/y/april2022/plant1/'
    PLANT2 = '/home/y/april2022/plant2/'

    APRIL13 = '/home/y/april2022/april13/p1'
    APRILTIP = '/home/y/april2022/april13/p2_tip'

    p1_nomix = load_files(APRIL13)
    # print("april13",p1_nomix)
    p1_nomix = get_data(p1_nomix)
    tip = load_files(APRILTIP)
    print(tip, "what is order")
    tip = get_data(tip)

    p1 = load_files(PLANT1)

    p1 = get_data(p1)
    p1_volts = []
    for x in p1:
        v = norma(x)
        p1_volts.append(v)

    p2 = load_files(PLANT2)
    p2 = get_data(p2)
    p2_volts = []
    for x in p2:
        v = norma(x)
        p2_volts.append(v)
    p1_blue = []
    for x in p1_nomix:
        v = norma(x)
        p1_blue.append(v)

    p_tip = []
    for x in tip:
        v = norma(x)
        p_tip.append(v)
    ######################### FOURIER ###########################
    for x in p1_blue:
        xp2, yp2 = fastfourier(len(x), 10, x)
        plt.plot(xp2, np.abs(yp2))
    plt.title("FFT amber blue amber - plant amber blue(only) amber")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()

    for x in p_tip:
        xp2, yp2 = fastfourier(len(x), 10, x)
        plt.plot(xp2, np.abs(yp2))
    plt.title("FFT amber blue amber - april 13 - tip of plant")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()
    for x in p1_volts:
        xp1, yp1 = fastfourier(len(x), 10, x)
        plt.plot(xp1, np.abs(yp1))
    plt.title("FFT amber blue amber - plant 1")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()
    time_x = np.linspace(0, 300, 3000)
    times = []
    start = 0
    for x in range(1, 11):
        end = 300 * x
        print('start:', start)
        print('end', end)
        n = np.linspace(start, end, 3000)
        times.append(n)
        start = end

    print(times)

    # print("what is length of timex",len(time_x),time_x[0])
    # xs = []
    # datap1 = []
    # for x in p1_volts:

    ################ BANSTOP ####################
    for x in p2_volts:
        xp2, yp2 = fastfourier(len(lowpass(x)), 10, lowpass(x))
        plt.plot(xp2, np.abs(yp2))
    plt.title("FFT amber blue amber - plant 2 - bandstop")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()

    for x in p1_volts:
        xp1, yp1 = fastfourier(len(lowpass(x)), 10, lowpass(x))
        plt.plot(xp1, np.abs(yp1))
    plt.title("FFT amber blue amber - plant 1 - banstop ")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()

    ########################### RAW ####################################
    for x in p1_volts:
        plt.plot(time_x, x)

    plt.title("Raw data , 10 readings same plant 1")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.show()

    for x in p2_volts:
        plt.plot(time_x, x)

    plt.title("Raw data , 10 readings same plant 2")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.show()

    for x in p1_blue:
        plt.plot(time_x, x)

    plt.title("Raw data , 10 readings same plant April13")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.legend(["r1", "r10", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"])
    plt.show()

    for x in p_tip:
        plt.plot(time_x, x)

    plt.title("Raw data , 10 readings same plant April13 - tip")
    plt.xlabel("seconds")
    plt.ylabel("Volts")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.legend(["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"])
    plt.show()
    ############### BANDSTOP FILTER ############################
    for x in p1_volts:
        plt.plot(time_x, lowpass(x))

    plt.title("banstop on data , 10 readings same plant 1")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.show()
    for x in p2_volts:
        plt.plot(time_x, lowpass(x))

    plt.title("banstop on data , 10 readings same plant 2")
    plt.legend(["r1", "r10", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"])
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')

    plt.show()

    for x in p1_blue:
        plt.plot(time_x, lowpass(x))

    plt.title("banstop on data , 10 readings same plant April13")
    plt.legend(["r1", "r10", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"])
    plt.xlabel("seconds")
    plt.ylabel("Volts")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')

    plt.show()

    for x in p_tip:
        plt.plot(time_x, lowpass(x))

    plt.title("banstop on data , 10 readings same plant April13 - tip")
    plt.legend(["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"])
    plt.xlabel("seconds")
    plt.ylabel("Volts")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')

    plt.show()

    lowpass2 = []
    ma2 = []
    for x in p2_volts:
        i = 0
        lowpass2.append(lowpass(x))
        ma2.append(moving_average(lowpass(x), 5))
        # plt.plot(times[i],lowpass(x))
        # i+=1
    # print(len(times),len(lowpass2))
    # plt.plot(times, lowpass2)

    # plt.title("banstop on data , 10 readings same plant 2")
    # plt.legend(["r1","r10","r2","r3","r4","r5","r6","r7","r8","r9"])
    # plt.xlabel("seconds")
    # plt.axvline(x=100, color = 'black')
    # plt.axvline(x=200,color = 'black')
    lowpass_blue = []
    ma_blue = []
    only_p1_blue = []
    for x in p_tip:
        i = 0
        lowpass_blue.append(lowpass(x))
        ma_blue.append(moving_average(lowpass(x), 5))
        blueblue = []
        for z in range(len(x)):
            if 1000 <= z <= 2000:
                blueblue.append(x[z])
        only_p1_blue.append(blueblue)

    for x in only_p1_blue:
        xp1, yp1 = fastfourier(len(x), 10, x)
        plt.plot(xp1, np.abs(yp1))
    plt.title("FFT April 13 only blue section ")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()
    p_tip_25 = [p_tip[1], p_tip[4]]
    for x in p_tip_25:
        xp1, yp1 = fastfourier(len(x), 10, lowpass(x))
        plt.plot(xp1, np.abs(yp1))
    plt.title("FFT April 13 only run 2 and 5")
    plt.ylabel("power (dB)")
    plt.ylim(0, 40)
    plt.xlabel("frequency (Hz)")
    plt.show()

    for x in only_p1_blue:
        plt.plot(lowpass(x))

    plt.title("banstop on data , 10 readings same plant April13 but only blue part of data")
    plt.legend(["r1", "r10", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"])
    # plt.xlabel("seconds")
    plt.ylabel("Volts")
    # plt.axvline(x=100, color = 'black')
    # plt.axvline(x=200,color = 'black')
    plt.show()

    plt.plot(times[0], lowpass_blue[0])
    plt.plot(times[1], lowpass_blue[1])
    plt.plot(times[2], lowpass_blue[2])
    plt.plot(times[3], lowpass_blue[3])
    plt.plot(times[4], lowpass_blue[4])
    plt.plot(times[5], lowpass_blue[5])
    plt.plot(times[6], lowpass_blue[6])
    plt.plot(times[7], lowpass_blue[7])
    plt.plot(times[8], lowpass_blue[8])
    plt.plot(times[9], lowpass_blue[9])
    plt.axvspan(100, 200, alpha=0.2, color='red')
    plt.axvspan(400, 500, alpha=0.2, color='red')
    plt.axvspan(700, 800, alpha=0.2, color='red')
    plt.axvspan(1000, 1100, alpha=0.2, color='red')
    plt.axvspan(1300, 1400, alpha=0.2, color='red')
    plt.axvspan(1600, 1700, alpha=0.2, color='red')
    plt.axvspan(1900, 2000, alpha=0.2, color='red')
    plt.axvspan(2200, 2300, alpha=0.2, color='red')
    plt.axvspan(2500, 2600, alpha=0.2, color='red')
    plt.axvspan(2800, 2900, alpha=0.2, color='red')
    plt.title("Chronological order of readings - amber, blue, amber - April 13 - tip")
    plt.legend(["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"])
    plt.xlabel("seconds")
    plt.ylabel("Volts")
    # plt.axvline(x=100, color='black')
    # ``plt.axvline(x=200, color='black')

    plt.show()

    plt.plot(times[0], lowpass2[0])
    plt.plot(times[1], lowpass2[2])
    plt.plot(times[2], lowpass2[3])
    plt.plot(times[3], lowpass2[4])
    plt.plot(times[4], lowpass2[5])
    plt.plot(times[5], lowpass2[6])
    plt.plot(times[6], lowpass2[7])
    plt.plot(times[7], lowpass2[8])
    plt.plot(times[8], lowpass2[9])
    plt.plot(times[9], lowpass2[1])
    plt.axvspan(100, 200, alpha=0.9, color='red')
    plt.axvspan(400, 500, alpha=0.9, color='red')
    plt.axvspan(700, 800, alpha=0.9, color='red')
    plt.axvspan(1000, 1100, alpha=0.9, color='red')
    plt.axvspan(1300, 1400, alpha=0.9, color='red')
    plt.axvspan(1600, 1700, alpha=0.9, color='red')
    plt.axvspan(1900, 2000, alpha=0.9, color='red')
    plt.axvspan(2200, 2300, alpha=0.9, color='red')
    plt.axvspan(2500, 2600, alpha=0.9, color='red')
    plt.axvspan(2800, 2900, alpha=0.9, color='red')
    plt.title("Chronological order of readings - amber, blue, amber")
    plt.legend(["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"])
    plt.xlabel("seconds")
    plt.ylabel("Volts")
    # plt.axvline(x=100, color='black')
    # ``plt.axvline(x=200, color='black')

    plt.show()

    # plt.show()

    plt.plot(times[0][:2996], ma2[0])
    plt.plot(times[1][:2996], ma2[2])
    plt.plot(times[2][:2996], ma2[3])
    plt.plot(times[3][:2996], ma2[4])
    plt.plot(times[4][:2996], ma2[5])
    plt.plot(times[5][:2996], ma2[6])
    plt.plot(times[6][:2996], ma2[7])
    plt.plot(times[7][:2996], ma2[8])
    plt.plot(times[8][:2996], ma2[9])
    plt.plot(times[9][:2996], ma2[1])
    plt.show()
    ##################### MOVING AVERAGE WITH BANDSTOP ############################
    for x in p1_volts:
        ma_2 = moving_average(lowpass(x), 5)
        timex = np.linspace(0, 300, len(ma_2))
        plt.plot(timex, ma_2)

    plt.title("banstop on data , 10 readings same plant 1 - moving av")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.show()
    for x in p2_volts:
        ma_2 = moving_average(lowpass(x), 5)
        timex = np.linspace(0, 300, len(ma_2))
        plt.plot(timex, ma_2)

    plt.title("banstop on data , 10 readings same plant 1- moving av")
    plt.xlabel("seconds")
    plt.axvline(x=100, color='black')
    plt.axvline(x=200, color='black')
    plt.show()
    ############################AUTOCORRELATION############
    # for x in p2_volts:
    #     plot_acf(x,lags=100)
    #
    # plt.title("autocorr")
    # plt.show()
    # for x in p2_volts:
    #     plot_acf(lowpass(x), lags=100)

    # plt.title("autocorr on bandstopdata")
    # plt.show()
    p1_1 = pd.Series(p1_blue[0])
    p1_10 = pd.Series(p1_blue[1])
    p1_2 = pd.Series(p1_blue[2])
    p1_3 = pd.Series(p1_blue[3])
    p1_4 = pd.Series(p1_blue[4])
    p1_5 = pd.Series(p1_blue[5])
    p1_6 = pd.Series(p1_blue[6])
    p1_7 = pd.Series(p1_blue[7])
    p1_8 = pd.Series(p1_blue[8])
    p1_9 = pd.Series(p1_blue[9])

    dataframe_1 = {'s1': p1_1, 's2': p1_2, 's3': p1_3, 's4': p1_4, 's5': p1_5, 's6': p1_6, 's7': p1_7, 's8': p1_8,
                   's9': p1_9, 's10': p1_10}
    df = pd.DataFrame(dataframe_1)
    corr = df.corr()
    plt.matshow(corr)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=10)
    plt.show()
    corr.to_csv('/home/y/april2022/plant1corr.csv')
    # xclean_b, yclean_b, clean_f_b = noise_removal(xblue, yblue)
    # #yclean_blue = butter_bandpass_filter(yblue, 2.5, 3.5, 10, 5)
    #
    # plt.ylim(0,40)
    # plt.plot(xamber, np.abs(yamber),label="amber", color="orange")
    # plt.plot(xwhite,np.abs(ywhite),label="white",color="grey")
    # plt.plot(xred,np.abs(yred),label="red",color="crimson")
    # plt.plot(xblue,np.abs(yblue),label="blue",color="blue")
    # plt.title("FFT for 100Kohm - best readings - allcolors")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # plt.legend()
    # plt.show()
    #
    # multiplot(xwhite,ywhite,xamber,yamber,xred,yred,xblue,yblue)
    #
    # plt.ylim(0,40)
    # plt.plot(xclean_a, np.abs(clean_f_a),label="amber", color="orange")
    # plt.plot(xclean_w,np.abs(clean_f_w),label="white",color="grey")
    # plt.plot(xclean_r,np.abs(clean_f_r),label="red",color="crimson")
    # plt.plot(xclean_b,np.abs(clean_f_b),label="blue",color="blue")
    # plt.title("FFT for 100Kohm - best readings - allcolors - clean")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # plt.legend()
    # plt.show()
    #
    # #plt.ylim(0, 80)
    #
    # plt.plot(yclean_a, label="amber filtered")#, label="amber", color="orange")
    # plt.plot(datanorm_a, label = "amber raw")
    # plt.legend()
    # plt.title("amber 100Kohm - gain8")
    # #plt.plot(xclean_w, np.abs(clean_f_w), label="white", color="grey")
    # #plt.plot(xclean_r, np.abs(clean_f_r), label="red", color="crimson")
    # #plt.plot(xclean_b, np.abs(clean_f_b), label="blue", color="blue")
    # #plt.title("FFT for 10Mohm - best readings - allcolors - clean")
    # #plt.ylabel("power (dB)")
    # #plt.xlabel("frequency (Hz)")
    # #plt.legend()
    # plt.show()
    #
    # plt.plot(yclean_w, label = "white filtered")#, label="amber", color="orange")
    # plt.plot(datanorm_w, label = "white raw")
    # plt.legend()
    # plt.title("white 100K0hm - gain 8")
    # plt.show()
    #
    # plt.plot(yclean_r, label = "red filtered")#, label="amber", color="orange")
    # plt.plot(datanorm_r, label = "red raw")
    # plt.legend()
    # plt.title("red 100Kohm - gain 16")
    # plt.show()
    # plt.plot(yclean_b, label = "blue filtered")#, label="amber", color="orange")
    # plt.plot(datanorm_b, label = "blue raw")
    # plt.title("blue 100Kohm- gain 16")
    # plt.show()
    #
    # multiplot_time(yclean_w,yclean_a,yclean_r,yclean_b)
    # plt.plot(yclean_b, label="blue filtered", color = "blue")
    # plt.plot(yclean_r, label="red filtered", color = "crimson")
    # plt.plot(yclean_w, label="white filtered", color = "grey")
    # plt.plot(yclean_a, label="amber filtered", color = "orange")
    # plt.legend()
    # plt.ylabel("voltage (V)")
    # plt.xlabel("sample points at 10Hz")
    # plt.show()
    #
    # ma_blue = moving_average(yclean_b,50)
    # ma_amber = moving_average(yclean_a,50)
    # ma_white = moving_average(yclean_w,50)
    # ma_red = moving_average(yclean_r,50)
    #
    #
    # plt.plot(ma_blue, label="blue smooth", color = "blue")
    # plt.plot(ma_red, label="red smooth", color = "crimson")
    # plt.plot(ma_white, label="white smooth", color = "grey")
    # plt.plot(ma_amber, label="amber smooth", color = "orange")
    # plt.legend()
    # plt.ylabel("voltage (V)")
    # plt.xlabel("sample points at 10Hz")
    # plt.show()
    #
    # multiplot_time(ma_white,ma_amber, ma_red, ma_blue)
    # plt.plot(yclean_a, color = "orange", label = "amber")
    # plt.plot(yclean_r, color = "crimson", label="red")
    # plt.plot(yclean_w, color ="grey", label="white")
    # plt.plot(yclean_b, color = "blue", label = "blue")
    # plt.legend()
    # plt.show()

    #
    # PATH1 = "/home/y/Documents/amber/amberdata_ampfirst_1000.csv"
    # df = pd.read_csv(PATH1)
    # first_column = df.iloc[:, 0]
    # data = first_column.iloc[:3000]
    # datanorm1 = norma(data)
    # print("data",len(data))
    # xpos1, ypos1 = fastfourier(len(datanorm1),10,datanorm1)
    #
    # PATH2 = "/home/y/Documents/amber/position2_amber_100kohm.csv"
    # df2 = pd.read_csv(PATH2)
    # first_column2 = df2.iloc[:, 0]
    # data2 = first_column2.iloc[:3000]
    # datanorm2 = norma(data2)
    # print("data",len(data2))
    # xpos2, ypos2 = fastfourier(len(datanorm2),10,datanorm2)
    #
    # PATH3 = "/home/y/Documents/amber/position3_amber_100ohmk.csv"
    # df3 = pd.read_csv(PATH3)
    # first_column3 = df3.iloc[:, 0]
    # data3 = first_column3.iloc[:3000]
    # datanorm3 = norma(data3)
    # print("data",len(data3))
    # xpos3, ypos3 = fastfourier(len(datanorm3),10,datanorm3)
    #
    # PATH4 = "/home/y/Documents/amber/position4.csv"
    # df4 = pd.read_csv(PATH4)
    # first_column4 = df4.iloc[:, 0]
    # data4 = first_column4.iloc[:3000]
    # datanorm4 = norma(data4)
    # print("data",len(data4))
    # xpos4, ypos4 = fastfourier(len(datanorm4),10,datanorm4)
    #
    # PATH5 = "/home/y/Documents/amber/position5.csv"
    # df5 = pd.read_csv(PATH5)
    # first_column5 = df5.iloc[:, 0]
    # data5 = first_column5.iloc[:3000]
    # datanorm5 = norma(data5)
    # print("data",len(data5))
    # xpos5, ypos5 = fastfourier(len(datanorm5),10,datanorm5)
    #
    # PATH6 = "/home/y/Documents/amber/position6.csv"
    # df6 = pd.read_csv(PATH6)
    # first_column6 = df6.iloc[:, 0]
    # data6 = first_column6.iloc[:3000]
    # datanorm6 = norma(data6)
    # print("data",len(data6))
    # xpos6, ypos6 = fastfourier(len(datanorm6),10,datanorm6)
    #
    #
    #
    #
    # plt.plot(xpos1, np.abs(ypos1),label="position 1")
    # plt.plot(xpos2, np.abs(ypos2),label="position 2")
    # plt.plot(xpos3, np.abs(ypos3),label="position 3")
    # plt.plot(xpos4, np.abs(ypos4),label="position 4")
    # plt.plot(xpos5, np.abs(ypos5), label="position 5")
    # plt.plot(xpos6, np.abs(ypos6), label="position 6")
    # plt.title("FFT for 100Kohm -amber - all positons")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # plt.ylim(0,50)
    # plt.legend()
    # plt.show()
    #
    # multiplot_pos(xpos1,ypos1,xpos2,ypos2,xpos3,ypos3,xpos4,ypos4,xpos5,ypos5,xpos6,ypos6)
    #
    # xclean_1, yclean_1, clean_f_1 = noise_removal(xpos1, ypos1)
    # xclean_2, yclean_2, clean_f_2 = noise_removal(xpos2, ypos2)
    # xclean_3, yclean_3, clean_f_3 = noise_removal(xpos3, ypos3)
    # xclean_4, yclean_4, clean_f_4 = noise_removal(xpos4, ypos4)
    # xclean_5, yclean_5, clean_f_5 = noise_removal(xpos5, ypos5)
    # xclean_6, yclean_6, clean_f_6 = noise_removal(xpos6, ypos6)
    #
    # plt.plot(yclean_1,label="position 1")
    # plt.plot(yclean_2,label="position 2")
    # plt.plot(yclean_3,label="position 3")
    # plt.plot(yclean_4,label="position 4")
    # plt.plot(yclean_5, label="position 5")
    # plt.plot(yclean_6, label="position 6")
    # plt.title(" amber - all positons - filtered signal time domain")
    # plt.ylabel("Voltage(V)")
    # plt.xlabel("samplepoints")
    # plt.ylim(-0.2,0.2)
    #
    # plt.legend()
    # plt.show()
    #
    # plt.plot(datanorm1,label="position 1")
    # plt.plot(datanorm2,label="position 2")
    # plt.plot(datanorm3,label="position 3")
    # plt.plot(datanorm4,label="position 4")
    # plt.plot(datanorm5, label="position 5")
    # plt.plot(datanorm6, label="position 6")
    # plt.title(" amber - all positons - original")
    # plt.ylabel("Voltage(V)")
    # plt.xlabel("samplepoints")
    #
    # plt.legend()
    # plt.show()
    #
    # plt.plot(xclean_1, np.abs(clean_f_1),label="position 1")
    # plt.plot(xclean_2, np.abs(clean_f_2),label="position 2")
    # plt.plot(xclean_3, np.abs(clean_f_3),label="position 3")
    # plt.plot(xclean_4, np.abs(clean_f_4),label="position 4")
    # plt.plot(xclean_5, np.abs(clean_f_5), label="position 5")
    # plt.plot(xclean_6, np.abs(clean_f_6), label="position 6")
    # plt.title(" FFT amber - all positons - filtered")
    # plt.ylabel("Power (dB)")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylim(0, 10)
    #
    # plt.legend()
    # plt.show()
    #
    # ma_1 = moving_average(yclean_1,50)
    # ma_2 = moving_average(yclean_2,50)
    # ma_3 = moving_average(yclean_3,50)
    # ma_4 = moving_average(yclean_4,50)
    # ma_5 = moving_average(yclean_5,50)
    # ma_6 = moving_average(yclean_6,50)
    #
    # plt.plot(ma_1, label = "position1")
    # plt.plot(ma_2, label="position2")
    # plt.plot(ma_3, label="position3")
    # plt.plot(ma_4, label="position4")
    # plt.plot(ma_5, label="position5")
    # plt.plot(ma_6, label="position6")
    #
    # plt.title(" amber - all positons - movingaverage w = 50")
    # plt.ylabel("Voltage(V)")
    # plt.xlabel("samplepoints")
    #
    # plt.legend()
    # plt.show()
    #
    # multiplot_time_pos(ma_1,ma_2,ma_3,ma_4,ma_5,ma_6)

    # PATH1 = "/home/y/blue150umol/inverse direction/gain16.csv"
    # ## 1mohm
    # df1 = pd.read_csv(PATH1)
    # first_column1 = df1.iloc[:, 0]
    # data1 = first_column1.iloc[:3000]
    # datanorm1 = norma(data1)
    # print("data",len(data1))
    # xpos1, ypos1 = fastfourier(len(datanorm1),10,datanorm1)
    #
    # PATH2 = "/home/y/blue150umol/1Mohm/gain2.csv"
    # df2 = pd.read_csv(PATH2)
    # first_column2 = df2.iloc[:, 0]
    # data2 = first_column2.iloc[:3000]
    # datanorm2 = norma(data2)
    # print("data",len(data2))
    # xpos2, ypos2 = fastfourier(len(datanorm2),10,datanorm2)
    #
    # plt.plot(datanorm1,label="opposite direction gain16")
    # plt.plot(datanorm2,label="normal direction gain2")
    #
    # plt.title(" blue - different directions - 1Mohm")
    # plt.ylabel("Voltage(V)")
    # plt.xlabel("samplepoints")
    # #
    # plt.legend()
    # plt.show()
    # xpos1, ypos1 = fastfourier(len(datanorm1),10,datanorm1)
    plt.plot(datanorm_a, label="amber raw")
    plt.plot(lowpass(datanorm_a), label="bandstop fitler on amber data")
    plt.title("Amber")
    plt.ylabel("V")
    plt.xlabel("sample point")
    plt.legend()
    plt.show()
    xlow_w, ylow_w = fastfourier(len(lowpass(datanorm_a)), 10, lowpass(datanorm_a))
    plt.plot(xwhite, np.abs(ywhite), label="fft amber")
    plt.plot(xlow_w, np.abs(ylow_w), label="fft with bandstop")
    plt.title("FFT for raw and lowpass")
    plt.ylabel("power (dB)")
    plt.xlabel("frequency (Hz)")
    plt.ylim(0, 60)
    plt.legend()
    plt.show()

    # xpos3, ypos3 = fastfourier(len(datanorm1), 10, datanorm1)
    # xpos4, ypos4 = fastfourier(len(lowpass(datanorm1)), 10, lowpass(datanorm1))

    # plt.plot(xpos3, np.abs(ypos3),label="opposite direction")
    # plt.plot(xpos4, np.abs(ypos4),label="nlowpass filtered")
    # plt.title("FFT for naw and lowpass")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # plt.ylim(0,200)
    # plt.legend()
    # plt.show()

    ma_1 = moving_average(datanorm_a, 5)
    ma_2 = moving_average(lowpass(datanorm_a), 5)

    ma_w = moving_average(lowpass(datanorm_w), 5)
    ma_a = moving_average(lowpass(datanorm_a), 5)
    ma_r = moving_average(lowpass(datanorm_r), 5)
    ma_b = moving_average(lowpass(datanorm_b), 5)

    plt.plot(ma_w, label="white bandstop, window of 5", color="grey")
    plt.plot(ma_a, label="amber bandstop, window of 5", color="orange")
    plt.plot(ma_r, label="red bandstop, window of 5", color="crimson")
    plt.plot(ma_b, label="blue bandstop, window of 5", color="blue")

    # plt.plot(datanorm_a, label="raw")
    # plt.plot(ma_1, label="moving average of 5 on raw")
    # plt.title("opposite direction")
    # plt.xlabel("sample points")
    # plt.ylabel("voltage (V)")
    # axs[0, 0].set_title('opposite direction')
    # plt.subplot(1,2,2)
    # plt.plot(ma_2, label="bandstop moving average of 5")
    # plt.plot(datanorm_w,label="raw")
    plt.title("Moving average for all colors")
    plt.xlabel("sample points")
    plt.ylabel("voltage (V)")
    plt.legend()
    plt.show()
    # clean_sig_r = irfft(ypos3)
    # clean_sig_bandstop = irfft(ypos4)
    #
    # plt.plot(clean_sig_r,label="unfiltered")
    # plt.plot(clean_sig_bandstop,label="filtered")
    # plt.show()
    #
    # plt.plot(xpos1, np.abs(ypos1),label="opposite direction")
    # plt.plot(xpos2, np.abs(ypos2),label="normal direction")
    #
    # plt.title("FFT for 100Kohm - directionality")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # plt.ylim(0,200)
    # plt.legend()
    # plt.show()
    #
    # xclean_1, yclean_1, clean_f_1 = noise_removal(xpos1, ypos1)
    # xclean_2, yclean_2, clean_f_2 = noise_removal(xpos2, ypos2)
    #
    # plt.plot(yclean_1,label="position 1")
    # plt.plot(yclean_2,label="position 2")
    #
    # plt.title(" Blue - directionality- filtered signal time domain")
    # plt.ylabel("Voltage(V)")
    # plt.xlabel("samplepoints")
    # # plt.ylim(-0.2,0.2)
    # #
    # plt.legend()
    # plt.show()
    #
    # plt.plot(xclean_1, np.abs(clean_f_1),label="opposite direction")
    # plt.plot(xclean_2, np.abs(clean_f_2),label="normal direction")
    #
    # plt.title("FFT for 100Kohm - directionality - filtered noise")
    # plt.ylabel("power (dB)")
    # plt.xlabel("frequency (Hz)")
    # #plt.ylim(0,50)
    # plt.legend()
    # plt.show()
    #
    # ma_1 = moving_average(clean_sig_r,20)
    # ma_2 = moving_average(clean_sig_bandstop,20)
    #
    # #plt.subplot(1,2,1)
    # plt.plot(ma_1, label="raw")
    # #plt.title("opposite direction")
    # #plt.xlabel("sample points")
    # #plt.ylabel("voltage (V)")
    # #axs[0, 0].set_title('opposite direction')
    # #plt.subplot(1,2,2)
    # plt.plot(ma_2, label = "bandstopfiltered")
    # plt.title("Smoothed 1Mohm different directions")
    # plt.xlabel("sample points")
    # plt.ylabel("voltage (V)")
    # plt.legend()
    # #axs[0, 1].set_title('normal direction')
    #
    # # for ax in axs.flat:
    # #     ax.set(xlabel='sample points', ylabel='voltage (V)')
    # # for ax in axs.flat:
    # #     ax.label_outer()
    #
    # #plt.suptitle('1Mohm signal without noise and smoothed- directionality')
    #
    # plt.show()
    #

def get_from_csv(PATH, gain):
    df = pd.read_csv(PATH)
    first_column = df.iloc[:, 0]
    data = first_column.iloc[:3000]
    datanorm_w = norma(data, gain)

    return datanorm_w

if __name__ == "__main__":
    PATH = '/home/y/amber150umol/100Kohm/gain0.csv'
    PATH1 = '/home/y/amber150umol/100Kohm/gain1.csv'
    PATH2 = '/home/y/amber150umol/100Kohm/gain2.csv'
    PATH4 = '/home/y/amber150umol/100Kohm/gain4.csv'
    PATH8 = '/home/y/amber150umol/100Kohm/gain8.csv'
    PATH16 = '/home/y/amber150umol/100Kohm/gain16.csv'

    PATH_M = '/home/y/amber150umol/1Mohm/gain0.csv'
    PATH_M2 = '/home/y/amber150umol/1Mohm/gain2.csv'
    PATH_10M = '/home/y/amber150umol/10Mohm/gain0.csv'
    PATH_10M2 = '/home/y/amber150umol/10Mohm/gain2.csv'

    # raw = load_files(PATH)
    # gain1 = load_files(PATH1)
    # gain2 = load_files(PATH2)
    # gain4 = load_files(PATH4)
    # gain8 = load_files(PATH8)
    # gain16 = load_files(PATH16)



    df_raw = get_from_csv(PATH, 0)
    df_gain1 = get_from_csv(PATH1, 1)
    df_gain2 = get_from_csv(PATH2, 2)
    df_gain4 = get_from_csv(PATH4, 4)
    df_gain8 = get_from_csv(PATH8, 8)
    df_gain16 = get_from_csv(PATH16,16)

    df_raw_1M = get_from_csv(PATH_M,0)
    df_raw_10M = get_from_csv(PATH_10M,0)
    df_gain2_1M = get_from_csv(PATH_M2,2)
    df_gain2_10M = get_from_csv(PATH_10M2,2)
    #df_gain_ = get_from_csv(PATH_M_16,16)
    plt.plot(df_raw, label = "raw")
    #plt.plot(df_gain1, label = "gain1")
    #plt.plot(df_gain2, label = "gain2")
    #plt.plot(df_gain4, label = "gain4")
    #plt.plot(df_gain8,label = "gain8")
    #plt.plot(df_gain16, label = "gain16")
    plt.plot(df_raw_1M,label="raw 1m")
    plt.plot(df_raw_10M,label="raw 10m")


    plt.legend()
    plt.show()

    xp1, yp1 = fastfourier(len(df_raw), 10, df_raw)
    xp2,yp2 = fastfourier(len(df_raw_1M),10,df_raw_1M)
    xp3,yp3 = fastfourier(len(df_raw_10M),10, df_raw_10M)


    fig, axs = plt.subplots(3)
    axs[0].plot(xp1, np.abs(yp1))
    axs[0].set_ylim(0, 20)
    axs[0].set_title('r = 100Kohm')

    axs[1].plot(xp2, np.abs(yp2))
    axs[1].set_ylim(0, 20)
    axs[1].set_title('r = 1Mohm')

    axs[2].plot(xp3, np.abs(yp3))
    axs[2].set_ylim(0, 20)
    axs[2].set_title('r = 10Mohm')

    for ax in axs.flat:
        ax.set(xlabel='Frequency (Hz)', ylabel='Power (dB)')
    for ax in axs.flat:
        ax.label_outer()

    plt.show()

    plt.plot(xp1, np.abs(yp1), label="100k")
    plt.plot(xp2,np.abs(yp2), label = "1m")
    plt.plot(xp3,np.abs(yp3),label = "10M")

    plt.ylim(0,10)
    plt.legend()
    plt.show()

    # plt.plot(df_gain16, label = "gain16 100kohm")
    # plt.plot(df_gain16_M,label="gain16  1M")
    # plt.legend()
    # plt.show()

    xp1, yp1 = fastfourier(len(df_gain16), 10, df_gain16)
    #xp2, yp2 = fastfourier(len(df_gain16_M), 10, df_gain16_M)
    plt.plot(xp1, np.abs(yp1), label = "100k")
    #plt.plot(xp2,np.abs(y2), label = "1M")
    plt.ylim(0,10)
    plt.show()

    plt.plot(df_gain2, label = "gain2 - r=100k")
    plt.plot(df_gain2_1M, label = "gain2 - r=1M")
    plt.plot(df_gain2_10M, label = "gain2 - r = 10M")
    plt.legend()
    plt.show()


    xp1, yp1 = fastfourier(len(df_gain2), 10, df_gain2)
    xp2,yp2 = fastfourier(len(df_gain2_1M),10,df_gain2_1M)
    xp3,yp3 = fastfourier(len(df_gain2_10M),10, df_gain2_10M)

    fig, axs = plt.subplots(3)
    axs[0].plot(xp1, np.abs(yp1))
    axs[0].set_ylim(0, 20)
    axs[0].set_title('r = 100Kohm - gain2')

    axs[1].plot(xp2, np.abs(yp2))
    axs[1].set_ylim(0, 20)
    axs[1].set_title('r = 1Mohm - gain2')

    axs[2].plot(xp3, np.abs(yp3))
    axs[2].set_ylim(0, 20)
    axs[2].set_title('r = 10Mohm - gain2')

    for ax in axs.flat:
        ax.set(xlabel='Frequency (Hz)', ylabel='Power (dB)')
    for ax in axs.flat:
        ax.label_outer()

    plt.show()