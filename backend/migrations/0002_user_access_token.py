# Generated by Django 3.2.5 on 2021-07-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(default='', max_length=250, verbose_name='oauth_token'),
            preserve_default=False,
        ),
    ]
