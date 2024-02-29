# Generated by Django 5.0.1 on 2024-02-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0017_alter_course_department_delete_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='instructor',
        ),
        migrations.AlterField(
            model_name='lecture',
            name='meeting_time',
            field=models.CharField(choices=[('8:00 - 10:00', '8:00 - 10:00'), ('10:00 - 12:00', '10:00 - 12:00'), ('12:00 - 2:00', '12:00 - 2:00'), ('2:00 - 4:00', '2:00 - 4:00'), ('4:00 - 6:00', '4:00 - 6:00')], max_length=20),
        ),
    ]
