# Generated by Django 4.2.7 on 2023-11-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeTable', '0002_alter_classroom_routers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
