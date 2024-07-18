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
""" Ce script à pour but d'associer les détections des différents caméras. Ainsi, l'identifiant de chaque caméra est associé à un même pilote
    Attention : Cette association est aujourd'hui réaliser de manière manuelle.
    A termes, il serait possible d'automatiser cela en utilisant : 
    - Les réseaux de neurones siamois
    - les descripteurs ORB ou SIFT et en utilisant les contraintes épipolaires"""


# %%
# Importation des fichiers de dépendances
upstream = None

# %% tags=["parameters"]
# Lien des fichiers nécessaire au code (ici on place None car on les récupère via la pipeline)
detections_cam_1: None
detections_cam_2: None
detections_cam_3: None
detections_cam_4: None
output_path: None


# %%
# Importation des librairies
import pandas as pd

# import des fihciers de détections
detections1 = pd.read_csv(detections_cam_1)
detections2 = pd.read_csv(detections_cam_2)
detections3 = pd.read_csv(detections_cam_3)
detections4 = pd.read_csv(detections_cam_4)

# %%
# Sélectionner les identifiants nécessaires pour l'association
detections1_filter = detections1[(detections1['id'] == 14)]
detections2_filter = detections2[(detections2['id'] == 6)]
detections3_filter = detections3[detections3['id'] == 13]
detections4_filter = detections4[(detections4['id'] == 19)]

# %%
# Renommer les colonnes pour les concaténer et placer le numéro de caméra pour chaque détection
detections1_filter = detections1_filter[['frame', 'x1_undistorted', 'y1_undistorted']].rename(columns={'x1_undistorted': 'x1', 'y1_undistorted': 'y1'})
detections2_filter = detections2_filter[['frame', 'x1_undistorted', 'y1_undistorted']].rename(columns={'x1_undistorted': 'x1', 'y1_undistorted': 'y1'})
detections3_filter = detections3_filter[['frame', 'x1_undistorted', 'y1_undistorted']].rename(columns={'x1_undistorted': 'x1', 'y1_undistorted': 'y1'})
detections4_filter = detections4_filter[['frame', 'x1_undistorted', 'y1_undistorted']].rename(columns={'x1_undistorted': 'x1', 'y1_undistorted': 'y1'})

print(detections1_filter, detections2_filter, detections3_filter, detections4_filter)

# %% 
def interpolate_missing_frames(df):
    # Vérifier que le DataFrame contient les colonnes nécessaires
    if not all(col in df.columns for col in ['frame', 'x1', 'y1']):
        raise ValueError("Le DataFrame doit contenir les colonnes 'frame', 'x1', et 'y1'")
    
    df['frame'] = df['frame'].astype(int)
    df = df.sort_values('frame')
    
    # Créer un DataFrame avec toutes les frames dans la plage
    all_frames = pd.DataFrame({'frame': range(df['frame'].min(), df['frame'].max() + 1)})
    
    # Fusionner avec le DataFrame original pour trouver les frames manquantes
    df_full = pd.merge(all_frames, df, on='frame', how='left')
    
    # Interpoler les valeurs manquantes
    df_full['x1'] = df_full['x1'].interpolate()
    df_full['y1'] = df_full['y1'].interpolate()
    
    return df_full

# %%
data_cam1_final = interpolate_missing_frames(detections1_filter)
data_cam2_final = interpolate_missing_frames(detections2_filter)
data_cam3_final = interpolate_missing_frames(detections3_filter)
data_cam4_final = interpolate_missing_frames(detections4_filter)

print(data_cam1_final, data_cam2_final, data_cam3_final, data_cam4_final)

# %%
df_merged = pd.merge(data_cam1_final, data_cam2_final, on='frame',how='outer', suffixes=('_cam1', '_cam2'))
df_merged_2 = pd.merge(data_cam3_final, data_cam4_final, on='frame', how='outer', suffixes=('_cam3', '_cam4'))

df_merged = df_merged.sort_values('frame')
df_merged_2 = df_merged_2.sort_values('frame')

df_merged_3 = pd.merge(df_merged, df_merged_2, on='frame', how='outer')

print(df_merged_3.sort_values('frame'))
df_merged_3.to_csv(output_path, index=False)