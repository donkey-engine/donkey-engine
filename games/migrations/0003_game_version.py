# Generated by Django 3.1.6 on 2021-02-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_mods'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='version',
            field=models.CharField(max_length=64),
            preserve_default=False,
        ),
    ]
