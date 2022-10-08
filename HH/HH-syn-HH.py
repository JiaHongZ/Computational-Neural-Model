# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:49:12 2022

@author: dell2
"""
import Neuron
import matplotlib.pyplot as plt
import numpy as np
import Synapsis

type = 0
step = 0.01
iters = int(100/step)
I = [20] * iters
# 没多少步做一次spike记录
neuron1 = Neuron.Neuron(iters,step)
syn = Synapsis.Synapsis(type,iters,step)
neuron2 = Neuron.Neuron(iters,step)

for i in range(1, iters):
    t1, v1 = neuron1.oula(i, I[i])
    ts = neuron1.spike_2()
print(ts)
for i in range(1, iters):
    syn.oula(i, neuron2.V[i-1], ts[0])
    t2, v2 = neuron2.oula(i, syn.I[i]+5)


t = [i for i in range(iters)]
plt.plot(t,neuron1.V,label='neuron1')
plt.plot(t,neuron2.V,label='neuron2')
plt.title('V')
plt.xlabel('t(ms)')
plt.ylabel('v(mV)')
plt.legend()
plt.show()

plt.plot(t,syn.g)
plt.title('Conductive')
plt.xlabel('t(ms)')
plt.ylabel('g(s/m)')
plt.show()

plt.plot(t,syn.I)
plt.title('Isyn')
plt.xlabel('t(ms)')
plt.ylabel('I(mA)')
plt.show()


