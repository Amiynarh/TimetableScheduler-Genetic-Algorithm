# Generated by Django 5.0.1 on 2024-02-18 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0008_alter_meetingtime_pid_alter_section_section_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='level',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_id',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False),
        ),
    ]
