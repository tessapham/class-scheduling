#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 21:17:46 2018

@author: Elizabeth Chan, Tessa Pham, Xinyi Wang

"""
"""
10:48 Fri: an easy way to handle the 0 position is just to have the time id and classes start
from 0. in reality you're converting the class numbers to numbers from 1 anyways. so why not.

BECAUSE when you keep an 0 in the front, sorting would be a big issue. including when you
are using zip. 


Parsing the Excels part hasn't been tested yet. The current code works for the demo data.


1. Preprocessing the data:

Parse a list of students and a list of their preferences.
For example:    Name            Preferred Classes
                Elizabeth       a, b, c, d
                Tessa           b, e, f, h
                Xinyi           c, g, m, n

Given a file like above, parse students = {Elizabeth, Tessa, Xinyi} and preferences = {[a, b, c, d], [b, e, f, h], [c, g, m, n]}.
Arrays we need from parsing: students, preferences, classes
    students -  array of all students
    preferences - array of preference lists of all students (parsed in same order as students)
    classes - array of all classes, each represented by an integer from 1 to m
    times - array of all time slots, each represented by an integer from 1 to w
"""

# parsing excel
import os
import pandas as pd
import xlrd


# write multiple parse functions (for the demo file, for the preference lists of students, etc.) if necessary

# parsing for demo data
def parse():
    students = []
    preferences = [] 
    classes = []
    times = []
    professorOfClass = []

    DSP2 = open("demo_studentprefs.txt", "r") # opens file with name of "test.txt"
    studentInfo = DSP2.read().replace("\t", " ").replace("\n", " ").split(" ")

    for i in range(1, int(studentInfo[1]) + 1):
        students.append(str(i))
#    print("students: ")
#    print(students)

    # preferences
    DSP1 = open("demo_studentprefs.txt", "r") # opens file with name of "test.txt"
    preferencesInfo = DSP1.read().replace("\t", " ").replace("\n", " ").split(" ")

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

    
    DC = open("demo_constraints.txt", "r") # opens file with name of "test.txt"
    splitDemoCon = DC.read().replace("\t", " ").replace("\n", " ").split(" ")

    # times
    for i in range(0, len(splitDemoCon)): 
        if splitDemoCon[i] == "Classes":
            # for j in range(0, int(splitDemoCon[i + 1])):
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                # print splitDemoCon[j]
                # classes.append(str(j))
                classes.append(j) # classes[0..13] will store 1 - 14, same as students above!
    
    # times
    for i in range(0, int(splitDemoCon[2])):
        times.append(str(i))
 #   print("times: ")
 #   print(times)

    # professorOfClass
    professorOfClass[0] = 0 # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                # print splitDemoCon[j]
                professorOfClass.append(splitDemoCon[j])
                # professorOfClass[1] should be Teacher 5, but in our way of parsing, professorOfClass[0] = Teacher 5.
 #   print("professorOfClass")
 #   print(professorOfClass)

    DC.close()
    
    # integerFormat = [int(c) for c in classes]
    # classes = integerFormat
    # Tessa: We don't need the 2 lines above because classes are already added to the array as integers. See line 97.

# Xinyi: Lizzy makes the start of all arrays a placeholder. I am un-doing it.
# Tessa: No. What Lizzy did was actually storing classes 1 - 14 as 0 - 13. I changed it to: classes[0..13] stores students 1 - 14, i.e. classes[0] = 1.
    
    
    #>>>????????????????????????
    
    # preferences.pop(0) 
    # classes.pop(0)
    # students.pop(0)
    # times.pop(0)
    # professorOfClass.pop(0) # did you do that??
    
    # classes[:]=[x-1 for x in classes]
    # students[:]=[x-1 for x in students]
    # times[:]=[x-1 for x in times]
    # professorOfClass[:]=[x-1 for x in professorOfClass]
    
    # Tessa: We don't need this! Just fixed the code above.

    return students, preferences, classes, times, professorOfClass

"""
# parsing for bmc data: 
def BMCparse(fileName):


    # students = 
    # preferences =
    classes = fileName["Class Nbr"]

    times = fileName["Srt1 AM/PM"] + " -" + fileName["End 1 AMPM"]
    # print times
    # parse file to build array professorOfClass: go through list of classes from top to bottom, save the professor's name in professorOfClass[c].
    professorOfClass = fileName["Name"]
    # print professorOfClass

"""
# Another level for constructing the inputs.
# def construct(students, preferences, classes, times, studentsInClass, overlap):
def construct(students, preferences, classes, studentsInClass, overlap): # we don't need times for this function
    # Tessa: Xinyi, please establish: studentsInClass.get(0) = 0; overlap[0][x] = overlap[x][0] = 0.
    # For overlap, we can initialize a 2D array of all zeroes (0 - 14 each side).
    
    for s, p in zip(students, preferences):
        # for each class c in the preference list of student s
        for c in p:
            # add s to student list of class c
            studentsInClass.get(c).append(s)
            # increment the overlaps of class c with each class in the rest of list p
            for other_c in p[(p.index(c) + 1)]:
                # in overlap and any other arrays we construct, all classes are 1 less than their original numbers in the data
                overlap[c][other_c] += 1
                overlap[other_c][c] += 1
    # the idea is: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses
    return studentsInClass, overlap



def assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes):
    min_overlap = float("inf")
    chosen_time = times[0]
    prof = professorOfClass[classes.index(c)]

    for t in times:
        # skip if the professor teaching class c is already teaching another class in this time
        if len(professorsInTime.get(t)) != 0 & prof in professorsInTime.get(t):
            continue

        # skip if no more available rooms
        if len(availableRoomsInTime.get(t)) == 0:
            continue

        # skip if number of students in class c is greater than the size of the biggest available room in time t
        if len(studentsInClass.get(c)) > availableRoomsInTime.get(t)[0]:
            continue
        
        count = 0
        for assigned_c in classesInTime.get(t):
            count += overlap[c][assigned_c]
        
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
    students, preferences, classes, times, professorOfClass = parse()
    # studentsInClass: a dictionary (key = class, value = list of students in that class)
    print(students)
    print('\n')
    print(preferences)
    print('\n')
    print(classes)
    print('\n')
    print(times)
    print('\n')
    print(professorOfClass)
"""    studentsInClass = {c: [] for c in classes}
    # classesInTime: a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from largest to smallest)
    availableRoomsInTime = {t: [] for t in times}
# overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = [[0 for c in classes] for c in classes]
    studentsInClass, overlap = construct(students, preferences, classes, times, studentsInClass, overlap)
    parse()

    for c in classes:
        assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)

    return classesInTime
"""    
if __name__ == "__main__":
    main()

"""
Lizzy/Tessa's comments in main
    # call parse methods here if necessary?
        # parse file to put values into global arrays: students, preferences, classes, times
    # Retrieve current working directory (`cwd`)

    # --- parsing for BMC data

    # cwd = os.getcwd()
    # os.chdir("brynmawr")
    # fileName = 'bmc-÷÷÷÷÷÷÷÷÷≥data-f17.xls'
    # fileName = 'bmc-data-f17.xls'
    # BMCdata = pd.read_excel(fileName)

    # BMCparse(BMCdata)

    # --- parsing for BMC data  
"""
