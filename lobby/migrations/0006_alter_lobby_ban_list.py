# Generated by Django 3.2.5 on 2021-07-23 14:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lobby', '0005_lobby_ban_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='ban_list',
            field=models.ManyToManyField(blank=True, related_name='ban', to=settings.AUTH_USER_MODEL),
        ),
    ]