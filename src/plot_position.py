# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
""" Ce script à pour but de réaliser un graphique représentant la position des pilotes au cours du temps sur la piste"""

# %% 
upstream = None

# %% tags=["parameters"]
positions3D = None

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
# Importation des données
result = pd.read_csv(positions3D)

# %%
plt.figure(figsize=(16,10))

#Limites des axes x et y
plt.xlim(0, 80)  
plt.ylim(-10,10)

# Tracer les bordures de la pistes
plt.axhline(y = 0, color = 'black', linestyle = '--')
plt.axhline(y = 8, color = 'black', linestyle = '--')

# Ajouter les lignes de bosses 
plt.plot([31.3, 31.3], [0, 8], color='black', linestyle='--', linewidth=0.5)
plt.plot([35, 35], [0, 8], color='black', linestyle='--', linewidth=0.5)
plt.plot([40.6, 40.6], [0, 8], color='black', linestyle='--', linewidth=0.5)
plt.plot([60.8, 60.8], [0, 8], color='black', linestyle='--', linewidth=0.5)
plt.plot([62.6, 62.6], [0, 8], color='black', linestyle='--', linewidth=0.5)
plt.plot([66.2, 66.2], [0, 8], color='black', linestyle='--', linewidth=0.5)

# Nom des axes 
plt.xlabel('Longueur de la piste (m)')
plt.ylabel('Largeur de la piste (m)')
plt.title('Position des pilotes au cours du temps')

# signaler les bosses
plt.text(31.3, 9, '1ère bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(35, -1, '2ème bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(40.6, 9, '3ème bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(57.8, 9, '4ème bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(62.6, -1, '5ème bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(66.2, 9, '6ème bosse', horizontalalignment='center', fontsize=10,
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))



plt.plot(result['x'], result['y'], 'ro', label='Trajectoire 3D', markersize=1)


plt.show()