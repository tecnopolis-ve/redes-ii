# Generated by Django 3.0.7 on 2023-07-15 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0009_remove_producto_tipo_puja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='orden',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='precio',
        ),
    ]
