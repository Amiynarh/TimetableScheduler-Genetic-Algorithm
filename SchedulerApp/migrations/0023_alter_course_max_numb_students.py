# Generated by Django 5.0.1 on 2024-02-24 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulerApp', '0022_rename_lecture_id_lecture_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='max_numb_students',
            field=models.IntegerField(default=0),
        ),
    ]
