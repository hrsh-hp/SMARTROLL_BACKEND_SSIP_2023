# Generated by Django 4.2.7 on 2023-11-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0007_lecture_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
