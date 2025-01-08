from django.contrib import admin

from ALC400_apoyos_economicos.models.models import PagoApoyo, ALC004TiposBecas, ALC401LecBecas

# Registro de las tablas en el admin
admin.site.register(PagoApoyo)
admin.site.register(ALC004TiposBecas)
admin.site.register(ALC401LecBecas)
