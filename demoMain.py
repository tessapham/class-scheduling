#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: Elizabeth Chan, Tessa Pham, Xinyi Wang
"""

"""
Structure:
1. Parsing the file
    - parseTXT() function parses the demo data file
        return students, preferences, classes, times, professorOfClass, classrooms, sizes
    - parseExcel() function to be added, to parse the excel data

This function incurs cheap costs.

2. Constructing the data
    - construct(students, preferences, classes)
        return studentsInClass, overlap, classes
    After we load the data in by either parseTXT() or parseExcel(), we feed the
    data into this construct function. The construct function takes inputs:
        students, preferences, classes, classrooms, sizesOfClassrooms, times
    and outputs:
        studentsInClass, overlap, classes, availableRoomsInTime
    The complexity of this function is O(k log k)+ O(w), which is the complexity to
    process the data

3. Assigning classes to times
    assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, professorOfClass, times, overlap, classes)
"""

import os
import pandas as pd
import xlrd
import copy

def parseTXT():
    students = []
    preferences = []
    classes = []
    times = []
    professorOfClass = []
    roomSize = {}

    # preferences
    DSP1 = open("basic/pref.txt", "r")
    preferencesInfo = DSP1.read().replace("\t", " ").replace("\n", " ").split(" ")

    for i in range(1, int(preferencesInfo[1]) + 1):
       students.append(str(i))

    temp = []
    count = 0
    for i in range (2, len(preferencesInfo)):
        if (count % 5  != 0):
            temp.append(preferencesInfo[i])
        count = count + 1

    count2 = 0
    individualPref = []
    preferences.append([])
    for i in range (0, len(temp)):
        individualPref.append(temp[i])
        count2 = count2 + 1
        if (count2 == 4):
            preferences.append(individualPref)
            count2 = 0
            individualPref = []

    DSP1.close()

    DC = open("basic/constraints.txt", "r")
    splitDemoCon = DC.read().replace("\t", " ").replace("\n", " ").split(" ")

    # classes
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Classes":
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                classes.append(j)

    # rooms
    i=0
    while splitDemoCon[i]!="Rooms":
        i+=1
    total_number_of_Rooms=int(splitDemoCon[i + 1]) + 1
    count=0
    while count<total_number_of_Rooms-1:
        roomSize[splitDemoCon[i+2]]=int(splitDemoCon[i+3])
        i+=2
        count+=1

    # times
    for i in range(0, int(splitDemoCon[2])):
        times.append(str(i))

    professorOfClass = [0] # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                professorOfClass.append(splitDemoCon[j])
    DC.close()
    ptemp=[[int(u) for u in x] for x in preferences]
    preferences=ptemp

    return roomSize, students, preferences, classes, times, professorOfClass

def construct(students, preferences, classes, roomSize, times):
    studentsInClass = {c: [] for c in range(0, 15)}
    studentsInClass.get(0).append(0)
    # overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = [[0 for c in range(0, 15)] for c in range(0, 15)]

    for s, p in zip(students, preferences):
        # for each class c in the preference list of student s
        for c in p:
            # add s to student list of class c
            if studentsInClass[c]==None:
                studentsInClass[c]=[s]
            else:
                studentsInClass[c].append(s)
            # increment the overlaps of class c with each class in the rest of list p
            for other_c in p[(p.index(c) + 1):]:
                # in overlap and any other arrays we construct, all classes are 1 less than their original numbers in the data
                overlap[c][other_c] += 1
                overlap[other_c][c] += 1
    
    # idea: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses
    sortedClassroom=[(k, roomSize[k]) for k in sorted(roomSize, key=roomSize.get, reverse=False)]
    availableRoomsInTime = {t: sortedClassroom for t in times}

    return studentsInClass, overlap, classes, availableRoomsInTime

def assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,profOfCDict,times,overlap,classes,timeOfClass,classroomOfClass):
    min_overlap = float("inf")
    chosen_time = times[0]

    prof = profOfCDict[c]

    for t in times:
        # skip if the professor teaching class c is already teaching another class in this time
        if (len(professorsInTime[t]) != 0) & (prof in professorsInTime[t]):
            continue

        # skip if no more available rooms
        if len(availableRoomsInTime[t]) == 0:
            continue

        # skip if number of students in class c is greater than the size of the biggest available room in time t
        if len(studentsInClass.get(c)) > availableRoomsInTime[t][-1][1]:
            continue

        count = 0

        for assigned_c in classesInTime[t]:
            count += overlap[c][assigned_c]

        if count < min_overlap:
            min_overlap = count
            chosen_time = t

    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    temp=copy.deepcopy(availableRoomsInTime[chosen_time])
    classroomOfClass[c]=temp.pop()[0]
    availableRoomsInTime[chosen_time]=copy.deepcopy(temp)
    timeOfClass[c]=chosen_time

def calculate_student_in_class(timeOfClass,classes, students,preferencesDict):
    studentsTakingClass={}
    for c in classes:
        studentsTakingClass[c]=[]
    for s in students:
        busyTime=[]
        wishList=preferencesDict[s]
        for i in range(0,4):
            if timeOfClass[wishList[i]] not in busyTime:
                busyTime.append(timeOfClass[wishList[i]])
                studentsTakingClass[wishList[i]].append(s)
    return studentsTakingClass

def main():
    roomSize, students, preferences, classes, times, professorOfClass = parseTXT()
    studentsInClass, overlap, classes, availableRoomsInTime = construct(students, preferences, classes,roomSize,times)

    classesInTime = {t: [] for t in times}
    professorsInTime = {t: [] for t in times}

    profOfCDict={}
    for c in classes:
        profOfCDict[c]=professorOfClass[int(c)]

    classroomOfClass={}
    timeOfClass={}
    for c in classes:
        assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,profOfCDict,times,overlap,classes,timeOfClass,classroomOfClass)

    preferencesDict={}
    for s in students:
        preferencesDict[s]=preferences[int(s)]

    studentsTakingClass=calculate_student_in_class(timeOfClass,classes, students,preferencesDict)

    f=open("schedule.txt","w+")
    f.write("Course"+'\t'+"Room"+'\t'+"Teacher"+'\t'+"Time"+'\t'+"Students"+'\n')
    for i in range(len(classes)):
        c=classes[i]
        f.write(str(c)+'\t'+str(classroomOfClass[c])+'\t'+profOfCDict[c]+'\t'+timeOfClass[c]+'\t'+' '.join(studentsTakingClass[c])+'\n')
    with open("schedule.txt") as f:
        print(f.read())

    total=0
    for key in studentsTakingClass:
        total+=len(studentsTakingClass[key])
    opt=total/(len(students)*4)
    print(opt)

if __name__ == "__main__":
    main()
