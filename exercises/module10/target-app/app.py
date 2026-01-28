import pyotp
import qrcode
import io
from flask import Flask, request, render_template, redirect, url_for, make_response, session, send_file

app = Flask(__name__)
app.secret_key = 'super-secret-key-target-app'

# Base de datos dummy
USERS = {
    "admin": "password123",
    "john": "secret"
}

# Secretos TOTP (Base32)
# admin secret: JBSWY3DPEHPK3PXP
USER_SECRETS = {
    "admin": "JBSWY3DPEHPK3PXP", 
    "john": pyotp.random_base32() 
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

@app.route('/qr_code')
def qr_code():
    if 'pre_auth_user' not in session:
        return "Unauthorized", 401
    
    user = session['pre_auth_user']
    secret = USER_SECRETS.get(user)
    if not secret:
        return "No secret found", 404
        
    # Generar URI para Google Authenticator
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user, issuer_name="SecureBank Workshop")
    
    # Generar imagen QR
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if 'pre_auth_user' not in session:
        return redirect(url_for('login'))
        
    user = session['pre_auth_user']
    
    if request.method == 'POST':
        token = request.form.get('otp')
        secret = USER_SECRETS.get(user)
        
        # Validar TOTP
        totp = pyotp.TOTP(secret)
        # verify() comprueba ventana de tiempo actual y pasado/futuro (window=1 -> +/- 30s)
        if totp.verify(token, valid_window=1): 
            # Login exitoso
            resp = make_response(redirect(url_for('dashboard')))
            # Generar Session ID segura
            session_id = secrets.token_hex(16)
            resp.set_cookie('SESSION_ID', session_id, httponly=True, secure=False) 
            session.pop('pre_auth_user')
            return resp
        else:
            return render_template('2fa.html', error="Código inválido o expirado")
            
    return render_template('2fa.html', show_qr=True)

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
