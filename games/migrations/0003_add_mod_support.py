# Generated by Django 3.1.8 on 2021-05-27 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_add_build_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='mod',
            field=models.FileField(default='', max_length=512, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mod',
            name='versions',
            field=models.ManyToManyField(to='games.GameVersion'),
        ),
        migrations.AlterUniqueTogether(
            name='mod',
            unique_together=set(),
        ),
        migrations.DeleteModel(
            name='ModVersion',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='game',
        ),
    ]
