#!/usr/bin/env python3
import requests
import time
import sys

TARGET_URL = "http://vulnerable-api:5000/api/login"
CHECK_IP_URL = "http://vulnerable-api:5000/api/check-ip"

def check_my_ip():
    try:
        r = requests.get(CHECK_IP_URL)
        data = r.json()
        print(f"[*] Mi IP actual vista por el servidor: {data['ip']} (Bloqueada: {data['blocked']})")
        return data['blocked']
    except Exception as e:
        print(f"[!] Error conectando a la API: {e}")
        return False

def attack():
    print(f"[*] Iniciando ataque directo a {TARGET_URL}")
    print("[*] Objetivo: Provocar bloqueo de IP por Rate Limiting")
    
    # Verificar estado inicial
    check_my_ip()
    
    for i in range(1, 15):
        try:
            payload = {
                "username": "admin",
                "password": f"password_incorrecto_{i}"
            }
            
            r = requests.post(TARGET_URL, json=payload, timeout=5)
            
            status = r.status_code
            print(f"[{i}] Intento login... Status: {status}")
            
            if status == 429:
                print(f"\n[!] ⛔ BLOQUEO DETECTADO en el intento {i}!")
                print(f"[!] Respuesta del servidor: {r.json()['error']}")
                check_my_ip()
                return
            
            if status == 200:
                print("[+] Login exitoso (Inesperado)")
                return

        except Exception as e:
            print(f"[!] Error: {e}")
        
    print("\n[-] No se detectó bloqueo tras 15 intentos. ¿Está activo el rate limiting?")

if __name__ == "__main__":
    attack()
