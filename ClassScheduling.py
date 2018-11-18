#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 21:17:46 2018

@author: Elizabeth Chan, Tessa Pham, Xinyi Wang

"""

"""
Structure:
    
1. Parsing the file

    - parseDemo() function parses the demo data file
        return students, preferences, classes, times, professorOfClass, classrooms, sizes
        (right now we do not yet have classrooms and sizes file, to be added later)
    - parseExcel() function to be added, to parse the excel data

This function incurs cheap costs.

2. Constructing the data

    - construct(students, preferences, classes)
        return studentsInClass, overlap, classes
    
    After we load the data in by either parseDemo() or parseExcel(), we feed the 
    data into this construct function. The construct function takes inputs:
        students, preferences, classes, classrooms, sizesOfClassrooms, times
    and outputs:
        studentsInClass, overlap, classes, availableRoomsInTime
        
    The complexity of this function is O(k log k)+ O(w), which is the complexity to 
    process the data

3. Assign the Classes to times
    assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)
    

"""



# parsing excel
import os
import pandas
import xlrd


# write multiple parse functions (for the demo file, for the preference lists of students, etc.) if necessary

# parsing for demo data
def parseDemo():
    '''
Given a file:
                Name            Preferred Classes
                Elizabeth       a, b, c, d
                Tessa           b, e, f, h
                Xinyi           c, g, m, n

return students = {Elizabeth, Tessa, Xinyi} 
preferences = {[a, b, c, d], [b, e, f, h], [c, g, m, n]}.
Arrays we need from parsing: students, preferences, classes
    students -  array of all students
    preferences - array of preference lists of all students (parsed in same order as students)
    classes - array of all classes, each represented by an integer from 1 to m
    times - array of all time slots, each represented by an integer from 1 to w
    '''
    students = []
    preferences = [] 
    classes = []
    times = []
    professorOfClass = []

    DSP2 = open("basic/demo_studentprefs.txt", "r") # opens file with name of "test.txt"
    studentInfo = DSP2.read().replace("\t", " ").replace("\n", " ").split(" ")

    for i in range(1, int(studentInfo[1]) + 1):
        students.append(str(i))
#    print("students: ")
#    print(students)

    # preferences
    DSP1 = open("basic/demo_studentprefs.txt", "r") # opens file with name of "test.txt"
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
    
    DC = open("basic/demo_constraints.txt", "r") # opens file with name of "test.txt"
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

    # professorOfClass
    professorOfClass = [0] # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                # print splitDemoCon[j]
                professorOfClass.append(splitDemoCon[j])
                # professorOfClass[1] should be Teacher 5, but in our way of parsing, professorOfClass[0] = Teacher 5.
 #   print("professorOfClass")
 #   print(professorOfClass)

    DC.close()
    ptemp=[[int(u) for u in x] for x in preferences]
    preferences=ptemp
    
    return students, preferences, classes, times, professorOfClass


# parsing for bmc data: 
def BMCparse():

    BMCexcel = pandas.read_excel('brynmawr/bmc-data-f17.xls')

    # times = [] has been replaced with following three lists 
    dayOfWeek = BMCexcel["Days 1"]
    startTime = BMCexcel["Srt1 AM/PM"]
    endTime = BMCexcel["End 1 AMPM"]

    classes = BMCexcel["Class Nbr"]

    professorOfClass = BMCexcel["Name"]

    studentCap = BMCexcel["Class Cap"]



    # data not availble from excel file
    # students = []
    # preferences = [] 




# def HCparse(fileName):




# Another level for constructing the inputs.

def construct(students, preferences, classes, classrooms, sizesOfClassrooms, times):
    # studentsInClass: a dictionary (key = class, value = list of students in that class)
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
    # the idea is: we want to sort the array classes, but we have to get the size from len(studentsInClass.get(c)) for each c in classes
    sizes = [len(studentsInClass.get(c)) for c in classes]
    sortedClasses = [x for _, x in sorted(zip(sizes, classes))]
    classes = sortedClasses

#sort the classroom from small to big, and pair with their size.
    sortedClassroom=[(y, x) for x, y in sorted(zip(sizesOfClassrooms, classrooms))]
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from smallest to largest)
    availableRoomsInTime = {t: sortedClassroom for t in times}  
    return studentsInClass, overlap, classes, availableRoomsInTime


def assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes):
    min_overlap = float("inf")
    chosen_time = times[0]
    
    prof = professorOfClass[classes.index(c)]

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
    # remove the last room from list of available rooms (because they're ranked by size)
    availableRoomsInTime[chosen_time].pop()

def main():
    students, preferences, classes, times, professorOfClass = parseDemo()
    
    #these two inputs are to be returned by parse() too. 
    classrooms=[x for x in range(20)]
    sizesOfClassrooms=[100]*20
    
    studentsInClass, overlap, classes, availableRoomsInTime = construct(students, preferences, classes,classrooms, sizesOfClassrooms,times)
    
    #Now, ready to assign classes to timeslots. initialize two arrays to store the result first.
    # classesInTime: a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}
    for c in classes:
        assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)
    
    # print("classesInTime: ")
    # print(classesInTime)
    # print("professorOfClass: ")
    # for i in range (0, len(professorOfClass)):
    # print(professorOfClass)
    # print("professorOfClass: ")
    # for i in range (0, len(professorOfClass)):
    #     print(professorOfClass[i])

    # demo = open("basic/demo_schedule.txt", "r") # opens file with name of "test.txt"
    # demoP = demo.read().split(" ")
    # print demoP

    # print classrooms

    # f= open("basic/our_schedule.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    # for i in range(0,len(classes)):
    #     f.write("{}\t{}\n".format(i+1,classes[i]))

    # f.seek(5)
    # f.write("\thello\t")
    

    # f = open("our_schedule.txt","w+")
    # for i 
    # f.write(classesInTime)

    # f.close()

    BMCparse()

    return classesInTime
   


if __name__ == "__main__":
    main()
    
"""
for testing, put in main:
    print(students)
    print('\n')
    print(preferences)
    print('\n')
    print(classes)
    print('\n')
    print(times)
    print('\n')
    print(professorOfClass)
    print(availableRoomsInTime)  

"""
"""
To handle the starting element:
    
10:48 Fri: an easy way to handle the 0 position is just to have the time id and classes start
from 0. in reality you're converting the class numbers to numbers from 1 anyways. so why not.

BECAUSE when you keep an 0 in the front, sorting would be a big issue. including when you
are using zip. 


Parsing the Excels part hasn't been tested yet. The current code works for the demo data.


"""
"""
Lizzy/Tessa's comments in main
    # call parse methods here if necessary?
        # parse file to put values into global arrays: students, preferences, classes, times
    # Retrieve current working directory (`cwd`)

    # --- parsing for BMC data

    # cwd = os.getcwd()
    # os.chdir("brynmawr")
    # fileName = 'bmc-÷÷÷÷÷÷÷÷÷≥data-f17.xls'
    # BMCdata = pd.read_excel(fileName)

    # BMCparse(BMCdata)

    # --- parsing for BMC data
    
    
"""
