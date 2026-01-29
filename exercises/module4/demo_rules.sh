#!/bin/bash

# demo_rules.sh
# Muestra transformaciones comunes automáticamente

function show_demo() {
    WORD=$1
    RULE=$2
    DESC=$3
    
    echo -e "\n📝 \033[1mDescripción: $DESC\033[0m"
    ./rule_tester.sh "$WORD" "$RULE"
    sleep 2
}

echo "======================================"
echo "   DEMO DE REGLAS DE HASHCAT 🦁"
echo "======================================"

chmod +x rule_tester.sh

show_demo "password" "c" "Capitalizar primera letra"
show_demo "password" "u" "Convertir todo a MAYÚSCULAS"
show_demo "admin" "r" "Revertir (escritura inversa)"
show_demo "password" "$1 $2 $3" "Añadir sufijo '123'"
show_demo "password" "^!" "Añadir prefijo '!'"
show_demo "dragon" "sao" "Sustituir 'a' por 'o' (dragon -> drogon)"
show_demo "password" "sa4 se3 si1 so0" "Leet Speak básico (a4 e3 i1 o0)"
show_demo "madrid" "c \$2 \$0 \$2 \$4" "Capitalizar + Añadir Año (2024)"

echo -e "\n✅ Fin de la demo. ¡Ahora prueba tú con ./rule_tester.sh!"
