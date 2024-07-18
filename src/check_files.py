# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
""" Ce script à pour but de vérifier l'existence des fichiers passés en paramètres. 
    Il est notamment utiliser pour vérifier la présence des fichiers de calibration de caméra : 
    - Matrice intrinsèques 
    - Matrice extrinsèques
    - Distorsion de l'objectif
    
    Ces fichiers sont obtenus à partir d'un script placé en dehors de la pipeline de donnée ( car non automatique et demandant de tester diverses situations)"""

# %% 
upstream = None

# %% tags=["parameters"]
 # Liste des fichiers à vérifier
files = None

# %% Vérification des fichiers 
import os

def check_files(files):
    """ Fonction qui permet de voir si les fichiers passés en paramètres existent bien dans notre dossier cible"""
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
    return True


# %% Exécution de la vérification 
check_files(files)

# Print dans le notebook 
print("All files exist.")