# ByteStream - Integración de API con Google Cloud Functions y Spotify

## Descripción

**ByteStream** es un proyecto que extrae datos de Spotify (información de artistas) usando la API de Spotify, y guarda esos datos en **Google Cloud Storage** utilizando **Google Cloud Functions**.

## Características

- **Autenticación**: Obtención de un **Access Token** de Spotify usando las credenciales de la API.
- **Extracción de Datos**: Obtención de información de artistas de Spotify.
- **Almacenamiento en Google Cloud**: Los datos extraídos se guardan en un bucket de **Google Cloud Storage**.
- **Despliegue en Google Cloud Functions**: La función se despliega en **Google Cloud Functions** para su ejecución sin servidor.

## Cómo ejecutar el proyecto

### Requisitos:

- Python 3.10 o superior
- Google Cloud SDK instalado
- Spotify API credentials
- Google Cloud Storage credentials

### Pasos para ejecutar localmente:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/ByteStream.git

2. Crea un entorno virtual e instala las dependencias:
    ```python -m venv venv
    source venv/bin/activate  # En W

3. Obtén las credenciales de Spotify y Google Cloud, y configura los archivos .env y las variables de entorno correspondientes.

4. Ejecuta el script de prueba:
    ```python test_script.py

 ### Despliegue en Google Cloud Functions:

- Asegúrate de haber configurado tu cuenta de Google Cloud con el SDK.
- Despliega la función en Google Cloud Functions:
    ```gcloud functions deploy extract_data --runtime python310 --trigger-http --allow-unauthentica