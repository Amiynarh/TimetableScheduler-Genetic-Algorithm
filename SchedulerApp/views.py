from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .genetic_algorithm import *
from django.contrib.auth import logout


VARS = {'generationNum': 0,
        'terminateGens': False}

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! You can now login.')
            return redirect('login')  
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Assuming you have a URL pattern named 'login'


@login_required
def schedule_page(request):
    return render(request, 'schedule_page.html')

def start_scheduling(request):
    best_timetable = run_genetic_algorithm()
    # Serialize the data, if necessary
    serialized_timetable = serialize_timetable(best_timetable)  # Implement this function
    request.session['best_timetable'] = serialized_timetable
    return redirect('view_timetable')

def serialize_timetable(timetable):
    if timetable is None:
        return []

    serialized_data = []
    existing_entries = set()  # To track existing entries and prevent duplicates

    for lecture in timetable:
        course = lecture.course
        departments = course.departments.all()
        for dept in departments:
            times = lecture.meeting_time.split(', ')
            for time in times:
                try:
                    day, time = time.split(' ', 1)
                except ValueError:
                    day, time = "Unknown", "Unknown"
                # Creating a unique identifier for each entry
                entry_identifier = (dept.name, course.level, course.course_name, ", ".join([instructor.name for instructor in course.instructors.all()]), lecture.room.room_name, day, time)

                if entry_identifier not in existing_entries:
                    existing_entries.add(entry_identifier)
                    serialized_data.append({
                        'department': dept.name,
                        'level': course.level,
                        'course_name': course.course_name,
                        'instructors': ", ".join([instructor.name for instructor in course.instructors.all()]),
                        'room': lecture.room.room_name,
                        'day': day,
                        'time': time
                    })
    return serialized_data



# # original code
# @login_required
# def view_timetable(request):
#     serialized_timetable = request.session.get('best_timetable', [])
#     department_levels = {}
#     for item in serialized_timetable:
#         dept_level = (item['department'], item['level'])
#         department_levels.setdefault(dept_level, []).append(item)
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     timeslots = ['8:00 - 10:00', '10:00 - 12:00', '12:00 - 2:00', '2:00 - 4:00', '4:00 - 6:00']
#     # print(f"Department Levels: {department_levels}")
#     return render(request, 'timetable.html', {
#         'department_levels': department_levels,
#         'days': days,
#         'timeslots': timeslots
#     })

@login_required
def view_timetable(request):
    serialized_timetable = request.session.get('best_timetable', [])
    department_levels = {}
    for item in serialized_timetable:
        dept_level = (item['department'], item['level'])
        department_levels.setdefault(dept_level, []).append(item)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = ['8:00 - 10:00', '10:00 - 12:00', '12:00 - 2:00', '2:00 - 4:00', '4:00 - 6:00']
    if request.method == 'POST' and 'print_button' in request.POST:
        return render(request, 'timetable_print.html', {
            'department_levels': department_levels,
            'days': days,
            'timeslots': timeslots
        })

    return render(request, 'timetable.html', {
        'department_levels': department_levels,
        'days': days,
        'timeslots': timeslots
    })

def apiGenNum(request):
    return JsonResponse({'genNum': VARS['generationNum']})

def apiterminateGens(request):
    VARS['terminateGens'] = True
    return redirect('home')

'''
Page Views
'''

def home(request):
    return render(request, 'index.html', {})

@login_required
def instructorAdd(request):
    form = InstructorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
            new_instructor = form.save()  # Save and get the instance
            messages.add_message(request, messages.INFO, f"Instructor {new_instructor.uid} {new_instructor.name} has been added")
            return redirect('instructorEdit')
    context = {'form': form}
    return render(request, 'instructorAdd.html', context)

@login_required
def instructorEdit(request):
    context = {'instructors': Instructor.objects.all()}
    return render(request, 'instructorEdit.html', context)


@login_required
def instructorDelete(request, pk):
    inst = Instructor.objects.filter(pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('instructorEdit')


@login_required
def roomAdd(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, f"Classroom {form.cleaned_data['room_name']} has been added")
        return redirect('roomEdit')  # Redirecting to roomEdit view
    context = {'form': form}
    return render(request, 'roomAdd.html', context)


@login_required
def roomEdit(request):
    context = {'rooms': Room.objects.all()}
    return render(request, 'roomEdit.html', context)



@login_required
def roomDelete(request, pk):
    rm = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('roomEdit')


@login_required
def courseAdd(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, f"Course {form.data['course_number']} - {form.data['course_name']} has been added")
            return redirect('courseEdit')
        else:
            print('Invalid')
    context = {'form': form}
    return render(request, 'courseAdd.html', context)

@login_required
def courseEdit(request):
    instructor = defaultdict(list)
    for course in Course.instructors.through.objects.all():
        course_number = course.course_id
        instructor_name = Instructor.objects.filter(
            id=course.instructor_id).values('name')[0]['name']
        instructor[course_number].append(instructor_name)

    context = {'courses': Course.objects.all(), 'instructor': instructor}
    return render(request, 'courseEdit.html', context)


@login_required
def courseDelete(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('courseEdit')



'''
Error pages
'''

def error_404(request, exception):
    return render(request,'errors/404.html', {})

def error_500(request, *args, **argv):
    return render(request,'errors/500.html', {})
