# Generated by Django 5.1.2 on 2024-11-28 04:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALC100_captacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesusuario',
            name='razones_interes',
            field=models.CharField(choices=[('Recibir apoyo económico para continuar estudios', 'Recibir apoyo económico'), ('Tener experiencia como líder en educación comunitaria y compartir conocimientos', 'Experiencia como líder'), ('No perder el año y realizar alguna actividad', 'No perder el año'), ('Conocer personas y trabajar con niños', 'Conocer personas'), ('Apoyar y participar en programas sociales', 'Apoyar en programas sociales')], max_length=100),
        ),
        migrations.CreateModel(
            name='Inscripciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('convocatoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='ALC100_captacion.convocatoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='ALC100_captacion.detallesusuario')),
            ],
        ),
    ]