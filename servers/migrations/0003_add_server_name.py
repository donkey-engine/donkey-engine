# Generated by Django 3.1.8 on 2021-05-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_update_servers'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='name',
            field=models.CharField(default='New server', max_length=64),
        ),
    ]
