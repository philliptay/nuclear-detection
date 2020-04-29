from weapon_signatures_ultra import *
from shielding_check import *
from simple_osprey_2020 import *
import sys
import numpy as np

# setup (copied from simple-osprey-2020.py)
imode = 1 # Standard input mode of OSPREY
group = 1 # Memory group
dtb = DeviceFactory.createInstance(DeviceFactory.DeviceInterface.IDevice)

# connect to osprey
connect2osprey("128.112.35.172")
HVon(910)


# 1. collect data: background (x3)
print('Please point the sensor towards the background. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running background collection 1')
data1 = collect_data()

# print('Background collection 1 complete. Please change location of background detector. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running background collection 2')
# data2 = collect_data()

# print('Background collection 2 complete. Please change location of background detector. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running background collection 3')
# data3 = collect_data()
# print('Background collection 3 complete.')

# 2. average the backgrounds
# background = avg_backgrounds(data1, data2, data3)
background = data1

# 3. collect data: sodium
print('Now, please point the sensor to sodium and place it 50 cm away. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection for sodium calibration 1')
na_raw1 = collect_data()

print ('Sodium data 1 collected. Please ready the sensor for reading 2. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection for sodium calibration 1')
na_raw2 = collect_data()
print ('Sodium data 2 is collected')

# 4. calibrate with sodium
(a,b) = sodium_calibration(background, na_raw1, na_raw2) # in weapon_signatures_ultra
na_noshielding =  na_raw1 - background


# 5. collect data: material at 50cm, 75cm, 100cm
print('Now, please point the sensor to the material and place it 50cm away from the material. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection at 50cm')
data50 = collect_data() - background

print('Data collection at 50cm complete. Please move the sensor to 75cm. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection at 75cm')
data75 = collect_data() - background

print('Data Collection at 75cm is complete. Please move the sensor to 100cm. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection at 100cm')
data100 = collect_data() - background
print('Data collection at 100cm is complete')

# 6. check for shielding. terminate if not below the limit
distances = [50,75,100] # in cm
min = 481
max = 576

excessive_shielding = check_shielding_run(distances, na_noshielding, min, max, data50, data75, data100, a)
if (excessive_shielding):
    print('the shielding level is within the accepted range.')
    print('would you like to continue? (Y/N)')
    answer = input()
    if answer != 'Y':
        print('answer is not yes, so program is shutting')
        sys.exit()
else:
    print('the shielding level is beyond accepted range.')
    print('program is shutting down')
    sys.exit()

# 7. data collection: final fissile material (x3)
print('Please point the sensor at the material for reading 1. When ready, input Y and press enter')
ans = input()
while ans != 'Y':
    ans = input()
print('Running data collection 1')
material_data1 = collect_data() - background

# print('Reading 1 complete. Please ready the sensor for reading 2. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running data collection 2')
# material_data2 = collect_data() - background

# print('Reading 2 complete. Please ready the sensor for reading 3. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running data collection 3')
# material_data3 = collect_data() - background
# print ('Reading 3 is complete')

# 8. verify the absence of fissile material
(bmatch1, cmatch1) = verify(material_data1, a)
# (bmatch2, cmatch2) = verify(material_data2, a)
# (bmatch3, cmatch3) = verify(material_data3, a)

# if (bmatch1 and bmatch2) or (bmatch1 and bmatch3) or (bmatch2 and bmatch3):
#     print('barium detected in a majority of the tests')
# else:
#     print('barium not detected in a majority of the tests')

# if (cmatch1 and cmatch2) or (cmatch1 and cmatch3) or (cmatch2 and cmatch3):
#     print('cobalt detected in a majority of the tests')
# else:
#     print('cobalt not detected in a majority of the tests')

if (bmatch1):
    print('barium detected')
if (cmatch1):
    print('cobalt deteceted')

HVoff()

# # 7. data collection: cobalt/barium ----- ??
# print('Please point the sensor at the material for reading 1. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running data collection 1')
# co_ba_1 = collect_data() - background

# print('Reading 1 complete. Please ready the sensor for reading 2. When ready, input Y and press enter')
# ans = input()
# while ans != 'Y':
#     ans = input()
# print('Running data collection 1')
# co_ba_2 = collect_data() - background
# print ('Reading 2 is complete')

# # 8. get weapon signatures for Ba-133 and Co-60 ---- ???
# co_ba_data = co_ba_data_find(background, co_ba_1, co_ba_2)
# (ba1_s2n, ba2_s2n) = barium_weapon_sig(background, co_ba_data)
# (co1_s2n, co2_s2n) = cobalt_weapon_sig(background, co_ba_data)

# ?? do we need this?
# exceeds_boolean = check_counts_barium(a,b,background)
