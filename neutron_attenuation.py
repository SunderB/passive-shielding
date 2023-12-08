import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json
from decimal import *
from astropy import constants as const
from astropy import units as u

# increase label text size to 14
font = {'size': 14}
plt.rc('font', **font)

DATA_DIR = "materials"

density = {}

with open(DATA_DIR + "/density.json") as f:
    data = json.load(f)
    density = data

# Loop through each file in the directory
data = pd.read_csv(DATA_DIR + "/neutron_att_coeff.csv", sep=',')

print("Density: " + str(density))
print(data)

# Input parameters
energy = 25.30e-3 * u.eV
max_count_rate = 0.1 / u.yr # 1 count per year
material = "lead"

material_data = data[data['material'] == material]

density = material_data['density'].values[0] * u.g / u.cm**3
molar_mass = material_data['molar_mass'].values[0] * u.g / u.mol
scat_coeff = material_data['scattering'].values[0] * u.barn
abs_coeff = material_data['absorption_2200'].values[0] * u.barn

# Calculate number density
number_density = (density * const.N_A / molar_mass).to(1/u.cm**3)
print(f"Number density: {number_density} cm^-3")

# Calculate the reduction in intensity required
print(f"Max count rate: {max_count_rate.to(1/u.s)} Hz = {max_count_rate} counts/year")

incoming_flux = 1.51e-7 / u.cm**2 / u.s # 1.3e-2 neutrons per cm^2 per second
surface_area = 5184 * u.cm**2 # cm^2
incoming_counts = (incoming_flux * surface_area).to(1/u.yr)
print(f"Incoming count rate: {incoming_counts.to(1/u.s)} Hz = {incoming_counts} counts/year")

reduction_required = (max_count_rate / incoming_counts).to(u.dimensionless_unscaled)
print(f"Reduction required: {reduction_required}")

# Scale the attenuation coefficients to match the neutron energy
velocity = np.sqrt(2 * energy / const.m_n).to(u.m/u.s)
print(f"Velocity: {velocity} m/s")

# Calculate the total attenuation coefficient
total_coeff = (scat_coeff).to(u.cm**2)
print(f"Total attenuation coefficient: {total_coeff}")

# Calculate the thickness required
thickness = (-(np.log(reduction_required))/(total_coeff * number_density)).to(u.cm)
print(f"Thickness required: {thickness} cm")

# print(material_data)
# scale_factor = ((2200 * u.m / u.s) / velocity).to(u.dimensionless_unscaled) # scales with 1/v
# print(f"Scale factor: {scale_factor}")
# abs_coeff = material_data['absorption_2200'].values[0] * u.barn
# abs_coeff = scale_factor * abs_coeff
# print(f"Absorption coefficient: {abs_coeff} cm^2")

# Calculate the total attenuation coefficient
total_coeff = (scat_coeff).to(u.cm**2)
print(f"Total attenuation coefficient: {total_coeff}")

# Calculate the thickness required
thickness = (-(np.log(reduction_required))/(total_coeff * number_density)).to(u.cm)
print(f"Thickness required: {thickness} cm")
