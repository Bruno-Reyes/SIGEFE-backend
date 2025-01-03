from ALC400_apoyos_economicos.models.models import PagoApoyo
from ALC000_sistema_base.models.models import Usuario, TipoUsuario
import random
from datetime import datetime, timedelta

# Datos de ejemplo
CONCEPTOS = ["Beca", "Seguimiento", "Continuacion"]
ESTADOS = ["pendiente", "completado", "rechazado"]

def crear_pagos():
    # Obtener usuarios LEC disponibles
    usuarios = Usuario.objects.filter(tipo_usuario= TipoUsuario.LIDER_LEC)  # Cambiar a "LEC" 
    if not usuarios.exists():
        print("No hay usuarios disponibles para asignar pagos. Por favor, crea usuarios primero.")
        return

    print("Poblando la base de datos con pagos de ejemplo...")

    # 10 pagos de ejemplo
    for _ in range(10):
        usuario = random.choice(usuarios)
        concepto = random.choice(CONCEPTOS)
        monto = round(random.uniform(1000, 10000), 2)  # Monto entre 1,000 y 10,000
        estatus = random.choice(ESTADOS)
        fecha_pago = datetime.now() - timedelta(days=random.randint(1, 365))  # Fecha aleatoria en el último año

        # Crear el registro de pago
        pago = PagoApoyo.objects.create(
            usuario=usuario,
            concepto=concepto,
            monto=monto,
            estatus=estatus,
            fecha_pago=fecha_pago,
            registrado_por="departamento.finanzas@conafe.com"
        )

        print(f"Pago creado: Usuario={usuario.email}, Concepto={concepto}, Monto={monto}, Estatus={estatus}")

    



