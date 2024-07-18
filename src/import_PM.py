# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
""" Ce script à pour but de créer la matrice de projection à partir des matrices intrinsèques et extrinsèques."""

# %% 
upstream = None

# %% tags=["parameters"]
# Paramètres à fournir par Ploomber
input_path = None
input_path2 = None
output_path = None


# %%
# Importer les librairies
import numpy as np
import os

# %%
def create_projection_matrix(K, Rt):
    """
    Crée la matrice de projection P à partir des matrices intrinsèques et extrinsèques.

    :param K: Matrice intrinsèque (3x3).
    :param R: Matrice de rotation et translation (3x4).
    :return: Matrice de projection (3x4).
    """
    P = np.dot(K, Rt)
    return P

# %%
def import_data(input_path,input_path2):
    """ Importer les données de matrice intrinseque et extrinseque """
    intrinseque = np.array(np.loadtxt(input_path),dtype = np.float32)
    extrinseque = np.array(np.loadtxt(input_path2),dtype = np.float32)
    return intrinseque, extrinseque

# %%
# Importer les matrices
intrinseque, extrinseque = import_data(input_path, input_path2)

# Créer la matrice de projection
P = create_projection_matrix(intrinseque, extrinseque)

# Sauvegarder la matrice de projection dans un fichier
np.savetxt(output_path, P)