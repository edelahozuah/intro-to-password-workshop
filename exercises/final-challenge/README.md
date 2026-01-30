# 🏆 Final Challenge: Real World Hash Crack

> ⏱️ **Tiempo estimado**: 60+ minutos

```bash
# Antes de comenzar, sitúate en el directorio del desafío:
cd /exercises/final-challenge
```

¡Bienvenido al desafío final!

Has recibido una filtración de datos real (`raw-md5.hashes.txt`) que contiene aproximadamente **3.5 millones de hashes MD5**.

Tu objetivo es **auditar** esta base de datos y recuperar la mayor cantidad posible de contraseñas en texto claro para evaluar la seguridad de los usuarios.

## 📂 Archivos
*   `raw-md5.hashes.txt.gz`: Lista de hashes comprimida (3.5M). 
    > **Nota**: Descomprimir antes de usar: `gzip -d raw-md5.hashes.txt.gz`

## 🚀 Primeros Pasos
Para no frustrarte al inicio, te recomendamos este flujo:

1.  **Verificación**: Comprueba el formato de los hashes.
    ```bash
    head raw-md5.hashes.txt
    ```
2.  **Prueba Rápida**: Lanza un ataque básico con RockYou para confirmar que todo funciona.
    ```bash
    hashcat -m 0 -a 0 raw-md5.hashes.txt /wordlists/seclists/rockyou.txt --show
    ```
    *Si ves contraseñas, ¡tu entorno funciona! Ahora ve a por todas.*

## 🎯 Objetivos
1.  **Descomprimir** el fichero.
2.  **Identificar** el tipo de hash (confirmado: MD5).
2.  **Crackear** usando **Diccionarios Básicos**.
3.  **Crackear** usando **Reglas Avanzadas**.
4.  **Analizar** tus resultados: ¿Qué porcentaje lograste romper?

## 🛠️ Instrucciones (Docker)

Accede al contenedor de ataque:
```bash
docker-compose exec attacker /bin/bash
```

Navega al directorio del desafío:
```bash
cd /exercises/final-challenge
```

### Paso 1: Ataque de Diccionario (RockYou)
Intenta romper los hashes fáciles usando el diccionario `rockyou.txt`.

```bash
# Hashcat (Modo 0 = MD5)
hashcat -m 0 -a 0 raw-md5.hashes.txt /wordlists/seclists/rockyou.txt -o cracked_rockyou.txt
```

### Paso 2: Ataque con Reglas (OneRuleToRuleThemAll)
Muchos usuarios usan variaciones (e.g., "Password123!"). Las reglas ayudan a generar estas variantes.

```bash
# Esto tardará más tiempo pero recuperará muchas más contraseñas
hashcat -m 0 -a 0 raw-md5.hashes.txt /wordlists/seclists/rockyou.txt -r /opt/rules/OneRuleToRuleThemAll.rule -o cracked_rules.txt
```

### Paso 3: Ver Resultados
Cuenta cuántas has recuperado:

```bash
wc -l cracked_*.txt
```

¿Puedes llegar al 50%? ¿Al 70%?

## 💡 Tips
*   Usa `--show` en hashcat para ver las contraseñas ya crackeadas.
*   Si hashcat se queja de la temperatura o driver en tu local (al no tener GPU dedicada en Docker), usa `--force` o `-O` (Optimized kernels) si es necesario, aunque en CPU será más lento.

¡Suerte, auditor! 🕵️‍♂️
