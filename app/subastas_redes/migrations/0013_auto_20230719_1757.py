# Generated by Django 3.0.7 on 2023-07-19 17:57

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0012_auto_20230715_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='duracion_minima',
            new_name='duracion',
        ),
        migrations.AddField(
            model_name='producto',
            name='fecha_inicio',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
    ]
