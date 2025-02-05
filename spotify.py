import os
import base64
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de las variables de entorno
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Función para obtener el Access Token de Spotify
def get_access_token():
    credentials = f'{client_id}:{client_secret}'
    base64_credentials = base64.b64encode(credentials.encode()).decode('utf-8')

    url = 'https://accounts.spotify.com/api/token'

    headers = {
        'Authorization': f'Basic {base64_credentials}'
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

# Función para obtener la información de un artista
def get_artist_data(access_token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    # Imprimir el código de estado y el cuerpo de la respuesta para depuración
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        return None
