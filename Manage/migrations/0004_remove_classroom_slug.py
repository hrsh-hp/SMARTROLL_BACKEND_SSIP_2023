# Generated by Django 4.2.7 on 2024-02-07 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0003_batch_division_timetable_semester_schedule_lecture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='slug',
        ),
    ]
