# Generated by Django 3.1.6 on 2021-02-15 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20210215_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='mods',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='games.game'),
            preserve_default=False,
        ),
    ]
