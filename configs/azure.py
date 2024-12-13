from azure.storage.blob import BlobServiceClient
from decouple import config

def azure_storage():
    connection_string = config('AZURE_STR_CONNECTION')
    service = BlobServiceClient.from_connection_string(connection_string)
    return service

def crear_contenedores():
    # Tomamos la instancia de Azure
    azure = azure_storage()
    # Contenedor para estados de certificados
    azure.create_container('certificados')
    # Contenedor para estados de identificaciones
    azure.create_container('identificaciones')
    # Contenedor para estados de cuentas
    azure.create_container('cuentas')
    
    containers = azure.list_containers()    

    azure.close()

    return containers