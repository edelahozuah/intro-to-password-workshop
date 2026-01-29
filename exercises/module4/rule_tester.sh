#!/bin/bash

# rule_tester.sh
# Uso: ./rule_tester.sh <palabra> <regla>
# Ejemplo: ./rule_tester.sh password "c $2 $0 $2 $4"

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <palabra> <regla>"
    echo "Ejemplo: $0 password 'c \$2 \$0 \$2 \$4'"
    exit 1
fi

WORD=$1
RULE=$2

echo "----------------------------------------"
echo -e "📥 Entrada:  \033[1;36m$WORD\033[0m"
echo -e "⚙️  Regla:    \033[1;33m$RULE\033[0m"
echo "----------------------------------------"
echo -n "📤 Salida:   "

# Hashcat --stdout aplica reglas sin crackear
echo "$WORD" | hashcat --stdout -r <(echo "$RULE") 2>/dev/null | sed 's/^/\x1b[1;32m/'; echo -e "\x1b[0m"

echo "----------------------------------------"
