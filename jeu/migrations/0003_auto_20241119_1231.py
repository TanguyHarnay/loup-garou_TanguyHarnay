# Generated by Django 2.2.28 on 2024-11-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeu', '0002_auto_20241119_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personnage',
            name='game',
        ),
        migrations.AlterField(
            model_name='personnage',
            name='role',
            field=models.CharField(max_length=20, verbose_name='Rôle'),
        ),
        migrations.AlterField(
            model_name='personnage',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
