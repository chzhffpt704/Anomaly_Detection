from scipy.stats import skew, kurtosis
import pandas as pd
import numpy as np

class Feature_extractor:
    def __init__(self, data):
        self.Features = []
        self.Data = data['acceleration']

    def AbsMax(self):
        self._AbsMax = np.abs(self.Data.max())
        return self._AbsMax

    def AbsMean(self):
        self._AbsMean = np.abs(self.Data.mean())
        return self._AbsMean

    def Mean(self):
        self._Mean = self.Data.mean()
        return self._Mean

    def Variance(self):
        self._Variance = self.Data.var()
        return self._Variance

    def P2P(self):
        self._P2P = self.Data.max() - self.Data.min()
        return self._P2P

    def Skewness(self):
        self._Skewness = skew(self.Data)
        return self._Skewness

    def Kurtosis(self):
        self._Kurtosis = kurtosis(self.Data)
        return self._Kurtosis

    def RMS(self):
        self._RMS = np.sqrt(np.sum(self.Data**2)/len(self.Data))
        return self._RMS

    def CrestFactor(self):
        self._CrestFactor = self.P2P()/self.RMS()
        return self._CrestFactor

    def ShapeFactor(self):
        self._ShapeFactor = self.RMS()/self.AbsMean()
        return self._ShapeFactor

    def ImpulseFactor(self):
        self.ImpulseFactor = self.AbsMax()/self.AbsMean()
        return self.ImpulseFactor

    def Feature(self):
        self.Features.append(self.AbsMax())        # Feature 1: Absolute Maximum 
        self.Features.append(self.AbsMean())       # Feature 2: Absolute Mean
        self.Features.append(self.P2P())           # Feature 3: Peak-to-Peak
        self.Features.append(self.RMS())           # Feature 4: Root-mean-square
        self.Features.append(self.Skewness())      # Feature 5: Skewness
        self.Features.append(self.Kurtosis())      # Feature 6: Kurtosis
        self.Features.append(self.CrestFactor())   # Feature 7: Crest Factor
        self.Features.append(self.ShapeFactor())   # Feature 8: Shape Factor
        self.Features.append(self.ImpulseFactor()) # Feature 9: Impulse Factor
        return self.Features
    
class Freq_extractor:
    def __init__(self, data, Hz, Fs):
        self.Data = data['acceleration']
        self.Fs = Fs #Sampling rate
        self.Rpm = Hz/60 # RPM
        
    
    def FFT(self):
        _N = len(self.Data)
        _dt = 1/self.Fs
        _yf_temp = np.fft.fft(self.Data)
        self.yf = np.abs(_yf_temp[:_N // 2]) / (_N/2) # 길이 조정 
        self.xf = np.fft.fftfreq(_N, d= _dt)[:_N // 2]
        return self.xf, self.yf
    
    def Freq_Freatures(self):
        _xf,_yf = self.FFT()
        # 주파수 위치 추출 (절대값 이후 가장 낮은 값을 추출해야 f_1x에 가장 가까운 위치를 뽑아줄꺼아냐)
        f_1x = self.Rpm
        fre_nx = [f_1x*i for i in range(1,5)] #1~4x 주파수
        idx_nx = [np.argmin(np.abs(_xf - fr)) for fr in fre_nx] # 주파수 위치 추출
        self.fft_nx = _yf[idx_nx] # fft 1~4x 값
        return self.fft_nx
            