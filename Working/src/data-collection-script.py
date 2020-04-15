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

# CALIBRATION

# find the peaks needed for calibration using Sodium
peak1_low = next(i for i, x in enumerate(channels) if x >= 600)
peak2_low = next(i for i, x in enumerate(channels) if x >= 1600)
peak1_high = next(i for i, x in enumerate(channels) if x >= 800)
peak2_high = next(i for i, x in enumerate(channels) if x >= 1800)

# find the peaks in these 2 ranges
peak1 = max(channels[peak1_low:peak1_high])
peak2 = max(channels[peak2_low:peak2_high])


# # check the energy ranges of Barium and find peak
# b_energies = []
# c_energies = 
# for i in range(0,n):
#     if energies[i] >= 265:
#         while energies[i] <= 425:
#             b_energies = energies[i]
#             i += 1
#         break

# bar_peak = max(b_energies)

# # check the energy ranges of Cobalt and find peaks
# c_energies = []
# for i in range(0,n):
#     if energies[i] >= 265:
#         while energies[i] <= 425:
#             b_energies = energies[i]
#             i += 1
#         break

# bar_peak = max(b_energies)
     

plt.figure()
plt.plot(data)
plt.plot(spectrum2)
plt.xlim(-50,2050)
plt.ylim(-10,310)
plt.grid(True)
plt.savefig('spectrumDetector1background.pdf', format='pdf')
plt.show()
