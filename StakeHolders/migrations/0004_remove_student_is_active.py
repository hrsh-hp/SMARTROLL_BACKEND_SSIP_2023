# Generated by Django 4.2.7 on 2024-01-24 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StakeHolders', '0003_student_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_active',
        ),
    ]