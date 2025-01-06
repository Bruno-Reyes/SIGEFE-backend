from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

from configs.azure import azure_storage
from decouple import config

def generate_sas_url(blob_name, container_name, blob_url):
    # Crear un cliente para la cuenta de almacenamiento
    blob_service_client = azure_storage()
    
    # Generar el SAS para el blob específico
    sas_token = generate_blob_sas(
        account_name=config('AZURE_STORAGE_ACCOUNT_NAME'),
        container_name=container_name,
        blob_name=blob_name,
        account_key=config('AZURE_STORAGE_ACCOUNT_KEY'),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1),  # Expira en 1 hora
    )
    # Crear la URL completa
    sas_url = f"{blob_url}?{sas_token}"    
    return sas_url