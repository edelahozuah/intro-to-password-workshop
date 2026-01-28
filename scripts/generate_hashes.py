#!/usr/bin/env python3
"""
Script para generar hashes de contraseñas para los ejercicios del taller.
Genera diferentes niveles de dificultad y tipos de hash.
"""

import hashlib
import random
import string
from typing import List, Tuple

def generate_pin_passwords(count: int = 10) -> List[str]:
    """Genera PINs de 4 dígitos"""
    pins = []
    for _ in range(count):
        pin = ''.join(random.choices(string.digits, k=4))
        pins.append(pin)
    return pins

def generate_simple_passwords(count: int = 20) -> List[str]:
    """Genera contraseñas alfanuméricas simples (4-6 caracteres)"""
    passwords = []
    wordlist = ['admin', 'user', 'test', 'demo', 'pass', 'root', 'login', 'web']
    
    for _ in range(count):
        if random.random() < 0.5:
            # Palabra del diccionario con números
            word = random.choice(wordlist)
            num = random.randint(0, 999)
            passwords.append(f"{word}{num}")
        else:
            # Alfanumérico aleatorio
            length = random.randint(4, 6)
            pwd = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            passwords.append(pwd)
    
    return passwords

def generate_complex_passwords(count: int = 15) -> List[str]:
    """Genera contraseñas con mayúsculas, minúsculas y números"""
    passwords = []
    words = ['Password', 'Welcome', 'Hello', 'Secret', 'Secure', 'Access']
    
    for _ in range(count):
        word = random.choice(words)
        num = random.randint(0, 9999)
        passwords.append(f"{word}{num}")
    
    return passwords

def generate_common_passwords() -> List[str]:
    """Lista de contraseñas comunes reales"""
    return [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'superman', 'qazwsx', 'michael', 'football', 'welcome',
        'jesus', 'ninja', 'mustang', 'password1', '123456789',
        'admin', 'root', 'toor', 'pass', 'test',
        'guest', 'oracle', 'changeme', 'password123', 'admin123'
    ]

def generate_policy_passwords(count: int = 25) -> List[str]:
    """Contraseñas que cumplen políticas de complejidad (8+ chars, may+min+num+especial)"""
    passwords = []
    base_words = ['Summer', 'Winter', 'Spring', 'Autumn', 'Monday', 'Friday',
                  'Coffee', 'Mountain', 'River', 'Ocean', 'Forest', 'Desert']
    special_chars = '!@#$'
    
    for _ in range(count):
        word = random.choice(base_words)
        year = random.randint(2010, 2024)
        special = random.choice(special_chars)
        passwords.append(f"{word}{year}{special}")
    
    return passwords

def hash_password(password: str, algorithm: str = 'md5') -> str:
    """Hashea una contraseña con el algoritmo especificado"""
    if algorithm == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(password.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(password.encode()).hexdigest()
    else:
        raise ValueError(f"Algoritmo no soportado: {algorithm}")

def save_hashes(passwords: List[str], filename: str, algorithm: str = 'md5',
                include_username: bool = False):
    """Guarda hashes en un archivo"""
    with open(filename, 'w') as f:
        for i, password in enumerate(passwords):
            pwd_hash = hash_password(password, algorithm)
            if include_username:
                username = f"user{i+1:03d}"
                f.write(f"{username}:{pwd_hash}\n")
            else:
                f.write(f"{pwd_hash}\n")
    print(f"✓ Generado {filename} con {len(passwords)} hashes {algorithm.upper()}")

def save_passwords(passwords: List[str], filename: str):
    """Guarda contraseñas en texto plano (para soluciones)"""
    with open(filename, 'w') as f:
        for password in passwords:
            f.write(f"{password}\n")
    print(f"✓ Guardadas {len(passwords)} contraseñas en {filename}")

def generate_credential_pairs(count: int = 50) -> List[Tuple[str, str]]:
    """Genera pares usuario:contraseña para credential stuffing"""
    credentials = []
    firstnames = ['john', 'mary', 'david', 'sarah', 'michael', 'jennifer', 'james',
                  'linda', 'robert', 'patricia', 'carlos', 'maria', 'jose', 'ana']
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'proton.me']
    passwords = generate_common_passwords()[:20]
    
    for _ in range(count):
        firstname = random.choice(firstnames)
        number = random.randint(1, 999)
        domain = random.choice(domains)
        username = f"{firstname}{number}@{domain}"
        password = random.choice(passwords)
        credentials.append((username, password))
    
    return credentials

def generate_module1():
    """Módulo 1: Ataques Offline - Fuerza Bruta"""
    print("\n[Módulo 1] Generando hashes para ataques de fuerza bruta...")
    
    # Level 1: PINs de 4 dígitos (MD5)
    pins = generate_pin_passwords(10)
    save_hashes(pins, '../exercises/module1/hashes_level1.txt', 'md5')
    save_passwords(pins, '../solutions/module1_level1_passwords.txt')
    
    # Level 2: Contraseñas cortas alfanuméricas (MD5)
    simple = generate_simple_passwords(20)
    save_hashes(simple, '../exercises/module1/hashes_level2.txt', 'md5')
    save_passwords(simple, '../solutions/module1_level2_passwords.txt')
    
    # Level 3: Contraseñas con mayúsculas (SHA1)
    complex_pwd = generate_complex_passwords(15)
    save_hashes(complex_pwd, '../exercises/module1/hashes_level3.txt', 'sha1')
    save_passwords(complex_pwd, '../solutions/module1_level3_passwords.txt')

def generate_module2():
    """Módulo 2: Ataques con Diccionario"""
    print("\n[Módulo 2] Generando hashes para ataques con diccionario...")
    
    # Contraseñas comunes (SHA-256)
    common = generate_common_passwords()
    save_hashes(common, '../exercises/module2/hashes_common.txt', 'sha256')
    save_passwords(common, '../solutions/module2_passwords.txt')

def generate_module3():
    """Módulo 3: Diccionarios Personalizados"""
    print("\n[Módulo 3] Generando escenario para CUPP...")
    
    # Contraseñas basadas en el perfil ficticio
    profile_passwords = [
        'Carlos1990', 'Garcia15', 'Laura2024', 'Max2020',
        'TechCorp123', 'RealMadrid', 'Futbol123', 'CarlosGarcia',
        'cgarcia1990', 'Madrid2024', 'MaxLaura', 'Tech@1990',
        'Carlos15031990', 'LauraMax', 'RealMadrid1990'
    ]
    
    save_hashes(profile_passwords, '../exercises/module3/target_hashes.txt', 'md5')
    save_passwords(profile_passwords, '../solutions/module3_passwords.txt')

def generate_module4():
    """Módulo 4: Reglas de Transformación"""
    print("\n[Módulo 4] Generando hashes con transformaciones comunes...")
    
    # Contraseñas base con transformaciones típicas
    base_words = ['password', 'welcome', 'admin', 'letmein', 'secure']
    policy_passwords = []
    
    for word in base_words:
        # Capitalización + año + especial
        policy_passwords.append(f"{word.capitalize()}2024!")
        policy_passwords.append(f"{word.capitalize()}2023#")
        # Leet speak básico
        leet = word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0')
        policy_passwords.append(f"{leet}123")
    
    save_hashes(policy_passwords, '../exercises/module4/policy_hashes.txt', 'sha256')
    save_passwords(policy_passwords, '../solutions/module4_passwords.txt')

def generate_module6():
    """Módulo 6: Credential Stuffing"""
    print("\n[Módulo 6] Generando credenciales filtradas ficticias...")
    
    credentials = generate_credential_pairs(100)
    
    # Guardar en formato usuario:contraseña
    with open('../exercises/module6/leaked_credentials.txt', 'w') as f:
        for username, password in credentials:
            f.write(f"{username}:{password}\n")
    
    print(f"✓ Generadas 100 credenciales en leaked_credentials.txt")

def main():
    """Genera todos los archivos de ejercicios"""
    print("=" * 60)
    print("Generador de Hashes - Taller de Seguridad en Contraseñas")
    print("=" * 60)
    
    generate_module1()
    generate_module2()
    generate_module3()
    generate_module4()
    generate_module6()
    
    print("\n" + "=" * 60)
    print("✅ Generación completada!")
    print("=" * 60)
    print("\nArchivos generados en exercises/ y solutions/")

if __name__ == "__main__":
    main()
