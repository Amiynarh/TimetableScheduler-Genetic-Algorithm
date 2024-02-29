from django.contrib import admin
from .models import *

admin.site.register(Room)
admin.site.register(Instructor)
# admin.site.register(MeetingTime)
admin.site.register(Course)
# admin.site.register(Department)
admin.site.register(Lecture)
admin.site.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)