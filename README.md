# Taller Práctico de Seguridad en Contraseñas

Un taller completo y reproducible diseñado para estudiantes de nivel iniciación que cubre el ciclo completo de ataques a contraseñas.

## 🎯 Objetivos del Taller

- Comprender cómo se almacenan y procesan las contraseñas
- Dominar técnicas de cracking offline y online
- Crear diccionarios personalizados y reglas de transformación
- Simular ataques de credential stuffing
- Analizar malware tipo stealer
- Aplicar el framework MITRE ATT&CK en análisis de amenazas

## 📋 Navegación de Módulos

| Módulo | Temática | Tiempo Estimado | Descripción Breve |
| :--- | :--- | :--- | :--- |
| **[Módulo 1](exercises/module1/README.md)** | **Ataques Offline** | 45 min | Fuerza bruta con John/Hashcat y Name-That-Hash. |
| **[Módulo 2](exercises/module2/README.md)** | **Diccionarios** | 45 min | Uso de SecLists, RockYou y Probable-Wordlists. |
| **[Módulo 3](exercises/module3/README.md)** | **Diccionarios Custom** | 45 min | CUPP, OSINT y Pydictor. |
| **[Módulo 4](exercises/module4/README.md)** | **Reglas** | 45 min | Reglas de mutación Hashcat y OneRuleToRuleThemAll. |
| **[Módulo 5](exercises/module5/README.md)** | **Ataques Online** | 60 min | Hydra contra SSH y HTTP, FFUF. |
| **[Módulo 6](exercises/module6/README.md)** | **Credential Stuffing** | 60 min | Automatización de ataques con credenciales filtradas. |
| **[Módulo 7](exercises/module7/README.md)** | **Stealers** | 45 min | Análisis forense de logs de info-stealers (MITRE ATT&CK). |
| **[Módulo 8](exercises/module8/README.md)** | **Blue Team** | 45 min | Análisis de logs, detección y Conditional Access. |
| **[Módulo 9](exercises/module9/README.md)** | **Evasión** | 30 min | Rotación de IPs con **Tor** para evadir bloqueos. |
| **[Módulo 10](exercises/module10/README.md)** | **Phishing 2FA** | 60 min | Bypass de 2FA usando **Modlishka**. |


## 🚀 Inicio Rápido

### Requisitos Previos

- Docker y Docker Compose instalados
- Al menos 4GB de RAM libre
- 10GB de espacio en disco

### Instalación

```bash
# Clonar o descargar este repositorio
cd password-security-workshop

# Levantar el entorno completo
docker-compose up -d

# Verificar que los servicios están corriendo
docker-compose ps

# Acceder al contenedor de trabajo
docker-compose exec attacker /bin/bash
```

### Verificación del Entorno

```bash
# Probar SSH target
ssh testuser@ssh-target -p 2222
# Contraseña: password123

# Probar DVWA
curl http://dvwa

# Verificar herramientas instaladas
john --version
hashcat --version
hydra -h
```

### 🐳 Ejecución de Comandos en Contenedores

La mayoría de herramientas (hydra, john, hashcat, scripts python) están instaladas **dentro** del contenedor `attacker`.

Tienes dos formas de ejecutar los comandos:

**Opción A: Shell Interactivo (Recomendado)**
Accedes a la terminal del contenedor y ejecutas los comandos "normalmente".
```bash
docker-compose exec attacker /bin/bash
# Una vez dentro:
cd /exercises/module1
john --version
```

**Opción B: Ejecución Directa**
Lanzas el comando desde tu host sin entrar al contenedor.
```bash
docker-compose exec attacker python3 /exercises/module9/verify_block.py
docker-compose exec attacker hydra -h
```

> ⚠️ **Importante**: Si intentas ejecutar `python3` o `john` directamente en tu terminal (fuera de Docker), podría funcionar si los tienes instalados, pero **no tendrán acceso a la red interna del taller** (no verán a `vulnerable-api` ni `ssh-target`). Usa siempre `docker-compose exec attacker ...`.

## 📂 Estructura del Proyecto

```
password-security-workshop/
├── README.md                    # Este archivo
├── docker-compose.yml           # Infraestructura completa
├── exercises/                   # Ejercicios por módulo
│   ├── module1/                # Ataques offline (fuerza bruta)
│   ├── module2/                # Diccionarios (rockyou)
│   ├── module3/                # CUPP (diccionarios personalizados)
│   ├── module4/                # Reglas de mutación
│   ├── module5/                # Ataques online (Hydra)
│   ├── module6/                # Credential stuffing
│   ├── module7/                # Stealers y MITRE ATT&CK
│   ├── module8/                # Detección y defensa (Blue Team)
│   ├── module9/                # Evasión y Rotación de IPs (Tor)
│   └── module10/               # Phishing 2FA (Modlishka)
├── wordlists/                  # Diccionarios de contraseñas
├── scripts/                    # Scripts de soporte
├── solutions/                  # Soluciones de ejercicios
└── vulnerable-api/             # API vulnerable para prácticas (Flask)
```

## 🎓 Uso del Taller

### Para Instructores

1. Revisa las [soluciones](solutions/) antes de la sesión
2. **Ejecuta las demos** en el orden propuesto en `/exercises`
3. Deja que los estudiantes trabajen en los ejercicios
4. Usa los scripts de verificación para comprobar el progreso

### Para Estudiantes

Cada módulo contiene:
- `README.md`: Instrucciones y teoría
- Archivos de práctica (hashes, diccionarios, etc.)
- Comandos de ejemplo
- Ejercicios de reflexión

Trabaja módulo por módulo en orden para mejor comprensión.

## ⚖️ Consideraciones Éticas y Legales

> [!CAUTION]
> Las técnicas enseñadas en este taller son **exclusivamente para fines educativos** en entornos controlados.

- **NUNCA** ejecutes estas técnicas contra sistemas sin autorización explícita
- El pentesting no autorizado es **ilegal** en la mayoría de jurisdicciones
- Usa únicamente el entorno Docker proporcionado
- Respeta las leyes de privacidad y protección de datos

## 🛠️ Troubleshooting

### El contenedor attacker no arranca

```bash
docker-compose down
docker-compose up -d --force-recreate attacker
```

### No puedo conectar al SSH target

Verifica que el puerto 2222 no esté en uso:
```bash
lsof -i :2222
```

### Hashcat no detecta GPU

Hashcat requiere drivers específicos. Para este taller, el modo CPU es suficiente:
```bash
hashcat -m 0 -a 3 hashes.txt ?d?d?d?d --force
```

## 📚 Recursos Adicionales

- [OWASP Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [John the Ripper Documentation](https://www.openwall.com/john/doc/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Have I Been Pwned](https://haveibeenpwned.com/)

## 📄 Licencia

Este material educativo se distribuye bajo licencia MIT para uso educativo.

## 🤝 Contribuciones

¿Mejoras o ejercicios adicionales? Pull requests son bienvenidos.
