# --- 
# jupyter: 
#   kernelspec: 
#     display_name: Python 3 
#     language: python 
#     name: python3 
# --- 
""" Ce script à pour but de corriger la distortion issues des détections à partir de la matrice intrinsèques, de la distortion obtenue lors du calibrage des données.
    Ce script est efficace pour les angles de vues dont on se charge de récupérer les coordonnées X1, Y1"""

# %%
upstream = None

# %% tags=["parameters"]
distortion = None    
detections_cam = None
matrice_I = None
output_path = None   


# %% import librairies 
import numpy as np 
import pandas as pd 
import cv2 


# %% Import detections 
def import_detections(detections_cam): 
    """ Importer les données de détection via le csv dans data/detections/*""" 
    detections = pd.read_csv(detections_cam, delimiter=',') 
    return detections[['frame','id', 'x1', 'y1']] 


# %% Matrice Intrinsèques 
def import_matrice_intrinseque(matrice_I): 
    """ Importer les données de matrice intrinseque depuis data/matrice_intrinseque/
        Les données importées sont au format 3X3 """ 
    intrinseque = np.loadtxt(matrice_I, dtype=np.float32) 
    return intrinseque 


# %% distortion 
def import_distortion(distortion): 
    """ Importer les données de distorsion depuis data/distortion/
        Les données sont au format 1X5""" 
    distortion = np.loadtxt(distortion, dtype=np.float32) 
    return distortion 


# %% Fonction de correction de distorsion 
def undistort_points(row, K, D): 
    """ La formule permet de prendre en compte la distorsion de l'objectif et de la corriger
        row: Ligne de la détection
        K: Matrice intrinsèque
        D: Matrice de distorsion
        
        On se sert par la suite de la fonction cv2.undistortPoints pour corriger les points de distorsion (https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)"""
    # Crée une liste vide pour stocker les résultats
    result = {} 
    
    # Récupération des colonnes x1 et y1
    x1_cols = [col for col in row.index if col.startswith('x1')] 
    y1_cols = [col for col in row.index if col.startswith('y1')] 

    # Pour chaque colonne x1 et y1, on récupère les points et on les corrige
    for x1_col, y1_col in zip(x1_cols, y1_cols): 
        pts = np.array([[row[x1_col], row[y1_col]]], dtype=np.float32).reshape(-1, 1, 2) # Reshape pour avoir la bonne dimension
        undistorted_pts = cv2.undistortPoints(pts, K, D, P=K)
        
        # Vérification des points corrigés
        print(f"Original points: ({row[x1_col]}, {row[y1_col]}) -> Undistorted points: ({undistorted_pts[0, 0, 0]}, {undistorted_pts[0, 0, 1]})")
        
        # Stockage des résultats
        result[f'{x1_col}_undistorted'] = undistorted_pts[0, 0, 0] 
        result[f'{y1_col}_undistorted'] = undistorted_pts[0, 0, 1] 
    return pd.Series(result) 


# %% 
# Importer les matrices 
intrinseque = import_matrice_intrinseque(matrice_I) 
detections = import_detections(detections_cam) 
distortion = import_distortion(distortion)

# %% Appliquer les détections 
cam1_undistorted = detections.apply(undistort_points, axis=1, K=intrinseque, D=distortion)
detections[['x1_undistorted', 'y1_undistorted']] = cam1_undistorted
detections_2 = detections.copy()


# %% sauvegarder les données 
detections_2.to_csv(output_path, index=False) 