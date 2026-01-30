#!/bin/bash

# Iniciar rsyslog para generar logs en /var/log/auth.log
service rsyslog start

# Iniciar SSH
service ssh start

# Iniciar Fail2Ban
service fail2ban start

echo "========================================"
echo "SSH Server con Fail2Ban iniciado"
echo "========================================"
echo "Usuarios disponibles:"
echo "  - testuser:password123"
echo "  - admin:admin2024"
echo "  - root:toor"
echo ""
echo "Fail2Ban status:"
fail2ban-client status
echo "========================================"

# Mantener contenedor activo
tail -f /var/log/auth.log /var/log/fail2ban.log
