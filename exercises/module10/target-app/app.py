from flask import Flask, request, render_template, redirect, url_for, make_response, session
import secrets

app = Flask(__name__)
app.secret_key = 'super-secret-key-target-app'

# Base de datos dummy
USERS = {
    "admin": "password123",
    "john": "secret"
}

TOKENS = {
    "admin": "123456",
    "john": "000000"
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('SESSION_ID'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['pre_auth_user'] = username
            return redirect(url_for('two_factor'))
        else:
            return render_template('login.html', error="Credenciales inválidas")
            
    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if 'pre_auth_user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        token = request.form.get('otp')
        user = session['pre_auth_user']
        
        if token == TOKENS.get(user, '123456'): # Por defecto 123456
            # Login exitoso
            resp = make_response(redirect(url_for('dashboard')))
            # Generar Session ID segura
            session_id = secrets.token_hex(16)
            resp.set_cookie('SESSION_ID', session_id, httponly=True, secure=False) # Secure=False para lab local sin HTTPS
            session.pop('pre_auth_user')
            return resp
        else:
            return render_template('2fa.html', error="Código inválido")
            
    return render_template('2fa.html')

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('SESSION_ID')
    if not token:
        return redirect(url_for('login'))
    return render_template('dashboard.html', token=token)

if __name__ == '__main__':
    # Ejecutamos en puerto 80 (HTTP) para debug y redirección interna si hiciera falta
    # Pero para Modlishka necesitamos port 443 (HTTPS)
    # Flask dev server no soporta dual stack fácil. Usaremos 443 con SSL.
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
