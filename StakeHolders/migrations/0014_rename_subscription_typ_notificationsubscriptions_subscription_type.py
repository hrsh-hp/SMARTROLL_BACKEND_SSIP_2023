# Generated by Django 4.2.7 on 2024-10-28 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StakeHolders', '0013_remove_notificationsubscriptions_subscription_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationsubscriptions',
            old_name='subscription_typ',
            new_name='subscription_type',
        ),
    ]