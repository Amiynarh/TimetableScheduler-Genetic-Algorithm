# Generated by Django 5.0.1 on 2024-02-24 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0018_remove_lecture_instructor_alter_lecture_meeting_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MeetingTime',
        ),
        migrations.AlterField(
            model_name='lecture',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
