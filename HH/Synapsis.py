# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:47:51 2022

@author: dell2
"""
import numpy as np
 
class Synapsis():
    def __init__(self, type, iter, step):
        self.type = type
        if type == 1:
            self.Esyn = 0 # 抑制性的为-50 兴奋性的为0
        else:
            self.Esyn = -80
 
        self.step = step # 步长0.01 ms
        self.iter = iter
        self.t = np.zeros(iter)
        self.g = np.zeros(iter)
        self.g_mid = np.zeros(iter)
        self.g[0] = 0
        self.I = np.zeros(iter)
        self.I[0] = 0

    def heav(self, x):
        return 1 if x>0 else 0

    def oula(self, i, v, ts):
        # for j in range(len(ts)):
        #     for k in range(0, i):
        #         # self.g[i] = self.g[i] + 1 * self.heav(i-ts[j]) * np.exp(-(i - ts[j]) / 5)
        #         self.g_mid[i] = self.g_mid[i] + 0.4 * self.heav(k-ts[j]) * np.exp(-(k - ts[j]) / 5)
        #         # self.g_mid[i] = 40 * np.exp(-(i - ts[j]) / 5)
        #         if self.g_mid[i] < 0:
        #             self.g_mid[i] = 0
        #     self.g[i] = self.g[i] + self.g_mid[i]

        for j in range(len(ts)):
            # self.g[i] = self.g[i] + 1 * self.heav(i-ts[j]) * np.exp(-(i - ts[j]) / 5)
            self.g_mid[i] = self.g_mid[i] + 0.4 * self.heav(i-ts[j]) * ((i - ts[j]) / 500) * np.exp(-(i - ts[j]) / 500)
            # self.g_mid[i] = 40 * np.exp(-(i - ts[j]) / 5)
            if self.g_mid[i] < 0:
                self.g_mid[i] = 0
        self.g = self.g_mid

        # self.g[i] = self.g[i-1] + self.g[i]
        # print(i, self.g[i - 1], self.g[i])
        # for j in range(len(self.g_mid)):
        #     self.g[i] += self.g_mid[j]
        # self.g = self.g_mid
        self.I[i] = - self.g[i] * (v - self.Esyn)
        return self.I, self.g, self.t

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    iters = 1000
    syn = Synapsis(1, iters, 0.01)
    for i in range(1, iters):
        syn.oula(i, -20, [100])

    t = [i for i in range(iters)]
    plt.plot(t,syn.g)
    plt.title('Conductive')
    plt.xlabel('t(ms)')
    plt.ylabel('g(s/m)')
    plt.show()

    plt.plot(t,syn.I)
    plt.title('Conductive')
    plt.xlabel('t(ms)')
    plt.ylabel('g(s/m)')
    plt.show()