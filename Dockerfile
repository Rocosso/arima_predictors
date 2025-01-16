# Imagen base
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo el contenido de la carpeta `app` al directorio de trabajo
COPY ./app .

# Copiar el archivo `requirements.txt` al directorio de trabajo
COPY requirements.txt .

# Copiar variables de entorno (deberian ser secretos de nube por lo general)
COPY .env .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para la API
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
