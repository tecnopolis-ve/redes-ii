# Generated by Django 3.0.7 on 2023-07-14 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subastas_redes', '0003_remove_user_nacionalidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='vive',
        ),
    ]
