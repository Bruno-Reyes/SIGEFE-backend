from ALC000_sistema_base.models.models import * # Importar todos los modelos

# Imprimir todos los registros de la tabla 'Usuario'
usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(usuario)
    
