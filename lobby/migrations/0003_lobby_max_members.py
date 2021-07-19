# Generated by Django 3.2.5 on 2021-07-17 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_auto_20210717_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='max_members',
            field=models.PositiveIntegerField(default=5, verbose_name='max_members'),
            preserve_default=False,
        ),
    ]