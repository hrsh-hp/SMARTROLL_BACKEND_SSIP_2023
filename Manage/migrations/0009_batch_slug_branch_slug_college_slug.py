# Generated by Django 4.2.7 on 2023-11-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0008_semester_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='college',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]