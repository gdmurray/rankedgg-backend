# Generated by Django 2.1.7 on 2019-03-23 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20190323_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='last_queried',
        ),
    ]
