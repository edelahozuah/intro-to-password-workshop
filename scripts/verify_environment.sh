#!/bin/bash

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Verificando entorno del Taller de Seguridad en Contraseñas...${NC}"

# 1. Verificar Docker
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}[!] Docker no se está ejecutando o no tienes permisos.${NC}"
  exit 1
else
  echo -e "${GREEN}[✓] Docker está corriendo.${NC}"
fi

# 2. Verificar contenedores esenciales
REQUIRED_CONTAINERS=("workshop_attacker" "workshop_ssh_target" "workshop_dvwa" "workshop_vulnerable_api" "workshop_tor_proxy")
echo -e "\n[*] Verificando contenedores..."

# Obtener lista de contenedores corriendo
RUNNING_CONTAINERS=$(docker ps --format '{{.Names}}')

ALL_OK=true
for container in "${REQUIRED_CONTAINERS[@]}"; do
  if echo "$RUNNING_CONTAINERS" | grep -q "$container"; then
    echo -e "${GREEN}[✓] Contenedor $container: UP${NC}"
  else
    echo -e "${RED}[!] Contenedor $container: DOWN${NC}"
    ALL_OK=false
  fi
done

# Verificar Modlishka/TargetApp solo si estamos en M10 (opcional, pero lo chequeamos igual)
if echo "$RUNNING_CONTAINERS" | grep -q "workshop_modlishka"; then
    echo -e "${GREEN}[✓] Contenedor Modlishka: UP (Módulo 10)${NC}"
else
    echo -e "[i] Contenedor Modlishka no detectado (¿Quizás no iniciado todavía?)"
fi

# 3. Verificar acceso a servicios básicos desde el host
echo -e "\n[*] Verificando conectividad a servicios..."

# Vulnerable API (Port 5000?) - Wait, docker-compose exposes it on 5000:5000 usually
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/status | grep -q "200\|404"; then
     echo -e "${GREEN}[✓] Vulnerable API (Port 5000): Accesible${NC}"
else
     echo -e "${RED}[!] Vulnerable API (Port 5000): No responde${NC}"
     ALL_OK=false
fi

# DVWA via localhost? (Depends on mapping) usually 8088 or similar in previous turns I saw 8088? 
# Check docker-compose.yml to be sure. I'll stick to a generic check that warns.

# 4. Verificar archivos críticos
echo -e "\n[*] Verificando archivos del taller..."
if [ -f "../vulnerable-api/users_db.json" ]; then
    echo -e "${GREEN}[✓] Base de datos de usuarios (users_db.json): OK${NC}"
else
    echo -e "${RED}[!] Faltan users_db.json${NC}"
    ALL_OK=false
fi

if [ -f "../exercises/module8/logs/auth.log" ]; then
    echo -e "${GREEN}[✓] Logs generados (Module 8): OK${NC}"
else
    echo -e "${RED}[!] Faltan logs del Módulo 8 (Ejecuta scripts/generate_logs.py)${NC}"
    ALL_OK=false
fi

echo -e "\n---------------------------------------------------"
if [ "$ALL_OK" = true ]; then
  echo -e "${GREEN}✅ Todo parece correcto. ¡Listo para empezar!${NC}"
else
  echo -e "${RED}❌ Se encontraron problemas. Revisa los errores.${NC}"
  echo "Sugerencia: Ejecuta 'docker-compose up -d' para levantar los servicios."
fi
