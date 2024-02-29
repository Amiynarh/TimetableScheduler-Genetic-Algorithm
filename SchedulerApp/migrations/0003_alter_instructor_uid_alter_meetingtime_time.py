# Generated by Django 5.0.1 on 2024-02-18 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0002_section_num_class_in_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='uid',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='meetingtime',
            name='time',
            field=models.CharField(choices=[('8:00 - 10:00', '8:00 - 10:00'), ('10:00 - 12:00', '10:00 - 12:00'), ('12:00 - 2:00', '12:00 - 2:00'), ('2:00 - 4:00', '2:00 - 4:00'), ('4:00 - 6:00', '4:00 - 6:00')], default='11:30 - 12:30', max_length=50),
        ),
    ]
