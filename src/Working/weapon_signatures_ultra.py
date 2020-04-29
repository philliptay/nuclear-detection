import numpy as np
import csv

collection_time = 300

# to collect data each time
def collect_data():
    data = np.zeros(2048)

    for i in range(12):
        data += simplespectrum(60)

    return data

# -----------------------------------------------------------------------------
    # Collect and average the background
# -----------------------------------------------------------------------------
def avg_background(b1, b2, b3):
#     b1 = np.loadtxt('ultradata-background-300s-run1.csv',delimiter=',')
#     b2 = np.loadtxt('ultradata-background-300s-run2.csv',delimiter=',')
#     b3 = np.loadtxt('ultradata-background-300s-run3.csv',delimiter=',')
    background = []
    for i in range(0,len(b1)):
        background.append((b1[i]+b2[i]+b3[i])/3)

    return background

# -----------------------------------------------------------------------------
    # Calibration with Na-22
# -----------------------------------------------------------------------------
def sodium_calibration(background, na_raw1, na_raw2):
    # na_raw1 = np.loadtxt('ultradata-NOTHING-na022-300s-run1.csv',delimiter=',')
    # na_raw2 = np.loadtxt('ultradata-NOTHING-na022-300s-run2.csv',delimiter=',')
    na1 = smooth(na_raw1 - background)
    na2 = smooth(na_raw2 - background)
    na = []
    for i in range(0,len(b1)):
        na.append((na1[i]+na2[i])/2)

    na_peak1 = 511
    na_peak2 = 1275
    peak1 = 0
    na_peak1_ch = 0
    peak2 = 0
    na_peak2_ch = 0
    for i in range(0,1024):
        if (na[i] > peak1):
            peak1 = na[i]
            na_peak1_ch = i
    for j in range(1024,2048):
        if (na[j] > peak2):
            peak2 = na[j]
            na_peak2_ch = j

    # y = ax + b
    a = (na_peak2-na_peak1)/(na_peak2_ch-na_peak1_ch)
    b = na_peak1 - a*na_peak1_ch

    return (a,b)


# Collects and calculates the counts per second for the max gamma line in a given interval
def get_cps(spectrum, min_kev, max_kev):
    total_count = 0
    n = 2048
    channels = np.arange(1,n+1)
    energies = np.zeros(n)
    for i in range(0,n):
        energies[i] = a*channels[i] + b

    peak = 0
    ch = 0
    for i in range(0,n):
        if (energies[i] >= min_kev and energies[i] <= max_kev):
            # get max. point and check how that individual count changes
            if (spectrum[i]>peak):
                peak = spectrum[i]
                ch = i
    return peak / collection_time

# Calculates the average background counts per second for a given interval
def avg_background(min_kev, max_kev):
    n = 2048
    channels = np.arange(1,n+1)
    energies = np.zeros(n)
    for i in range(0,n):
        energies[i] = a*channels[i] + b
    temp = []
    for i in range(0,n):
        if (energies[i] >= min_kev and energies[i] <= max_kev):
            temp.append(background[i])
    avg = np.average(temp) / collection_time
    # print(avg)
    return avg

# Takes in a spectrum and outputs the expected signal and S/N ratio
# with 4 cm of shielding in a warhead configuration.
def calculate_signal(spectrum, min_kev, max_kev, distance):
    cps = get_cps(spectrum, min_kev, max_kev)
    G = 0.1
    d = 75 # distance from source to detector
    activity1 = cps / (G*3.14*2.54**2/(4*3.14*d**2)*0.5)

    # constants
    shielding = 4 # cm
    density_pb = 11.342 # g/cm^3
    mu_pb = .07

    signal = G*np.exp(-shielding*density_pb*mu_pb)*3.14*2.54**2/(4*3.14*distance**2)*.5*activity1
    # signal to noise ratio
    # collect average background
    s2n = signal / avg_background(min_kev,max_kev)
    return signal, s2n

distances = [75,100,150] # in cm

# ----------------------------------------------------------------------
# Smooth dataset
# ----------------------------------------------------------------------

def smooth(data):
    smooth = 7 # Use (2 x smooth + 1 points) for averaging

    smoothdata = []

    smoothdata.extend(data[:smooth]) # First elements (unsmoothed)

    for i in range(smooth,len(data)-smooth):

        smoothdata.append(np.mean(data[i-smooth:i+smooth]))

    smoothdata.extend(data[-smooth:]) # Last elements (unsmoothed)

    return smoothdata

# -----------------------------------------------------------------------------
    # Verify absence of fissile material
# -----------------------------------------------------------------------------

def verify(material_data, a):
    # smooth data
    smoothed_data = smooth(material_data)

    # we know that barium peak should be be at approx 696 counts
    barium_exists = False
    barium_peak1_energy = 324.075
    barium_peak2_energy = 380.7
    b1_low = int(275/a)
    b1_high = int(348/a)
    b2_high = int(418/a)
    max_in_barium_range1 = (np.where(smoothed_data[b1_low:b1_high] == np.amax(smoothed_data[b1_low:b1_high]))[0] + b1_low) * a
    max_in_barium_range2 = (np.where(smoothed_data[b1_high:b2_high] == np.amax(smoothed_data[b1_high:b2_high]))[0] + b1_high) * a
#     print (max_in_barium_range1)
#     print (max_in_barium_range2)
    for i in max_in_barium_range1:
        if (i > (barium_peak1_energy - 15)) and (i < (barium_peak1_energy + 15)):
            for j in max_in_barium_range2:
                if (j > (barium_peak2_energy - 15)) and (j < (barium_peak2_energy + 15)):
                    barium_exists = True

    # we know that cobalt peaks would be at approx 1209 and 1362
    cobalt_exists = False
    cobalt_peak1_energy = 1211
    cobalt_peak2_energy = 1365.33
    c1_low = int(1125/a)
    c1_high = int(1273/a)
    c2_high = int(1415/a)
    max_in_cobalt_range1 = (np.where(smoothed_data[c1_low:c1_high] == np.amax(smoothed_data[c1_low:c1_high]))[0] + c1_low) * a
    max_in_cobalt_range2 = (np.where(smoothed_data[c1_high:c2_high] == np.amax(smoothed_data[c1_high:c2_high]))[0] + c1_high) * a
#     print(max_in_cobalt_range1)
#     print(max_in_cobalt_range2)
    for i in max_in_cobalt_range1:
        if (i > (cobalt_peak1_energy - 15)) and (i < (cobalt_peak1_energy + 15)):
            for j in max_in_cobalt_range2:
                if (j > (cobalt_peak2_energy - 15)) and (j < (cobalt_peak2_energy + 15)):
                    cobalt_exists = True

    # return the presence of barium and cobalt
    return (barium_exists, cobalt_exists)

# -----------------------------------------------------------------------------
    # Ba-133
# -----------------------------------------------------------------------------

def co_ba_data_find(background, co_ba_1, co_ba_2):
    # co_ba_1 = np.loadtxt('ultradata-co060-ba133-300s-run1.csv',delimiter=',') - background
    # co_ba_2 = np.loadtxt('ultradata-co060-ba133-300s-run2.csv',delimiter=',') - background
    co_ba_data = []
    for i in range(0,len(co_ba_1)):
        co_ba_data.append((co_ba_1[i]+co_ba_2[i])/2) # average the 2 datasets

    return co_ba_data

def barium_weapon_sig(background, co_ba_data):
    # regions of interest
    ba_1a = 265
    ba_1b = 348
    ba_1c = 418

    ba1_signals = []
    ba1_s2n = []
    ba2_signals = []
    ba2_s2n = []

    # signal to noise
    # this builds the weapons signatures
    for i in range(0, len(distances)):
        temp1, temp2 = calculate_signal(co_ba_data,ba_1a,ba_1b,distances[i])
        ba1_signals.append(temp1) # peak 1
        ba1_s2n.append(temp2)
        temp3, temp4 = calculate_signal(co_ba_data,ba_1b,ba_1c,distances[i])
        ba2_signals.append(temp3) # peak 2
        ba2_s2n.append(temp4)

    print("Barium-133:")
    print(ba1_s2n)
    print(ba2_s2n)

    return (ba1_s2n, ba2_s2n)

# cps
# ba1_cps = get_cps(co_ba_data,ba_1a,ba_1b)
# print(ba1_cps)
# bg = avg_background(ba_1a,ba_1b)
# sig = ba1_cps / bg
# print (sig)

# -----------------------------------------------------------------------------
    # Co-60
# -----------------------------------------------------------------------------

def cobalt_weapon_sig(background, co_ba_data):
    # regions of interest
    co_1a = 1125
    co_1b = 1273
    co_1c = 1415

    co1_signals = []
    co1_s2n = []
    co2_signals = []
    co2_s2n = []

    # this builds the weapons signatures
    for i in range(0, len(distances)):
        temp1, temp2 = calculate_signal(co_ba_data,co_1a,co_1b,distances[i])
        co1_signals.append(temp1) # peak 1
        co1_s2n.append(temp2)
        temp3, temp4 = calculate_signal(co_ba_data,co_1b,co_1c,distances[i])
        co2_signals.append(temp3) # peak 2
        co2_s2n.append(temp4)

    print("Cobalt-60:")
    print(co1_s2n)
    print(co2_s2n)

    return (co1_s2n, co2_s2n)
