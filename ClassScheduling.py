# Name: Elizabeth Chan, Tessa Pham, Xinyi Wang
# File: ClassScheduling.py

'''
1. Preprocessing the data:
Parse a list of students and a list of their preferences.

For example:    Name            Preferred Classes
                Elizabeth       a, b, c, d
                Tessa           b, e, f, h
                Xinyi           c, g, m, n
TESSA: Hey Lizzy! If you're just parsing the demo data, since we don't have preference lists of students, please create some table like the one above and write a function to parse it.

If given a table like this, parse students = {Elizabeth, Tessa, Xinyi} and preferences = {[a, b, c, d], [b, e, f, h], [c, g, m, n]}.

Arrays we need from parsing: students, preferences, classes
    students - list of all students
    preferences - list of lists of preferred classes for all students (parsed in same order as students)
    classes - list of all classes
    times - list of time slots
'''
# global arrays
students = []
preferences = []
classes = []
times = []
professorOfClass = []


'''
# write multiple parse functions (for the demo file, for the preference lists of students, etc.) if necessary
def parse(file):
    # parse file to put values into global arrays: students, preferences, classes, times
    # parse file to build array professorOfClass: go through list of classes from top to bottom, save the professor's name in professorOfClass[c].
'''

# Now that we have the arrays above, we can initialize these following arrays. The order can't be changed!

# studentsInClass: a dictionary (key = class, value = list of students in that class)
studentsInClass = {c: [] for c in classes}
# classesInTime: a dictionary (key = time, value = list of classes in that time)
classesInTime = {t: [] for t in times}
# classesInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
professorsInTime = {t: [] for t in times}
# availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from largest to smallest)
availableRoomsInTime = {t: [] for t in times}
# overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
overlap = [[0 for c in classes] for c in classes]

def construct():
    for s, p in zip(students, preferences):
        # for each class c in the preference list of student s
        for c in p:
            # add s to student list of class c
            studentsInClass.get(c).append(s)
            # increment the overlaps of class c with each class in the rest of list p
            for other_c in p[(p.index(c) + 1)]:
                overlap[classes.index(c)][classes.index(other_c)] += 1
                overlap[classes.index(other_c)][classes.index(c)] += 1

# sort classes by size in descending order (this function is not working though, someone who knows Python please help figure out!)
# the idea is: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
sorted(classes, key = lambda c: len(studentsInClass.get(c)), reverse = True)

def assignClassToTime(c):
    min_overlap = float("inf")
    chosen_time = times[0]
    prof = professorOfClass[classes.index(c)]

    for t in times:
        # skip if the professor teaching class c is already teaching another class in this time
        if prof in professorsInTime.get(t):
            continue

        # skip if no more available rooms
        if len(availableRoomsInTime.get(t)) == 0:
            continue

        # skip if number of students in class c is greater than the size of the biggest available room in time t
        if len(studentsInClass.get(c)) > availableRoomsInTime.get(t)[1]:
            continue
        
        count = 0
        for assigned_c in classesInTime.get(t):
            count += overlap[classes.index(c)][classes.index(assigned_c)]
        
        if count < min_overlap:
            min_overlap = count
            chosen_time = t
    
    # add class c to the chosen time
    classesInTime.get(chosen_time).append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime.get(chosen_time).append(prof)
    # remove the first room from list of available rooms (because they're ranked by size, as well as the classes)
    availableRoomsInTime.pop(0)

def main():
    # call parse methods here if necessary?
    for c in classes:
        assignClassToTime(c)


