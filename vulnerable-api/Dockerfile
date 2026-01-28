FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app.py .
COPY users_db.json .

# Exponer puerto
EXPOSE 5000

# Usuario no-root
RUN useradd -m apiuser && chown -R apiuser:apiuser /app
USER apiuser

CMD ["python", "app.py"]
