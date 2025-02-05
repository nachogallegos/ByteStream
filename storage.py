from google.cloud import storage
import json

# Función para guardar los datos en Google Cloud Storage
def save_to_cloud_storage(data, bucket_name, file_name, storage_client):
    try:
        # Obtén el bucket de Google Cloud Storage
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Bucket encontrado: {bucket.name}")
        
        # Crea un blob (objeto) que representa el archivo en el bucket
        blob = bucket.blob(file_name)
        
        # Subir los datos a Cloud Storage como un archivo JSON
        blob.upload_from_string(json.dumps(data), content_type='application/json')
        print(f'Data saved to Cloud Storage: {file_name}')
        
    except Exception as e:
        print(f"Error al guardar los datos en Cloud Storage: {e}")
