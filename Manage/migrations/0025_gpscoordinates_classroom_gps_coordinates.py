# Generated by Django 4.2.7 on 2024-02-25 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0024_remove_classroom_router_delete_router'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPSCoordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long', models.CharField(blank=True, max_length=255, null=True)),
                ('latt', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='gps_coordinates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Manage.gpscoordinates'),
        ),
    ]