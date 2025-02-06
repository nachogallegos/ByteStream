from spotify import get_access_token, get_artist_data
from storage import save_to_cloud_storage
from google.oauth2 import service_account
from google.cloud import storage, bigquery
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

        # Lista de IDs de artistas
        artist_ids = ['5XQWXnMwsvuvCPMneXUbsy', '1Yj5Xey7kTwvZla8sqdsdE']  # Marcianeke y Cris Mj
        artist_data_all = []

        for artist_id in artist_ids:
            artist_data = get_artist_data(access_token, artist_id)
            if artist_data:
                artist_data_all.append(artist_data)

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
        save_to_cloud_storage(artist_data_all, 'bytestream-data', 'spotify_artists_data.json', storage_client)

        print("Datos guardados en Google Cloud Storage correctamente.")

        # Crear el cliente de BigQuery con las credenciales
        bq_client = bigquery.Client(credentials=credentials, project="bytestream-450003")
        
        # Definir el dataset y la tabla en BigQuery
        dataset_id = 'bytestream-450003.spotify_data'
        table_id = 'bytestream-450003.spotify_data.spotify_artists_data'  # ID completo de la tabla

        # Convertir los datos de los artistas a un formato adecuado para BigQuery
        rows_to_insert = [
            {
                "artist_id": artist["id"],
                "artist_name": artist["name"],
                "followers": artist["followers"],
                "genres": artist["genres"],
                "images": artist["images"] if isinstance(artist["images"], list) else [],  # Asegúrate de que sea un array de strings,
                "popularity": artist["popularity"]
            }
            for artist in artist_data_all
        ]

        # Inserción de datos en BigQuery
        errors = bq_client.insert_rows_json(table_id, rows_to_insert)

        if errors:
            print(f"Error al insertar los datos en BigQuery: {errors}")
        else:
            print(f"Datos insertados correctamente en BigQuery.")
        
        return 'Data extracted, saved to Cloud Storage and BigQuery'

    except Exception as e:
        print(f"Error en la ejecución de la función: {e}")
        return f"Internal Server Error: {str(e)}", 500
