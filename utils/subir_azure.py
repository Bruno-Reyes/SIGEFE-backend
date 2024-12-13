from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Prueba subir un archivo
file_name = default_storage.save('data/prueba.pdf', ContentFile(b'Contenido de prueba'))
print(file_name)

# Obtener la URL del archivo
file_url = default_storage.url(file_name)
print(file_url)
