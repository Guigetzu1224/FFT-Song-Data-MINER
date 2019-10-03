import matplotlib.pyplot as plt
from scipy.fftpack import fft # Fast fourier transform
from scipy.io import wavfile
from scipy import stats
import numpy as np
import math

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
    elif frq < 200000:
        return 'Brilliance'
    elif frq > 20000:
        return 'Out of human hearing'

def band_generator(freq,intensity):
    band = freq_band(freq)
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
    return [Subbass,Bass,Low_Midrange,Midrange,Upper_Midrange,Presence,Brilliance]



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
    data_array = set(zip(frq_axis,log_fft))
    frequency_list = []
    for d_point in data_array:
        band = freq_band(d_point[0])
        frequency_list.append([d_point[0],d_point[1],band])

    plt.plot(frq_axis,log_fft,'g')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(frq_axis, log_fft)
 #   return [slope,intercept,r_value,p_value,std_err]
    return frequency_list

print(analyze_song('../Sexual_Healing.wav'))
print(analyze_song('../Toto-Africa.wav'))