import matplotlib.pyplot as plt
from scipy.fftpack import fft # Fast fourier transform
from scipy.io import wavfile
from scipy import stats
import numpy as np
import math
import time
import pandas as pd

time_1 = 60
time_2 = 150

def freq_band(frq):
    if frq < 60:
        return 'Subbass'
    elif frq < 250:
        return 'Bass'
    elif frq < 500:
        return 'Low Midrange'
    elif frq < 2000:
        return 'Midrange'
    elif frq < 4000:
        return 'Upper Midrange'
    elif frq < 6000:
        return 'Presence'
    elif frq < 20000:
        return 'Brilliance'
    elif frq > 20000:
        return 'Out of human hearing'

def band_generator(freq,intensity):
    DataSet = set(zip(freq,intensity))
    Subbass = []
    Bass = []
    Low_Midrange = []
    Midrange = []
    Upper_Midrange = []
    Presence = []
    Brilliance = []
    NA = []
    for data in DataSet:
        b_point = freq_band(data[0])
        if b_point == 'Subbass':
            Subbass.append([data[0],data[1],b_point])
        elif b_point == 'Bass':
            Bass.append([data[0],data[1],b_point])
        elif b_point == 'Low Midrange':
            Low_Midrange.append([data[0],data[1],b_point])
        elif b_point == 'Midrange':
            Midrange.append([data[0],data[1],b_point])
        elif b_point == 'Upper Midrange':
            Upper_Midrange.append([data[0],data[1],b_point])
        elif b_point == 'Presence':
            Presence.append([data[0],data[1],b_point])
        elif b_point == 'Brilliance':
            Brilliance.append([data[0],data[1],b_point])
        else:
            NA.append([data[0],data[1],b_point])
    return [Subbass,Bass,Low_Midrange,Midrange,Upper_Midrange,Presence,Brilliance,NA]



def analyze_song(SONG_PATH):

    bit_rate, data = wavfile.read(SONG_PATH)
    t_1 = bit_rate*time_1 # Create a sub section of the data to analyze
    t_2 = bit_rate*time_2 # Length of song can increase data points, dont want that.
    data = data[t_1:t_2]

    normalized_data = [(dp / 2 ** 16) * 2 - 1 for dp in data]
    norm_fft = fft(normalized_data)
    real_fft = int(len(norm_fft) / 2)
    real_fft_data = abs(norm_fft[:(real_fft-1)])
    log_fft = [math.log(x, 10) for x in real_fft_data]
    for (pos ,point) in enumerate(log_fft):
        if point < 0 :
            log_fft[pos]=0
    k = np.arange(len(real_fft_data))
    T = len(data) / bit_rate
    frq_axis = k / T
    means = []
    audio_class = band_generator(frq_axis,log_fft)
    for frq_band in audio_class:
        frq_ax = [item[0] for item in frq_band]
        frq_app = [item[1] for item in frq_band]
        sum = 0
        for item in frq_band:
            sum += item[1]
        if len(frq_band) > 0:
            mean_y = sum/len(frq_band)
        else:
            mean_y = 0
        means.append(mean_y)
        rand_color = np.random.rand(3,)
        plt.plot(frq_ax,frq_app,'o', c = rand_color)
        plt.axhline(y=mean_y, c = rand_color, linestyle='-')
    plt.show()
    plt.show()
    return means
    slope, intercept, r_value, p_value, std_err = stats.linregress(frq_axis, log_fft)
 #   return [slope,intercept,r_value,p_value,std_err]
Cols = ['Subbass','Bass','Low Midrange','Midrange','Upper Midrange','Presence','Brilliance','Out of hearing']
print(analyze_song('../Sexual_Healing.wav'))
print(analyze_song('../Toto-Africa.wav'))