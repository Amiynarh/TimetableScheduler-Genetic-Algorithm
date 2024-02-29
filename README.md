# Timetable Scheduler
----------------------------------------------------------------------------------------------------------------------------
### An intelligent timetable generator that generates University timetable using `Genetic Algorithm`.

#### Dependencies:
 1. python 3.6 or above
 2. Django 2.0 or above

#### Run on your local machine by:
* `git clone URL`
* `cd TimetableScheduler`
* `python manage.py runserver`
* then go to port `http://127.0.0.1:8000/` to run the local server

#### About the project:
Project uses genetic algorithm to satisfy the constraints related to Timetable scheduling. The program satisfies the following constraints:-

| Hard Constraints                                  | Soft Constraints                                     |
| --------------------------------------------------|:----------------------------------------------------:|
| Class timing considering instructors preference   | Classes are alloted according to Departments|
| Course.students <= room.seating capacity          | All courses are according to their Department        |
| Two classes dont have same room                   | Even distribution of course in a Department per week  |
| Class timing for each teacher is unique           |
| Teachers are allocated to their course accordingly|



