# Taller Práctico de Seguridad en Contraseñas

Un taller completo y reproducible diseñado para estudiantes de nivel iniciación que cubre el ciclo completo de ataques a contraseñas.

## 🎯 Objetivos del Taller

- Comprender cómo se almacenan y procesan las contraseñas
- Dominar técnicas de cracking offline y online
- Crear diccionarios personalizados y reglas de transformación
- Simular ataques de credential stuffing
- Analizar malware tipo stealer
- Aplicar el framework MITRE ATT&CK en análisis de amenazas

## 📋 Módulos y Herramientas

1. **Ataques Offline**: Fuerza bruta con **John/Hashcat** y **Name-That-Hash**.
2. **Diccionarios**: **SecLists**, **Probable-Wordlists** y **Weakpass**.
3. **Diccionarios Inteligentes**: **Pydictor** y profiling OSINT. **Mentalist** (visualización).
4. **Reglas de Mutación**: **OneRuleToRuleThemAll** y **Hob0Rules**.
5. **Ataques Online**: **Hydra** y **FFUF** (Web Fuzzing moderno).
6. **Credential Stuffing**: **CredMaster** (teoría) y scripts custom.
7. **Stealers**: Análisis de logs tipo **LaZagne/DonPAPI** con MITRE ATT&CK.
8. **Detección y Defensa**: Green/Blue Team, análisis de logs y **Conditional Access**.

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
│   └── module8/                # Detección y defensa (Blue Team)
├── wordlists/                  # Diccionarios de contraseñas
├── scripts/                    # Scripts de soporte
├── solutions/                  # Soluciones de ejercicios
├── slides/                     # Material de presentación
└── vulnerable-api/             # API vulnerable para prácticas (Flask)
```

## 🎓 Uso del Taller

### Para Instructores

1. Revisa las [soluciones](solutions/) antes de la sesión
2. Presenta cada módulo con las [slides](slides/)
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
