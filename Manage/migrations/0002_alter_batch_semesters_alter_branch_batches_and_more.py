# Generated by Django 4.2.7 on 2023-11-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='semesters',
            field=models.ManyToManyField(to='Manage.semester'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='batches',
            field=models.ManyToManyField(to='Manage.batch'),
        ),
        migrations.AlterField(
            model_name='college',
            name='branches',
            field=models.ManyToManyField(to='Manage.branch'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='semester',
            name='subjects',
            field=models.ManyToManyField(to='Manage.subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='credit',
            field=models.IntegerField(),
        ),
    ]