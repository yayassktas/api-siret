# 🚀 Guide de Démarrage Rapide

## Installation en 5 minutes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer l'API

```bash
python main.py
```

L'API est maintenant accessible sur **http://localhost:8000**

### 3. Tester l'API

Ouvrir dans votre navigateur : **http://localhost:8000/docs**

Vous verrez l'interface Swagger interactive !

## Premier test

### Avec cURL

```bash
curl -X POST "http://localhost:8000/api/v1/verify/siret" \
  -H "X-API-Key: demo_key_123" \
  -H "Content-Type: application/json" \
  -d '{"siret": "12345678901234"}'
```

### Avec Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/verify/siret",
    headers={"X-API-Key": "demo_key_123"},
    json={"siret": "12345678901234"}
)

print(response.json())
```

## Clés de test

```
demo_key_123 - Plan Free (100 requêtes/jour)
premium_key_456 - Plan Premium (10 000 requêtes/jour)
```

## Prochaines étapes

1. ✅ Lire le README.md complet
2. ✅ Explorer le BUSINESS_PLAN.md
3. ✅ Adapter l'API à vos besoins
4. ✅ Déployer en production

## Support

Questions ? Contactez support@docverify.fr

---

**Bon développement ! 🚀**
