#!/usr/bin/env python3
"""
🧪 Client Test - French Documents Verification API
===================================================
Script de démonstration pour tester l'API de vérification de documents français.

Teste plusieurs entreprises françaises connues et affiche les résultats en couleur.
"""

import requests
import time
from datetime import datetime
import json

# Configuration de l'API
API_URL = "http://localhost:8000"
API_KEY = "demo_key_123"

# Codes couleur ANSI pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    """Affiche un en-tête stylisé"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_success(text):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Affiche une information"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def verify_siret(siret, company_name):
    """
    Vérifie un numéro SIRET
    
    Args:
        siret: Le numéro SIRET à vérifier
        company_name: Le nom de l'entreprise (pour l'affichage)
    
    Returns:
        dict: Résultat de la vérification avec timing
    """
    print(f"\n{Colors.BOLD}🏢 Test : {company_name}{Colors.END}")
    print(f"   SIRET : {siret}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/verify/siret",
            json={"siret": siret},
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # en millisecondes
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print_success(f"SIRET valide ({duration:.0f}ms)")
                
                # Afficher les détails si disponibles
                if data.get("data"):
                    details = data["data"]
                    if details.get("format_valid"):
                        print(f"   {Colors.GREEN}Format : ✓ Valide{Colors.END}")
                
                return {
                    "success": True,
                    "company": company_name,
                    "duration": duration,
                    "data": data
                }
            else:
                print_error(f"SIRET invalide : {data.get('error', 'Erreur inconnue')}")
                return {
                    "success": False,
                    "company": company_name,
                    "duration": duration,
                    "error": data.get("error")
                }
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return {
                "success": False,
                "company": company_name,
                "duration": duration,
                "error": f"HTTP {response.status_code}"
            }
            
    except requests.exceptions.RequestException as e:
        print_error(f"Erreur de connexion : {str(e)}")
        return {
            "success": False,
            "company": company_name,
            "error": str(e)
        }

def verify_tva(siren, company_name):
    """
    Vérifie un numéro de TVA intracommunautaire
    
    Args:
        siren: Le numéro SIREN (9 chiffres)
        company_name: Le nom de l'entreprise
    
    Returns:
        dict: Résultat de la vérification
    """
    print(f"\n{Colors.BOLD}💶 Test TVA : {company_name}{Colors.END}")
    print(f"   SIREN : {siren}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/verify/tva",
            json={"siren": siren},
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print_success(f"TVA calculée ({duration:.0f}ms)")
                
                if data.get("data") and data["data"].get("tva"):
                    tva = data["data"]["tva"]
                    print(f"   {Colors.CYAN}Numéro TVA : {tva}{Colors.END}")
                
                return {
                    "success": True,
                    "company": company_name,
                    "duration": duration,
                    "data": data
                }
            else:
                print_error(f"Erreur : {data.get('error')}")
                return {"success": False, "company": company_name, "error": data.get("error")}
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return {"success": False, "company": company_name, "error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print_error(f"Erreur de connexion : {str(e)}")
        return {"success": False, "company": company_name, "error": str(e)}

def verify_iban(iban, label):
    """
    Vérifie un IBAN
    
    Args:
        iban: Le numéro IBAN
        label: Le label pour l'affichage
    
    Returns:
        dict: Résultat de la vérification
    """
    print(f"\n{Colors.BOLD}🏦 Test IBAN : {label}{Colors.END}")
    print(f"   IBAN : {iban}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/verify/iban",
            json={"iban": iban},
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print_success(f"IBAN valide ({duration:.0f}ms)")
                
                if data.get("data"):
                    details = data["data"]
                    print(f"   {Colors.CYAN}Pays : {details.get('country', 'N/A')}{Colors.END}")
                    print(f"   {Colors.CYAN}Code banque : {details.get('code_banque', 'N/A')}{Colors.END}")
                    print(f"   {Colors.CYAN}Code guichet : {details.get('code_guichet', 'N/A')}{Colors.END}")
                
                return {
                    "success": True,
                    "label": label,
                    "duration": duration,
                    "data": data
                }
            else:
                print_error(f"IBAN invalide : {data.get('error')}")
                return {"success": False, "label": label, "error": data.get("error")}
        else:
            print_error(f"Erreur HTTP {response.status_code}")
            return {"success": False, "label": label, "error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print_error(f"Erreur de connexion : {str(e)}")
        return {"success": False, "label": label, "error": str(e)}

def test_api_health():
    """Teste si l'API est accessible"""
    print_info("Vérification de la connexion à l'API...")
    
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print_success(f"API accessible sur {API_URL}")
            return True
        else:
            print_error(f"API répond avec le code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Impossible de se connecter à l'API : {str(e)}")
        print_warning("Assurez-vous que l'API est lancée avec : python main.py")
        return False

def print_statistics(results):
    """Affiche les statistiques des tests"""
    print_header("📊 STATISTIQUES")
    
    total = len(results)
    success = sum(1 for r in results if r.get("success"))
    failed = total - success
    
    print(f"Total de tests : {Colors.BOLD}{total}{Colors.END}")
    print(f"Succès : {Colors.GREEN}{success}{Colors.END}")
    print(f"Échecs : {Colors.RED}{failed}{Colors.END}")
    
    if success > 0:
        avg_duration = sum(r.get("duration", 0) for r in results if r.get("success")) / success
        print(f"Temps moyen de réponse : {Colors.CYAN}{avg_duration:.0f}ms{Colors.END}")
    
    success_rate = (success / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.BOLD}Taux de succès : ", end="")
    if success_rate >= 80:
        print(f"{Colors.GREEN}{success_rate:.1f}%{Colors.END}")
    elif success_rate >= 50:
        print(f"{Colors.YELLOW}{success_rate:.1f}%{Colors.END}")
    else:
        print(f"{Colors.RED}{success_rate:.1f}%{Colors.END}")

def main():
    """Fonction principale"""
    print_header("🇫🇷 TEST CLIENT - API DE VÉRIFICATION DE DOCUMENTS")
    
    print(f"{Colors.BOLD}Configuration :{Colors.END}")
    print(f"  URL API : {Colors.CYAN}{API_URL}{Colors.END}")
    print(f"  Clé API : {Colors.CYAN}{API_KEY}{Colors.END}")
    print(f"  Date : {Colors.CYAN}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.END}")
    
    # Tester la connexion à l'API
    if not test_api_health():
        return
    
    # Liste des tests à effectuer
    results = []
    
    print_header("🧪 TESTS DE VÉRIFICATION SIRET")
    
    # Test 1 : Apple France
    results.append(verify_siret("44306184100047", "Apple France"))
    
    # Test 2 : Google France
    results.append(verify_siret("44332823500047", "Google France"))
    
    # Test 3 : Microsoft France
    results.append(verify_siret("32751478500013", "Microsoft France"))
    
    # Test 4 : Amazon France
    results.append(verify_siret("44350019600025", "Amazon France"))
    
    # Test 5 : SIRET invalide (pour tester la détection d'erreur)
    results.append(verify_siret("12345678901234", "Entreprise Test (invalide)"))
    
    print_header("🧪 TESTS DE VÉRIFICATION TVA")
    
    # Test TVA Apple France
    results.append(verify_tva("443061841", "Apple France"))
    
    # Test TVA Google France
    results.append(verify_tva("443328235", "Google France"))
    
    print_header("🧪 TESTS DE VÉRIFICATION IBAN")
    
    # Test IBAN valide
    results.append(verify_iban("FR7630006000011234567890189", "IBAN Français"))
    
    # Test IBAN invalide
    results.append(verify_iban("FR1234567890", "IBAN Test (invalide)"))
    
    # Afficher les statistiques finales
    print_statistics(results)
    
    print_header("✅ TESTS TERMINÉS")
    
    print(f"\n{Colors.BOLD}Pour voir plus de détails :{Colors.END}")
    print(f"  • Documentation : {Colors.CYAN}http://localhost:8000/docs{Colors.END}")
    print(f"  • Tester manuellement : Interface Swagger ci-dessus")
    print(f"\n{Colors.BOLD}Pour modifier ce script :{Colors.END}")
    print(f"  • Fichier : {Colors.CYAN}test_client.py{Colors.END}")
    print(f"  • Ajoutez vos propres tests !")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrompu par l'utilisateur{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur inattendue : {str(e)}{Colors.END}")
