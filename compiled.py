from weapon_signatures_ultra import *
from data-collection-script import check_counts_barium
from shielding_check import *
import sys

# 1. collect data: background (x3), barium, cobalt, sodium

# 2. average the backgrounds
background = avg_background()

# 3. check for shielding. terminate if not below the limit
distances = [50,100,125] # in cm
cs_min = 634
cs_max = 738

excessive_shielding = check_shielding_run(distances, cs_min, cs_max)
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

# 4. calibrate with sodium
(a,b) = sodium_calibrate(background) # in weapon_signatures_ultra

# 5. get weapon signatures for Ba-133 and Co-60
co_ba_data = co_ba_data_find(background)
(ba1_s2n, ba2_s2n) = barium_weapon_sig(background, co_ba_data)
(co1_s2n, co2_s2n) = cobalt_weapon_sig(background, co_ba_data)

# 6. verify the absence of fissile material
match = verify(background)
if match:
    print('barium found!')
else:
    print('barium not found!')

# ?? do we need this?
exceeds_boolean = check_counts_barium(a,b,background)
