# Generated by Django 4.2.7 on 2024-02-29 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0027_alter_branch_branch_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]