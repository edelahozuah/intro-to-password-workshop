# Módulo 3: Diccionarios Personalizados (OSINT + CUPP)

> ⏱️ **Tiempo estimado**: 45 minutos

```bash
# Antes de comenzar, sitúate en el directorio del módulo:
cd /exercises/module3
```

## 🎯 Objetivos de Aprendizaje

- Comprender la importancia del OSINT en seguridad
- Crear wordlists basadas en información del objetivo
- Utilizar CUPP (Common User Passwords Profiler)
- Aplicar técnicas de ingeniería social

## 📖 Teoría

### OSINT (Open Source Intelligence)

Recopilación de información de **fuentes públicas**:

- Redes sociales (LinkedIn, Twitter, Facebook)
- Sitios web corporativos
- Registros públicos
- Metadatos de documentos

### ¿Por qué personalizar wordlists?

Los usuarios incorporan información **personal** en contraseñas:

| Tipo de Información | Ejemplos | Frecuencia |
|---------------------|----------|------------|
| Nombres | Carlos, Laura, Max | Muy alta |
| Fechas | 1990, 15031990 | Alta |
| Lugares | Madrid, España | Media |
| Aficiones | Futbol, RealMadrid | Media |
| Empresas | TechCorp, Google | Baja |

**Estudio real** (2020): ~30% de contraseñas contienen el nombre del usuario.

### Herramientas Modernas

#### 1. Pydictor (El "Francotirador") 🎯
Más potente y flexible que CUPP. Permite manipulaciones complejas como longitud, prefijos/sufijos de empresa, y leetspeak avanzado.
- **Uso**: Generar listas inteligentes y compactas (50MB) en lugar de terabytes de basura.

#### 2. Mentalist (Visualización) 🧠
Herramienta gráfica (host) para crear "cadenas de reglas" (Nombre -> Añadir Año -> Mayúsculas).
- **Valor pedagógico**: Ayuda a visualizar el proceso de mutación antes de pasar a la línea de comandos.

---

## 🛠️ Herramientas en el Taller

### Pydictor

```bash
# Ubicación
cd /opt/pydictor

# Uso básico
python3 pydictor.py -base /exercises/module3/carlos_base.txt -o carlos_dict.txt
```

### CUPP (Legacy/Sencillo)

```bash
# Ubicación en el contenedor
cd /opt/cupp

# Ayuda
python3 cupp.py -h

# Modo interactivo
python3 cupp.py -i

# Modo con archivo de configuración
python3 cupp.py -w perfil.txt
```

### CeWL (Custom Word List generator)

Extrae palabras de sitios web:

```bash
# Sintaxis básica
cewl [opciones] URL -w salida.txt

# Opciones útiles
-d [depth]      # Profundidad de crawling
-m [min_length] # Longitud mínima de palabras
-o              # Incluir metadatos
```

---

## 💻 Ejercicio Práctico

### Escenario: Campaña de Spear Phishing

**Objetivo ficticio**: Carlos García

Has recopilado esta información mediante OSINT:

```yaml
Información Personal:
  Nombre: Carlos
  Apellido: García
  Apodo: Carlitos
  Fecha de nacimiento: 15/03/1990
  
Relaciones:
  Pareja: Laura
  Hijos: Ninguno
  Mascota: Max (perro)

Profesional:
  Empresa: TechCorp
  Puesto: Desarrollador Senior
  
Intereses:
  Deporte: Fútbol
  Equipo: Real Madrid
  Hobby: Gaming
```

---

### Paso 1: Generar wordlist con CUPP 🎨

```bash
cd /exercises/module3

# Ejecutar CUPP en modo interactivo
python3 /opt/cupp/cupp.py -i
```

**Responde las preguntas** con la información del perfil:

```
> First Name: Carlos
> Surname: Garcia
> Nickname: Carlitos
> Birthdate (DDMMYYYY): 15031990

> Partner's name: Laura
> Partner's nickname: 
> Partner's birthdate (DDMMYYYY): 

> Child's name: 
> Child's nickname: 
> Child's birthdate (DDMMYYYY): 

> Pet's name: Max
> Company name: TechCorp

> Do you want to add some key words about the victim? Y/N: y
> Please enter the words, separated by comma. [i.e. hacker,juice,black]: futbol,RealMadrid,gaming,Madrid

> Do you want to add special chars at the end of words? Y/N: y
> Do you want to add some random numbers at the end of words? Y/N: y
> Leet mode? (i.e. leet = 1337) Y/N: y
```

**Respuesta**: CUPP generará un archivo como `carlos.txt`

---

### Paso 2b: Generación avanzada con Pydictor 🚀

Supongamos que sabemos que la política de la empresa obliga a passwords de 8 caracteres y al menos 1 dígito.

```bash
cd /opt/pydictor
# Crear diccionario base
echo "Carlos\nGarcia\nTechCorp\nRealMadrid" > /tmp/base.txt

# Generar permutaciones con configuración específica
# -len 8 16: longitud 8 a 16
# --head: Prefijos comunes
python3 pydictor.py -base /tmp/base.txt -len 8 16 -o /exercises/module3/pydictor_words.txt
```

---

### 🎓 Ejercicio Especial: Auditoría UAH

Vamos a simular una auditoría ética para la **Universidad de Alcalá**.

#### Parte 1: Perfilado con CUPP (Mascotas y Fechas)

Hemos creado una ficha de un "objetivo ficticio" basada en datos que podrían encontrarse en redes sociales.

1.  **Revisa la ficha del objetivo**:
    ```bash
    cat /exercises/module3/target_uah.txt
    ```

2.  **Genera un diccionario personalizado**:
    Usa `cupp` en modo interactivo e introduce los datos de **María García López** (ver ficha).

    ```bash
    python3 /opt/cupp/cupp.py -i
    ```
    
    *Consejos para el input:*
    -   **Keywords**: uah,alcala,politecnico,cisne
    -   **Birthday**: 15031995
    -   **Partner**: Carlos
    -   **Pet**: Luna
    -   **Leet mode**: Yes (¡Siempre!)

3.  **Verifica el resultado**:
    ¿Cuántas contraseñas se generaron? ¿Ves combinaciones como `Luna123` o `Alcala2024`?

#### Parte 2: Contexto Web con CeWL 🕷️

Las contraseñas corporativas suelen contener términos relacionados con la institución. Usaremos **CeWL** para extraer palabras clave de la web pública de la UAH.

> [!CAUTION]
> **Ética**: Solo escaneamos la página principal (`-d 1`). No hagas crawling profundo de sitios que no te pertenecen sin autorización explícita.

```bash
# Extraer palabras de la web de la UAH
# -d 1: Profundidad 1 (solo la home)
# -m 5: Mínimo 5 letras (evita "de", "la", "en")
# -w uah_context.txt: Guardar en archivo

cewl -d 1 -m 5 https://www.uah.es -w uah_context.txt

# Ver las palabras más frecuentes
sort uah_context.txt | uniq -c | sort -nr | head -n 20
```

**Reflexión**: ¿Cuántas de estas palabras podrían ser parte de una contraseña débil? (ej: `Estudios2024`, `Investigacion!`, `Futuro_UAH`).

---

### Paso 3: Analizar la wordlist generada 📊

```bash
# Ver tamaño
wc -l carlos.txt

# Primeras 20 líneas
head -20 carlos.txt

# Buscar patrones específicos
grep "Carlos" carlos.txt | head
grep "1990" carlos.txt
grep "Madrid" carlos.txt
```

**Pregunta**: ¿Cuántas variaciones generó CUPP? ¿Encuentras combinaciones lógicas?

---

### Paso 3: Crackear hashes del objetivo 🔓

```bash
# Hashes del objetivo (generados del perfil)
cat target_hashes.txt

# Ataque con wordlist personalizada
hashcat -m 0 -a 0 target_hashes.txt carlos.txt

# Ver resultados
hashcat -m 0 target_hashes.txt --show
```

**Resultado esperado**: Alta tasa de éxito (>70%) debido a la personalización.

---

### Paso 4: Crear wordlist desde web corporativa 🌐

Supongamos que TechCorp tiene un blog público.

```bash
# CeWL desde sitio web (ejemplo)
cewl https://techcrunch.com -d 2 -m 5 -w techcorp-words.txt

# Combinar con CUPP
cat carlos.txt techcorp-words.txt > combined-wordlist.txt

# Eliminar duplicados
sort combined-wordlist.txt | uniq > carlos-final.txt

# Usar en ataque
hashcat -m 0 -a 0 target_hashes.txt carlos-final.txt
```

---

## 🔬 Experimentos Avanzados

### Variación 1: Leet Speak Manual

```bash
# Generar variaciones leet a partir de una palabra
echo "Carlos" | sed 's/a/4/g; s/e/3/g; s/i/1/g; s/o/0/g'
# Resultado: C4rl0s
```

**Crear script** para aplicar leet a todo el wordlist:

```bash
#!/bin/bash
while read word; do
    echo "$word"
    echo "$word" | sed 's/a/4/g; s/e/3/g; s/i/1/g; s/o/0/g'
done < carlos.txt > carlos-leet.txt
```

### Variación 2: Reglas de años

```bash
# Añadir años comunes al final
for year in {2010..2024}; do
    while read word; do
        echo "${word}${year}"
    done < carlos.txt
done > carlos-years.txt
```

---

## 🌍 Caso Real: Filtraciones Targeted

### Ejemplo: CEO de Sony Pictures (2014)

Atacantes usaron información pública para:
1. Identificar nombres de familiares
2. Fechas importantes (cumpleaños)
3. Aficiones conocidas

**Resultado**: Acceso a cuentas personales y corporativas.

---

## 🤔 OSINT Ético vs Malicioso

### ✅ Uso Ético (Legal)

- **Pentesting autorizado**: Cliente da permiso explícito
- **Auditorías de seguridad**: Evaluar exposición de empleados
- **Educación**: Concienciar sobre riesgos

### ❌ Uso Malicioso (Ilegal)

- Stalking o acoso
- Acceso no autorizado
- Robo de identidad
- Ingeniería social con fines criminales

> [!CAUTION]
> Recopilar información pública es legal. **Usarla para acceder a sistemas sin autorización es un delito.**

---

## 📊 Comparativa de Efectividad

| Wordlist | Tamaño | Hashes Crackeados | Tiempo |
|----------|--------|-------------------|--------|
| rockyou-subset | 100,000 | 5/15 (33%) | 30s |
| rockyou completo | 14M | 8/15 (53%) | 2min |
| **CUPP personalizado** | **5,000** | **12/15 (80%)** | **10s** |

**Conclusión**: Personalización >> Volumen

---

## 🛡️ Defensas

### Para Usuarios

1. **No usar información personal** en contraseñas
2. **Gestores de contraseñas**: Generan contraseñas aleatorias
3. **Limitar exposición en redes sociales**

### Para Organizaciones

1. **Políticas de contraseñas**: Prohibir nombres, fechas de nacimiento
2. **Entrenamiento**: Concienciar sobre OSINT
3. **Validación**: Rechazar contraseñas en diccionarios personalizados

---

## 📚 Recursos Adicionales

- [CUPP en GitHub](https://github.com/Mebus/cupp)
- [OSINT Framework](https://osintframework.com/)
- [Guía de OSINT para Red Team](https://www.redteamguide.com/)

---

## ✅ Criterios de Completitud

Has completado este módulo cuando:

- [ ] Generaste una wordlist con CUPP
- [ ] Crackeaste ≥10/15 hashes del objetivo
- [ ] Comprendes cómo OSINT potencia ataques
- [ ] Experimentaste con CeWL o variaciones manuales
- [ ] Reflexionaste sobre el uso ético de estas técnicas

---

🔙 [Anterior: Módulo 2 - Diccionarios](../module2/README.md) | 🔜 [Siguiente: Módulo 4 - Reglas de Transformación](../module4/README.md)
