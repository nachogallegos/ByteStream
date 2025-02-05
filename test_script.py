from spotify import get_access_token, get_artist_data
from storage import save_to_cloud_storage
from google.oauth2 import service_account
from google.cloud import storage

# Obtener el Access Token de Spotify
token = get_access_token()

if token:
    print(f"Access Token obtenido: {token}")

    # Obtener información del artista (por ejemplo, Marcianeke)
    artist_id = '5XQWXnMwsvuvCPMneXUbsy'  # ID de Marcianeke
    artist_data = get_artist_data(token, artist_id)

    if artist_data:
        print(f"Datos del artista obtenidos: {artist_data['name']}")

        # Guardar los datos en Google Cloud Storage
        try:
            # Usa las credenciales explícitamente para evitar errores con las credenciales predeterminadas
            credentials = service_account.Credentials.from_service_account_file(
                "C:/Users/nazho/OneDrive/Escritorio/python/ByteStream/credentials.json"  # Ruta a tus credenciales
            )
            
            # Crear el cliente de Google Cloud Storage
            storage_client = storage.Client(credentials=credentials, project="bytestream-450003")

            # Llamar a la función que guarda los datos en Cloud Storage
            save_to_cloud_storage(artist_data, 'bytestream-data', 'spotify_artist_data.json', storage_client)
            
            print("Datos guardados en Google Cloud Storage correctamente.")

        except Exception as e:
            print(f"Error al guardar los datos en Cloud Storage: {e}")
    else:
        print("No se pudo obtener la información del artista.")
else:
    print("No se pudo obtener el Access Token")
