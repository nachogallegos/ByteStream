import os
import requests
from google.cloud import storage

def extract_data(request):
    # URL de la API pública
    url = 'https://api.publicapis.org/entries'  # API pública de ejemplo
    response = requests.get(url)
    data = response.json()

    # Crear cliente de Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket('byteStream-data')  # Cambia con tu bucket
    blob = bucket.blob('data.json')  # Nombre del archivo que guardará los datos

    # Subir los datos a Cloud Storage
    blob.upload_from_string(str(data), content_type='application/json')

    return 'Data extracted and saved to Cloud Storage'
