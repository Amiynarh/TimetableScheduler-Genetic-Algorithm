import random
import os
import sys
import django
sys.path.append('/Users/macbookair/Downloads/TimetableScheduler')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Scheduler.settings')
django.setup()
from SchedulerApp.models import *

class SchedulerData:
    def __init__(self):
        self.courses = self.get_courses()
        self.instructors = self.get_instructors()
        self.rooms = self.get_rooms()
        self.departments = self.get_departments()
        self.current_schedules = {}

    def get_instructors(self):
        return Instructor.objects.all()
    def get_rooms(self):
        return Room.objects.all()
    def get_courses(self):
        return Course.objects.prefetch_related('departments', 'instructors').all()
    def get_departments(self):
        return Department.objects.prefetch_related('courses').all()
    def get_department_occupied_timeslots(self, department):
        return department.get_occupied_timeslots()

# def format_meeting_time(day, timeslot):
#     return f"{day} {timeslot}"

def format_meeting_time(day, timeslot):
    # Check if the input is a tuple and format accordingly
    if isinstance(day, tuple) and isinstance(timeslot, tuple):
        # Assuming day and timeslot tuples are of the same length and correspond to each other
        formatted_times = [f"{d} {t}" for d, t in zip(day, timeslot)]
        return ', '.join(formatted_times)
    elif isinstance(day, str) and isinstance(timeslot, str):
        # Handle the standard case where day and timeslot are simple strings
        return f"{day} {timeslot}"
    else:
        # Fallback for any unexpected input format
        return "Invalid input format"


def identify_common_courses(courses):
    common_courses = {}
    for course in courses:
        departments = course.departments.all()
        if len(departments) > 1:
            common_courses[course] = list(departments)
    return common_courses

def is_preferred_time(instructor, meeting_time, scheduler_data):
    preferred_times = [f"{day} {timeslot}" for day in instructor.preferred_days for timeslot in instructor.preferred_time_slots]
    return meeting_time in preferred_times

def is_department_level_overlap(course, meeting_time, timetable):
    for scheduled_course in timetable:
        if scheduled_course.meeting_time == meeting_time:
            if course.level == scheduled_course.course.level and \
               set(course.departments.all()).intersection(set(scheduled_course.course.departments.all())):
                return True  # Found an overlap
    return False

# def find_preferred_timeslots(instructors):
#     preferred_timeslots = {}
#     for instructor in instructors:
#         for day in instructor.preferred_days:
#             for timeslot in instructor.preferred_time_slots:
#                 key = f"{day} {timeslot}"
#                 if key in preferred_timeslots:
#                     preferred_timeslots[key] += 1
#                 else:
#                     preferred_timeslots[key] = 1
#     # Sort timeslots by the number of instructors preferring them, descending
#     sorted_preferred_timeslots = sorted(preferred_timeslots.items(), key=lambda x: x[1], reverse=True)
#     return [timeslot for timeslot, count in sorted_preferred_timeslots]

def find_preferred_timeslots(instructors):
    preferred_timeslots = []
    for instructor in instructors:
        for day in instructor.preferred_days:
            for timeslot in instructor.preferred_time_slots:
                preferred_timeslots.append((day, timeslot))
    return preferred_timeslots

# def schedule_course(course, timetable):
#     suitable_rooms = sorted([room for room in Room.objects.all() if room.seating_capacity >= course.max_numb_students],
#                             key=lambda r: abs(r.seating_capacity - course.max_numb_students))
#     selected_room = suitable_rooms[0] if suitable_rooms else random.choice(Room.objects.all())

#     combined_slots = [(day, time) for day in DAYS_OF_WEEK for time in TIME_SLOTS]
#     random.shuffle(combined_slots)

#     instructors = course.instructors.all()
#     preferred_timeslots = find_preferred_timeslots(instructors, combined_slots)

#     # Try to schedule in a preferred timeslot first
#     for timeslot in preferred_timeslots:
#         if not any(lecture.meeting_time == timeslot and lecture.course == course for lecture in timetable) and not is_department_level_overlap(course, timeslot, timetable):
#             new_lecture = Lecture(course=course, room=selected_room, meeting_time=timeslot)
#             timetable.append(new_lecture)
#             return  # Successfully scheduled with preference

#     # If no preferred time found or scheduled, try without preference but avoid department level overlap
#     for day, timeslot in combined_slots:
#         meeting_time = format_meeting_time(day, timeslot)
#         if not any(lecture.meeting_time == meeting_time and lecture.course == course for lecture in timetable) and not is_department_level_overlap(course, meeting_time, timetable):
#             new_lecture = Lecture(course=course, room=selected_room, meeting_time=meeting_time)
#             timetable.append(new_lecture)
#             break  # Successfully scheduled without causing overlap

def schedule_course(course, timetable, scheduler_data):
    # Get suitable rooms from scheduler_data
    suitable_rooms = sorted([room for room in scheduler_data.rooms if room.seating_capacity >= course.max_numb_students],
                            key=lambda r: abs(r.seating_capacity - course.max_numb_students))
    selected_room = suitable_rooms[0] if suitable_rooms else random.choice(scheduler_data.rooms)

    combined_slots = [(day, time) for day in DAYS_OF_WEEK for time in TIME_SLOTS]
    random.shuffle(combined_slots)

    instructors = course.instructors.all()
    preferred_timeslots = find_preferred_timeslots(instructors)

    # Try to schedule in a preferred timeslot first
    for timeslot in preferred_timeslots:
        day, time = timeslot
        meeting_time = format_meeting_time(day, time)
        if not any(lecture.meeting_time == meeting_time and (lecture.room == selected_room or set(lecture.course.instructors.all()).intersection(instructors)) for lecture in timetable):
            if not is_department_level_overlap(course, meeting_time, timetable):
                new_lecture = Lecture(course=course, room=selected_room, meeting_time=meeting_time)
                timetable.append(new_lecture)
                return  # Successfully scheduled with preference

    # If no preferred time found, try without preference
    for day, timeslot in combined_slots:
        meeting_time = format_meeting_time(day, timeslot)
        if not any(lecture.meeting_time == meeting_time and (lecture.room == selected_room or set(lecture.course.instructors.all()).intersection(instructors)) for lecture in timetable):
            if not is_department_level_overlap(course, meeting_time, timetable):
                new_lecture = Lecture(course=course, room=selected_room, meeting_time=meeting_time)
                timetable.append(new_lecture)
                break  # Successfully scheduled without causing overlap




def schedule_common_course(course, common_courses, timetable, rooms):
    total_students = course.max_numb_students
    suitable_room = select_suitable_room_for_common_course(total_students, rooms)
    instructors = list(course.instructors.all())
    # Ensure the timeslot selected has not already been assigned to this course
    suitable_timeslot = None
    attempts = 0
    while not suitable_timeslot and attempts < 100:  # Prevent infinite loop
        proposed_timeslot = select_timeslot_for_common_course(common_courses[course], instructors)
        if not any(lecture.course == course and lecture.meeting_time == proposed_timeslot for lecture in timetable):
            suitable_timeslot = proposed_timeslot
        attempts += 1

    if suitable_timeslot:
        lecture = Lecture(course=course, room=suitable_room, meeting_time=suitable_timeslot)
        timetable.append(lecture)
    else:
        print(f"Failed to schedule common course {course.name} due to timeslot conflicts.")


def select_timeslot_for_common_course(departments, instructors):
    occupied_timeslots = set()
    for dept in departments:
        occupied_timeslots.update(dept.get_occupied_timeslots())  # Assuming a method that returns occupied timeslots
    # Step 2: Consider instructor preferences
    preferred_timeslots = set()
    for instructor in instructors:
        for day in instructor.preferred_days:
            for timeslot in instructor.preferred_time_slots:
                preferred_timeslots.add(f"{day} {timeslot}")
    # Step 3: Identify suitable timeslots
    all_timeslots = set([(day, time) for day in DAYS_OF_WEEK for time in TIME_SLOTS])
    suitable_timeslots = all_timeslots - occupied_timeslots
    # Step 4: Prioritize preferred timeslots
    final_choices = preferred_timeslots.intersection(suitable_timeslots) or suitable_timeslots
    # Step 5: Select a timeslot
    return format_meeting_time(*random.choice(list(final_choices)))
    # return format_meeting_time(selected_day, selected_timeslot)


def select_suitable_room_for_common_course(total_students, rooms):
    suitable_rooms = [room for room in rooms if room.seating_capacity >= total_students]
    return min(suitable_rooms, key=lambda r: abs(r.seating_capacity - total_students)) if suitable_rooms else random.choice(rooms)


# def generate_individual(scheduler_data):
#     courses = scheduler_data.courses
#     rooms = scheduler_data.rooms
#     timetable = []
#     assigned_instructors = {}
#     common_courses = identify_common_courses(scheduler_data.courses)
#     scheduled_courses = set()
#     used_meeting_times = set()  # Initialize the set to track used meeting times
#     # Schedule common courses first
#     for course in common_courses:
#         if course.course_number not in scheduled_courses:
#             schedule_common_course(course, common_courses, timetable, scheduler_data.rooms)
#             scheduled_courses.add(course.course_number)
#     # Schedule remaining courses
#     for course in courses:
#         if course.course_number not in scheduled_courses:
#             suitable_rooms = sorted([room for room in rooms if room.seating_capacity >= course.max_numb_students], key=lambda r: abs(r.seating_capacity - course.max_numb_students))
#             selected_room = suitable_rooms[0] if suitable_rooms else random.choice(rooms)
#             combined_slots = [(day, time) for day in DAYS_OF_WEEK for time in TIME_SLOTS]
#             # Revise instructor preferences handling
#             instructor_preferences = []
#             for instructor in course.instructors.all():
#                 if instructor.preferred_days and instructor.preferred_time_slots:
#                     for day in instructor.preferred_days:
#                         for timeslot in instructor.preferred_time_slots:
#                             instructor_preferences.append((day, timeslot))

#             random.shuffle(combined_slots)
#             # Initialize a set to track used meeting times and a flag to indicate if meeting_time is applied
#             used_meeting_times = set()
#             meeting_time_applied = False

#             # Process instructor preferences first
#             for preference in instructor_preferences:
#                 day, timeslot = preference
#                 meeting_time = f"{day} {timeslot}"
#                 if meeting_time not in used_meeting_times:
#                     used_meeting_times.add(meeting_time)
#                     meeting_time_applied = True
#                     # Logic to create and append Lecture object goes here, ensuring meeting_time is applied
#                     break  # Exit the loop since meeting_time is applied

#             # If no preference applied, proceed with combined slots
#             if not meeting_time_applied:
#                 for day, timeslot in combined_slots:
#                     meeting_time = f"{day} {timeslot}"
#                     if meeting_time not in used_meeting_times:
#                         used_meeting_times.add(meeting_time)
#                         # Logic to create and append Lecture object goes here, using this selected meeting_time
#                         break  # Exit the loop since a meeting_time has now been applied

#             lecture = Lecture(course=course, room=selected_room, meeting_time=meeting_time)
#             timetable.append(lecture)
#             for instructor in course.instructors.all():
#                 assigned_instructors.setdefault(meeting_time, []).append(instructor)
#             scheduled_courses.add(course.course_number)

#     return timetable
def generate_individual(scheduler_data):
    courses = scheduler_data.courses
    timetable = []
    assigned_instructors = {}
    common_courses = identify_common_courses(scheduler_data.courses)
    scheduled_courses = set()

    # Schedule common courses first
    for course in common_courses:
        if course.course_number not in scheduled_courses:
            schedule_common_course(course, common_courses, timetable, scheduler_data.rooms)
            scheduled_courses.add(course.course_number)

    # Schedule remaining courses
    for course in courses:
        if course.course_number not in scheduled_courses:
            schedule_course(course, timetable, scheduler_data)
            scheduled_courses.add(course.course_number)

    return timetable



def generate_initial_population(population_size, scheduler_data):
    return [generate_individual(scheduler_data) for _ in range(population_size)]

def calculate_fitness(timetable, scheduler_data):
    penalty = 0
    HIGH_PENALTY = 200
    PREFERENCE_PENALTY = 100
    DEPT_LEVEL_PENALTY = 100
    detailed_logs = []

    for i, lecture1 in enumerate(timetable):
        for j, lecture2 in enumerate(timetable):
            if i != j:
                # Check for room and instructor overlap
                if lecture1.room == lecture2.room and lecture1.meeting_time == lecture2.meeting_time:
                    detailed_logs.append(f"Room overlap: {lecture1.course.course_name} and {lecture2.course.course_name} in {lecture1.room.room_name} at {lecture1.meeting_time}")
                    penalty += HIGH_PENALTY
                if set(lecture1.course.instructors.all()).intersection(lecture2.course.instructors.all()) and lecture1.meeting_time == lecture2.meeting_time:
                    instructors = ', '.join([instructor.name for instructor in set(lecture1.course.instructors.all()).intersection(lecture2.course.instructors.all())])
                    detailed_logs.append(f"Instructor overlap: {instructors} for courses {lecture1.course.course_name} and {lecture2.course.course_name} at {lecture1.meeting_time}")
                    penalty += HIGH_PENALTY

                # Check for department and level overlap
                departments1 = set(lecture1.course.departments.all())
                departments2 = set(lecture2.course.departments.all())
                if departments1.intersection(departments2) and lecture1.course.level == lecture2.course.level and lecture1.meeting_time == lecture2.meeting_time:
                    dept_names = ', '.join([dept.name for dept in departments1.intersection(departments2)])
                    detailed_logs.append(f"Department and level overlap: {dept_names} for courses {lecture1.course.course_name} and {lecture2.course.course_name} at {lecture1.meeting_time}")
                    penalty += DEPT_LEVEL_PENALTY

    for lecture in timetable:
        # Check room capacity
        if lecture.course.max_numb_students > lecture.room.seating_capacity:
            detailed_logs.append(f"Room capacity exceeded: {lecture.course.course_name} has {lecture.course.max_numb_students} students but room {lecture.room.room_name} has capacity {lecture.room.seating_capacity}")
            penalty += HIGH_PENALTY

        # Check for instructor preferences
        for instructor in lecture.course.instructors.all():
            if not is_preferred_time(instructor, lecture.meeting_time, scheduler_data):
                detailed_logs.append(f"Instructor preference not met: {instructor.name} does not prefer {lecture.meeting_time} for {lecture.course.course_name}")
                penalty += PREFERENCE_PENALTY

    # Print detailed logs
    for log in detailed_logs:
        print(log)

    return penalty



# def calculate_fitness(timetable, scheduler_data):
#     penalty = 0
#     HIGH_PENALTY = 100
#     PREFERENCE_PENALTY = 50  # Penalty for not meeting instructor preferences
#     DEPT_LEVEL_PENALTY = 50  # Penalty for department and level overlap

#     for i, lecture1 in enumerate(timetable):
#         for j, lecture2 in enumerate(timetable):
#             if i != j:
#                 # Check for room and instructor overlap
#                 if lecture1.room == lecture2.room and lecture1.meeting_time == lecture2.meeting_time:
#                     print(f"Room overlap penalty: {lecture1.course.course_name} and {lecture2.course.course_name} in {lecture1.room.room_name} at {lecture1.meeting_time}")

#                     penalty += HIGH_PENALTY
#                 if set(lecture1.course.instructors.all()).intersection(lecture2.course.instructors.all()) and lecture1.meeting_time == lecture2.meeting_time:
#                     instructors = ', '.join([instructor.name for instructor in lecture1.course.instructors.all().intersection(lecture2.course.instructors.all())])
#                     print(f"Instructor overlap penalty: {instructors} for courses {lecture1.course.course_name} and {lecture2.course.course_name} at {lecture1.meeting_time}")
#                     penalty += HIGH_PENALTY

#                 # Check for department and level overlap
#                 departments1 = set(lecture1.course.departments.all())
#                 departments2 = set(lecture2.course.departments.all())
#                 if departments1.intersection(departments2) and lecture1.course.level == lecture2.course.level and lecture1.meeting_time == lecture2.meeting_time:
#                     dept_names = ', '.join([dept.name for dept in departments1.intersection(departments2)])
#                     print(f"Department and level overlap penalty: {dept_names} for courses {lecture1.course.course_name} and {lecture2.course.course_name} at {lecture1.meeting_time}")
#                     penalty += DEPT_LEVEL_PENALTY

#     for lecture in timetable:
#         # Check room capacity
#         if lecture.course.max_numb_students > lecture.room.seating_capacity:
#             print(f"Room capacity penalty: {lecture.course.course_name} has {lecture.course.max_numb_students} students but room {lecture.room.name} has capacity {lecture.room.seating_capacity}")
#             penalty += HIGH_PENALTY

#         # Check for instructor preferences
#         for instructor in lecture.course.instructors.all():
#             if not is_preferred_time(instructor, lecture.meeting_time, scheduler_data):
#                 print(f"Instructor preference penalty: {instructor.name} does not prefer {lecture.meeting_time} for {lecture.course.course_name}")
#                 penalty += PREFERENCE_PENALTY

#     return penalty


# def tournament_selection(population, fitness_scores, tournament_size=3):
#     selected_parents = []
#     for _ in range(len(population) // 2):
#         tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
#         winner = min(tournament, key=lambda x: x[1])  # Lower fitness score is better
#         selected_parents.append(winner[0])
#     return selected_parents


# def one_point_crossover(parent1, parent2, scheduler_data):
#     crossover_point = random.randint(1, len(parent1) - 1)
#     child1 = parent1[:crossover_point] + parent2[crossover_point:]
#     child2 = parent2[:crossover_point] + parent1[crossover_point:]

#     for child in [child1, child2]:
#         for lecture in child:
#             if is_conflict(lecture, child):
#                 lecture.room = select_suitable_room(lecture.course, scheduler_data.rooms)
#                 lecture.meeting_time = select_preferred_time_slot(lecture.course.instructors, scheduler_data)
#     return child1, child2

def tournament_selection(population, fitness_scores, tournament_size=3):
    selected_parents = []
    for _ in range(len(population) // 2):
        tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
        winner = min(tournament, key=lambda x: x[1])  # Lower fitness score is better
        selected_parents.append(winner[0])
    return selected_parents

def one_point_crossover(parent1, parent2, scheduler_data):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    for child in [child1, child2]:
        for lecture in child:
            if is_conflict(lecture, child):
                lecture.room = select_suitable_room(lecture.course, scheduler_data.rooms)
                lecture.meeting_time = select_preferred_time_slot(lecture.course.instructors, scheduler_data)
    return child1, child2


def is_conflict(lecture, timetable):
    for other_lecture in timetable:
        if lecture != other_lecture:
            if (lecture.room == other_lecture.room and lecture.meeting_time == other_lecture.meeting_time) or \
               (lecture.course.instructors.all().intersection(other_lecture.course.instructors.all()) and lecture.meeting_time == other_lecture.meeting_time):
                return True
    return False


def select_preferred_time_slot(instructors, scheduler_data):
    preferred_times = []
    for instructor in instructors.all():
        if instructor.preferred_days and instructor.preferred_time_slots:
            for day in instructor.preferred_days:
                for timeslot in instructor.preferred_time_slots:
                    preferred_times.append(format_meeting_time(day, timeslot))

    return random.choice(preferred_times) if preferred_times else random.choice([format_meeting_time(day, time) for day, time in TIME_SLOTS])


# def mutate_timetable(timetable, mutation_rate, scheduler_data):
#     mutated_timetable = []
#     for lecture in timetable:
#         if random.random() < mutation_rate:
#             if random.random() < 0.5:
#                 lecture.meeting_time = select_preferred_time_slot(lecture.course.instructors, scheduler_data)
#             else:
#                 departments = set(lecture.course.departments.all())
#                 lecture.meeting_time = select_time_avoiding_dept_conflicts(departments, lecture.course.level, scheduler_data.current_schedules)
#                 update_current_schedules(departments, lecture.course.level, lecture.meeting_time, scheduler_data.current_schedules)

#             lecture.room = select_suitable_room(lecture.course, scheduler_data.rooms)

#         mutated_timetable.append(lecture)
#     return mutated_timetable


def mutate_timetable(timetable, mutation_rate, scheduler_data):
    mutated_timetable = []
    for lecture in timetable:
        if random.random() < mutation_rate:
            # Remove the lecture and try to reschedule it
            timetable.remove(lecture)
            schedule_course(lecture.course, timetable, scheduler_data)
        else:
            mutated_timetable.append(lecture)
    return mutated_timetable

def update_current_schedules(departments, level, meeting_time, current_schedules):
    day, timeslot = meeting_time.split()[:2]  # Split and take the first two elements
    for department in departments:
        key = (department, level, day, timeslot)
        if key in current_schedules:
            current_schedules[key] += 1
        else:
            current_schedules[key] = 1


SOME_THRESHOLD = 3 
def select_time_avoiding_dept_conflicts(departments, level, current_schedules):
    combined_slots = [(day, time) for day in DAYS_OF_WEEK for time in TIME_SLOTS]
    less_scheduled_slots = [slot for slot in combined_slots if all(current_schedules.get((dept, level, *slot), 0) < SOME_THRESHOLD for dept in departments)]
    return format_meeting_time(*random.choice(less_scheduled_slots if less_scheduled_slots else combined_slots))


def select_suitable_room(course, rooms):
    suitable_rooms = [room for room in rooms if room.seating_capacity >= course.max_numb_students]
    if suitable_rooms:
        return min(suitable_rooms, key=lambda r: abs(r.seating_capacity - course.max_numb_students))
    else:
        return random.choice(rooms)  # Fallback if no suitable room is found

def run_genetic_algorithm():
    population_size = 100
    scheduler_data = SchedulerData()
    population = generate_initial_population(population_size, scheduler_data)
    fitness_scores = [calculate_fitness(individual, scheduler_data) for individual in population]
    num_generations = 15
    mutation_rate = 0.1

    for generation in range(num_generations):
        selected_parents = tournament_selection(population, fitness_scores)
        if len(selected_parents) % 2 != 0:
            selected_parents.pop()

        offspring = []
        for i in range(0, len(selected_parents), 2):
            parent1, parent2 = selected_parents[i], selected_parents[i + 1]
            offspring1, offspring2 = one_point_crossover(parent1, parent2, scheduler_data)
            offspring.extend([offspring1, offspring2])

        mutated_offspring = [mutate_timetable(child, mutation_rate, scheduler_data) for child in offspring]
        combined_population = selected_parents + mutated_offspring

        fitness_scores = [calculate_fitness(individual, scheduler_data) for individual in combined_population]
        best_fitness = min(fitness_scores)
        print(f"Generation {generation + 1}: Best Fitness Score: {best_fitness}")

    best_timetable_index = fitness_scores.index(min(fitness_scores))
    best_timetable = population[best_timetable_index]
    print("Best Timetable:")
    for lecture in best_timetable:
        instructors = ', '.join([instructor.name for instructor in lecture.course.instructors.all()])
        print(f"Course: {lecture.course.course_name}, Instructors: {instructors}, Room: {lecture.room.room_name}, Time: {lecture.meeting_time}")

    return best_timetable

if __name__ == "__main__":
    run_genetic_algorithm()


# def run_genetic_algorithm():
#     population_size = 100  
#     scheduler_data = SchedulerData()  # Initialize data
#     current_schedules = {}  # Initialize it at the start of your algorithm
#     population = generate_initial_population(population_size, scheduler_data)
#     fitness_scores = [calculate_fitness(individual, scheduler_data) for individual in population]
#     num_generations = 15
#     mutation_rate = 0.1

#     # GA Main Loop
#     for generation in range(num_generations):
#         # Selection
#         selected_parents = tournament_selection(population, fitness_scores)
       
#         # Ensure an even number of selected parents for crossover
#         if len(selected_parents) % 2 != 0:
#             selected_parents.pop()
       
#         # Crossover
#         offspring = []
#         for i in range(0, len(selected_parents), 2):
#             parent1, parent2 = selected_parents[i], selected_parents[i+1]
#             offspring1, offspring2 = one_point_crossover(parent1, parent2, scheduler_data)
#             offspring.extend([offspring1, offspring2])

#         # Mutation
#         mutated_offspring = [mutate_timetable(child, mutation_rate, scheduler_data) for child in offspring]

#         # Combine parents and offspring for next generation
#         combined_population = selected_parents + mutated_offspring

#         # Recalculate fitness scores for the new population
#         fitness_scores = [calculate_fitness(individual, scheduler_data) for individual in combined_population]

#         # Print fitness score of the best timetable in this generation
#         best_fitness = min(fitness_scores)
#         print(f"Generation {generation + 1}: Best Fitness Score: {best_fitness}")
#     # Extract the best timetable
#     best_timetable_index = fitness_scores.index(min(fitness_scores))
#     best_timetable = population[best_timetable_index]
#     # Display the best timetable
#     print("Best Timetable:")
#     for lecture in best_timetable:
#         instructors = ', '.join([instructor.name for instructor in lecture.course.instructors.all()])
#         print(f"Course: {lecture.course.course_name}, Instructors: {instructors}, Room: {lecture.room.room_name}, Time: {lecture.meeting_time}")

#     return best_timetable

# if __name__ == "__main__":
#     run_genetic_algorithm()
