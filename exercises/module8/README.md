# Módulo 8: Detección y Defensa (Blue Team)

## 🎯 Objetivos de Aprendizaje

- Detectar ataques de fuerza bruta y spraying en logs de sistema
- Identificar credential stuffing en logs web
- Comprender y aplicar conceptos de **Conditional Access**
- Analizar logs JSON con `jq` para detectar viajes imposibles y dispositivos no conformes

## 📖 Teoría

### ¿Qué buscan los defensores (Blue Team)?

Mientras el atacante necesita **un** éxito, el defensor necesita detectar cualquiera de los **miles** de intentos fallidos.

| Ataque | Patrón en Logs |
|--------|---------------|
| **Fuerza Bruta** | Misma IP, mismo usuario, muchos fallos rápidos |
| **Password Spraying** | Misma IP, **muchos usuarios diferentes**, 1-2 fallos por usuario |
| **Credential Stuffing** | IPs rotatorias (o misma IP), usuarios aleatorios, ratio alto de fallos pero posible éxito (200 OK) |

### Conditional Access (Acceso Condicional)

El paradigma moderno "Zero Trust" no confía solo en usuario/password. Evalúa el **contexto** del acceso.

Señales de riesgo:
1.  **Impossible Travel**: Login en Madrid a las 10:00 y en Tokio a las 11:00. Físicamente imposible.
2.  **Unmanaged Device**: Dispositivo sin certificado corporativo o antivirus inactivo.
3.  **Risky IP**: Acceso desde Tor, IPs de reputación maliciosa o países sancionados.

**Políticas típicas**:
> "Si el usuario entra desde un país nuevo (riesgo medio), exigir MFA."
> "Si el dispositivo no es conforme (riesgo alto), bloquear acceso."

---

## 🛠️ Herramientas

### Comandos Linux esenciales

- `grep`: Filtrar líneas
- `awk`: Extraer columnas
- `sort | uniq -c`: Contar ocurrencias
- `jq`: Procesar JSON (vital para logs cloud como AWS/Azure)

---

## 💻 Ejercicios Prácticos

### Preparación

```bash
cd /exercises/module8/logs
ls -lh
# auth.log           (SSH)
# access.log         (Web Apache/Nginx)
# ad_signin_logs.json (Azure AD Simulado)
```

---

### Ejercicio 1: Detección en SSH (`auth.log`) 🕵️‍♂️

Analiza `auth.log` para identificar patrones.

#### 1. Identificar Fuerza Bruta
Busca una IP que intente insistentemente contra un solo usuario.

```bash
grep "Failed password" auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
# Nota: La columna $11 es la IP (ajustar según formato)
```

**Pregunta**: ¿Qué IP está atacando al usuario `root`?

#### 2. Identificar Password Spraying
Busca una IP que pruebe *muchos* usuarios distintos.

```bash
grep "Failed password" auth.log | grep "invalid user" | awk '{print $13}' | sort | uniq -c
# $13 es la IP en este formato de log
```

**Pregunta**: ¿Qué IP está probando usuarios como `admin`, `guest`, `oracle`?

---

### Ejercicio 2: Detección Web (`access.log`) 🌐

#### 1. Encontrar el ataque exitoso
Un ataque de fuerza bruta suele generar muchos errores 401 (Unauthorized) seguidos de un 302 (Redirect) o 200 (OK).

```bash
# Filtrar intentos de login (POST /login.php)
grep "POST /login.php" access.log

# Buscar quién tuvo éxito (código distinto a 401)
grep "POST /login.php" access.log | grep -v "401"
```

**Pregunta**: ¿Qué IP logró entrar? ¿A qué hora?

---

### Ejercicio 3: Conditional Access y JSON (`ad_signin_logs.json`) 🛡️

Los logs modernos (Azure, AWS, Okta) son JSON. Usaremos `jq` para analizarlos.

#### 1. Ver estructura

```bash
cat ad_signin_logs.json | jq .
```

#### 2. Detectar "Impossible Travel"
Buscamos un usuario que se haya movido distancias irreales en poco tiempo.

```bash
# Filtrar campos clave: timestamp, usuario, ubicación
cat ad_signin_logs.json | jq -c '.[] | {time: .timestamp, user: .user, loc: .location, alert: .alert}'
```

**Caso a analizar**: Busca a `carlos.garcia`.
- 08:15 -> Madrid
- 09:30 -> Tokyo
**Veredicto**: ¡Viaje Imposible! Credencial probablemente robada o VPN.

#### 3. Detectar Dispositivos No Conformes

```bash
# Filtrar logins exitosos PERO desde dispositivos no conformes (is_compliant: false)
cat ad_signin_logs.json | jq '.[] | select(.status=="success" and .is_compliant==false)'
```

**Reflexión**: ¿Por qué es peligroso permitir esto? (Malware en el dispositivo podría robar el token de sesión).

---

## 🛡️ Contramedidas y Respuesta

1.  **Block IP**: En el firewall / Fail2Ban.
2.  **Reset Password**: Obligar al usuario a cambiar contraseña.
3.  **Revoke Sessions**: Matar sesiones activas (cookies).
4.  **MFA Challenge**: Si es sospechoso pero no seguro, pedir 2FA.

---

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Identificaste la IP de fuerza bruta en SSH
- [ ] Identificaste la IP de password spraying
- [ ] Encontraste el login web exitoso entre los fallidos
- [ ] Usaste `jq` para detectar el "Impossible Travel"
- [ ] Entiendes la diferencia entre logs planos y estructurados (JSON)

---

**Anterior**: [Módulo 7 - Stealers](../module7/README.md)

---

## 🎓 Fin del Taller

¡Felicidades por completar el **Taller Práctico de Seguridad en Contraseñas**!

### Resumen de Aprendizajes

| Módulo | Técnicas Aprendidas |
|--------|---------------------|
| **1** | Cracking offline, fuerza bruta, John/Hashcat |
| **2** | Diccionarios (rockyou, SecLists, Weakpass) |
| **3** | CUPP, perfilado OSINT, diccionarios personalizados |
| **4** | Reglas de mutación, OneRuleToRuleThemAll |
| **5** | Ataques online con Hydra, FFUF |
| **6** | Credential stuffing, automatización |
| **7** | Stealers, análisis MITRE ATT&CK, IOCs |
| **8** | Detección Blue Team, Conditional Access, logs |

### Próximos Pasos

1. **Practica** en plataformas como [HackTheBox](https://hackthebox.com), [TryHackMe](https://tryhackme.com)
2. **Certifícate**: CEH, OSCP, GPEN, GIAC
3. **Participa** en CTFs (Capture The Flag)
4. **Contribuye** a la comunidad open source de seguridad

### Recursos Adicionales

- [OWASP Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Have I Been Pwned](https://haveibeenpwned.com/)
- [Hashcat Wiki](https://hashcat.net/wiki/)

---

> [!TIP]
> Recuerda: las técnicas aprendidas son **exclusivamente para uso ético y legal** en entornos autorizados.

---

🔙 [Volver al README principal](../../README.md)

