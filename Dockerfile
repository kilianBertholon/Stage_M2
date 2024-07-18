# Utiliser une image de base Python
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.lock.txt et installer les dépendances
COPY requirements.lock.txt .
RUN pip install --no-cache-dir -r requirements.lock.txt

# Installer les dépendances supplémentaires
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

# Copier le reste du code de l'application
COPY . .

# Exposer le port 5000 si nécessaire
EXPOSE 5000

# Lancer le serveur HTTP et exécuter le script ploomber
CMD bash -c "echo 'Starting HTTP server...' && python3 -m http.server 5000 & \
    echo 'Starting ploomber build...' && ploomber build; \
    echo 'Ploomber build completed or failed. Starting ploomber plot...' && ploomber plot; \
    echo 'Ploomber plot completed or failed. Keeping the container running...' && sleep 200"