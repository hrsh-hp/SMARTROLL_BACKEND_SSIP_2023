# Generated by Django 4.2.7 on 2023-11-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0008_alter_lecture_end_time_alter_lecture_start_time'),
        ('Manage', '0009_remove_semester_time_table_semester_time_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='time_table',
        ),
        migrations.AddField(
            model_name='semester',
            name='time_table',
            field=models.ManyToManyField(blank=True, to='TimeTable.timetable'),
        ),
    ]
