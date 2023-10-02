# Usar una imagen base de Python 3.8
FROM python:3.8.12

# Establecer un directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación en el contenedor
COPY app_masw_2Dto1D.py .

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app_masw_2Dto1D.py", "--server.port", "8866", "--server.address", "0.0.0.0"]
