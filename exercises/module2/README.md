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

## 🛠️ Herramientas y Diccionarios

### 📦 ¿Qué incluye el entorno?

El contenedor `attacker` ya viene preconfigurado con las mejores colecciones de diccionarios. No necesitas descargar nada de Internet, ya están en estas rutas locales del contenedor:

1.  **RockYou**: `/wordlists/rockyou.txt` (El clásico imprescindible).
    *   *Nota: En algunos entornos puede estar comprimido en `/usr/share/wordlists/`.*
2.  **SecLists**: `/opt/SecLists/`
    *   La colección estándar de la industria.
    *   Passwords: `/opt/SecLists/Passwords/`
    *   Usernames: `/opt/SecLists/Usernames/`
3.  **Palabrario**: `/opt/palabrario/`
    *   Diccionarios específicos en **Español**.

### 📂 Cargar tus propios diccionarios (Custom Volume)

Hemos habilitado un volumen especial para que puedas usar tus propios ficheros `.txt` sin reconstruir el contenedor.

1.  **En tu máquina (Host)**:
    Deja cualquier fichero en la carpeta `custom_wordlists/` que está en la raíz del proyecto.
    
    ```bash
    # Ejemplo: Crear un diccionario personalizado rápido
    echo "admin123" > custom_wordlists/mi_diccionario.txt
    ```

2.  **En el contenedor (Attacker)**:
    El fichero aparecerá automáticamente en `/custom_wordlists/`.

    ```bash
    # Verificar desde dentro del contenedor
    ls -l /custom_wordlists/
    ```

Este método es ideal para cargar diccionarios generados por herramientas externas (como `cupp`) o descargados de otras fuentes.

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

### Módulo 2: Diccionarios y Listas de Palabras

> ⏱️ **Tiempo estimado**: 45 minutos

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

🔙 [Anterior: Módulo 1 - Fuerza Bruta](../module1/README.md) | 🔜 [Siguiente: Módulo 3 - Diccionarios Personalizados](../module3/README.md)
