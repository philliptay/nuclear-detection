# -*- coding: utf-8 -*-

"""

Created in March 2016

Simple Monte Carlo Random Walk Demo for Sphere

"""

import random
import numpy as np

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt

# import scipy

# ---------------------------------------------------------------------------
# Sampling isotropic direction (points on unit sphere)
# ---------------------------------------------------------------------------

def isotropic_direction():

    rnum1 = random.random()
    rnum2 = random.random()

    w = 1 - 2 * rnum1

    rho = np.sqrt(1 - w**2)

    phi = 2 * np.pi * rnum2

    u = rho * np.cos(phi)
    v = rho * np.sin(phi)

    return np.array([u, v, w])

# ---------------------------------------------------------------------------
# Propagate particle to new position
# ---------------------------------------------------------------------------

def new_position(pos, mfp):

    return pos - mfp * np.log(random.random()) * isotropic_direction()

# ---------------------------------------------------------------------------
# Radial coordinate of [x,y,z] position
# ---------------------------------------------------------------------------

def rad(position):

    r = np.sqrt(position[0]**2 + position[1]**2 + position[2]**2)

    return r

# ---------------------------------------------------------------------------
# Number of neutrons generated in fission event
# ---------------------------------------------------------------------------

# This choice gives an average of 2.455 neutrons (close to 2.47)

def simpnu():

    if random.random() < 0.53:
        nu = 2
    else:
        nu = 3

    return nu

# ---------------------------------------------------------------------------
# Defining some constants for the material and the configuration
# ---------------------------------------------------------------------------

# Cross section are given for 100% U-235 assempbly

sigma_tot = 8.15 #   Total cross section
sigma_fis = 1.24 # Fission cross section
sigma_cap = 0.14 # Capture cross section

density = 19.0 # Material density in g per cm^3

mfp = 235.04 / (6.022e23 * density * sigma_tot * 1e-24) # Total mean free path

# print(mfp)

radius = 8.6 # Radius of sphere

print(" ")
print("Radius of assembly =", radius)

mass = density / 1000.0 * 4.0 / 3.0 * np.pi * radius**3

print("  Mass of assembly =", round(mass,2))

# Probability of scattering

prob_sca = (sigma_tot - sigma_fis - sigma_cap) / sigma_tot

# Probability of fission after absorption

prob_fis = sigma_fis / (sigma_fis + sigma_cap)

# ---------------------------------------------------------------------------
# Running the demo
# ---------------------------------------------------------------------------

n_gen = 10000 # Number of neutrons per generation
cycles =  210 # Number of cycles

# Initial positions of neutrons (in first generation)

pos = np.zeros([n_gen, 3])

# Here, all neutrons start on the edge of the sphere

for i in range(n_gen):

    pos[i] = radius * isotropic_direction()

# Initialize k as a list

kefflist = []
radilist = []

# Run the Monte Carlo Simulation


for j in range(cycles):

    # Initialize the positions for the next generation

    nextgenpos = []

    for k in range(n_gen):

        # Pick a neutron

        currentpos = pos[k]

        leak = 0 # Neutron has not leaked
        abso = 0 # Neutron has not been absorbed

        # While the neutron keeps scattering and doesn't leak,
        # continue the random walk ...

        while (leak == 0 and abso == 0):

            # Determine new position

            currentpos = new_position(currentpos, mfp)

            if rad(currentpos) > radius:

                leak = 1 # The neutron has just leaked from the sphere

            elif random.random() > prob_sca:

                abso = 1 # The neutron has just been absorbed

        else:

            # If the neutron is absorbed, does it cause a fission event?

            if (leak == 0 and abso == 1 and random.random() < prob_fis):

                # If yes, then create new neutrons for the next generation
                # If not, then the neutron is forgotten

                for l in range(simpnu()): # Generate 2 or 3 new neutrons

                    # Append current position to next generation positions (nu) times

                    nextgenpos.append(currentpos)

    # Convert numpy arrays into a single one (Python hack)

    nextgenpos = np.array(nextgenpos)

    # At the end of every cycle,
    # append the current cycle value of k to the k list

    kefflist.append(np.float(len(nextgenpos))/np.float(len(pos)))

    # Pick n_gen neutrons at random for the next generation
    # This really isn't the best way to do this

    pos = nextgenpos[np.random.randint(len(nextgenpos),size=n_gen),:]

    #print(j)

    # Radial positions of all neutrons in cycle

    if (j >= 10):

        templist = np.array([rad(pos[x]) for x in range(len(pos))])
        radilist = np.append(radilist,templist)

# Finally, dump the results from the first 10 cycles and print k average

print(" ")
print("*** k(eff) =", np.mean(kefflist[10:])," ***")
print(" ")

# ---------------------------------------------------------------------------
# For use below: Solution of diffusion equation
# ---------------------------------------------------------------------------

b = 0.308

def n(r): return (1/0.308) * np.sin(0.308 * r) / r

# ---------------------------------------------------------------------------
# Determine neutron flux/density as a function of radius
# ---------------------------------------------------------------------------

# Number of bins and list of bins (for plot)

bins = 100
binlist = np.linspace(0.1,10,bins)

# Identify bin number for elements in radlist

digitized = np.digitize(radilist,binlist)

# Count number of neutrons in each bin and scale by (exact) volume

temp1 = np.bincount(digitized,minlength=bins)
temp2 = np.delete(np.append(binlist,0)**3-np.insert(binlist,0,0)**3,-1)
temp3 = temp1 / temp2

# ---------------------------------------------------------------------------
# Scale results for same area (dropping extrapolation length manually)
# ---------------------------------------------------------------------------

scale = sum(temp2[:-14]*n(binlist[:-14])) / sum(temp2[:-14]*temp3[:-14])

temp4 = scale * temp3

#%%

plt.plot(binlist,temp4)
plt.xlabel('Radius [cm]')
plt.ylabel('Neutron density [au]')

# ---------------------------------------------------------------------------
# Plot solution of diffusion equation
# ---------------------------------------------------------------------------

b = 0.308

def n(r): return (1/0.308) * np.sin(0.308 * r) / r

plt.plot(binlist,n(binlist))
plt.ylim(-0.03,1.03)
plt.grid(True)
plt.savefig('pythoncriticality.pdf',format='pdf')
plt.show()


# ---------------------------------------------------------------------------
# THE END
# ---------------------------------------------------------------------------
