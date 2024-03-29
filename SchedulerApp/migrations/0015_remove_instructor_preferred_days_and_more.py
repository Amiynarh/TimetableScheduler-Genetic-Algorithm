# Generated by Django 5.0.1 on 2024-02-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0014_day_timeslot_remove_instructor_available_time_slots_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='preferred_days',
        ),
        migrations.RemoveField(
            model_name='instructor',
            name='preferred_time_slots',
        ),
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.AddField(
            model_name='instructor',
            name='preferred_days',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=50),
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
        migrations.AddField(
            model_name='instructor',
            name='preferred_time_slots',
            field=models.CharField(blank=True, choices=[('8:00 - 10:00', '8:00 - 10:00'), ('10:00 - 12:00', '10:00 - 12:00'), ('12:00 - 2:00', '12:00 - 2:00'), ('2:00 - 4:00', '2:00 - 4:00'), ('4:00 - 6:00', '4:00 - 6:00')], max_length=50),
        ),
    ]
