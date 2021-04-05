# Generated by Django 3.1.6 on 2021-04-05 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=64)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versions',
                'ordering': ['version'],
            },
        ),
        migrations.CreateModel(
            name='Mods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='games.game')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.version')),
            ],
            options={
                'verbose_name': 'Mod',
                'verbose_name_plural': 'Mods',
                'ordering': ['name'],
            },
        ),
    ]
