# Generated by Django 3.0.6 on 2020-06-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0004_auto_20200605_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuseraccount',
            name='biography',
            field=models.TextField(null=True, verbose_name='bio'),
        ),
        migrations.AddField(
            model_name='myuseraccount',
            name='profession',
            field=models.CharField(max_length=255, null=True, verbose_name='profession'),
        ),
    ]