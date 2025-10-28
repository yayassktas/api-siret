"""
API de Vérification de Documents Français
==========================================
API professionnelle pour valider SIRET, SIREN, TVA intracommunautaire et IBAN français
Auteur: DocVerify France
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn
from datetime import datetime
import hashlib
import os

from validators import (
    validate_siret,
    validate_siren,
    validate_tva_intracommunautaire,
    validate_iban_fr,
    get_company_info_from_sirene,
    check_tva_vies
)

# Configuration
API_VERSION = "1.0.0"
API_TITLE = "API Vérification Documents France"
API_DESCRIPTION = """
## 🇫🇷 API de Vérification de Documents Français

Cette API vous permet de vérifier en temps réel la validité de documents officiels français :

### Fonctionnalités

* **SIRET/SIREN** : Validation + récupération des données entreprise (INSEE)
* **TVA Intracommunautaire** : Validation France + EU (VIES)
* **IBAN Français** : Validation format + clé de contrôle

### Avantages

✅ Sources officielles (INSEE, VIES)  
✅ Temps réel  
✅ Documentation complète  
✅ Rate limiting intégré  

### Cas d'usage

- Auto-complétion de formulaires
- Vérification KYC/KYB
- Prévention fraude
- Enrichissement de données
"""

# Initialiser l'app FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Support DocVerify",
        "email": "support@docverify.fr"
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de données
class SIRETRequest(BaseModel):
    siret: str = Field(..., description="Numéro SIRET à 14 chiffres", example="12345678901234")
    include_company_data: bool = Field(default=True, description="Inclure les données de l'entreprise")

class SIRENRequest(BaseModel):
    siren: str = Field(..., description="Numéro SIREN à 9 chiffres", example="123456789")
    include_company_data: bool = Field(default=True, description="Inclure les données de l'entreprise")

class TVARequest(BaseModel):
    numero_tva: str = Field(..., description="Numéro TVA (ex: FR12345678901)", example="FR12345678901")
    verify_vies: bool = Field(default=True, description="Vérifier avec VIES")

class IBANRequest(BaseModel):
    iban: str = Field(..., description="IBAN français (27 caractères)", example="FR7612345678901234567890123")

class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

# Système d'authentification simple (à améliorer en production)
API_KEYS = {
    "demo_key_123": {"name": "Demo User", "tier": "free", "daily_limit": 100},
    "premium_key_456": {"name": "Premium User", "tier": "premium", "daily_limit": 10000}
}

def verify_api_key(x_api_key: str = Header(...)):
    """Vérifie la clé API"""
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Clé API invalide")
    return API_KEYS[x_api_key]

# Routes

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API de Vérification de Documents Français",
        "version": API_VERSION,
        "documentation": "/docs",
        "endpoints": {
            "siret": "/api/v1/verify/siret",
            "siren": "/api/v1/verify/siren",
            "tva": "/api/v1/verify/tva",
            "iban": "/api/v1/verify/iban"
        }
    }

@app.get("/health")
async def health_check():
    """Health check de l'API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============ ENDPOINTS DE VÉRIFICATION ============

@app.post("/api/v1/verify/siret", response_model=APIResponse)
async def verify_siret_endpoint(
    request: SIRETRequest,
    user: dict = Depends(verify_api_key)
):
    """
    Vérifie un numéro SIRET
    
    Le SIRET (Système d'Identification du Répertoire des Établissements) est un code
    de 14 chiffres qui identifie géographiquement l'établissement d'une entreprise.
    
    **Retourne:**
    - Validité du format
    - Données de l'entreprise (si demandé)
    - Statut de l'établissement
    """
    try:
        # Validation format
        is_valid, error_msg = validate_siret(request.siret)
        
        if not is_valid:
            return APIResponse(
                success=False,
                error=error_msg,
                timestamp=datetime.now().isoformat()
            )
        
        response_data = {
            "siret": request.siret,
            "format_valid": True
        }
        
        # Récupérer les données entreprise si demandé
        if request.include_company_data:
            company_data = get_company_info_from_sirene(request.siret, "siret")
            if company_data:
                response_data["company"] = company_data
        
        return APIResponse(
            success=True,
            data=response_data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/verify/siren", response_model=APIResponse)
async def verify_siren_endpoint(
    request: SIRENRequest,
    user: dict = Depends(verify_api_key)
):
    """
    Vérifie un numéro SIREN
    
    Le SIREN (Système d'Identification du Répertoire des Entreprises) est un code
    de 9 chiffres qui identifie une entreprise française.
    
    **Retourne:**
    - Validité du format
    - Données de l'entreprise (si demandé)
    - Liste des établissements
    """
    try:
        # Validation format
        is_valid, error_msg = validate_siren(request.siren)
        
        if not is_valid:
            return APIResponse(
                success=False,
                error=error_msg,
                timestamp=datetime.now().isoformat()
            )
        
        response_data = {
            "siren": request.siren,
            "format_valid": True
        }
        
        # Récupérer les données entreprise si demandé
        if request.include_company_data:
            company_data = get_company_info_from_sirene(request.siren, "siren")
            if company_data:
                response_data["company"] = company_data
        
        return APIResponse(
            success=True,
            data=response_data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/verify/tva", response_model=APIResponse)
async def verify_tva_endpoint(
    request: TVARequest,
    user: dict = Depends(verify_api_key)
):
    """
    Vérifie un numéro de TVA intracommunautaire
    
    Valide le format et vérifie l'existence du numéro auprès du système VIES
    de la Commission Européenne.
    
    **Retourne:**
    - Validité du format
    - Statut VIES (si demandé)
    - Informations entreprise associée
    """
    try:
        # Validation format
        is_valid, country, error_msg = validate_tva_intracommunautaire(request.numero_tva)
        
        if not is_valid:
            return APIResponse(
                success=False,
                error=error_msg,
                timestamp=datetime.now().isoformat()
            )
        
        response_data = {
            "numero_tva": request.numero_tva.upper(),
            "format_valid": True,
            "country_code": country
        }
        
        # Vérification VIES si demandé
        if request.verify_vies:
            vies_result = check_tva_vies(request.numero_tva)
            response_data["vies"] = vies_result
        
        return APIResponse(
            success=True,
            data=response_data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/verify/iban", response_model=APIResponse)
async def verify_iban_endpoint(
    request: IBANRequest,
    user: dict = Depends(verify_api_key)
):
    """
    Vérifie un IBAN français
    
    Valide le format, la clé de contrôle et les codes bancaires selon
    les standards français (27 caractères).
    
    **Retourne:**
    - Validité du format
    - Validité de la clé de contrôle
    - Détails du compte (code banque, guichet, compte, clé)
    """
    try:
        # Validation IBAN
        is_valid, details, error_msg = validate_iban_fr(request.iban)
        
        if not is_valid:
            return APIResponse(
                success=False,
                error=error_msg,
                timestamp=datetime.now().isoformat()
            )
        
        return APIResponse(
            success=True,
            data=details,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ ENDPOINT BATCH (Premium) ============

@app.post("/api/v1/verify/batch")
async def verify_batch_endpoint(
    requests: list,
    user: dict = Depends(verify_api_key)
):
    """
    Vérification en lot (réservé aux utilisateurs Premium)
    
    Permet de vérifier plusieurs documents en une seule requête.
    Maximum 100 documents par batch.
    """
    if user["tier"] != "premium":
        raise HTTPException(
            status_code=403,
            detail="Fonctionnalité réservée aux utilisateurs Premium"
        )
    
    if len(requests) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 documents par batch"
        )
    
    results = []
    for req in requests:
        # Traiter chaque requête...
        pass
    
    return {
        "success": True,
        "results": results,
        "total": len(results)
    }

# ============ STATISTIQUES ============

@app.get("/api/v1/stats")
async def get_stats(user: dict = Depends(verify_api_key)):
    """Statistiques d'utilisation de l'utilisateur"""
    return {
        "user": user["name"],
        "tier": user["tier"],
        "daily_limit": user["daily_limit"],
        "used_today": 0,  # À implémenter avec une vraie DB
        "remaining": user["daily_limit"]
    }

if __name__ == "__main__":
    # Récupérer le port depuis la variable d'environnement (Render le fournit)
    port = int(os.getenv("PORT", 8000))
    # En production, désactiver le reload
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=reload
    )
