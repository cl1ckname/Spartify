# Generated by Django 3.2.5 on 2021-08-06 10:05

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0008_alter_lobby_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='id',
            field=models.UUIDField(default=shortuuid.main.ShortUUID.uuid, primary_key=True, serialize=False),
        ),
    ]