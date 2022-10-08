# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 19:19:23 2022

@author: dell2
"""
import numpy as np
import matplotlib.pyplot as plt
from Synapsis import Synapsis as Syn
from scipy.signal import find_peaks

class Neuron():
    def __init__(self, iter, step, window=100):
        self.gl = 0.3
        self.gk = 36.0
        self.gna = 120.0
        self.El = -54.4
        self.Ek = -77.0
        self.Ena = 50.0
        self.Cm = 1.0
        self.V0 = -65.0

        # 反转电位-？
        self.v_threshold = 20
        # 不应期
        self.refs_default = 10
        self.refs = 10 # 10个step
        self.ref = False
        # spike trains
        self.ts = []

        self.step = step
        # self.window = window
        # self.iter = int(100/self.step)
        self.V = np.zeros(int(iter))
        self.V[0] = self.V0
        self.am = 0.1 * (self.V[0] + 40) / (1 - np.exp(-(self.V[0] + 40) / 10))
        self.bm = 4 * np.exp(-(self.V[0] + 65) / 18)
        self.ah = 0.07 * np.exp(-(self.V[0] + 65) / 20)
        self.bh = 1 / (np.exp(-(self.V[0] + 35) / 10) + 1)
        self.an = 0.01 * (self.V[0] + 55) / (1 - np.exp(-(self.V[0] + 55) / 10))
        self.bn = 0.125 * np.exp(-(self.V[0] + 65) / 80)
 
        self.m = self.am / (self.am + self.bm)
        self.h = self.ah / (self.ah + self.bh)
        self.n = self.an / (self.an + self.bn)
 
    def oula(self, i, I):

        self.am = 0.1 * (self.V[i-1] + 40) / (1 - np.exp(-(self.V[i-1] + 40) / 10))
        self.bm = 4 * np.exp(-(self.V[i-1] + 65) / 18)
        self.ah = 0.07 * np.exp(-(self.V[i-1] + 65) / 20)
        self.bh = 1 / (np.exp(-(self.V[i-1] + 35) / 10) + 1)
        self.an = 0.01 * (self.V[i-1] + 55) / (1 - np.exp(-(self.V[i-1] + 55) / 10))
        self.bn = 0.125 * np.exp(-(self.V[i-1] + 65) / 80)

        self.m = self.m + self.step * (self.am * (1 - self.m) - self.bm * self.m)
        self.h = self.h + self.step * (self.ah * (1 - self.h) - self.bh * self.h)
        self.n = self.n + self.step * (self.an * (1 - self.n) - self.bn * self.n)

        self.V[i] = self.V[i-1] + self.step * (
                    (-self.gl * (self.V[i-1] - self.El) - self.gna * self.m ** 3 * self.h * (self.V[i-1] - self.Ena)
                     - self.gk * self.n ** 4 * (self.V[i-1] - self.Ek) + I) / self.Cm)

        # self.am = 0.1 * (self.V[i] + 40) / (1 - np.exp(-(self.V[i] + 40) / 10))
        # self.bm = 4 * np.exp(-(self.V[i] + 65) / 18)
        # self.ah = 0.07 * np.exp(-(self.V[i] + 65) / 20)
        # self.bh = 1 / (np.exp(-(self.V[i] + 35) / 10) + 1)
        # self.an = 0.01 * (self.V[i] + 55) / (1 - np.exp(-(self.V[i] + 55) / 10))
        # self.bn = 0.125 * np.exp(-(self.V[i] + 65) / 80)
        #
        # self.m = self.m + self.step * (self.am * (1 - self.m) - self.bm * self.m)
        # self.h = self.h + self.step * (self.ah * (1 - self.h) - self.bh * self.h)
        # self.n = self.n + self.step * (self.an * (1 - self.n) - self.bn * self.n)

        # self.spike(i)

        return self.V[i], self.ts

    def spike_2(self):
        self.ts = find_peaks(self.V)
        return self.ts

    def spike(self, i):
        # if self.V[i] > self.v_threshold:
        #     self.ts.append(i)
        if self.ref == True:
            self.refs -= 1
            if self.refs <= 0:
                self.ref = False
        elif self.V[i] > self.v_threshold and self.ref == False:
            # self.V[i-1] = self.v_top
            # 进入不应期
            # self.V[i] = self.v_top
            self.ts.append(i)
            self.ref = True
            self.refs = self.refs_default
        return self.V[i], self.ts
        