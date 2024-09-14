# Generated by Django 4.2.7 on 2024-09-12 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0029_subject_included_batches_term_type'),
        ('StakeHolders', '0008_alter_teacher_web_push_subscription'),
        ('AdditionalFeatures', '0002_rename_created_by_survey_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('link', models.URLField()),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='StakeHolders.teacher')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Manage.subject')),
            ],
        ),
    ]