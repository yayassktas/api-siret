# Dockerfile pour DocVerify API

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY main.py .
COPY validators.py .

# Exposer le port
EXPOSE 8000

# Commande pour lancer l'application
CMD ["python", "main.py"]
