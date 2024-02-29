from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
import uuid





TIME_SLOTS = (
    ('8:00 - 10:00'  , '8:00 - 10:00'),
    ('10:00 - 12:00', '10:00 - 12:00'),
    ('12:00 - 2:00', '12:00 - 2:00'),
    ('2:00 - 4:00'  , '2:00 - 4:00'),
    ('4:00 - 6:00'  , '4:00 - 6:00'),
)


DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)
    
    
class Instructor(models.Model):
    uid = models.CharField(max_length=3, blank=True)
    name = models.CharField(max_length=25)
    preferred_time_slots = models.JSONField(blank=True, null=True)
    preferred_days = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            # Generate a 6-character UUID
            self.uid = str(uuid.uuid4())[:3]
        super(Instructor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.uid} {self.name}'
    def formatted_time_slots(self):
        if isinstance(self.preferred_time_slots, list):
            return ", ".join(self.preferred_time_slots)
        return self.preferred_time_slots  # Fallback if it's a string

    def formatted_days(self):
        if isinstance(self.preferred_days, list):
            return ", ".join(self.preferred_days)
        return self.preferred_days  # Fallback if it's a string

class Room(models.Model):
    room_name = models.CharField(max_length=20, default='Default Room')  # Adjust max_length as needed
    seating_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.room_name   
    

class Course(models.Model):
    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
    ]

    course_number = models.CharField(max_length=5, primary_key=True)
    course_name = models.CharField(max_length=40)
    max_numb_students = models.IntegerField(default=0)
    instructors = models.ManyToManyField(Instructor)
    departments = models.ManyToManyField('Department', related_name='courses')  # Many-to-Many relationship
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)

    def __str__(self):
        return f'{self.course_number} {self.course_name}'

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def get_occupied_timeslots(self):
        # This is a conceptual implementation. 
        # You'll need to adjust it according to your actual data models and relationships.
        occupied_timeslots = set()
        for course in self.courses.all():  # Assuming a reverse relationship from Course to Department
            for lecture in course.lecture_set.all():
                occupied_timeslots.add(lecture.meeting_time)
        return occupied_timeslots
    def __str__(self):
        return self.name


class Lecture(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null=True, blank=True)
    meeting_time = models.CharField(max_length=20, choices=TIME_SLOTS, blank=True)

    def __str__(self):
        return f"{self.course.course_name}, Room: {self.room.room_name}, Time: {self.meeting_time}"

