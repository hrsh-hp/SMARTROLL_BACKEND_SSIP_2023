# Generated by Django 4.2.7 on 2023-11-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0002_alter_batch_semesters_alter_branch_batches_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='branches',
            field=models.ManyToManyField(blank=True, to='Manage.branch'),
        ),
    ]