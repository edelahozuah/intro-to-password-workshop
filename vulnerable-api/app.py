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

@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint de login vulnerable
    NO implementa: rate limiting, account lockout, CAPTCHA
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing username or password'
        }), 400
    
    username = data['username']
    password = data['password']
    
    # Log del intento (para debugging)
    print(f"[{datetime.now()}] Login attempt: {username}")
    
    # Verificar credenciales
    if username in users:
        # Comparar hash MD5 (inseguro)
        if users[username]['password_hash'] == hash_password(password):
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'username': username,
                    'email': users[username]['email']
                },
                'token': f"TOKEN_{username}_{datetime.now().timestamp()}"
            }), 200
    
    # Fallo de autenticación
    return jsonify({
        'success': False,
        'error': 'Invalid username or password'
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
            'rate_limiting': False,
            'account_lockout': False,
            'captcha': False,
            'mfa': False,
            'password_hashing': 'MD5 (WEAK)'
        }
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
