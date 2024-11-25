import pandas as pd
from ALC100_captacion.models.models import DetallesUsuario

def exportar_a_csv():
    # Obtén todos los registros del modelo DetallesUsuario
    detalles_usuarios = DetallesUsuario.objects.all().values()

    # Crea un DataFrame de pandas a partir de los registros
    df = pd.DataFrame(detalles_usuarios)

    # Exporta el DataFrame a un archivo CSV
    df.to_csv('data/detalles_usuarios.csv', index=True)
    print("Datos exportados a detalles_usuarios.csv")

def exportar_a_excel():
    # Obtén todos los registros del modelo DetallesUsuario
    detalles_usuarios = DetallesUsuario.objects.all().values()

    # Crea un DataFrame de pandas a partir de los registros
    df = pd.DataFrame(detalles_usuarios)

    # Exporta el DataFrame a un archivo Excel
    df.to_excel('detalles_usuarios.xlsx', index=False)
    print("Datos exportados a detalles_usuarios.xlsx")

# Llama a las funciones para exportar los datos
exportar_a_csv()
# exportar_a_excel()