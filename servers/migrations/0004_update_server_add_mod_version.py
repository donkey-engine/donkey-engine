# Generated by Django 3.1.8 on 2021-06-09 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_mod_versions'),
        ('servers', '0003_add_server_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='mods',
        ),
        migrations.AddField(
            model_name='server',
            name='mods',
            field=models.ManyToManyField(blank=True, to='games.ModVersion'),
        ),
    ]
