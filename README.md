# Timetable Scheduler
----------------------------------------------------------------------------------------------------------------------------
### An intelligent timetable generator powered by Genetic Algorithm.
#### This project utilizes a genetic algorithm to generate university timetables while satisfying various constraints.

#### Key Features:

* Efficient optimization: Generates timetables that meet both hard and soft constraints. (#hard-constraints, #soft-constraints)
* Flexibility: Accommodates a wide range of scheduling preferences for students, lecturers, and courses.
* Customizable: Can be easily adapted to different universities and their specific requirements.

#### Dependencies:
 1. Python 3.6 or later
 2. Django 2.0 or later

#### Run on your local machine by:
* Clone the repository: `git clone URL`
* Navigate to the project directory: `cd TimetableScheduler`
* Install dependencies: `pip install -r requirements.txt`
* Run the development server: `python3 manage.py runserver`
* Access the local server: `http://127.0.0.1:8000/` 

#### About the project:
Project uses genetic algorithm to satisfy the constraints related to Timetable scheduling. The program satisfies the following constraints:-

| Hard Constraints                                                  | Soft Constraints                                     |
| --------------------------------------------------                |:----------------------------------------------------:|
| A lecturer cannot be assigned to two lectures at the same time.   | Attempts to minimize conflicts with student schedules.
| The assigned room must have enough capacity for the students enrolled in the course.        | All courses are according to their Department        |
| Lectures cannot be scheduled during a lecturer's unavailable time.                   | Prioritizes lecturers' preferred days or time slots. per week  |
| Certain courses might require specific spacing between lectures.            |
| Two classes cannot share the same room at the same time.|



