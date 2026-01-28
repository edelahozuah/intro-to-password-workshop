#!/usr/bin/env python3
"""
API Vulnerable para Credential Stuffing
Simula una API REST con autenticación débil (sin rate limiting)
"""

from flask import Flask, request, jsonify
import json
import hashlib
from datetime import datetime

app = Flask(__name__)

# Base de datos simulada de usuarios
USERS_DB_FILE = 'users_db.json'

def load_users():
    """Carga usuarios desde JSON"""
    try:
        with open(USERS_DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def hash_password(password):
    """Hash MD5 débil (intencionalmente inseguro)"""
    return hashlib.md5(password.encode()).hexdigest()

# Cargar usuarios
users = load_users()

@app.route('/')
def index():
    return jsonify({
        'service': 'Vulnerable API',
        'version': '1.0',
        'endpoints': ['/api/login', '/api/register', '/api/profile']
    })

# Rate Limiting simulación
FAILED_ATTEMPTS = {}
BLOCKED_IPS = {}
BLOCK_DURATION = 60  # segundos

def get_client_ip():
    """Obtiene la IP del cliente (soporta X-Forwarded-For)"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def is_ip_blocked(ip):
    """Verifica si una IP está bloqueada"""
    if ip in BLOCKED_IPS:
        if datetime.now().timestamp() < BLOCKED_IPS[ip]:
            return True
        else:
            del BLOCKED_IPS[ip]  # Expira bloqueo
            if ip in FAILED_ATTEMPTS:
                del FAILED_ATTEMPTS[ip]
    return False

@app.route('/api/check-ip', methods=['GET'])
def check_ip():
    """Endpoint para verificar la IP de origen (útil para probar proxies)"""
    client_ip = get_client_ip()
    return jsonify({
        'ip': client_ip,
        'blocked': is_ip_blocked(client_ip),
        'headers': dict(request.headers)
    })

@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint de login vulnerable pero con Rate Limiting simple
    """
    client_ip = get_client_ip()
    
    # Verificar bloqueo
    if is_ip_blocked(client_ip):
        return jsonify({
            'success': False,
            'error': 'Too many failed attempts. IP blocked temporarily.'
        }), 429

    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing username or password'
        }), 400
    
    username = data['username']
    password = data['password']
    
    # Log del intento
    print(f"[{datetime.now()}] Login attempt: {username} from {client_ip}")
    
    # Verificar credenciales
    if username in users:
        if users[username]['password_hash'] == hash_password(password):
            # Reset intentos fallidos al éxito
            if client_ip in FAILED_ATTEMPTS:
                del FAILED_ATTEMPTS[client_ip]
                
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'username': username,
                    'email': users[username]['email']
                },
                'token': f"TOKEN_{username}_{datetime.now().timestamp()}"
            }), 200
    
    # Registrar fallo
    FAILED_ATTEMPTS[client_ip] = FAILED_ATTEMPTS.get(client_ip, 0) + 1
    
    # Bloquear si > 5 intentos
    if FAILED_ATTEMPTS[client_ip] >= 5:
        BLOCKED_IPS[client_ip] = datetime.now().timestamp() + BLOCK_DURATION
        print(f"⚠️ BLOCKING IP {client_ip} for {BLOCK_DURATION}s")
    
    return jsonify({
        'success': False,
        'error': 'Invalid username or password',
        'attempts_left': max(0, 5 - FAILED_ATTEMPTS.get(client_ip, 0))
    }), 401

@app.route('/api/register', methods=['POST'])
def register():
    """Endpoint para registrar nuevos usuarios"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
    
    username = data['username']
    
    if username in users:
        return jsonify({
            'success': False,
            'error': 'Username already exists'
        }), 409
    
    users[username] = {
        'email': data['email'],
        'password_hash': hash_password(data['password']),
        'created': datetime.now().isoformat()
    }
    
    # Guardar en archivo
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully'
    }), 201

@app.route('/api/profile/<username>', methods=['GET'])
def profile(username):
    """Obtener perfil de usuario (requiere token en producción)"""
    if username not in users:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'user': {
            'username': username,
            'email': users[username]['email'],
            'created': users[username].get('created', 'Unknown')
        }
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Estadísticas de la API"""
    return jsonify({
        'total_users': len(users),
        'service_status': 'running',
        'security_features': {
            'rate_limiting': True,
            'account_lockout': False,
            'captcha': False,
            'mfa': False,
            'password_hashing': 'MD5 (WEAK)'
        },
        'blocked_ips_count': len(BLOCKED_IPS)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Vulnerable API Server")
    print("=" * 60)
    print("WARNING: This API is intentionally insecure!")
    print("For educational purposes only.")
    print("=" * 60)
    print(f"Total users loaded: {len(users)}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
