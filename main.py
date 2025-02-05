from spotify import get_access_token, get_artist_data
from storage import save_to_cloud_storage
from google.oauth2 import service_account
from google.cloud import storage
import os

# Función principal que se ejecutará en Cloud Functions
def extract_data(request):
    try:
        print("Obteniendo el Access Token de Spotify...")
        # Obtener el Access Token de Spotify
        access_token = get_access_token()
        if not access_token:
            print("No se pudo obtener el Access Token.")
            return "Error obtaining Access Token from Spotify", 500

        print(f"Access Token obtenido: {access_token}")

        # Obtener información del artista (por ejemplo, Marcianeke)
        artist_id = '5XQWXnMwsvuvCPMneXUbsy'  # ID de Marcianeke
        artist_data = get_artist_data(access_token, artist_id)

        if not artist_data:
            print("No se pudo obtener la información del artista.")
            return "Error fetching artist data", 500

        print(f"Datos del artista obtenidos: {artist_data['name']}")

        # Descargar el archivo de credenciales desde Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('bytestream-data')  # Nombre de tu bucket
        blob = bucket.blob('credentials.json')  # Nombre del archivo de credenciales en el bucket
        credentials_path = '/tmp/credentials.json'
        blob.download_to_filename(credentials_path)
        
        # Usar las credenciales descargadas desde Cloud Storage
        credentials = service_account.Credentials.from_service_account_file(credentials_path)

        # Crear el cliente de Google Cloud Storage con las credenciales
        storage_client = storage.Client(credentials=credentials, project="bytestream-450003")

        print("Subiendo los datos a Google Cloud Storage...")
        # Guardar los datos en Google Cloud Storage
        save_to_cloud_storage(artist_data, 'bytestream-data', 'spotify_artist_data.json', storage_client)

        print("Datos guardados en Google Cloud Storage correctamente.")
        return 'Data extracted and saved to Cloud Storage'
    
    except Exception as e:
        print(f"Error en la ejecución de la función: {e}")
        return f"Internal Server Error: {str(e)}", 500
