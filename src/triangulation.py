# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

""" Ce script à pour but de préparer la triangulation des points 3D à partir des points 2D détectés par les caméras.
    Dans un premier temps, on initalise une formule se basant sur la décomposition en valeurs singulières pour réaliser la triangulation.
    Puis on récupère les données issues du fichiers associations.
    Enfin, on place les points dans un repère homogènes afin qu'il soit apte à être trianguler.
    On utilise la fonction triangulation pour obtenir les coordonnées 3D des points sur les points qui comporte des concordancances sur au moins 2 caméras."""

# %% 
upstream = None

# %% tags=["parameters"]
association = None
matrice_projection_cam1 = None
matrice_projection_cam2 = None
matrice_projection_cam3 = None
matrice_projection_cam4 = None
output_path = None


# %%
# Importation des libraries
import numpy as np
import pandas as pd 
from scipy.linalg import svd

# %% 
# Créer un dictionnaire contenant les matrices de projection des 4 caméras
P1 = np.loadtxt(matrice_projection_cam1)
P2 = np.loadtxt(matrice_projection_cam2)
P3 = np.loadtxt(matrice_projection_cam3)
P4 = np.loadtxt(matrice_projection_cam4)

# %%
projections = [P1, P2, P3, P4]
# Récupération des données du fichier d'association
association = pd.read_csv(association)

# %%    
results = []

def triangulate(points, projections):
    """
    Triangule un point 3D à partir de plusieurs vues.

    :param points: Liste de points projetés, chaque point étant de la forme [x, y, 1].
                   Exemple : [np.array([x1, y1, 1]), np.array([x2, y2, 1]), ...]
    :param projections: Liste de matrices de projection correspondantes.
                        Exemple : [P1, P2, P3, ...]
    :return: Coordonnées 3D du point sous forme d'un np.array.
    :raises ValueError: Si le nombre de points ne correspond pas au nombre de projections ou si les dimensions sont incorrectes.
    """
    if len(points) != len(projections):
        raise ValueError("Le nombre de points doit correspondre au nombre de matrices de projection.")

    A = []
    for point, P in zip(points, projections):
        if point.shape != (3,) or P.shape != (3, 4):
            raise ValueError("Les points doivent être de forme (3,) et les matrices de projection de forme (3, 4).")
        
        A.append(point[0] * P[2] - P[0])
        A.append(point[1] * P[2] - P[1])
    
    A = np.vstack(A)

    # Résolution par SVD
    U, S, Vt = svd(A)
    X = Vt[-1]
    X = X / X[-1]  # Normalisation des coordonnées homogènes

    return X[:3]

# %%
# Vérifier les colonnes attendues
expected_columns = [f'x1{i+1}' for i in range(4)] + [f'y1{i+1}' for i in range(4)]
for col in expected_columns:
    if col not in association.columns:
        print(f"Attention : la colonne {col} n'existe pas dans le DataFrame fusionné.")

# Itérer sur chaque frame du DataFrame fusionné
for index, row in association.iterrows():
    points = []
    projection_list = []
    
    # Collecter les points et les matrices de projection valides
    for i, cam in enumerate(['cam1', 'cam2', 'cam3', 'cam4']):
        x_col = f'x1_{cam}'
        y_col = f'y1_{cam}'
        
        # Vérifier si les colonnes existent et ne sont pas NaN
        if x_col in row and y_col in row:
            if pd.notna(row[x_col]) and pd.notna(row[y_col]):
                points.append(np.array([row[x_col], row[y_col], 1]))
                projection_list.append(projections[i])
                print(f"Frame {row['frame']}: Point ajouté pour {cam} - ({row[x_col]}, {row[y_col]})")
            else:
                print(f"Frame {row['frame']}: NaN détecté pour {cam} - ({row[x_col]}, {row[y_col]})")
        else:
            print(f"Frame {row['frame']}: Colonne manquante pour {cam}")

    # Appliquer la triangulation si au moins deux points sont valides
    if len(points) >= 2:
        try:
            point_3d = triangulate(points, projection_list)
            results.append({'frame': row['frame'], 'x': point_3d[0], 'y': point_3d[1], 'z': point_3d[2]})
            print(f"Frame {row['frame']}: Point 3D triangulé - ({point_3d[0]}, {point_3d[1]}, {point_3d[2]})")
        except Exception as e:
            print(f"Erreur lors de la triangulation de la frame {row['frame']}: {e}")
    else:
        print(f"Frame {row['frame']}: Moins de 2 points valides, triangulation non appliquée.")

# Convertir les résultats en DataFrame
df_results = pd.DataFrame(results)
df_results.to_csv(output_path, index=False)