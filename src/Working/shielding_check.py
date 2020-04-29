import numpy as np
import csv

# testing code
# collect spectrum for ba-133
collection_time = 300
# data = np.zeros(2048)
# for i in range(12):
#     data += so.simplespectrum(collection_time)

# -----------------------------------------------------------------------------
    # Step 1: Collect the background
# -----------------------------------------------------------------------------

# background = np.loadtxt('megadata-910V-300s-background.csv',delimiter=',')
#
# # -----------------------------------------------------------------------------
#     # Step 2: Calibrate with Cs137
# # -----------------------------------------------------------------------------
#     # collect raw spectrum
# cs137_raw = np.loadtxt('megadata-910V-300s-cesium-137.csv',delimiter=',')
# cs137 = cs137_raw - background # subtract the background

# -----------------------------------------------------------------------------
    # Step 3: Check that there is not too much shielding using Cs-137 peak
# -----------------------------------------------------------------------------
distances = [50,75,100] # in cm
# look for peaks, define these regions of interest manually
# This is for Cs-137
# cs_min = 634
# cs_max = 738

# Collects and calculates the counts per second in a given interval
def get_cps(spectrum, min_kev, max_kev, a):
    total_count = 0
    n = 2048
    channels = np.arange(1,n+1)
    energies = np.zeros(n)
    for i in range(0,n):
        energies[i] = a*channels[i]

    for i in range(0,n):
        if (energies[i] >= min_kev and energies[i] <= max_kev):
            total_count += spectrum[i]
    peak_cps = total_count / collection_time # number of counts per sec for this region
    # print(peak1_cps)
    return peak_cps

# Calculates the average background counts per second for a given interval
def avg_background(min_kev, max_kev, a):
    n = 2048
    channels = np.arange(1,n+1)
    energies = np.zeros(n)
    for i in range(0,n):
        energies[i] = a*channels[i]
    temp = []
    for i in range(0,n):
        if (energies[i] >= min_kev and energies[i] <= max_kev):
            temp.append(background[i])
    return np.average(temp) / collection_time

# Takes in a spectrum and outputs the expected signal and S/N ratio
# with 2 cm of shielding in a warhead configuration.
def calculate_signal(spectrum, min_kev, max_kev, distance):
    cps = get_cps(spectrum, min_kev, max_kev)

    G = 0.1
    d = 20 # distance from source to detector
    activity1 = cps / (G*3.14*2.54**2/(4*3.14*d**2)*0.5)
    # print(activity1)

    # constants
    shielding = 2 # cm
    density_pb = 11.342 # g/cm^3
    mu_pb = .07

    signal = G*np.exp(-shielding*density_pb*mu_pb)*3.14*2.54**2/(4*3.14*distance**2)*.5*activity1

    # signal to noise ratio
    # collect average background
    s2n = signal / avg_background(min_kev,max_kev)
    return signal, s2n

def check_shielding_run(distances, na_noshielding, min, max, data50, data75, data100, a):
    signals = []
    ref_s2n_list = []
    # this builds the reference signal to noise ratios to compare with using Cs-137
    for i in range(0, len(distances)):
        temp1, temp2 = calculate_signal(na_noshielding, min, max,distances[i])
        signals.append(temp1)
        ref_s2n_list.append(temp2)

    # print(s2ns)

    # measure at 50 cm:
    # data50 = np.loadtxt('ba-133.csv',delimiter=',') # placeholder for now, would collect a full spectrum and subtract background
    cps50 = get_cps(data50,min,max, a)

    # measure at 75 cm:
    # data100 = np.loadtxt('ba-133.csv',delimiter=',') # placeholder for now, would collect a full spectrum and subtract background
    cps100 = get_cps(data75,min,max, a)

    # measure at 100 cm:
    # data125 = np.loadtxt('ba-133.csv',delimiter=',') # placeholder for now, would collect a full spectrum and subtract background
    cps125 = get_cps(data100,min,max, a)

    # Calculate all signal to noise ratios and put in a list
    avg_bg = avg_background(min,max, a)
    s2n_list = [cps50/avg_bg, cps100/avg_bg, cps125/avg_bg]
    print(ref_s2n_list)
    print(s2n_list)

    excessive_shielding = False
    for i in range(0,len(s2n_list)):
        if (s2n_list[i] < ref_s2n_list[i]):
            excessive_shielding = True

    return excessive_shielding

#     if (excessive_shielding): print('shielding exceeds limit allowed.')
#     else: print('shielding acceptable.')


# -----------------------------------------------------------------------------
    # Verify shielding does not exceed 2 cm (1 cm thick shell surrounding core)
# -----------------------------------------------------------------------------

# cs_137_signals, cs_137_s2n = calculate_signals(634,738,cs137) # calculate the expected based on collected data (cs137)
# print (s2n0)
