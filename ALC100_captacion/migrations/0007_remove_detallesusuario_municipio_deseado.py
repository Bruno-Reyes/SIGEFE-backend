# Generated by Django 5.1.2 on 2024-12-12 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ALC100_captacion', '0006_remove_detallesusuario_estado_deseado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallesusuario',
            name='municipio_deseado',
        ),
    ]
