from django import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('logout/', logout_view, name='logout'),
    path('schedule_page/', schedule_page, name='schedule_page'),
    path('start-scheduling/', start_scheduling, name='start_scheduling'),
    path('generate-timetable/', generate_timetable, name='generate_timetable'),


    path('timetable/select-view/', select_timetable_view, name='select_timetable_view'),
    path('timetable/view/<int:timetable_id>/', view_timetable, name='view_timetable'),
    path('timetable/instructor-view/<int:timetable_id>/', view_instructor_timetable, name='instructor_timetable'),

    path('instructorAdd/', instructorAdd, name='instructorAdd'),
    path('instructorEdit/', instructorEdit, name='instructorEdit'),
    path('instructorDelete/<int:pk>/', instructorDelete, name='deleteinstructor'),

    path('roomAdd/', roomAdd, name='roomAdd'),
    path('roomEdit/', roomEdit, name='roomEdit'),
    path('roomEdit/<int:pk>/', roomEdit, name='roomEdit'),  # For editing specific rooms
    path('roomDelete/<int:pk>/', roomDelete, name='deleteroom'),

    path('courseAdd/', courseAdd, name='courseAdd'),
    path('courseEdit/', courseEdit, name='courseEdit'),
    path('courseDelete/<str:pk>/', courseDelete, name='deletecourse'),

    path('api/genNum/', apiGenNum, name='apiGenNum'),
    path('api/terminateGens/', apiterminateGens, name='apiterminateGens')

]
