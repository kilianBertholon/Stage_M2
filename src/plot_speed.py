# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
""" Ce script à pour but de réaliser un graphique représentant la vitesse des pilotes au cours du temps."""

# %%
upstream = None

# %% tags=["parameters"]
# This is a placeholder, leave it as None
speed = None

#%%
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# %%
# Importation des données
vitesse = pd.read_csv(speed, delimiter=',')

# %%
plt.figure(figsize=(16, 10))
plt.plot(np.arange(len(vitesse['vitesse'])) / 30, vitesse['vitesse'], label='Vitesse originale (km/h)', color='blue')
# plt.plot(np.arange(len(vitesse_original_smooth)) / 30, vitesse_original_smooth, label='Vitesse lissée (km/h)', color='red')
# plt.plot(np.arange(len(interpolated_velocities)) / 60, interpolated_velocities, label='Interpolated Velocities (km/h)', color='green')
# plt.plot(np.arange(len(interpolated_smooth)) / 60, interpolated_smooth, label='Smoothed Interpolated Velocities (km/h)', color='orange')
plt.xlabel('Temps (s)')
plt.ylim(0, 60)
plt.ylabel('Vitesse (km/h)')
plt.title('Vitesse d\'une athlète en finale')
plt.legend()
plt.show() 
