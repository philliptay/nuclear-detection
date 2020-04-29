#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:39:46 2020

@author: aglaser
"""

# ----------------------------------------------------------------------
# Initialize
# ----------------------------------------------------------------------

import Utilities

import matplotlib.pyplot as plt
import time
import csv
import numpy as np

Utilities.setup()

from DeviceFactory import *
from ParameterCodes import *
from CommandCodes import *
from ParameterTypes import *
from PhaData import *

# ----------------------------------------------------------------------

imode = 1 # Standard input mode of OSPREY
group = 1 # Memory group

# Stabilized_Probe_Busy = 0x00080000
# Stabilized_Probe_OK = 0x00100000

dtb = DeviceFactory.createInstance(DeviceFactory.DeviceInterface.IDevice)

# to collect data each time
def collect_data():
    data = np.zeros(2048)

    for i in range(1):
        data += simplespectrum(10)

    return data

# ----------------------------------------------------------------------
# Function to log into OPSREY and take control
# ----------------------------------------------------------------------

def connect2osprey(ipaddress):

    dtb.open("", ipaddress)

    name = dtb.getParameter(ParameterCodes.Network_MachineName, 0)

    dtb.lock("administrator", "mae354#cov!id=cs137", imode)

    dtb.control(4, imode) # Stop acquisition (4)

    dtb.setParameter(ParameterCodes.Input_Mode, 0, imode) # Set to PHA mode
    dtb.setParameter(ParameterCodes.Preset_Options, 0, imode) # No presets
    dtb.setParameter(ParameterCodes.Input_CurrentGroup, group, imode)
    dtb.control(CommandCodes.Clear, imode) # Clear data and time

    print("Connected to:", name)

    return

# ----------------------------------------------------------------------
# FUNCTIONS TO CONTROL HIGH VOLTAGE
# ----------------------------------------------------------------------

def HVon(voltage):

    if voltage > 1000: voltage = 1000 # Limit maximum voltage

    dtb.setParameter(ParameterCodes.Input_Voltage, int(voltage), imode)
    dtb.setParameter(ParameterCodes.Input_VoltageStatus, True, imode)

    while(dtb.getParameter(ParameterCodes.Input_VoltageRamping, imode) is True):
        print("HV is ramping up ... %d V"%(dtb.getParameter(ParameterCodes.Input_VoltageReading, imode)))
        time.sleep(.2)

    print("HV is ON!")

    return

# ----------------------------------------------------------------------

def HVoff():

    dtb.setParameter(ParameterCodes.Input_Voltage, 0, imode)
    dtb.setParameter(ParameterCodes.Input_VoltageStatus, True, imode)

    while(dtb.getParameter(ParameterCodes.Input_VoltageRamping, imode) is True):

        print("HV is going down ... %d V"%(dtb.getParameter(ParameterCodes.Input_VoltageReading, imode)))
        time.sleep(.2)

    print("HV is OFF!")

    return

# ----------------------------------------------------------------------
# FUNCTIONS TO ACQUIRE SPECTRA
# ----------------------------------------------------------------------

def simplespectrum(acqtime): # Specify time in seconds

    dtb.control(CommandCodes.Start, imode) # Start acquisition

    time.sleep(acqtime) # Wait until time is up

    sd = dtb.getSpectralData(imode, group)
    spec = sd.getSpectrum()

    cnts = spec.getCounts()

    dtb.control(CommandCodes.Stop, imode) # Stop acquisition
    dtb.control(CommandCodes.Clear, imode) # Clear data

    return cnts

# ----------------------------------------------------------------------

# This function is similar to simplespectrum,
# but requests data from the detector as often as possible
# and uses the detector clock

def timedspectrum(acqtime): # Specify time in seconds

    dtb.control(CommandCodes.Start, imode) # Start acquisition

    liveT = 0
    total = 0

    while (liveT < acqtime):

        sd = dtb.getSpectralData(imode, group)
        spec = sd.getSpectrum()

        cnts = spec.getCounts()
        bins = spec.getNumberOfChannels() # Not used

        total = sum(cnts)

        liveT = sd.getLiveTime()/1000000.0
        realT = sd.getRealTime()/1000000.0 # Not used

    dtb.control(CommandCodes.Stop, imode) # Stop acquisition
    dtb.control(CommandCodes.Clear, imode) # Clear data

    return cnts

# ----------------------------------------------------------------------

def countspectrum(target): # Specify number of desired counts

    dtb.control(CommandCodes.Start, imode) # Start acquisition

    liveT = 0
    total = 0

    while (total < target):

        sd = dtb.getSpectralData(imode, group)
        spec = sd.getSpectrum()

        cnts = spec.getCounts()
        bins = spec.getNumberOfChannels() # Not used

        total = sum(cnts)

        liveT = sd.getLiveTime()/1000000.0 # Not used
        realT = sd.getRealTime()/1000000.0 # Not used

    dtb.control(CommandCodes.Stop, imode) # Stop acquisition
    dtb.control(CommandCodes.Clear, imode) # Clear data

    return cnts

#%%

# ----------------------------------------------------------------------
# SIMPLE RUN
# ----------------------------------------------------------------------

# Detector 1 is "128.112.35.172"
# Detector 2 is "128.112.35.212"

#connect2osprey("128.112.35.172")
#
# HVon(870)
# data = np.zeros(2048)
#
# for i in range(12):
#     data += simplespectrum(60)
#
# np.savetxt('dataDetector1background.csv',data,delimiter=',')
#
# spectrum2 = countspectrum(50000) # Total counts in spectrum

#HVoff()


# plt.figure()
# plt.plot(data)
# plt.plot(spectrum2)
# plt.xlim(-50,2050)
# plt.ylim(-10,310)
# plt.grid(True)
# plt.savefig('spectrumDetector1background.pdf', format='pdf')
# plt.show()

# ----------------------------------------------------------------------
# THE END
# ----------------------------------------------------------------------
