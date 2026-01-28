# Módulo 7: Análisis de Stealers (Info-Stealers)

> ⏱️ **Tiempo estimado**: 45 minutos

## 🎯 Objetivos de Aprendizaje

- Comprender cómo funcionan los info-stealers
- Analizar logs y datos extraídos
- Mapear comportamiento a MITRE ATT&CK
- Identificar Indicators of Compromise (IOCs)
- Proponer contramedidas

## 📖 Teoría

### ¿Qué son los Stealers?

**Info-stealers** (ladrones de información) son malware diseñado para extraer datos sensibles:

- Credenciales de navegadores
- Cookies de sesión
- Wallets de criptomonedas
- Información del sistema
- Archivos y documentos
- Claves SSH/FTP

### Modelos de distribución

| Modelo | Descripción | Ejemplos |
|--------|-------------|----------|
| **MaaS** | Malware-as-a-Service, panel de control | Redline, Raccoon, Vidar |
| **Open Source** | Código disponible públicamente | Kematian, AgentTesla (versiones antiguas) |
| **Custom** | Desarrollados ad-hoc para campañas específicas | APT stealers |

---

## 🦠 Stealers Comunes

### Redline Stealer

- **Precio**: ~$150-200 (MaaS)
- **Capacidades**:
  - Navegadores: Chrome, Firefox, Edge, Opera
  - Wallets: Exodus, Electrum, Atomic
  - Aplicaciones: Discord, Telegram, Steam
  - Captura de screenshots

### Raccoon Stealer

- **Precio**: ~$75/semana
- **Características**:
  - Sistema de plugins modular
  - Soporte para 60+ navegadores
  - Exfiltración vía Telegram

### Vidar

- **Fork de** Arkei Stealer
- **Distribución**: Malvertising, phishing
- **Enfoque**: Crypto wallets y credenciales

## 🦠 Herramientas de Extracción (Post-Explotación)

Para generar estos logs en un pentest (o por un atacante), se usan herramientas como:

### LaZagne
- **Estándar Open Source**.
- Recupera contraseñas almacenadas localmente (Browsers, WiFi, Git, SVN, bases de datos).
- El ejercicio simulado se basa en el output típico de LaZagne.

### DonPAPI
- Especializado en extraer credenciales protegidas por **DPAPI** en Windows.
- Ataca secretos de dominio cacheados.

---

## 💻 Ejercicio Práctico

### Escenario

Has obtenido logs de un stealer de un sistema comprometido (simulado). Tu tarea es **analizar** qué información fue robada y **mapear** a MITRE ATT&CK.

### Estructura de archivos

```bash
cd /exercises/module7/stealer_logs

tree
# .
# ├── system_info.txt       # Información del sistema
# ├── passwords.txt         # Credenciales de navegadores
# ├── cookies.txt           # Cookies de sesión
# ├── autofill.txt          # Datos de autocompletado
# ├── crypto_wallets/       # Wallets detectadas
# └── process_list.txt      # Procesos en ejecución
```

---

### Paso 1: Análisis de system_info.txt 🖥️

```bash
cat system_info.txt
```

**Contenido esperado**:
```
OS: Windows 10 Pro 21H2
Hostname: DESKTOP-ABC123
Username: john.doe
IP Address: 192.168.1.105
Public IP: 203.0.113.45
Location: Madrid, Spain
ISP: Telefonica
Installed AV: Windows Defender (Real-time: Disabled)
Screen Resolution: 1920x1080
```

**Técnicas MITRE ATT&CK**:
- **T1082**: System Information Discovery
- **T1016**: System Network Configuration Discovery
- **T1518.001**: Software Discovery - Security Software

---

### Paso 2: Análisis de passwords.txt 🔑

```bash
head -20 passwords.txt
```

**Formato típico**:
```
URL: https://gmail.com
Username: john.doe@company.com
Password: MyP@ssw0rd123
Browser: Chrome 118.0

URL: https://github.com
Username: johndoe
Password: GitHub2024!
Browser: Chrome 118.0

URL: https://company-vpn.com
Username: jdoe
Password: VPN_Secret_456
Browser: Firefox 119.0
```

**Análisis**:
- ¿Cuántas credenciales únicas?
- ¿Qué servicios están comprometidos?
- ¿Hay reutilización de contraseñas?

```bash
# Contar credenciales
grep "URL:" passwords.txt | wc -l

# Servicios únicos
grep "URL:" passwords.txt | cut -d' ' -f2 | cut -d'/' -f3 | sort | uniq

# Passwords reutilizadas
grep "Password:" passwords.txt | sort | uniq -d
```

**Técnica MITRE ATT&CK**:
- **T1555.003**: Credentials from Web Browsers

---

### Paso 3: Análisis de cookies.txt 🍪

```bash
head -10 cookies.txt
```

**Formato**:
```
Domain: .github.com
Name: user_session
Value: GH1_abc...xyz
Expires: 2025-01-30
Secure: Yes
HttpOnly: Yes
```

**Impacto**: Cookies de sesión permiten **session hijacking** sin necesidad de credenciales.

**Servicios críticos**:
- Banking/finanzas
- Email corporativo
- VPN
- Admin panels

**Técnica MITRE ATT&CK**:
- **T1539**: Steal Web Session Cookie

---

### Paso 4: Análisis de crypto_wallets/ 💰

```bash
ls crypto_wallets/
# Metamask.txt
# Exodus.txt
# Electrum.txt
```

**Contenido típico**:
- Direcciones de wallets
- Private keys (si están sin cifrar)
- Seed phrases
- Balances

> [!CAUTION]
> En un caso real, esta información permite **robo directo** de fondos.

**Técnica MITRE ATT&CK**:
- **T1005**: Data from Local System
- (Customizada): Cryptocurrency Wallet Theft

---

### Paso 5: Completar mapeo MITRE ATT&CK 🗺️

Edita `mitre_mapping.md`:

```markdown
# MITRE ATT&CK Mapping - Stealer Analysis

## Tactics & Techniques

### Initial Access
- **T1566.001** Phishing: Spearphishing Attachment
  - Probable vector de infección

### Discovery
- **T1082** System Information Discovery
  - Evidencia: system_info.txt contiene OS, hostname, user
- **T1016** System Network Configuration Discovery
  - Evidencia: IP addresses (local y pública)
- **T1518.001** Software Discovery: Security Software Discovery
  - Evidencia: Detección de Windows Defender
- **T1057** Process Discovery
  - Evidencia: process_list.txt

### Credential Access
- **T1555.003** Credentials from Web Browsers
  - Evidencia: passwords.txt con múltiples credenciales
- **T1539** Steal Web Session Cookie
  - Evidencia: cookies.txt

### Collection
- **T1005** Data from Local System
  - Evidencia: Wallets, autofill data
- **T1113** Screen Capture (si hay screenshots)

### Exfiltration
- **T1041** Exfiltration Over C2 Channel
  - Asumido: Los datos fueron enviados al atacante

## Indicators of Compromise (IOCs)

### File Paths
- `%APPDATA%\stealer.exe`
- `%TEMP%\system_info.txt`

### Registry Keys
- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater`

### Network
- C2 IP: 198.51.100.42:443
- Domain: update-server[.]com

## Impact Assessment

- **High**: Credenciales corporativas comprometidas (VPN, email)
- **High**: Sesiones activas robadas
- **Critical**: Private keys de crypto wallets
- **Medium**: Información personal (autofill)

## Recommended Mitigations

1. Forzar reset de todas las contraseñas comprometidas
2. Invalidar todas las sesiones activas
3. Transferir fondos de wallets comprometidas
4. Habilitar MFA en todas las cuentas
5. Reinstalar el sistema operativo
6. Actualizar reglas de EDR para detectar stealer
```

---

## 🔬 Análisis Forense Adicional

### Buscar patrones de exfiltración

```bash
# Si tienes logs de red (PCAP)
strings network.pcap | grep -E "(password|cookie|wallet)"

# Buscar archivos ZIP (stealers suelen comprimir datos)
find / -name "*.zip" -mtime -1
```

### Analizar proceso sospechoso

```bash
# Si process_list.txt contiene el PID del stealer
grep "stealer" process_list.txt

# Ejemplo output:
# PID: 4532
# Name: svchost.exe
# Path: C:\Users\john.doe\AppData\Roaming\svchost.exe  <-- SOSPECHOSO
```

---

## 🛡️ Contramedidas

### Para Usuarios

1. **Password Manager**: Nunca guardar contraseñas en navegadores
2. **2FA/MFA**: Siempre habilitar
3. **Antivirus actualizado**: Con protección en tiempo real
4. **Evitar ejecutables sospechosos**: No abrir adjuntos desconocidos

### Para Organizaciones

1. **EDR (Endpoint Detection & Response)**:
   - CrowdStrike Falcon
   - Microsoft Defender for Endpoint
   - SentinelOne

2. **Network Segmentation**: Limitar movimiento lateral

3. **Application Whitelisting**: Solo ejecutables autorizados

4. **User training**: Phishing awareness

---

## 📊 Caso Real: Redline Distribution (2023)

**Método**:
1. Malvertising en Google Ads
2. Sitio falso de software popular (e.g., "Download Zoom")
3. Usuario descarga ejecutable troyanizado
4. Redline se ejecuta silenciosamente
5. Datos exfiltrados a panel C2

**Impacto**:
- Miles de usuarios comprometidos
- Credenciales vendidas en dark web
- Estimado: $50-100 por "log" completo

---

## 🔍 Herramientas de Análisis

### Análisis de malware (fuera del alcance del taller)

- **Sandbox**: ANY.RUN, Joe Sandbox
- **Decompilers**: IDA Pro, Ghidra
- **Behavioral analysis**: Process Monitor, Procmon

### YARA Rules para detección

```yara
rule Redline_Stealer
{
    meta:
        description = "Detects Redline Stealer"
        author = "Researcher"
    
    strings:
        $s1 = "Cookies" wide
        $s2 = "Autofills" wide
        $s3 = "LocalState" wide
        $url = /https?:\/\/[a-z0-9\-\.]+\/panel/ nocase
    
    condition:
        3 of them
}
```

---

## 🤔 Preguntas de Reflexión

1. **Prevención**: ¿Qué habría prevenido esta infección?

2. **Detección**: ¿Cómo detectarías un stealer activo en tu sistema?

3. **Respuesta**: Si fueras el CISO, ¿cuáles serían tus primeras acciones?

4. **Valoración**: ¿Cuál es el impacto real de credenciales robadas para una organización?

---

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Analizaste todos los archivos del stealer
- [ ] Completaste el mapeo a MITRE ATT&CK
- [ ] Identificaste al menos 5 técnicas
- [ ] Propusiste contramedidas específicas
- [ ] Comprendiste el modelo de negocio MaaS

---

🔙 [Anterior: Módulo 6 - Credential Stuffing](../module6/README.md) | 🔜 [Siguiente: Módulo 8 - Detección y Defensa](../module8/README.md)

---

## 🎓 ¿Qué sigue?

Has completado el análisis de stealers. Ahora pasarás a la perspectiva del defensor en el **Módulo 8**.

Has aprendido:
- ✅ Cracking offline (fuerza bruta, diccionarios, reglas)
- ✅ Perfiling con CUPP
- ✅ Ataques online con Hydra
- ✅ Credential stuffing
- ✅ Análisis de stealers y MITRE ATT&CK

**Próximos pasos**:
1. Practica en plataformas como **HackTheBox**, **TryHackMe**
2. Obtén certificaciones: **CEH**, **OSCP**, **GPEN**
3. Participa en **CTFs**
4. Contribuye a la comunidad de seguridad
