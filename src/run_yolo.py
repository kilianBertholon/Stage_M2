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
""" Ce script à pour but de réaliser la détection automatique à partir de notre réseau CNN.
    
    Dans un premier temps, il récupère les données issues du fichiers de synchronisation native de dartfish. 
    On s'occure dans un premier temps de récupérer la valeur de SynchronizationHandicap. Cette valeur va nous servir à synchroniser nos detections en utilsiant un timecode externe synchronisé
    et en nous donnant une valeur de frame de départ poiur chaque caméra.
    
    Dans un second temps, on part de la source vidéo (ici mp4) pour extraire un fichier csv de detections contenant : ['frame', 'id', 'conf', 'x1', 'y1', 'x2', 'y2']
    - La frame de la capture
    - L'identifiant de l'objet détecté via l'utilisation d'un tracker issues de BotSort
    - La confiance de la détection
    - Les coordonnées des bounding boxes x1, y1, x2, y2"""

# %%
upstream = None

# %% tags=['parameters']
video_path = None
output_path = None
dartclip_path = None
model_path = None
tracker_path = None

# %%
import re
import math
import os
import cv2 
from ultralytics import YOLO
import numpy as np
import pandas as pd

# %%
def extract_synchronization_handicap(file_path):
    """ Permet de sortir le retard associé au Timecode de la caméra.
    
        filepath: lien du fichier dartclip 
        """
    # ouvrir le fichier
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Utiliser une expression régulière pour extraire la valeur de SynchronizationHandicap
    match = re.search(r'SynchronizationHandicap="(\d+)"', content)
    
    if match:
        synchronization_handicap = match.group(1)
        return synchronization_handicap
    else:
        return None
# Application 
synchronization_handicap = extract_synchronization_handicap(dartclip_path)

# %%
# Transformer la valeur issue de la formule en entier 
synchronization_handicap = int(synchronization_handicap)
# Expressio que l'on a déterminé pour obtenir le retard en frame (30 fps ici)
frame_begin = synchronization_handicap/330000
#Arrondir à la frame inf
frame_begin = math.floor(frame_begin)
print(frame_begin)

# %%
class VideoProcessor:
    
    """ Initialise un processeur de vidéo pour détecter des objets avec YOLO.
    model : Modèle YOLO à utiliser pour la détection d'objets.
    video_path : Chemin de la vidéo à traiter.
    output_video_path : Chemin de la vidéo de sortie annotée avec les bounding boxes.
    df : Dataframe contenant les données de la vidéo.
    """
    # Initialisation des différents paramètres 
    def __init__(self, model_path, video_path):
        self.model = self.load_model(model_path) # Charger le modèle CNN
        self.cap = self.load_video(video_path) # Charger la vidéo 
        self.output_video_path = video_path.replace('.mp4', '_annotated.mp4') # Préparer le fichier de sortie
        self.data = pd.DataFrame(columns=['frame', 'id', 'conf', 'x1', 'y1', 'x2', 'y2']) # Préparer le DataFrame en initalisant les colonnes

    # charger le modèle YOLO
    def load_model(self, path_model): 
        """ Fonction qui permet de charger le modèle YOLO"""  
        model = YOLO(path_model)
        return model

    # charger la vidéo
    def load_video(self, video_path):
        """ Fonction qui permet de charger la vidéo"""
        cap = cv2.VideoCapture(video_path) # Charger la vidéo à partir d'opencv (https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
        if not cap.isOpened():
            print("Erreur lors du chargement de la vidéo.")
            return None
        else:
            print("Vidéo chargée avec succès.")
            return cap

    # charger le tracker
    def detect_objects_yolo(self, image):
        """ Charger le tracker pour suivre les athlètes au cours du temps. Deux possibilités : 
        - Soit on utilise le tracker de BotSort (data/tracker/botsort.yaml)
        - soit on utilise le tracker de bytetrack (data/tracker/bytetrack.yaml)
        """
        results = self.model.track(image, persist=True, save_dir="output", tracker= tracker_path)
        return results
    


    # traiter la vidéo
    def process_video(self):
        """ Définir le processus de traitement de la vidéo
            1) Récupérer les informations issues de la vidéos originale (fps, frame_width, frame_height)
            2) Définir le codec et créer l'objet VideoWriter
            3) Définir la frame de départ (à partir de la fonction extract_synchronization_handicap)
            4) Boucle de traitement de la vidéo
            5) Écrire le frame annoté dans la vidéo de sortie et sauvegarder les données dans un fichier csv
        """
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Obtenir les propriétés de la vidéo originale
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Obtenir les propriétés de la vidéo originale
        fps = int(self.cap.get(cv2.CAP_PROP_FPS)) # Obtenir les propriétés de la vidéo originale

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Définir le codec et créer l'objet VideoWriter
        out = cv2.VideoWriter(self.output_video_path, fourcc, fps, (frame_width, frame_height)) # Définir le codec et créer l'objet VideoWriter (https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
        
        # Définir la frame de départ
        frame_count = frame_begin

        # Boucle de traitement de la vidéo
        while self.cap.isOpened():
            ret, frame = self.cap.read() # valider l'ouverture de la vidéo et récupérer le frame
            if not ret:
                break
            
            # Appliquer le modèle YOLO pour détecter les objets dans le frame
            results = self.detect_objects_yolo(frame) # Détecter les objets dans le frame
            # annoter la frame
            annotated_frame = results[0].plot(conf = False, line_width = 1, font_size = 10)
            
            # Récupérer les informations des objets détectés
            if results[0].boxes is not None and len(results[0].boxes) > 0: # Vérifier si des objets ont été détectés
                confs = results[0].boxes.conf.cpu().numpy() if results[0].boxes.conf is not None else np.array([]) # Récupérer les confiances des objets détectés
                x1s = results[0].boxes.xyxy[:, 0].cpu().numpy() if results[0].boxes.xyxy is not None else np.array([]) # Récupérer les coordonnées x1 des objets détectés
                y1s = results[0].boxes.xyxy[:, 1].cpu().numpy() if results[0].boxes.xyxy is not None else np.array([]) # Récupérer les coordonnées y1 des objets détectés
                x2s = results[0].boxes.xyxy[:, 2].cpu().numpy() if results[0].boxes.xyxy is not None else np.array([]) # Récupérer les coordonnées x2 des objets détectés
                y2s = results[0].boxes.xyxy[:, 3].cpu().numpy() if results[0].boxes.xyxy is not None else np.array([]) # Récupérer les coordonnées y2 des objets détectés
                classes = results[0].boxes.cls.cpu().numpy() if results[0].boxes.cls is not None else np.array([])  # Récupérer les classes des objets détectés (ici dans notre cas seulement BMX)
                ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else np.array([]) # Récupérer les identifiants des objets détectés
                
                # Ajouter les informations des objets détectés dans le DataFrame sous la forme d'une boucle
                for i in range(len(confs)):
                    # Vérifier que tous les attributs ont des valeurs à l'indice i
                    if i < len(ids) and i < len(confs) and i < len(x1s) and i < len(y1s) and i < len(x2s) and i < len(y2s) and i < len(classes):
                        # Ajouter les informations des objets détectés dans le DataFrame
                        self.data.loc[len(self.data)] = {
                            'frame': frame_count,
                            'id': ids[i],
                            'conf': confs[i],
                            'x1': x1s[i],
                            'y1': y1s[i],
                            'x2': x2s[i],
                            'y2': y2s[i],
                            'class': classes[i]
                        }

            # Écrire le frame annoté dans la vidéo de sortie
            out.write(annotated_frame)
            
            # Afficher l'image avec les bounding boxes
            cv2.imshow('YOLO Object Detection', annotated_frame)
            
            # Temps de latence et affichage de la vidéo + arret de la vidéo si pression sur le q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Ajouter une frame au compteur
            frame_count += 1
         
        # Relacher la capture et fermer les fenêtres
        self.cap.release()
        # Fermer la vidéo de sortie
        out.release()
        # Détruire toutes les fenêtres
        cv2.destroyAllWindows()
        
        # Exporter les données du df dans un csv 
        self.data.to_csv(output_path, index=False)


# %%

def run_yolo(output_path):
    """  Si le fichier de sortie n'existe pas, on lance le traitement de la vidéo avec le modèle YOLO.
        Sinon, on use la détection déjà existante"""
    if not os.path.exists(output_path):        
        processor = VideoProcessor(model_path, video_path) # Initialiser le processeur de vidéo à partir de la class initialisée
        processor.process_video() # Lancer le traitement de la vidéo
        
    else:
        print(f"Detections already exist at {output_path}, skipping CNN.")
        
run_yolo(output_path)
