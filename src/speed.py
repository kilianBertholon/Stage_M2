# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
""" Permet de calculer la vitesse du pilote en dérivant la position du pilote au cours du temps."""

# %% 
upstream = None
# %% tags=["parameters"]
output_path = None
positions3D = None

# %%
import pandas as pd
import numpy as np

# %%
# Importation des données
result = pd.read_csv(positions3D)

# %%
def calculate_velocity(points, time_interval=1/30):
    # Calculate distances between consecutive points
    distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    # Convert distances to velocities in m/s
    velocities_mps = distances / time_interval
    # Convert m/s to km/h
    velocities_kph = velocities_mps * 3.6
    return np.insert(velocities_kph, 0, 0)

original_vitesse = calculate_velocity(result[['x', 'y', 'z']].values)

result['vitesse'] = original_vitesse
result.to_csv(output_path, index=False)