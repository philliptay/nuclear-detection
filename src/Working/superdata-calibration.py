#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:08:52 2020

@author: aglaser
"""

# ----------------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit

data0 = np.genfromtxt("../data/superdata-original-sources-060min.csv", delimiter=",")
time0 = 60 * 60

plt.plot(data0)
plt.show()

# No correction for background here

# ----------------------------------------------------------------------
# Smooth calibration dataset
# ----------------------------------------------------------------------

smooth = 7 # Use (2 x smooth + 1 points) for averaging

smoothdata0 = []

smoothdata0.extend(data0[:smooth]) # First elements (unsmoothed)

for i in range(smooth,len(data0)-smooth):

    smoothdata0.append(np.mean(data0[i-smooth:i+smooth]))

smoothdata0.extend(data0[-smooth:]) # Last elements (unsmoothed)

# ----------------------------------------------------------------------
# Analyze peaks and find their maximums
# ----------------------------------------------------------------------

roi1 = [ 550, 750]
roi2 = [1040,1230]
roi3 = [1200,1380]

# -----------------

roi = roi1

maxval = max(smoothdata0[roi[0]:roi[1]])
maxpos = roi[0] + smoothdata0[roi[0]:roi[1]].index(maxval)

plt.plot(data0)
plt.plot(smoothdata0)
plt.axvline(maxpos)
plt.xlim(roi[0],roi[1])
plt.show()

maxval1 = maxval
maxpos1 = maxpos # Channel number (center of peak)

# -----------------

roi = roi2

maxval = max(smoothdata0[roi[0]:roi[1]])
maxpos = roi[0] + smoothdata0[roi[0]:roi[1]].index(maxval)

plt.plot(data0)
plt.plot(smoothdata0)
plt.axvline(maxpos)
plt.xlim(roi[0],roi[1])
plt.show()

maxval2 = maxval
maxpos2 = maxpos # Channel number (center of peak)

# -----------------

roi = roi3

maxval = max(smoothdata0[roi[0]:roi[1]])
maxpos = roi[0] + smoothdata0[roi[0]:roi[1]].index(maxval)

plt.plot(data0)
plt.plot(smoothdata0)
plt.axvline(maxpos)
plt.xlim(roi[0],roi[1])
plt.show()

maxval3 = maxval
maxpos3 = maxpos # Channel number (center of peak)

# -----------------

channels = [maxpos1, maxpos2, maxpos3]
energies = [  661.7,  1173.2,  1332.5]

print('Channels:', channels)
print('Energies:', energies)


#%%

# ----------------------------------------------------------------------
# Calibration (quadratic, no offset)
# ----------------------------------------------------------------------

def calibrate(x,a,b):

	return a*x + b*(x**2)

popt, pcov = curve_fit(calibrate, channels, energies)

def cha2ene(x): # Channel to energy

	return popt[0]*x + popt[1]*(x**2)

# ----------------------------------------------------------
# Inverse calibration (convert from energy to channel number
# ----------------------------------------------------------

qopt, qcov = curve_fit(calibrate, energies, channels)

def ene2cha(x): # Energy to channel

	return qopt[0]*x + qopt[1]*(x**2)

# ----------------------------------------------------------------------

refenerg1 =  661.7
refwidth1 =   70.0

refenerg2 = 1173.2
refwidth2 =   80.0

channel1lo = int(ene2cha(refenerg1 - refwidth1))
channel1hi = int(ene2cha(refenerg1 + refwidth1))

channel2lo = int(ene2cha(refenerg2 - refwidth2))
channel2hi = int(ene2cha(refenerg2 + refwidth2))

# Plots are never (fully) calibrated; still use channel numbers on x-axis
# Regions of interest are defined by (and highlighted as) channel ranges

fig, ax = plt.subplots()
ax.plot(data0)
ax.axvspan(channel1lo, channel1hi, alpha=0.25, color='red')
ax.axvspan(channel2lo, channel2hi, alpha=0.25, color='red')
plt.axvline(ene2cha(refenerg1), linestyle=':', color='red')
plt.axvline(ene2cha(refenerg2), linestyle=':', color='red')
plt.grid(True)

# ----------------------------------------------------------------------

cps1 = int(1000*sum(data0[channel1lo:channel1hi])/time0)/1000
cps2 = int(1000*sum(data0[channel2lo:channel2hi])/time0)/1000

print()

print('Total counts in ROI1:', cps1, 'cps')
print('Total counts in ROI2:', cps2, 'cps')

# ----------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------
