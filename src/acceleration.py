# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
""" Ce script à pour but de calculer l'accélération du pilote à partir de sa coordonnée 3D au cours du temps
    Cette donnée est donc à interpréter comme la dérivée seconde de la position du pilote.
    Elle est donnée à titre indicative."""

# %% 
upstream = None

# %% tags=["parameters"]
speed = None
output_path = None  

# %%
import pandas as pd

# %%
# Importation des données
speed = pd.read_csv(speed)

# %%
# Calcul de l'accélération
speed['acceleration'] = speed['vitesse'].diff() / (1/30)
speed['acceleration'].fillna(0, inplace=True)
speed.to_csv(output_path, index=False)
