# Módulo 4: Reglas de Transformación

## 🎯 Objetivos de Aprendizaje

- Comprender cómo funcionan las reglas de mutación
- Aplicar reglas predefinidas de Hashcat y John
- Crear reglas personalizadas
- Optimizar wordlists con transformaciones eficientes

## 📖 Teoría

### ¿Qué son las reglas?

Las **reglas** aplican transformaciones sistemáticas a cada palabra de un diccionario:

- **Sin reglas**: `password` → 1 intento
- **Con reglas**: `password` → `Password`, `password1`, `password!`, `p@ssword`, `Password123!`, etc.

### Políticas de contraseñas comunes

Muchas organizaciones requieren:
- ✅ Al menos 8 caracteres
- ✅ Mayúscula + minúscula + número + especial
- ❌ Sin palabras del diccionario

**Resultado**: Usuarios transforman palabras simples → `Password123!`

### Reglas más efectivas

| Regla | Descripción | Ejemplo |
|-------|-------------|---------|
| `c` | Capitalizar | password → Password |
| `u` | Todo mayúsculas | password → PASSWORD |
| `l` | Todo minúsculas | PASSWORD → password |
| `$1 $2 $3` | Añadir 123 al final | password → password123 |
| `^S` | Añadir S al inicio | password → Spassword |
| `sa4` | Sustituir a por 4 | password → p4ssword |
| `c $2 $0 $2 $4` | Capitalizar + año | password → Password2024 |

---

## 🛠️ Sintaxis de Reglas

### Hashcat Rules

```bash
# Aplicar reglas
hashcat -m [hash_type] -a 0 hashes.txt wordlist.txt -r rules.rule

# Reglas predefinidas (Estándar)
/usr/share/hashcat/rules/best64.rule           # Top 64 reglas
/usr/share/hashcat/rules/dive.rule             # Reglas profundas

# Reglas Modernas (Probabilísticas)
/opt/rules/OneRuleToRuleThemAll.rule           # La "navaja suiza" estadística
/opt/rules/hob064.rule                         # De Hob0Rules (análisis de brechas)
```

### John the Ripper Rules

```bash
# Aplicar reglas
john --wordlist=wordlist.txt --rules=All hashes.txt

# Reglas predefinidas
--rules=Single    # Modo single
--rules=Wordlist  # Wordlist mode
--rules=Extra     # Extra mutations
--rules=All       # Todas las reglas
```

---

## 💻 Ejercicios Prácticos

### Preparación

```bash
cd /exercises/module4

# Archivos disponibles
ls -lh
# policy_hashes.txt - Hashes SHA-256 con políticas de complejidad
# base_wordlist.txt - Diccionario base pequeño
```

---

### Ejercicio 1: Reglas Best64 de Hashcat 🟢

```bash
# Ver las reglas
head /usr/share/hashcat/rules/best64.rule

# Aplicar best64 al diccionario base
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Ver resultados
hashcat -m 1400 policy_hashes.txt --show
```

**Pregunta**: ¿Cuántos hashes crackeaste? ¿Qué porcentaje del total?

---

### Ejercicio 2: Combinar múltiples reglas 🟡

```bash
# Aplicar dive.rule (más agresivo)
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r /usr/share/hashcat/rules/dive.rule

# Combinar best64 + leetspeak
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  -r /usr/share/hashcat/rules/leetspeak.rule
```

**Advertencia**: Múltiples reglas incrementan exponencialmente el tiempo.

---

### Ejercicio 3: Crear reglas personalizadas 🔴

Crea un archivo `custom_rules.rule`:

```bash
cat > custom_rules.rule << 'EOF'
# Capitalizar
c

# Capitalizar + año 2024
c $2 $0 $2 $4

# Capitalizar + año 2023
c $2 $0 $2 $3

# Capitalizar + !
c $!

# Capitalizar + 123
c $1 $2 $3

# Capitalizar + año + !
c $2 $0 $2 $4 $!

# Todo mayúsculas + 123
u $1 $2 $3

# Leet speak simple (a->4, e->3, i->1, o->0)
sa4 se3 si1 so0

# Leet + año
sa4 se3 si1 so0 $2 $0 $2 $4

# Duplicar palabra
d

# Primera letra mayúscula + invertir caso resto + 123
c t $1 $2 $3
EOF

# Aplicar reglas personalizadas
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r custom_rules.rule
```

---

### Ejercicio 4: John the Ripper con reglas 🌟

```bash
# Convertir hashes a formato John (si es necesario)
# Para este ejercicio, John puede leer hashes raw SHA-256

# Aplicar todas las reglas de John
john --format=raw-sha256 --wordlist=base_wordlist.txt --rules=All policy_hashes.txt

# Ver crackeados
john --show --format=raw-sha256 policy_hashes.txt
```

---

## 🔬 Análisis de Eficiencia

### Comparar cobertura

```bash
# Solo diccionario base (sin reglas)
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt

# Con best64
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Con custom rules
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r custom_rules.rule
```

**Resultado esperado**:

| Configuración | Candidatos | Crackeados | Tiempo |
|---------------|------------|------------|--------|
| Sin reglas | 10 | 2 (20%) | 0.1s |
| Best64 | 640 | 12 (48%) | 1s |
| Custom | 120 | 15 (60%) | 0.5s |

---

## 📝 Sintaxis Completa de Reglas

### Comandos básicos

```
:       No hacer nada (passthrough)
l       Lowercase todo
u       Uppercase todo
c       Capitalize (primera mayúscula)
C       Lowercase primera, uppercase resto
t       Toggle case (invertir)
TN      Toggle posición N
r       Reverse (invertir cadena)
d       Duplicate (duplicar)
f       Reflect (reflejar: xyz → xyzyx)
{       Rotate left
}       Rotate right
$X      Append character X
^X      Prepend character X
```

### Sustituciones

```
sXY     Sustituir todas las X por Y
@X      Purge character X (eliminar)
```

### Leet speak avanzado

```
sa4     a→4
sa@     a→@
se3     e→3
si1     i→1
si!     i→!
so0     o→0
ss$     s→$
sS$     S→$
st7     t→7
```

---

## 🧪 Regla de Oro: OneRuleToRuleThemAll 🏆

Esta regla única intenta aplicar las mutaciones más **estadísticamente probables** (años recientes, símbolos comunes) en un solo archivo. Es el equilibrio perfecto entre `best64` (muy simple) y fuerza bruta.

```bash
# Usar OneRuleToRuleThemAll (ya descargada en /opt/rules)
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r /opt/rules/OneRuleToRuleThemAll.rule
```

**Ejercicio 5: Hob0Rules**:
Intenta también con `hob064.rule` que está basada en estadísticas de análisis de brechas reales.

```bash
hashcat -m 1400 -a 0 policy_hashes.txt base_wordlist.txt -r /opt/rules/hob064.rule
```

---

## 🌍 Caso Real: Pwned Passwords

Troy Hunt (Have I Been Pwned) analizó **613M contraseñas filtradas**.

**Top transformaciones detectadas**:
1. Capitalizar primera letra (27%)
2. Añadir año al final (18%)
3. Añadir `!` o `1` al final (15%)
4. Leet speak básico (12%)

Las reglas simulan exactamente estos patrones.

---

## 🎨 Generador de Reglas Interactivo

Script para diseñar reglas:

```bash
#!/bin/bash
# rule_tester.sh
echo "Palabra base: $1"
echo "Regla: $2"
echo "$1" | hashcat --stdout -r <(echo "$2")
```

Uso:
```bash
chmod +x rule_tester.sh
./rule_tester.sh password "c $2 $0 $2 $4"
# Output: Password2024
```

---

## 🤔 Preguntas de Reflexión

1. **Equilibrio**: ¿Más reglas siempre es mejor? ¿Cuál es el trade-off?

2. **Políticas**: Las políticas de complejidad, ¿realmente mejoran la seguridad?

3. **Aprendizaje automático**: ¿Podrían las reglas generarse mediante ML analizando filtraciones?

4. **Defensa**: Como usuario, ¿cómo derrotar estos ataques basados en reglas?

---

## 📚 Recursos Adicionales

- [Hashcat Rule-Based Attack](https://hashcat.net/wiki/doku.php?id=rule_based_attack)
- [OneRuleToRuleThemAll GitHub](https://github.com/NotSoSecure/password_cracking_rules)
- [John the Ripper Rules Syntax](https://www.openwall.com/john/doc/RULES.shtml)

---

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Aplicaste best64 y crackeaste ≥10 hashes
- [ ] Creaste un archivo de reglas personalizado
- [ ] Comprendiste la sintaxis de reglas
- [ ] Comparaste eficiencia: diccionario vs diccionario+reglas
- [ ] Reflexionaste sobre el impacto de políticas de complejidad

---

**Anterior**: [Módulo 3 - CUPP](../module3/README.md)  
**Siguiente**: [Módulo 5 - Ataques Online](../module5/README.md)
