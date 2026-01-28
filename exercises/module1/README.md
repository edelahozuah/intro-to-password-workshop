# Módulo 1: Ataques Offline - Fuerza Bruta

## 🎯 Objetivos de Aprendizaje

- Comprender cómo se almacenan las contraseñas (hashing)
- Utilizar John the Ripper y Hashcat para fuerza bruta
- Evaluar la complejidad temporal de diferentes ataques
- Reconocer la importancia de contraseñas fuertes

## 📖 Teoría

### ¿Qué es un hash?

Un **hash criptográfico** es una función matemática que convierte cualquier entrada en una cadena de longitud fija. Propiedades:

- **Unidireccional**: No se puede revertir (en teoría)
- **Determinística**: Misma entrada = mismo hash
- **Efecto avalancha**: Pequeño cambio → hash completamente diferente

### Algoritmos comunes

| Algoritmo | Longitud | Estado | Uso |
|-----------|----------|--------|-----|
| MD5 | 128 bits | ⛔ Roto | Evitar |
| SHA-1 | 160 bits | ⚠️ Débil | Deprecado |
| SHA-256 | 256 bits | ✅ Seguro | Recomendado |
| bcrypt | Variable | ✅ Seguro | Contraseñas |

### Ataques de fuerza bruta

Probar **todas** las combinaciones posibles hasta encontrar la correcta.

**Espacio de búsqueda**:
- 4 dígitos (0-9): 10⁴ = 10,000 combinaciones
- 6 letras minúsculas: 26⁶ = 308,915,776 combinaciones
- 8 alfanuméricos: 62⁸ = 218,340,105,584,896 combinaciones

## 🛠️ Herramientas

### Identificación de Hashes: Name-That-Hash (NTH)

Herramienta moderna (reemplazo de hash-identifier) que usa probabilidad para detectar tipos de hash.

```bash
# Uso básico
nth --text "5f4dcc3b5aa765d61d8327deb882cf99"

# Identificar desde archivo
nth -f hashes.txt
```

### John the Ripper

```bash
# Sintaxis básica
john [opciones] archivo_hashes

# Modos
--incremental=Digits    # Solo dígitos
--incremental=Alpha     # Solo letras
--incremental=Alnum     # Alfanumérico

# Ver contraseñas crackeadas
john --show archivo_hashes
```

### Hashcat

```bash
# Sintaxis básica
hashcat -m [tipo_hash] -a [modo_ataque] archivo_hashes mascara

# Tipos de hash comunes
-m 0      # MD5
-m 100    # SHA1
-m 1400   # SHA256

# Modo de ataque
-a 3      # Fuerza bruta (mask attack)

# Máscaras
?d  # Dígito (0-9)
?l  # Minúscula (a-z)
?u  # Mayúscula (A-Z)
?a  # Todos los caracteres
```

## 💻 Ejercicios Prácticos

### Preparación

```bash
# Desde el contenedor attacker
cd /exercises/module1

# Verificar archivos
ls -lh
# Deberías ver:
# - hashes_level1.txt (10 hashes MD5 - PINs)
# - hashes_level2.txt (20 hashes MD5 - alfanuméricos cortos)
# - hashes_level3.txt (15 hashes SHA1 - con mayúsculas)
```

### Nivel 1: PINs de 4 dígitos 🟢

**Objetivo**: Crackear 10 hashes MD5 de PINs numéricos (0000-9999)

#### Con John the Ripper

```bash
# Ejecutar cracking
john --format=raw-md5 --incremental=Digits hashes_level1.txt

# Ver resultados
john --show --format=raw-md5 hashes_level1.txt
```

#### Con Hashcat

```bash
# Máscara: 4 dígitos
hashcat -m 0 -a 3 hashes_level1.txt ?d?d?d?d

# Ver resultados
hashcat -m 0 hashes_level1.txt --show
```

**Pregunta de reflexión**: ¿Cuánto tiempo tardó? ¿Por qué fue tan rápido?

---

### Nivel 2: Contraseñas alfanuméricas cortas 🟡

**Objetivo**: Crackear hashes MD5 de contraseñas de 4-6 caracteres (letras minúsculas y números)

#### Con Hashcat (recomendado para este nivel)

```bash
# Probar longitudes incrementales
hashcat -m 0 -a 3 hashes_level2.txt ?l?l?l?l        # 4 caracteres
hashcat -m 0 -a 3 hashes_level2.txt ?l?l?l?l?l      # 5 caracteres
hashcat -m 0 -a 3 hashes_level2.txt --increment --increment-min=4 --increment-max=6 ?a
```

**Nota**: Este nivel puede tardar más. El espacio de búsqueda crece exponencialmente.

---

### Nivel 3: Con mayúsculas y números 🔴

**Objetivo**: Crackear hashes SHA-1 de contraseñas con mayúsculas y números

```bash
# Hashcat con máscara mixta
hashcat -m 100 -a 3 hashes_level3.txt ?u?l?l?l?l?l?d?d?d?d

# Alternativa: dejar que Hashcat intente patrones comunes
hashcat -m 100 -a 3 hashes_level3.txt --increment --increment-min=6 --increment-max=10 ?a
```

**Advertencia**: Este nivel puede tardar **horas o días** dependiendo de tu hardware.

### Optimización: Probable-Wordlists

En un escenario real, antes de la fuerza bruta pura, usaríamos listas estadísticas como **Probable-Wordlists** o **Weakpass Top 100k**. Estas listas ordenan las contraseñas por probabilidad de uso, reduciendo el tiempo de cracking drásticamente comparado con un ataque de fuerza bruta lineal.

---

## 🧪 Experimentos Adicionales

### Comparar velocidad de algoritmos

```bash
# Benchmark de Hashcat
hashcat -b -m 0      # MD5
hashcat -b -m 100    # SHA1
hashcat -b -m 1400   # SHA256
hashcat -b -m 3200   # bcrypt
```

**Observa**: MD5 es mucho más rápido que bcrypt. ¿Por qué esto importa para la seguridad?

### Calcular tiempo estimado

Si Hashcat reporta **1,000,000 H/s** (hashes por segundo) para MD5:

- 4 dígitos (10,000 combinaciones): **0.01 segundos**
- 6 letras minúsculas (308M combinaciones): **5 minutos**
- 8 alfanuméricos (218T combinaciones): **~7 años**

## 📊 Verificación de Progreso

```bash
# Ver cuántos hashes has crackeado
john --show hashes_level1.txt | wc -l
john --show hashes_level2.txt | wc -l
john --show hashes_level3.txt | wc -l
```

**Objetivo mínimo**:
- ✅ Nivel 1: 10/10 (100%)
- ✅ Nivel 2: 15/20 (75%)
- ⚠️ Nivel 3: Variable (depende del tiempo disponible)

## 🤔 Preguntas de Reflexión

1. **Escalabilidad**: Si crackear 4 dígitos toma 0.01s, ¿cuánto tardaría 5 dígitos? ¿Y 6?

2. **Hardware**: ¿Cómo afectaría tener una GPU de alta gama al tiempo de cracking?

3. **Defensa**: Como administrador de sistemas, ¿qué medidas tomarías para proteger contraseñas?

4. **Ética**: ¿En qué situaciones es legal y ético realizar estos ataques?

## 📚 Recursos Adicionales

- [Hashcat Wiki - Mask Attack](https://hashcat.net/wiki/doku.php?id=mask_attack)
- [John the Ripper Modes](https://www.openwall.com/john/doc/MODES.shtml)
- [Password Hashing Competition](https://password-hashing.net/)

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Crackeaste exitosamente los hashes del Nivel 1
- [ ] Comprendes cómo funciona el ataque de fuerza bruta
- [ ] Puedes estimar el tiempo de cracking basado en el espacio de búsqueda
- [ ] Ejecutaste al menos un benchmark de Hashcat
- [ ] Respondiste las preguntas de reflexión

---

**Siguiente**: [Módulo 2 - Ataques con Diccionario](../module2/README.md)
