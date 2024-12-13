from configs.azure import azure_storage
import uuid

# Funcion para subir archivos a azure
def subir_archivo_azure(FILE, CONTAINER_NAME:str):
    try:
        # Conectamos el bucket de azure
        azure = azure_storage()
        # Obtenemos una instancia del contenedor
        container_client = azure.get_container_client(CONTAINER_NAME)
        # Generar nombre aleatorio para el archivo
        nombre_archivo = f"{uuid.uuid4()}.pdf"
        # Subir el archivo al blob
        blob_client = container_client.get_blob_client(blob=nombre_archivo)

        # Leer el archivo y subirlo
        blob_client.upload_blob(FILE.file, overwrite=True)

        # Generar la URL del archivo subido
        blob_url = f"https://sigefe.blob.core.windows.net/{CONTAINER_NAME}/{nombre_archivo}"
        return blob_url

    except Exception as e:
        print(f"Error subiendo archivo a Azure: {e}")
        return None