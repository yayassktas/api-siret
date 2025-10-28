# 🚀 Guide de Déploiement

## Options de déploiement

### Option 1 : Docker (Recommandé)

```bash
# Build l'image
docker build -t docverify-api .

# Run le conteneur
docker run -d -p 8000:8000 docverify-api
```

### Option 2 : Heroku

```bash
# Se connecter à Heroku
heroku login

# Créer l'app
heroku create docverify-api

# Déployer
git push heroku main

# Ouvrir l'app
heroku open
```

### Option 3 : Railway.app (Gratuit)

1. Créer un compte sur railway.app
2. Connecter votre repo GitHub
3. Railway détecte automatiquement le Dockerfile
4. Déploiement automatique !

### Option 4 : DigitalOcean App Platform

1. Créer une App
2. Connecter GitHub
3. Choisir Python + main.py
4. Déployer

### Option 5 : AWS Lambda + API Gateway

Utiliser Mangum pour adapter FastAPI :

```python
# main.py
from mangum import Mangum
handler = Mangum(app)
```

### Option 6 : VPS (OVH, Scaleway)

```bash
# Sur le serveur
git clone votre-repo
cd docverify-api
pip install -r requirements.txt

# Avec gunicorn
pip install gunicorn
gunicorn main:app --workers 4 --bind 0.0.0.0:8000

# Ou avec systemd
sudo nano /etc/systemd/system/docverify.service
sudo systemctl enable docverify
sudo systemctl start docverify
```

## Configuration HTTPS (Nginx)

```nginx
server {
    listen 80;
    server_name api.docverify.fr;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Puis utiliser Let's Encrypt :

```bash
sudo certbot --nginx -d api.docverify.fr
```

## Variables d'environnement en production

```bash
# Créer un fichier .env
API_DEBUG=False
SECRET_KEY=votre-clef-secrete-forte
DATABASE_URL=postgresql://...
```

## Monitoring

### Option 1 : Sentry

```python
import sentry_sdk
sentry_sdk.init(dsn="votre-dsn")
```

### Option 2 : Datadog

```bash
pip install ddtrace
ddtrace-run python main.py
```

## Checklist avant production

- [ ] HTTPS activé
- [ ] Variables d'environnement sécurisées
- [ ] Rate limiting configuré
- [ ] Monitoring activé
- [ ] Backups database configurés
- [ ] Documentation API à jour
- [ ] Tests automatisés

## Coûts estimés

| Plateforme | Prix/mois | Trafic supporté |
|------------|-----------|-----------------|
| Railway.app | 0-5€ | Petit |
| Heroku | 7-25€ | Moyen |
| DigitalOcean | 5-50€ | Élevé |
| AWS | Variable | Très élevé |

## Support

Questions ? support@docverify.fr
