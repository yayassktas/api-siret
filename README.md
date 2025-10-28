# 🇫🇷 API Vérification Documents France

**API professionnelle pour valider en temps réel les documents officiels français**

## ✨ Fonctionnalités

### Documents supportés

✅ **SIRET** - Validation + enrichissement (INSEE Sirene)  
✅ **SIREN** - Validation + enrichissement (INSEE Sirene)  
✅ **TVA Intracommunautaire** - Validation France + EU (VIES)  
✅ **IBAN France** - Validation format + clé MOD97

## 🚀 Installation rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'API
python main.py
```

L'API sera accessible sur : **http://localhost:8000**  
Documentation : **http://localhost:8000/docs**

## 📖 Utilisation

### Exemple Python

```python
import requests

API_KEY = "demo_key_123"
headers = {"X-API-Key": API_KEY}

# Vérifier un SIRET
response = requests.post(
    "http://localhost:8000/api/v1/verify/siret",
    headers=headers,
    json={"siret": "12345678901234"}
)

result = response.json()
print(result)
```

### Exemple cURL

```bash
curl -X POST "http://localhost:8000/api/v1/verify/tva" \
  -H "X-API-Key: demo_key_123" \
  -H "Content-Type: application/json" \
  -d '{"numero_tva": "FR12345678901"}'
```

## 🔌 Endpoints disponibles

- `POST /api/v1/verify/siret` - Vérifier SIRET
- `POST /api/v1/verify/siren` - Vérifier SIREN
- `POST /api/v1/verify/tva` - Vérifier TVA
- `POST /api/v1/verify/iban` - Vérifier IBAN
- `GET /api/v1/stats` - Statistiques

## 💰 Monétisation

### Plans tarifaires recommandés

| Plan | Requêtes/jour | Prix/mois |
|------|--------------|-----------|
| Free | 100 | 0€ |
| Starter | 1 000 | 29€ |
| Pro | 10 000 | 99€ |
| Enterprise | 100 000+ | Sur devis |

**Revenus potentiels : 12 000€+/mois**

## 📈 Cas d'usage

- ✅ Auto-complétion formulaires
- ✅ Vérification KYC/KYB
- ✅ Prévention fraude
- ✅ Enrichissement CRM

## 🤝 Support

Email : support@docverify.fr

---

**Made with ❤️ in France** 🇫🇷
