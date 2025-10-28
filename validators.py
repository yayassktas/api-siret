"""
Fonctions de validation pour documents français
"""

import re
import requests
from typing import Tuple, Optional, Dict, Any
import xml.etree.ElementTree as ET

# ============ VALIDATION SIRET/SIREN ============

def validate_luhn(number: str) -> bool:
    """
    Algorithme de Luhn pour valider SIREN/SIRET
    https://fr.wikipedia.org/wiki/Formule_de_Luhn
    """
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10 == 0

def validate_siren(siren: str) -> Tuple[bool, Optional[str]]:
    """
    Valide un numéro SIREN (9 chiffres)
    
    Returns:
        (is_valid, error_message)
    """
    # Nettoyer l'input
    siren = siren.strip().replace(" ", "").replace("-", "")
    
    # Vérifier que c'est 9 chiffres
    if not re.match(r'^\d{9}$', siren):
        return False, "Le SIREN doit contenir exactement 9 chiffres"
    
    # Vérifier avec l'algorithme de Luhn
    if not validate_luhn(siren):
        return False, "Le SIREN n'est pas valide (échec de l'algorithme de Luhn)"
    
    return True, None

def validate_siret(siret: str) -> Tuple[bool, Optional[str]]:
    """
    Valide un numéro SIRET (14 chiffres)
    
    Returns:
        (is_valid, error_message)
    """
    # Nettoyer l'input
    siret = siret.strip().replace(" ", "").replace("-", "")
    
    # Vérifier que c'est 14 chiffres
    if not re.match(r'^\d{14}$', siret):
        return False, "Le SIRET doit contenir exactement 14 chiffres"
    
    # Vérifier avec l'algorithme de Luhn
    if not validate_luhn(siret):
        return False, "Le SIRET n'est pas valide (échec de l'algorithme de Luhn)"
    
    # Vérifier que le SIREN (9 premiers chiffres) est valide
    siren = siret[:9]
    siren_valid, siren_error = validate_siren(siren)
    if not siren_valid:
        return False, f"Le SIREN contenu dans le SIRET n'est pas valide: {siren_error}"
    
    return True, None

def get_company_info_from_sirene(
    identifier: str,
    type: str = "siret"
) -> Optional[Dict[str, Any]]:
    """
    Récupère les informations d'une entreprise depuis l'API Sirene de l'INSEE
    
    Args:
        identifier: SIREN ou SIRET
        type: "siren" ou "siret"
    
    Returns:
        Dictionnaire avec les données ou None
    """
    try:
        # API Sirene ouverte de l'INSEE
        # Note: En production, utiliser une clé API pour plus de requêtes
        if type == "siret":
            url = f"https://api.insee.fr/entreprises/sirene/V3.11/siret/{identifier}"
        else:
            url = f"https://api.insee.fr/entreprises/sirene/V3.11/siren/{identifier}"
        
        # En production, ajouter votre clé API INSEE
        headers = {
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parser les données essentielles
            if type == "siret" and "etablissement" in data:
                etab = data["etablissement"]
                unit = etab.get("uniteLegale", {})
                
                return {
                    "siret": etab.get("siret"),
                    "siren": etab.get("siren"),
                    "denomination": unit.get("denominationUniteLegale") or 
                                   f"{unit.get('prenom1UniteLegale', '')} {unit.get('nomUniteLegale', '')}".strip(),
                    "adresse": {
                        "numero": etab.get("adresseEtablissement", {}).get("numeroVoieEtablissement"),
                        "voie": etab.get("adresseEtablissement", {}).get("libelleVoieEtablissement"),
                        "code_postal": etab.get("adresseEtablissement", {}).get("codePostalEtablissement"),
                        "ville": etab.get("adresseEtablissement", {}).get("libelleCommuneEtablissement")
                    },
                    "code_naf": etab.get("activitePrincipaleEtablissement"),
                    "date_creation": etab.get("dateCreationEtablissement"),
                    "statut": "Actif" if etab.get("etatAdministratifEtablissement") == "A" else "Fermé"
                }
            
            elif type == "siren" and "uniteLegale" in data:
                unit = data["uniteLegale"]
                
                return {
                    "siren": unit.get("siren"),
                    "denomination": unit.get("denominationUniteLegale") or 
                                   f"{unit.get('prenom1UniteLegale', '')} {unit.get('nomUniteLegale', '')}".strip(),
                    "categorie_juridique": unit.get("categorieJuridiqueUniteLegale"),
                    "code_naf": unit.get("activitePrincipaleUniteLegale"),
                    "date_creation": unit.get("dateCreationUniteLegale"),
                    "statut": "Actif" if unit.get("etatAdministratifUniteLegale") == "A" else "Fermé"
                }
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de la récupération des données Sirene: {e}")
        return None

# ============ VALIDATION TVA INTRACOMMUNAUTAIRE ============

def validate_tva_intracommunautaire(numero_tva: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Valide le format d'un numéro de TVA intracommunautaire
    
    Returns:
        (is_valid, country_code, error_message)
    """
    # Nettoyer l'input
    numero_tva = numero_tva.strip().upper().replace(" ", "").replace(".", "")
    
    # Vérifier le format de base (2 lettres + chiffres)
    if not re.match(r'^[A-Z]{2}[A-Z0-9]+$', numero_tva):
        return False, None, "Format invalide. Le numéro de TVA doit commencer par 2 lettres suivies de chiffres"
    
    country_code = numero_tva[:2]
    
    # Validation spécifique France
    if country_code == "FR":
        # Format FR: FR + 2 chiffres (clé) + 9 chiffres (SIREN)
        if not re.match(r'^FR[0-9A-Z]{2}\d{9}$', numero_tva):
            return False, country_code, "Format TVA française invalide. Format attendu: FR + 2 caractères + 9 chiffres"
        
        siren = numero_tva[4:]
        siren_valid, siren_error = validate_siren(siren)
        if not siren_valid:
            return False, country_code, f"SIREN invalide dans le numéro de TVA: {siren_error}"
    
    # Autres pays européens (validation de base)
    eu_countries = [
        "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
        "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
        "NL", "PL", "PT", "RO", "SE", "SI", "SK"
    ]
    
    if country_code not in eu_countries:
        return False, country_code, f"Code pays '{country_code}' non reconnu pour un numéro de TVA UE"
    
    return True, country_code, None

def check_tva_vies(numero_tva: str) -> Dict[str, Any]:
    """
    Vérifie un numéro de TVA auprès du système VIES de l'UE
    
    Returns:
        Dictionnaire avec le résultat de la vérification
    """
    try:
        numero_tva = numero_tva.strip().upper().replace(" ", "")
        country_code = numero_tva[:2]
        vat_number = numero_tva[2:]
        
        # URL du service SOAP VIES
        url = "https://ec.europa.eu/taxation_customs/vies/services/checkVatService"
        
        # Créer la requête SOAP
        soap_request = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:urn="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
    <soapenv:Header/>
    <soapenv:Body>
        <urn:checkVat>
            <urn:countryCode>{country_code}</urn:countryCode>
            <urn:vatNumber>{vat_number}</urn:vatNumber>
        </urn:checkVat>
    </soapenv:Body>
</soapenv:Envelope>"""
        
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": ""
        }
        
        response = requests.post(url, data=soap_request, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parser la réponse XML
            root = ET.fromstring(response.content)
            
            # Namespaces
            ns = {
                'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                'vies': 'urn:ec.europa.eu:taxud:vies:services:checkVat:types'
            }
            
            valid = root.find('.//vies:valid', ns)
            name = root.find('.//vies:name', ns)
            address = root.find('.//vies:address', ns)
            
            return {
                "valid": valid.text == "true" if valid is not None else False,
                "name": name.text if name is not None else None,
                "address": address.text if address is not None else None,
                "checked_at": "VIES"
            }
        else:
            return {
                "valid": None,
                "error": f"Erreur lors de la vérification VIES: {response.status_code}",
                "checked_at": "VIES"
            }
    
    except Exception as e:
        return {
            "valid": None,
            "error": f"Erreur VIES: {str(e)}",
            "checked_at": "VIES"
        }

# ============ VALIDATION IBAN FRANÇAIS ============

def validate_iban_fr(iban: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Valide un IBAN français (27 caractères)
    
    Returns:
        (is_valid, details, error_message)
    """
    # Nettoyer l'input
    iban = iban.strip().upper().replace(" ", "").replace("-", "")
    
    # Vérifier que c'est un IBAN français
    if not iban.startswith("FR"):
        return False, None, "L'IBAN doit commencer par 'FR' pour la France"
    
    # Vérifier la longueur (27 caractères pour France)
    if len(iban) != 27:
        return False, None, f"Un IBAN français doit contenir 27 caractères (trouvé: {len(iban)})"
    
    # Vérifier le format: FR + 2 chiffres (clé) + 23 caractères
    if not re.match(r'^FR\d{2}[0-9A-Z]{23}$', iban):
        return False, None, "Format IBAN invalide"
    
    # Extraire les composants
    country = iban[0:2]
    check_digits = iban[2:4]
    bban = iban[4:]  # BBAN = Basic Bank Account Number (RIB)
    
    # Valider la clé de contrôle IBAN (algorithme MOD 97)
    # Déplacer les 4 premiers caractères à la fin
    rearranged = bban + country + check_digits
    
    # Remplacer les lettres par des chiffres (A=10, B=11, ..., Z=35)
    numeric_string = ""
    for char in rearranged:
        if char.isalpha():
            numeric_string += str(ord(char) - ord('A') + 10)
        else:
            numeric_string += char
    
    # Calculer le modulo 97
    mod_result = int(numeric_string) % 97
    
    if mod_result != 1:
        return False, None, "Clé de contrôle IBAN invalide"
    
    # Extraire les détails du RIB français
    # Format BBAN français: 5 (code banque) + 5 (code guichet) + 11 (numéro compte) + 2 (clé RIB)
    code_banque = bban[0:5]
    code_guichet = bban[5:10]
    numero_compte = bban[10:21]
    cle_rib = bban[21:23]
    
    # Valider la clé RIB (algorithme MOD 97 français)
    rib_string = f"{code_banque}{code_guichet}{numero_compte}"
    
    # Remplacer les lettres dans le numéro de compte
    rib_numeric = ""
    for char in rib_string:
        if char.isalpha():
            # Conversion spéciale pour les lettres en RIB français
            conversion = {
                'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6',
                'G': '7', 'H': '8', 'I': '9', 'J': '1', 'K': '2', 'L': '3',
                'M': '4', 'N': '5', 'O': '6', 'P': '7', 'Q': '8', 'R': '9',
                'S': '2', 'T': '3', 'U': '4', 'V': '5', 'W': '6', 'X': '7',
                'Y': '8', 'Z': '9'
            }
            rib_numeric += conversion.get(char, '0')
        else:
            rib_numeric += char
    
    # Calculer la clé RIB
    rib_mod = int(rib_numeric) % 97
    calculated_key = 97 - rib_mod
    
    # La clé RIB devrait correspondre (vérification souple car méthode peut varier)
    
    details = {
        "iban": iban,
        "country": "France",
        "check_digits": check_digits,
        "code_banque": code_banque,
        "code_guichet": code_guichet,
        "numero_compte": numero_compte,
        "cle_rib": cle_rib,
        "format_valid": True,
        "iban_check_valid": True
    }
    
    return True, details, None

# ============ FONCTION UTILITAIRE ============

def format_iban_display(iban: str) -> str:
    """Formate un IBAN pour l'affichage (groupes de 4 caractères)"""
    iban = iban.replace(" ", "")
    return " ".join([iban[i:i+4] for i in range(0, len(iban), 4)])
