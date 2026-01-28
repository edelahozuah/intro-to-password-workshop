#!/usr/bin/env python3
import random
import time
import json
import os
from datetime import datetime, timedelta

# Configuración
LOG_DIR = "../exercises/module8/logs"
START_TIME = datetime.now() - timedelta(days=1)

# IPs
ATTACKER_IP_BRUTE = "192.168.1.105"
ATTACKER_IP_SPRAY = "203.0.113.42"
ATTACKER_IP_STUFFING = "198.51.100.23"
VICTIM_IP = "10.0.0.5"
VALID_USERS = ["admin", "john", "maria", "support", "test"]
COMMON_PASSWORDS = ["123456", "password", "admin", "welcome"]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_auth_log():
    """Genera logs SSH simulando Brute Force y Password Spraying"""
    filepath = os.path.join(LOG_DIR, "auth.log")
    print(f"[+] Generando {filepath}...")
    
    logs = []
    current_time = START_TIME
    
    # 1. Tráfico normal (ruido)
    for _ in range(200):
        current_time += timedelta(minutes=random.randint(1, 20))
        user = random.choice(VALID_USERS)
        ip = f"10.0.0.{random.randint(10, 50)}"
        timestamp = current_time.strftime("%b %d %H:%M:%S")
        
        if random.random() > 0.9: # 10% fallos normales
            msg = f"{timestamp} sshd[1234]: Failed password for {user} from {ip} port {random.randint(30000, 60000)} ssh2"
        else:
            msg = f"{timestamp} sshd[1234]: Accepted password for {user} from {ip} port {random.randint(30000, 60000)} ssh2"
        logs.append(msg)

    # 2. Ataque Brute Force (Misma IP, usuario existente, muchos intentos)
    bf_time = current_time + timedelta(hours=2)
    target_user = "root"
    for i in range(50):
        bf_time += timedelta(seconds=2)
        timestamp = bf_time.strftime("%b %d %H:%M:%S")
        msg = f"{timestamp} sshd[5678]: Failed password for {target_user} from {ATTACKER_IP_BRUTE} port {random.randint(30000, 60000)} ssh2"
        logs.append(msg)
    
    # 3. Password Spraying (Usuarios inexistentes -> "invalid user")
    spray_time = bf_time + timedelta(hours=4)
    users_to_spray = ["root", "admin", "service", "guest", "backup", "carlos", "laura"] + VALID_USERS
    for user in users_to_spray:
        spray_time += timedelta(minutes=5)
        timestamp = spray_time.strftime("%b %d %H:%M:%S")
        # Simular que algunos son invalidos para que grep "invalid user" funcione
        if user not in VALID_USERS and user != "root":
             msg = f"{timestamp} sshd[9999]: Failed password for invalid user {user} from {ATTACKER_IP_SPRAY} port {random.randint(30000, 60000)} ssh2"
        else:
             msg = f"{timestamp} sshd[9999]: Failed password for {user} from {ATTACKER_IP_SPRAY} port {random.randint(30000, 60000)} ssh2"
        logs.append(msg)

    # Ordenar y guardar
    logs.sort(key=lambda x: datetime.strptime(x[:15], "%b %d %H:%M:%S").replace(year=START_TIME.year))
    
    with open(filepath, "w") as f:
        f.write("\n".join(logs) + "\n")

def generate_access_log():
    """Genera logs Apache/Nginx simulando Credential Stuffing"""
    filepath = os.path.join(LOG_DIR, "access.log")
    print(f"[+] Generando {filepath}...")
    
    logs = []
    current_time = START_TIME
    
    # User Agents
    ua_normal = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ua_bot = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    
    # 1. Tráfico normal
    for _ in range(100):
        current_time += timedelta(minutes=random.randint(1, 10))
        ip = f"192.168.1.{random.randint(10, 50)}"
        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        logs.append(f'{ip} - - [{timestamp}] "GET /index.php HTTP/1.1" 200 2326 "-" "{ua_normal}"')
        logs.append(f'{ip} - - [{timestamp}] "GET /style.css HTTP/1.1" 200 562 "-" "{ua_normal}"')

    # 2. Credential Stuffing (Muchos POST /login fallidos, uno exitoso oculto)
    stuff_time = current_time + timedelta(hours=3)
    
    for i in range(100):
        stuff_time += timedelta(seconds=1)
        timestamp = stuff_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        
        # 1 de cada 100 es éxito
        if i == 42:
            status = 302 
            size = 532
            logs.append(f'{ATTACKER_IP_STUFFING} - - [{timestamp}] "POST /login.php HTTP/1.1" {status} {size} "-" "{ua_bot}"')
            logs.append(f'{ATTACKER_IP_STUFFING} - - [{timestamp}] "GET /dashboard.php HTTP/1.1" 200 4523 "-" "{ua_bot}"')
        else:
            status = 200 # Login erróneo
            size = 3400
            logs.append(f'{ATTACKER_IP_STUFFING} - - [{timestamp}] "POST /login.php HTTP/1.1" {status} {size} "-" "{ua_bot}"')

    with open(filepath, "w") as f:
        f.write("\n".join(logs) + "\n")

def generate_ad_logs():
    """Genera JSON logs de Azure AD para Impossible Travel"""
    filepath = os.path.join(LOG_DIR, "ad_signin_logs.json")
    print(f"[+] Generando {filepath}...")
    
    events = []
    base_time = datetime.now().replace(microsecond=0)
    
    # Caso Impossible Travel: Madrid -> Tokyo en 10 minutos
    
    # Evento 1: Login Madrid (Legítimo)
    t1 = base_time - timedelta(hours=2)
    events.append({
        "timestamp": t1.isoformat() + "Z",
        "user": "carlos.garcia@corp.local",
        "ip": "80.58.20.100",
        "location": {"city": "Madrid", "country": "ES"},
        "status": "success",
        "app": "Office 365",
        "is_compliant": True
    })
    
    # Evento 2: Login Tokyo (Sospechoso) - 10 mins después
    t2 = t1 + timedelta(minutes=10)
    events.append({
        "timestamp": t2.isoformat() + "Z",
        "user": "carlos.garcia@corp.local",
        "ip": "1.2.3.4",
        "location": {"city": "Tokyo", "country": "JP"},
        "status": "success",
        "app": "Office 365",
        "is_compliant": True,
        "alert": "Impossible Travel Detected"
    })
    
    # Caso Non-Compliant Device
    t3 = base_time - timedelta(hours=5)
    events.append({
        "timestamp": t3.isoformat() + "Z",
        "user": "maria.lopez@corp.local",
        "ip": "200.1.1.1",
        "location": {"city": "Bogota", "country": "CO"},
        "status": "success",
        "app": "Salesforce",
        "is_compliant": False
    })
    
    # Relleno
    for _ in range(20):
        t_rand = base_time - timedelta(hours=random.randint(1, 24))
        events.append({
            "timestamp": t_rand.isoformat() + "Z",
            "user": random.choice(["maria.lopez@corp.local", "john.doe@corp.local"]),
            "ip": f"100.20.{random.randint(1,255)}.{random.randint(1,255)}",
            "location": {"city": "New York", "country": "US"},
            "status": "success",
            "app": "SharePoint",
            "is_compliant": True
        })

    # Guardar JSON
    with open(filepath, "w") as f:
        json.dump(events, f, indent=2)

if __name__ == "__main__":
    ensure_dir(LOG_DIR)
    generate_auth_log()
    generate_access_log()
    generate_ad_logs()
    print("[*] Logs generados exitosamente en " + LOG_DIR)
