# Generated by Django 3.2.5 on 2021-07-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_lobby_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='history',
            field=models.JSONField(default=[]),
        ),
    ]