# Generated by Django 4.2.7 on 2023-11-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0009_batch_slug_branch_slug_college_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='timetable',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]