# Generated by Django 3.2.5 on 2021-07-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_lobby_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='history',
            field=models.JSONField(blank=True, default=list),
        ),
    ]