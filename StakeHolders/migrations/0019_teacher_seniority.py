# Generated by Django 4.2.7 on 2024-11-19 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StakeHolders', '0018_teacher_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='seniority',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
