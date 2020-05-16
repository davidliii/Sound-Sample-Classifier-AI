#############################################
# Module to calculate features from         #
# audio objects                             #
#############################################
import numpy as np
import matplotlib.pyplot as plt
import math
from read_wave import *
from file_manage import *

class FeatureObj:
    def __init__(self, signal, sampleRate, filename):
        self.filename = filename[10:len(filename)-4]
        self.sampleRate = sampleRate
        self.signal = signal
        self.duration = len(self.signal) / self.sampleRate

        # Features:
        self.zeroCrossingRate = self.calcZeroCrossingrate()
        self.fft = self.calcFFT()
        self.filterBanks = self.calcFilterBanks()
        self.mfcc = self.calcMFCC()

    def calcZeroCrossingrate(self):
        # Formula from : https://en.wikipedia.org/wiki/Zero-crossing_rate
        data = self.signal
        T = len(data)
        numCrossings = 0

        for t in range(1, T):
            if data[t] * data[t-1] < 0:
                numCrossings += 1

        return numCrossings / T

    def calcFFT(self):
        freq = np.fft.rfftfreq(len(self.signal), d=1/self.sampleRate)
        full_fft = np.fft.rfft(self.signal)
        response = abs(full_fft / len(full_fft)) # normalize (can also try len(full_fft) or max(abs(full_fft)))
        return (response, freq)

    def calcFilterBanks(self):
        frame_length = 0.02
        frame_offset = 0.01

        pointsToRead = math.floor(self.sampleRate * frame_length)
        pointsOffset =  math.floor(self.sampleRate * frame_offset)

        fft_frames = []
        return

    def calcMFCC(self):
        '''
        Algorithm: http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/
        1. get time frames of time domain signal (20 ms in length, each frame offset by around 10 ms)
        2. On each time frame, perform FFT, and retrive the absolute value normalized (same as regular FFT)
           Now we have the FFTs of many frames of audio data over time, we'll call them fft_frames
        3. For each fft_frame, compute the Mel-spaced filterbank (26 total).
                a. Set lower and upper bounds on the range of frequencies (eg. 300 Hz to 10,000 Hz)
                b. Convert the bounds to mels
                c. If we use 26 filters, we will need 28 equally spaced points between the mel bounds
                d. Convert the 28 points back to Hz
                e. Filters are built using these points now, each ranges three points.
                   eg. Filter 1: (p1: 0, p2: 1, p3: 0) Filter 2: (p2: 0, p3: 1, p4: 0)
                   To do this, we need to calculate lines between points to form triangular filters
                f. Apply the each filter over the fft_frame by multiplying the corresponding frequencies
                   and add up the coefficients.
                g. Take the log of each of the 26 coefficients to get filterbank energies
                h. Take DCT of each energy to get MFCC (only keep the lower 13)
        '''
        return


def plotFeatures(featureObjs):
    numCols = len(featureObjs) # show these along the horizontal (columns)
    numRows = 4 # Time domain, FFT, frequency banks, MFCC

    fig, ax = plt.subplots(nrows=numRows, ncols=numCols, sharey=False, figsize=(16, 9))
    plt.subplots_adjust(left=0.075, right=.975, top=0.9, bottom=0.05)
    fig.suptitle('Feature Plots')
    for i in range(numCols):
        ax[0, i].set_title(featureObjs[i].filename)

    ax[0, 0].set_ylabel('Time Domain')
    ax[1, 0].set_ylabel('FFT')
    ax[2, 0].set_ylabel('Filter Banks')
    ax[3, 0].set_ylabel('MFCC')

    for i in range(numCols):
        # Plot time domain signal
        frames = range(len(featureObjs[i].signal))
        time = [frame / featureObjs[i].sampleRate for frame in frames]
        ax[0, i].plot(time, featureObjs[i].signal, '#ff7878')
        ax[0, i].set_facecolor('#e0e0e0')

    for i in range(numCols):
        ax[1, i].plot(featureObjs[i].fft[1], featureObjs[i].fft[0], '#ff7878')
        ax[1, i].set_facecolor('#e0e0e0')


data1, sr1 = read_wave(test_file_1)
data2, sr2 = read_wave(test_file_2)
data3, sr3 = read_wave(test_file_3)
data4, sr4 = read_wave(test_file_4)
data5, sr5 = read_wave(test_file_5)


f1 = FeatureObj(data1, sr1, test_file_1)
f2 = FeatureObj(data2, sr2, test_file_2)
f3 = FeatureObj(data3, sr3, test_file_3)
f4 = FeatureObj(data4, sr4, test_file_4)
f5 = FeatureObj(data5, sr5, test_file_5)

plotFeatures([f1, f2, f3, f4, f5])
plt.show()
