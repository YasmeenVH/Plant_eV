# IMPORTS
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt


def volts(gain, data):
    """ data = list of list of data fro trial
        gain = is the settign on the ADS1115 amplifier used on the NodeMcu

        volt_data = returns the volt value for original data
        center_line = is the middle point based off the gain
    """

    volt_data = []

    if gain == 0:
        resolution = 3.3 / 32768

    if gain == 1:
        resolution = 4.096 / 32768

    if gain == 2:
        resolution = 2.048 / 32768

    if gain == 4:
        resolution = 1.024 / 32768

    if gain == 8:
        resolution = 0.512 / 32768

    if gain == 16:
        resolution = 0.256 / 32768

    for x in data:
        v = x * resolution
        volt_data.append(v)

    center_line = (32768 / 2) * resolution

    return volt_data, center_line


def moving_average(data, window):
    """ data = the electrical potential data
        window = size of moving window, how many points to slide

        Function returns smoothed data with different sized window chosen by the user
    """
    return np.convolve(data, np.ones(window), 'valid') / window


def fast_fourier(n, freq, data):
    """n = number of sample points
       freq = sampling frequency of the time series, needs to be in Hz

    Return will be frequency values with dB intensity """

    yf = rfft(data)
    xf = rfftfreq(n, 1 / freq)

    return xf, yf


def butter_filter(sig, order, lowcut, highcut, freq):
    """sig = signal to analyze
       order = order of the filter, the higher the more sever the dropoff
       lowfreq =  cutoff frequency that is included. Beyond this one it fades out
       sample freq = number of sample points
       freq = sampling frequency of the time series, needs to be in Hz
       Return will be a plotand values with dB intensity """
    # lowcut = 2.2 , highcut = 3.2 , order = 10, freq = 10hz
    sos = signal.butter(order, [lowcut, highcut], btype='bandstop', output='sos', fs=freq)
    filtered = signal.sosfilt(sos, sig)

    return filtered




if __name__ == '__main__':
    v = volts(gain=0)
    print(v)
