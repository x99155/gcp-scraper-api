# Utilise la version 3.8 de l'image de python slim
# On exécute sur une plateforme amd64 pour une compatibilité avec GCP
FROM --platform=linux/amd64 python:3.8-slim as build

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copy le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installe les dépendances définient dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port 8000 sur lequel l'application va tourner
EXPOSE 8000

# Copie le reste des fichier de notre application dans le répertoire de travail
COPY . .

# Exécute notre application au démarrage du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]