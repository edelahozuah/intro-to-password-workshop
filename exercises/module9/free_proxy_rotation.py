#!/usr/bin/env python3
"""
Rotación de IPs usando Proxies Gratuitos (Scraping)
Basado en la técnica de 'Free Proxy Automation'
"""
import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures

# URL para obtener proxies gratuitos (SSL Proxies)
PROXY_SOURCE_URL = "https://www.sslproxies.org/"

# URL para verificar IP (pública)
# IMPORTANTE: Los proxies públicos NO pueden acceder a nuestra red local Docker (vulnerable-api)
# Por eso usamos httpbin.org para demostrar que la IP cambia.
TARGET_URL = "https://httpbin.org/ip"

def get_free_proxies():
    """Scrapea la lista de proxies gratuitos"""
    print(f"[*] Obteniendo lista de proxies desde {PROXY_SOURCE_URL}...")
    try:
        response = requests.get(PROXY_SOURCE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-striped table-bordered')
        
        proxies = []
        if table:
             for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    ip = columns[0].text
                    port = columns[1].text
                    https = columns[6].text
                    if https == "yes":
                        proxies.append(f"{ip}:{port}")
        
        print(f"[*] Se encontraron {len(proxies)} proxies HTTPS.")
        return proxies
    except Exception as e:
        print(f"[!] Error obteniendo proxies: {e}")
        return []

def check_proxy(proxy):
    """Verifica si un proxy funciona y cuál es su IP de salida"""
    try:
        proxies = {"https": proxy, "http": proxy}
        # Timeout corto porque los proxies gratuitos son lentos/inestables
        r = requests.get(TARGET_URL, proxies=proxies, timeout=5)
        if r.status_code == 200:
            origin = r.json().get("origin")
            print(f"[+] Proxy Funcional: {proxy} -> IP Remota: {origin}")
            return proxy
    except:
        # print(f"[-] Proxy Fallido: {proxy}")
        pass
    return None

def main():
    print("="*60)
    print("DEMOSTRACIÓN DE ROTACIÓN CON PROXIES GRATUITOS")
    print("⚠️  ADVERTENCIA: Los proxies públicos externos NO pueden acceder")
    print("    a la red Docker interna (http://vulnerable-api:5000).")
    print("    Esta demo verifica la rotación contra https://httpbin.org/ip")
    print("="*60)
    
    # 1. Obtener lista
    proxies = get_free_proxies()
    if not proxies:
        return

    # 2. Seleccionar muestra aleatoria para no saturar
    sample_size = min(20, len(proxies))
    proxy_sample = random.sample(proxies, sample_size)
    
    print(f"[*] Verificando muestra de {sample_size} proxies (Multithreading)...")
    
    # 3. Verificar en paralelo
    working_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_proxy, proxy_sample)
        for result in results:
            if result:
                working_proxies.append(result)
    
    print("\n" + "="*60)
    print(f"RESUMEN: {len(working_proxies)} proxies funcionales de {sample_size} probados.")
    print("="*60)
    
    if len(working_proxies) > 0:
        print("Técnica demostrada: La IP de origen cambia con cada proxy exitoso.")
        print("En un ataque real, iterarías sobre 'working_proxies' para lanzar peticiones.")

if __name__ == "__main__":
    main()
