# Generated by Django 3.0.7 on 2023-07-15 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0007_auto_20230714_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='ganador',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, default=None, max_length=255, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen_thumb',
            field=models.ImageField(blank=True, default=None, max_length=255, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='puja',
            name='ganador',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Divisa',
        ),
        migrations.DeleteModel(
            name='Pais',
        ),
    ]