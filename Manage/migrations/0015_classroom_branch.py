# Generated by Django 4.2.7 on 2024-02-08 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0014_alter_branch_admins_alter_branch_students_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.branch'),
        ),
    ]
