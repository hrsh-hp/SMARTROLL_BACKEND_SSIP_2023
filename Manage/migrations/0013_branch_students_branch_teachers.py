# Generated by Django 4.2.7 on 2024-02-08 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StakeHolders', '0001_initial'),
        ('Manage', '0012_subject_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='students',
            field=models.ManyToManyField(to='StakeHolders.student'),
        ),
        migrations.AddField(
            model_name='branch',
            name='teachers',
            field=models.ManyToManyField(to='StakeHolders.teacher'),
        ),
    ]