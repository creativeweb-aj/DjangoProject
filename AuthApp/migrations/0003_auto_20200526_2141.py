# Generated by Django 3.0.6 on 2020-05-26 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0002_myuseraccount_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuseraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
