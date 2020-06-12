# Generated by Django 3.0.6 on 2020-06-07 10:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PostApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='Likes', to=settings.AUTH_USER_MODEL, verbose_name='Post Likes'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='Tags', to=settings.AUTH_USER_MODEL, verbose_name='Tagged User'),
        ),
    ]