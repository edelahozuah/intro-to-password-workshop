# Módulo 10: Phishing 2FA con Modlishka

## 🎯 Objetivo de Aprendizaje
Entender la amenaza de los ataques de **Reverse Proxy Phishing** capaces de eludir la autenticación de doble factor (2FA) capturando no solo credenciales, sino también tokens SMS/TOTP y cookies de sesión.

---

## 🏗️ Arquitectura del Escenario

El entorno incluye dos nuevos contenedores:

1.  **Víctima Simulada (`target-app`)**: Una aplicación bancaria falsa pero funcional.
    *   URL real (inaccesible directamente): `http://target-app`
    *   Flujo: Login -> 2FA (Token: 123456) -> Dashboard.
2.  **Atacante (`modlishka`)**: Reverse Proxy malicioso.
    *   Dominio Phishing: `https://phishing.local`
    *   Intermediario: Cliente <-> Modlishka <-> Víctima.

---

## 🚀 Instrucciones de Ejecución

### 1. Configuración de DNS Local
Para simular un dominio, necesitamos engañar a tu ordenador para que `phishing.local` apunte a tu máquina local (donde corre Docker).

Edita tu archivo hosts:
*   **Mac/Linux**: `sudo nano /etc/hosts`
*   **Windows**: `notepad c:\windows\system32\drivers\etc\hosts` (Como admin)

Añade la siguiente línea:
```
127.0.0.1 phishing.local
```

### 2. Iniciar el Entorno
Asegúrate de reconstruir para crear los nuevos contenedores:
```bash
docker-compose up -d --build
```

### 3. El Ataque 🕵️‍♂️

1.  Abre tu navegador (Firefox/Chrome).
2.  Navega a: `https://phishing.local`
3.  **Advertencia de Seguridad**: Verás una alerta de certificado SSL no válido.
    *   *¿Por qué?* Modlishka ha generado un certificado autofirmado para `phishing.local`. En un ataque real, el atacante usaría Let's Encrypt para tener candado verde.
    *   **Acción**: Acepta el riesgo y continúa.
4.  Verás la página de login del banco. ¡Parece real!
5.  Introduce:
    *   User: `admin`
    *   Pass: `password123`
6.  Te pedirá 2FA. Introduce `123456`.
7.  Accederás al Dashboard.

### 4. Ver los Datos Robados 🔓

Mientras hacías esto, Modlishka ha estado interceptando todo.
Mira los logs del contenedor Modlishka:

```bash
docker logs -f workshop_modlishka
```

Busca líneas que contengan:
*   `Post data: username=admin...`
*   `Post data: otp=123456...`
*   **SESSION_ID**: ¡El atacante ha robado tu cookie de sesión! Con esto puede acceder a tu cuenta sin necesitar password ni 2FA.

---

## 🛡️ Contramedidas

¿Cómo detiene esto el **FIDO2 / WebAuthn** (Llaves de seguridad, Passkeys)?

A diferencia de los SMS/TOTP, WebAuthn vincula criptográficamente el login con el **dominio del navegador**.
*   Si estás en `google.com`, la llave firma para `google.com`.
*   Si estás en `phishing.local`, la llave firma para `phishing.local` (o se niega a firmar).
*   El servidor real (`google.com`) recibe una firma inválida y rechaza el acceso, deteniendo el ataque de Modlishka.
