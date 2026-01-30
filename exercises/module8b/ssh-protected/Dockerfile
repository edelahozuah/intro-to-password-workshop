FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    fail2ban \
    rsyslog \
    iptables \
    vim \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Configurar SSH
RUN mkdir -p /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN useradd -m -s /bin/bash testuser && echo 'testuser:password123' | chpasswd
RUN useradd -m -s /bin/bash admin && echo 'admin:admin2024' | chpasswd

# Permitir login con password
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Configurar Fail2Ban
COPY jail.local /etc/fail2ban/jail.local

# Crear directorio para logs
RUN mkdir -p /var/log && touch /var/log/auth.log

# Script de inicio
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

CMD ["/entrypoint.sh"]
