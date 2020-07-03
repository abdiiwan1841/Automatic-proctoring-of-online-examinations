from scipy.io import wavfile
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import subprocess


sample_rate, samples = wavfile.read('audio.wav')


import webrtcvad

vad = webrtcvad.Vad()
vad.set_mode(3)
import struct
#convert samples to raw 16 bit per sample stream needed by webrtcvad
raw_samples = struct.pack("%dh" % len(samples), *samples)
window_duration = .03 # duration in seconds

samples_per_window = int(window_duration * sample_rate + 0.5)

bytes_per_sample = 2
segments = []
count=0

for start in np.arange(0, len(samples), samples_per_window):
    stop = min(start + samples_per_window, len(samples))
    
    is_speech = vad.is_speech(raw_samples[start * bytes_per_sample: stop * bytes_per_sample], 
                              sample_rate = sample_rate)
    #print is_speech
    """ if is_speech:
        count=count+1y
        if count>10:
            print("Speaking")
            sys.stdout.flush() """
    segments.append(dict(
       start = start,
       stop = stop,
       is_speech = is_speech))

plt.figure(figsize = (10,7))
plt.plot(samples)

ymax = max(samples)
#print samples
#print segments
# plot segment identifed as speech
for segment in segments:
    if segment['is_speech']:
        plt.plot([ segment['start'], segment['stop'] - 1], [ymax * 1.1, ymax * 1.1], color = 'purple')

plt.xlabel('sample')
plt.grid()

speech_samples = np.concatenate([ samples[segment['start']:segment['stop']] for segment in segments if segment['is_speech']])
#print speech_samples

wavfile.write("out_f.wav",sample_rate,speech_samples )

#plt.ion()
plt.show()
