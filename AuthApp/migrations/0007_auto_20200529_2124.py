# Generated by Django 3.0.6 on 2020-05-29 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0006_remove_myuseraccount_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailhandler',
            name='is_expiry',
            field=models.BigIntegerField(null=True, verbose_name='Is expiry'),
        ),
        migrations.AlterField(
            model_name='emailhandler',
            name='retry_count',
            field=models.IntegerField(null=True, verbose_name='Retry counter'),
        ),
    ]
