# Generated by Django 3.0.7 on 2023-07-14 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0002_auto_20230714_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nacionalidad',
        ),
    ]