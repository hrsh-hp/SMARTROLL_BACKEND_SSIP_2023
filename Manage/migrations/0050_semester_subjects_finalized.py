# Generated by Django 4.2.7 on 2024-11-07 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0049_alter_permanentsubject_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='subjects_finalized',
            field=models.BooleanField(default=False),
        ),
    ]
