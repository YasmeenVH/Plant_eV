import scipy
from scipy import fftpack
import numpy as np
import matplotlib.pyplot as plt
from extract import timeframe
from extract import extract_data
from scipy.signal import butter,filtfilt
import pandas as pd
from scipy import stats


def decompose(signal, time):
    N = len(signal)
    T = 1/N
    T2 = 1/time  # test
    x = np.linspace(0, 2*np.pi*N*T, N)
    x2 = np.linspace(0, 2*np.pi*N*T2, N) # test
    y_ep = fftpack.fft(signal)

    xf = np.linspace(0.0, 1.0//(2.0*T), N//2)
    xf2 = np.linspace(0.0, 1.0//(2.0 * T2), N//2)
    plt.plot(xf, (2.0//N)*np.abs(y_ep[0:N//2]))

    #sig_fft = scipy.fftpack.fft(signal)
    #power = np.abs(sig_fft)
    #sample_freq = fftpack.fftfreq(signal.size, d=)
    #sig_amp = 2 / time.size * np.abs(sig_fft)
    #sig_freq = np.abs(scipy.fftpack.fftfreq(time.size, ))
    plt.show()

def decompose2(signal, time):

    y_ep = fftpack.fft(signal)
    print("this is time: ",time)
    amp = 2 / time * np.abs(y_ep)
    sig_freq = np.abs(fftpack.fftfreq(int(time)))
    plt.plot(sig_freq, amp)
    plt.show()

def decompose3(signal, time):

    y_ep = fftpack.fft(signal)
    print(len(y_ep), " amount of data points")
    print("this is time: ",time)
    amp = 2 / int(time) * np.abs(y_ep)
    print(len(amp), " amplitude points")
    sig_freq = np.abs(fftpack.fftfreq(y_ep.size))
    print(len(sig_freq), " sig freq len")
    plt.plot(sig_freq, amp)
    plt.show()
    pd.Series(amp).nlargest(1).round(0).astype(int).tolist()
    magnitudes = abs(y_ep[np.where(sig_freq >=0)])
    peak_freq = np.sort((np.argpartition(magnitudes,-2)[-2:])/time)
    cutoff = peak_freq[0]
    return cutoff

def lowpass_filter(data):
    #sampling_freq = n_samples/sample_time  # sample time needs to be in seconds
    cutoff = 1.2
    order = 2
    print("Cutoff freq " + str(cutoff))
    fs = 5
    nyq = 0.5 * fs # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=True)
    y = filtfilt(b, a, data)
    #plt.plot(y)
    #plt.title("lowpass")
    #plt.show
    return y








if __name__ == '__main__':

    t = timeframe(1 / 24)
    r = extract_data('timestamp', 10, t)
    print(r[0])
    print(len(r[0]))
    print(r[1])
    time_n = []
    for x in r[1]:
        time_n.append(datetime.utcfromtimestamp(x))
    print(time_n)