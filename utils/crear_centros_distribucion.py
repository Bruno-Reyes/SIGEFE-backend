from ALC600_logistica.models.models import CentrosDistribucion
# Crear centros de distribución
centros_distribucion = [    
    { "nombre" : "AGUASCALIENTES", "latitud" : 21.885998, "longitud" : -102.305116 },    
    { "nombre" : "BAJA CALIFORNIA SUR", "latitud" : 24.135095, "longitud" : -110.344218 },
    { "nombre" : "BAJA CALIFORNIA", "latitud" : 32.639125, "longitud" : -115.472697 },
    { "nombre" : "CAMPECHE", "latitud" : 19.847939, "longitud" : -90.536065 },
    { "nombre" : "CIUDAD DE MÉXICO", "latitud" : 19.362180, "longitud" : -99.169843 },
    { "nombre" : "CHIAPAS", "latitud" : 16.770584, "longitud" : -93.091974 },
    { "nombre" : "CHIHUAHUA", "latitud" : 28.621595, "longitud" : -106.062359 },
    { "nombre" : "COAHUILA DE ZARAGOZA", "latitud" : 25.425353, "longitud" : -100.981724 },
    { "nombre" : "COLIMA", "latitud" : 19.308520, "longitud" : -103.756277 },
    { "nombre" : "DURANGO", "latitud" : 24.028272, "longitud" : -104.650212 },
    { "nombre" : "GUANAJUATO", "latitud" : 21.514606, "longitud" : -101.195652 },
    { "nombre" : "GUERRERO", "latitud" : 17.534771, "longitud" : -99.498997 },
    { "nombre" : "HIDALGO", "latitud" : 20.108700, "longitud" : -98.712257 },
    { "nombre" : "JALISCO", "latitud" : 20.705807, "longitud" : -103.354497 },
    { "nombre" : "MÉXICO", "latitud" : 19.296139, "longitud" : -99.672021 },
    { "nombre" : "MICHOACÁN DE OCAMPO", "latitud" : 19.718639, "longitud" : -101.152552 },
    { "nombre" : "MORELOS", "latitud" : 18.948777, "longitud" : -99.227542 },
    { "nombre" : "NAYARIT", "latitud" : 21.490430, "longitud" : -104.884869 },
    { "nombre" : "NUEVO LEÓN", "latitud" : 25.658578, "longitud" : -100.226490 },
    { "nombre" : "OAXACA", "latitud" : 17.056314, "longitud" : -96.673083 },
    { "nombre" : "PUEBLA", "latitud" : 19.078711, "longitud" : -98.207788 },     
    { "nombre" : "QUERÉTARO", "latitud" : 20.552924, "longitud" : -100.429206 },
    { "nombre" : "QUINTANA ROO", "latitud" : 18.515467, "longitud" : -88.328101 },
    { "nombre" : "SAN LUIS POTOSÍ", "latitud" : 22.121657, "longitud" : -100.982680 },
    { "nombre" : "SINALOA", "latitud" : 24.798435 , "longitud" : -107.404940 },
    { "nombre" : "SONORA", "latitud" : 29.072531, "longitud" : -110.960010 },
    { "nombre" : "TABASCO", "latitud" : 17.994324, "longitud" : -92.918545 },
    { "nombre" : "TAMAULIPAS", "latitud" : 23.726500, "longitud" : -99.137828 },
    { "nombre" : "TLAXCALA", "latitud" : 19.320527, "longitud" : -98.208277 },
    { "nombre" : "VERACRUZ DE IGNACIO DE LA LLAVE", "latitud" : 19.507613, "longitud" : -96.886972 }, 
    { "nombre" : "YUCATÁN", "latitud" : 20.963580, "longitud" : -89.597230 },
    { "nombre" : "ZACATECAS", "latitud" : 22.731131, "longitud" : -102.522601 }
    ]

for centro in centros_distribucion:
    CentrosDistribucion.objects.create(
        estado = centro["nombre"],
        latitud = centro["latitud"],
        longitud = centro["longitud"]
    )