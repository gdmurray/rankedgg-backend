# Generated by Django 2.1.7 on 2019-03-23 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_remove_player_last_queried'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermeta',
            name='last_queried',
        ),
        migrations.AddField(
            model_name='player',
            name='last_queried',
            field=models.DateTimeField(null=True),
        ),
    ]
