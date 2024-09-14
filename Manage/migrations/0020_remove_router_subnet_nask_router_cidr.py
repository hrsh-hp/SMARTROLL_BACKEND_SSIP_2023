# Generated by Django 4.2.7 on 2024-02-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0019_rename_routers_classroom_router_router_subnet_nask_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='router',
            name='subnet_nask',
        ),
        migrations.AddField(
            model_name='router',
            name='CIDR',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]