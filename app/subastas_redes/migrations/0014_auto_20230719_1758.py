# Generated by Django 3.0.7 on 2023-07-19 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0013_auto_20230719_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='fecha_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]