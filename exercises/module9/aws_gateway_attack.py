#!/usr/bin/env python3
"""
Rotación de IPs usando AWS API Gateway
Requiere credenciales AWS válidas y cuestas de pago (Free tier disponible)
Librería: requests-ip-rotator
"""
import sys
import requests
try:
    from requests_ip_rotator import ApiGateway
except ImportError:
    print("Se requiere 'requests-ip-rotator'. Ejecuta: pip install requests-ip-rotator")
    sys.exit(1)

# Configuración (Requiere keys reales)
# NO INCLUIR KEYS EN CÓDIGO REAL
AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
AWS_REGION = "us-east-1"  # Región AWS

# Objetivo (Debe ser accesible desde INTERNET, no localhost)
# API Gateway no puede enrutar a 127.0.0.1 o red docker interna
TARGET_SITE = "https://httpbin.org" 

def main():
    print("="*60)
    print("DEMOSTRACIÓN AWS API GATEWAY ROTATION")
    print("⚠️  Requisitos:")
    print("    1. Credenciales AWS configuradas")
    print("    2. Objetivo accesible desde Internet (Public IP)")
    print("="*60)

    if AWS_ACCESS_KEY_ID == "YOUR_ACCESS_KEY":
        print("[!] Por favor edita el script y configura tus AWS Keys.")
        return

    print(f"[*] Inicializando API Gateway para {TARGET_SITE}...")
    
    # Crea el gateway
    gateway = ApiGateway(
        TARGET_SITE,
        regions=[AWS_REGION],
        access_key_id=AWS_ACCESS_KEY_ID,
        access_key_secret=AWS_SECRET_ACCESS_KEY
    )
    
    try:
        gateway.start()
        print("[+] Gateway iniciado. Las peticiones saldrán desde IPs de AWS.")
        
        # Crear sesión
        session = requests.Session()
        session.mount(TARGET_SITE, gateway)
        
        # Realizar peticiones
        for i in range(5):
            print(f"[*] Petición {i+1}...")
            # La IP de origen cambiará en cada petición
            resp = session.get(f"{TARGET_SITE}/get") 
            print(f"    Status: {resp.status_code}")
            # Ver headers para confirmar X-Forwarded-For etc.
            
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Limpiando recursos AWS...")
        gateway.shutdown()

if __name__ == "__main__":
    main()
