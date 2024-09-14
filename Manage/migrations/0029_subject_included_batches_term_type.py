# Generated by Django 4.2.7 on 2024-09-12 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0028_alter_subject_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='included_batches',
            field=models.ManyToManyField(blank=True, to='Manage.batch'),
        ),
        migrations.AddField(
            model_name='term',
            name='type',
            field=models.CharField(blank=True, choices=[('even', 'Even'), ('odd', 'Odd')], max_length=4, null=True),
        ),
    ]