# To collect data, convert bin numbers to energy, pick up cps in regions
# defined on the spreadsheet

import simple-osprey-2020 as so
import Utilities

import matplotlib.pyplot at plt
import time
import csv
import numpy as np

Utilities.setup()

from DeviceFactory import *
from ParameterCodes import *
from CommandCodes import *
from ParameterTypes import *
from PhaData import *

imode = 1 # Standard input mode of OSPREY
group = 1 # Memory group

# Stabilized_Probe_Busy = 0x00080000
# Stabilized_Probe_OK = 0x00100000

dtb = DeviceFactory.createInstance(DeviceFactory.DeviceInterface.IDevice)


# ---------------------------
# Collecting the Data

# Detector 1 is "128.112.35.172"
# Detector 2 is "128.112.35.212"

connect2osprey("128.112.35.172")

so.HVon(870)
data = np.zeros(2048)

# how much time do we want to collect data for?
for i in range(12):
    data += so.simplespectrum(60)

np.savetxt('background1.csv',data,delimiter=',')

spectrum2 = so.countspectrum(50000) # Total counts in spectrum

so.HVoff()

# number of channels
n = len(data)
channels = np.arange(0,n) # create list corresponding to channels

# convert channels into energies
energies = []
for i in range(0,n):
    energies[i] = 0.87 * channels[i] + 23.45

plt.figure()
plt.plot(data)
plt.plot(spectrum2)
plt.xlim(-50,2050)
plt.ylim(-10,310)
plt.grid(True)
plt.savefig('spectrumDetector1background.pdf', format='pdf')
plt.show()
