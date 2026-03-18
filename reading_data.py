import punpy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import fp_environmental_correction as fp_envicor
# import fc_solar_correction as fc_solarcor
import json


def read_measured_data(path):
    # read the data from file
    data = pd.read_csv(path, delimiter='\t')

    # assign columns to arrays
    datetime = crns_example_data['datetime'].array
    press = crns_example_data['press1'].array
    temp = crns_example_data['temp1'].array
    relhum = crns_example_data['relhum1'].array
    volt = crns_example_data['volt'].array
    counts = crns_example_data['counts1'].array
    nsecs = crns_example_data['nsecs1'].array
    counts_bare = crns_example_data['counts_bare'].array
    nsecs_bare = crns_example_data['nsecs_bare'].array
    cph_filtered = crns_example_data['cph_filtered'].array

    print(len(datetime), len(cph_filtered))

    return datetime, press, temp, relhum, volt, counts, nsecs, counts_bare, nsecs_bare, cph_filtered

path_data = "./observations/"
crns_example_data = pd.read_csv(path_data+'1_CRNS.txt', delimiter='\t', skiprows=1)

# Clean up data
crns_example_data = crns_example_data[np.invert(np.isnan(crns_example_data.press1))]
crns_example_data = crns_example_data.head(1000)

# print(crns_example_data.columns)

with open(path_data+'crns_meta.json', 'r') as file:
    data = json.load(file)

# print(json.dumps(data, indent=4))

path_data_2 ="./observations/"
with open(path_data_2+'swc_meta.json', 'r') as file:
    data = json.load(file)

# print(json.dumps(data, indent=4))

