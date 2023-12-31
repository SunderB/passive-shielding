import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json
from decimal import *

# increase label text size to 14
font = {'size': 14}
plt.rc('font', **font)

DATA_DIR = "materials"

gamma_att_coeff = {}
density = {}

layers = [
    ["lead", 20],
    ["copper", 10]
]

# with open(DATA_DIR + "/density.json") as f:
#     data = json.load(f)
#     density = data

# def get_layer_description(layers):
#     description = ""
#     for layer in layers:
#         description += layer[0] + " (" + str(layer[1]) + " cm), "
#     return description[:-2]

for filename in os.listdir(DATA_DIR + "/gamma_att_coeff"):
    if (filename == ".DS_Store" or filename == "desktop.ini"):
        continue

    print("Plotting " + filename)
    # Read in the data
    df = pd.read_csv(DATA_DIR + "/gamma_att_coeff/" + filename, sep=',')
    material_name = filename.split(".")[0]

    # Calculate the gamma attenuation coefficient for 2.615 MeV
    gamma_energy = 2.615
    gamma_att_coeff[material_name] = np.interp(gamma_energy, df['energy'], df['coeff'])



print("Gamma attenuation coefficients:")

df = pd.read_csv(DATA_DIR + "/neutron_att_coeff.csv", sep=',')
print("Attenuation coefficients: " + str(gamma_att_coeff))
    
# # Determine the reduction in intensity
# energy = np.linspace(0.01, 5, 1000)
# intensity = 1
# for layer in layers:
#     material = layer[0]
#     coeff = np.interp(energy, gamma_att_coeff[material]['energy'], gamma_att_coeff[material]['coeff'])
#     intensity *= np.exp(-coeff * density[material] * layer[1])

# print("Intensity: " + str(intensity))
# fig, ax = plt.subplots()
# ax.plot(energy, intensity, "-")
# ax.vlines(2.615, min(intensity), max(intensity), colors='r', linestyles='dashed', label='2.615 MeV (Tl-208)')
# ax.set_title(get_layer_description(layers))
# ax.set_xlabel('Energy (MeV)')
# ax.set_ylabel('Intensity (fraction)')
# ax.margins(x=0, y=0)
# # ax.set_xscale('log')
# # ax.set_yscale('log')
# fig.tight_layout()

print(df)

energy = 2.615
material = "water"
material_data = df[df['material'] == material]
density = material_data['density'].values[0]

max_count_rate = Decimal(0.1)/Decimal(360*24*60*60) # 1 count per year
print(f"Max count rate: {max_count_rate} Hz = {max_count_rate*60*60*24*365} counts/year")

incoming_counts = Decimal("1.3e-2")
print(f"Incoming count rate: {incoming_counts} Hz = {incoming_counts*60*60*24*365} counts/year")

reduction_required = float(max_count_rate / incoming_counts)
print(f"Reduction required: {reduction_required}")

thickness = -(np.log(reduction_required))/(gamma_att_coeff[material] * density)
print(f"Thickness required: {thickness} cm")
