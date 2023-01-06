# -*- coding: utf-8 -*-
"""
Created on Tue May  4 00:10:56 2021

@author: SHUBHANKAR
"""

import matplotlib.pyplot as plt
import scipy
import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import winsound
import scipy.signal as signal
from scipy import fftpack

#Origninal Audio
samplerate, data_original = read("name.wav")
duration = len(data_original) / samplerate
time = np.arange(0, duration, 1 / samplerate)
plt.title("Original signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.plot(time, data_original)
plt.show()

transform = np.fft.fft(data_original)
N = len(data_original)
n = np.arange(N)
freq = n*(samplerate/N)
mag = abs(transform)


plt.title("FFT of original signal")
plt.xlabel("Freq")
plt.ylabel("Magnitude")
plt.plot(freq, mag)
plt.show()

#Noisy Audio
samplerate, data = read("noisySYB02new.wav") 

duration = len(data) / samplerate
time = np.arange(0, duration, 1 / samplerate)
plt.title("Noisy audio")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.plot(time, data)
plt.show()

transform = fftpack.fft(data)
N = len(data)
n = np.arange(N)
freq = n*(samplerate/N)
mag = abs(transform)

plt.title("FFT of noisy audio")
plt.xlabel("Freq")
plt.ylabel("Magnitude")
plt.plot(freq, mag)
plt.show()

#Filters
Fs=44100
nyq_rate =Fs/2
N1 = 1001   
N2 = 9501
N3 = 6001
a = signal.firwin(N1, cutoff = (180/nyq_rate), window = "hanning", pass_zero="highpass")
b = signal.firwin(N2, cutoff = (150/nyq_rate,160/nyq_rate, 240/nyq_rate,260/nyq_rate, 290/nyq_rate,310/nyq_rate, 340/nyq_rate,360/nyq_rate, 390/nyq_rate,410/nyq_rate, 440/nyq_rate,460/nyq_rate, 480/nyq_rate,520/nyq_rate, 580/nyq_rate,620/nyq_rate, 680/nyq_rate,710/nyq_rate,940/nyq_rate,960/nyq_rate,), window = "hanning", pass_zero="bandstop")
c = signal.firwin(N3, cutoff = (100/nyq_rate,650/nyq_rate), window = "hanning", pass_zero="bandpass")


filtered_x = signal.lfilter(c, 1.0, data)
filtered_x1 = signal.lfilter(b, 1.0, filtered_x)
filtered_x2 = signal.lfilter(a, 1.0, filtered_x1)

d1 = fftpack.fft(filtered_x)#Bandpass
d2 = fftpack.fft(filtered_x1)#Bandstop
d3 = fftpack.fft(filtered_x2)#Highpass

m1 = abs(d1)
m2 = abs(d2)
m3 = abs(d3)

plt.figure()
plt.xlim(0, 1000)
plt.title("Filter1 fft Bandpass")
plt.xlabel("Freq")
plt.ylabel("Magnitude")
plt.plot(freq,m1)
plt.show()

plt.figure()
plt.xlim(0, 1000)
plt.title("Filter2 fft Bandstop")
plt.xlabel("Freq")
plt.ylabel("Magnitude")
plt.plot(freq,m2)
plt.show()

plt.figure()
plt.xlim(0, 600)
plt.title("Filter3 fft High pass")
plt.xlabel("Freq")
plt.ylabel("Magnitude")
plt.plot(freq,m3)
plt.show()

x2 = 9*filtered_x2
write("Filter_audio.wav", samplerate, np.int16(x2))
winsound.PlaySound("Filter_audio.wav", winsound.SND_FILENAME)
samplerate,data=read("Filter_audio.wav")
duration= len(data)/samplerate
time=np.arange(0,duration,1/samplerate)


plt.figure()
plt.title("Filtered signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.plot(time,data)


FFT=fftpack.fft(data)
N=len(data)
n=np.arange(N)
f = n*(samplerate/N)
Mag = abs(FFT)

plt.figure()
plt.xlim(0,800)
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of filtered signal")
plt.plot(f,Mag)