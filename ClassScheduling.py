#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 21:17:46 2018

@author: Elizabeth Chan, Tessa Pham, Xinyi Wang

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

3. Assign the Classes to times
    assignClassToTime(c,availableRoomsInTime,professorsInTime,classesInTime,studentsInClass,professorOfClass,times,overlap,classes)


"""

# parsing excel
import os
import pandas as pd
import xlrd
import copy
import csv
import datetime
import math
import numpy as np


# write multiple parse functions (for the demo file, for the preference lists of students, etc.) if necessary

# parsing for demo data
def parseTXT():
    """
    Parses the constraints.txt and pref.txt, return roomSize, students, preferences, classes, times, professorOfClass.
    Outputs look like:
        
    students: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    classes: [6, 5, 4, 8, 1, 7, 3, 2]
    preferences: [[], [7, 4, 2, 8], [2, 3, 4, 1], [4, 6, 5, 3], [3, 1, 7, 2], [5, 1, 3, 4], [7, 8, 2, 3], [5, 1, 2, 8], [2, 6, 8, 7], [2, 1, 3, 7], [3, 6, 4, 2]]
    times: ['0', '1', '2', '3']
    roomSize:{'1': 876, '2': 815, '3': 232, '4': 101}
    professorOfClass: [0, '4', '4', '2', '1', '1', '3', '3', '2']

    """
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
        if (count % 5 != 0):
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
            # for j in range(0, int(splitDemoCon[i + 1])):
            for j in range(1, int(splitDemoCon[i + 1]) + 1): # range(1, 15)
                classes.append(j) # classes[0..13] will store 1 - 14, same as students above!

    # parse classrooms and roomSize
    i = 0    
    while splitDemoCon[i] != "Rooms":
        i += 1
    totalNumOfRooms = int(splitDemoCon[i + 1]) + 1
    count = 0
    while count < (totalNumOfRooms - 1):
        roomSize[splitDemoCon[i+2]] = int(splitDemoCon[i + 3])
        i += 2
        count += 1

    # times
    for i in range(0, int(splitDemoCon[2])):
        times.append(str(i))

    # professorOfClass
    professorOfClass = [0] # class 0 is not valid
    for i in range(0, len(splitDemoCon)):
        if splitDemoCon[i] == "Teachers":
            for j in range(i + 3, len(splitDemoCon), 2):
                professorOfClass.append(splitDemoCon[j])
    DC.close()
    ptemp = [[int(u) for u in x] for x in preferences]
    preferences = ptemp
    
    return roomSize, students, preferences, classes, times, professorOfClass


# parsing for bmc data:
def is_nan(x):
    return (x is np.nan or x != x)

def BMCparse():

    BMCexcel = pd.read_excel('brynmawr/bmc-data-f17.xls')

    # times = [] has been replaced with following three lists 
    daysOfWeek = BMCexcel["Days 1"]
    startTime = BMCexcel["Srt1 AM/PM"]
    endTime = BMCexcel["End 1 AMPM"]

    classes = BMCexcel["Class Nbr"]

    professorOfClass = BMCexcel["Name"]

    # no list of students for students = []
    # instead use this array that is the number of student capacity 
    studentCap = BMCexcel["Class Cap"]


    # print("\n\ndaysOfWeek \n {}".format(daysOfWeek))
    # print("\n\nstartTime \n {}".format(startTime))
    # print("\n\nendTime \n {}".format(endTime))
    # print("\n\nclasses \n {}".format(classes))
    # print("\n\nprofessorOfClass \n {}".format(professorOfClass))

    f = open("brynmawr_date.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in daysOfWeek:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_startTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in startTime:
        f.write("{}\n".format(i))
    f.close()


    f = open("brynmawr_endTime.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in endTime:
        f.write("{}\n".format(i))
    f.close()

    timeTupes = list(zip(startTime, endTime, daysOfWeek))

    f = open("brynmawr_allTimes.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in timeTupes:
        f.write("{}\n".format(i))
    f.close()

    # for Xinyi
    # from original excel file 
    subject = BMCexcel["Subject"]
    classSubject = {}
    for x in range(len(classes)):
        classSubject.update( {classes[x] : subject[x]} )

    f = open("brynmawr_classSubject.txt","w+")
    for i in classSubject:
        f.write("{}\t{}\n".format(i, classSubject[i]))
    f.close()

    # new excel file made by Xinyi
    BMCclassroom = pd.read_excel('brynmawr/bmc-classroom-data-f17.xlsx')

    # times = [] has been replaced with following three lists 
    subject_ = BMCclassroom["Subject"]
    classroomID = BMCclassroom["Facil ID 1"]
    classroomCap = BMCclassroom["Room Capacity"]

    roomSize = {}
    for x in range(len(classroomID)):
        roomSize.update( {classroomID[x] : classroomCap[x]} )

    f = open("brynmawr_roomSize.txt","w+")
    for i in roomSize:
        f.write("{}\t{}\n".format(i, roomSize[i]))
    f.close()

    roomAndSubject = {}
    for x in range(len(subject_)):
        roomAndSubject.update( { classroomID[x]: subject_[x] } )

    sortedSubjectClassroom = {}
    roomOptions = []
    for x in range(len(subject_)):
        if subject_[x] in sortedSubjectClassroom:
            if classroomID[x] not in sortedSubjectClassroom[subject_[x]] and is_nan(classroomID[x]) == False:
                toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
                sortedSubjectClassroom[subject_[x]].append(toAppend)
        else:
            toAppend = tuple((classroomID[x], roomSize[classroomID[x]])) 
            sortedSubjectClassroom.update({subject_[x] : [toAppend]})

    sortedSubjectClassroom["SOWK"].pop(0)
    del sortedSubjectClassroom["VILLANOV"]
    # print(sortedSubjectClassroom)

    for k in sortedSubjectClassroom:
        sortedSubjectClassroom[k].sort(key=lambda tup: tup[1], reverse=True)

    f = open("brynmawr_sortedSubjectClassroom.txt","w+")
    for i in sortedSubjectClassroom:
        f.write("{}\t{}\n".format(i, sortedSubjectClassroom[i]))
    f.close()


    # data not availble from excel file
    # preferences = [] 

    # overview of all arrays created in this function
    '''
    **see txt files with [college]_[name of data structure].txt for external version of parsed data

    !!following are parsed from bmc-data-f17.xls file
    startTime = [] - list of start times 
    endTime = [] - list of end times
    daysOfWeek = [] - list of days a timeslot is run 
    timeTupes = {} - previous three lists correspond to one another and are all formatted in this data structure 

    classes = [] - list of classes
    professorOfClass = [] - list of professors
    studentCap = [] - student capacity 

    subject = [] - list of subjects 
    classSubject = {} - dictionary of classes:subject

    !!following are parsed from bmc-classroom-data-f17.xlsx file
    subject_ = [] - list of subjects
    classroomID = [] - list of classroom IDs
    classroomCap = [] - list of capacities for each clasroom

    roomSize = {} - dictionary of classroomID:classroomCap
    roomAndSubject = {} - dictionary of classroomID:subject_
    sortedSubjectClassroom = {} - dictionary of subject_:[list of tuples that store (classroomID, classroomCap) that are availble for that key/subject_] where the items in the second part of the tuple, meaning the classroomIDs, are sorted in order of LARGEST cap room to SMALLEST cap room
    '''

    return daysOfWeek, startTime, endTime, timeTupes, classes, professorOfClass, studentCap, subject, classSubject, subject_, classroomID, classroomCap, roomSize, roomAndSubject, sortedSubjectClassroom




def HCparse():

    professorOfClass = []
    with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            professorOfClass_ = row[11]
            professorOfClass.append(professorOfClass_)
     
        professorOfClass.pop(0)
        

        # populating arrays from haverfordConstraints.txt file and haverfordConstraints_withZerios.txt file 

        timeID = []
        for i in range(1,61):
            timeID.append(str(i))
        # print timeID

        HCconstraints = open("haverford/haverfordConstraints.txt", "r")
        constraints = HCconstraints.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

        constraints = list(filter(None, constraints))
        
        justTimes = []
        for i in range(4, 363):
            justTimes.append(constraints[i])
        # print justTimes

        startTime = []
        endTime = []
        daysOfWeek = []

        count = 0
        for i in range (len(justTimes)):
            if count % 6 == 0:
                startTime.append(justTimes[i]+""+justTimes[i+1])
            count = count + 1
        count = 0

        for i in range (2, len(justTimes)):
            if count % 6 == 0:
                endTime.append(justTimes[i]+""+justTimes[i+1])
            count = count + 1

        # print endTime
        
        count = 0
        for i in range (4, len(justTimes)):
            if count % 6 == 0:
                daysOfWeek.append(justTimes[i])
            count = count + 1

        timeTupes = list(zip(timeID, startTime, endTime, daysOfWeek))
        # print timeTupes

        f = open("haverford_times.txt","w+")
        # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for i in range(len(timeTupes)):
            f.write("{}\t{}\t{}\n".format(startTime[i], endTime[i], daysOfWeek[i]))

        for i in timeTupes: 
            f.write("{}\n".format(i))
        f.close()



        justRooms = []
        for i in range(365, 465):
            justRooms.append(constraints[i])
        # print justRooms

        classroomID_fromtxt = []
        classroomCap = []
        roomSize = {}
        count = 0 
        for i in range (len(justRooms)):
            if count % 2 == 0:
                classroomID_fromtxt.append(justRooms[i])
            count = count + 1; 

        # print roomSizeName

        count = 0
        for i in range (1, len(justRooms)):
            if count % 2 == 0:
                classroomCap.append(justRooms[i])
            count = count + 1; 

        # print roomSizeCap

        roomSize = dict(zip(classroomID_fromtxt, classroomCap))

        f = open("haverford_roomSize.txt","w+")
        # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for i in roomSize:
            f.write("{}\t{}\n".format(i, roomSize[i]))
        f.close()

        # HCconstraints.close()

        HCconstraintsEnd = open("haverford/haverfordConstraints_withZeros.txt", "r")
        Endconstraints = HCconstraintsEnd.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")


        justClassesAndTeachers = []
        for i in range(564, len(Endconstraints)):
            justClassesAndTeachers.append(Endconstraints[i])
        # print justClassesAndTeachers

        classID = []
        teacherID = []
        classID_teacherID = {}
        count = 0 
        for i in range (len(justClassesAndTeachers)):
            if count % 2 == 0:
                classID.append(justClassesAndTeachers[i])
            count = count + 1; 

        # print classID

        count = 0
        for i in range (1, len(justClassesAndTeachers)):
            if count % 2 == 0:
                teacherID.append(justClassesAndTeachers[i])
            count = count + 1; 

        # print teacherID

        # for i in range(len(classID)):
        #     classID_teacherID.update({classID[i], teacherID[i]})
        
        classID_teacherID = dict(zip(classID, teacherID))

        # print classID_teacherID

        f = open("haverford_classID_teacherID.txt","w+")
        for i in classID_teacherID:
            f.write("{}\t{}\n".format(i, classID_teacherID[i]))
        f.close()

        HCconstraintsEnd.close()

        
        HCstudentprefs = open("haverford/haverfordStudentPrefs.txt", "r")
        studentprefs = HCstudentprefs.read().replace("\t", " ").replace("\r", " ").split('\n')

        studentprefs.pop(0)

        studentNumber = []
        for i in range(len(studentprefs)-1):
            temp = studentprefs[i].split(' ', 1)
            studentNumber.append(temp[0])

        student_pref = []

        for i in range(len(studentNumber)):
            temp = studentprefs[i].split(' ', 1)
            individualPrefs = temp[1].split(" ")
            individualPrefs.pop(-1)
            student_pref.append(individualPrefs)
        # print student_pref[0]

        studentPreferences = dict(zip(studentNumber, student_pref))


        f = open("haverford_studentPreferences.txt","w+")
        for i in studentNumber:
            f.write("{}\t{}\n".format(i, studentPreferences[i]))
        f.close()



        courseID = []
        subject = []
        classroomID = []

        # new excel file made by Xinyi
        with open('haverford/haverford-classroom-data.csv') as csvfile:
            readHC = csv.reader(csvfile, delimiter = ',')

            for row in readHC:
                courseID_ = row[0]
                subject_ = row[1]
                classroomID_ = row[2]

                courseID.append(courseID_)
                subject.append(subject_)
                classroomID.append(classroomID_)

            courseID.pop(0)
            subject.pop(0)
            classroomID.pop(0)

        # print classroomID 
        
        classSubject = {}
        for x in range(len(courseID)):
            classSubject.update( {courseID[x] : subject[x]} )

        f = open("haverford_classSubject.txt","w+")
        for i in classSubject:
            f.write("{}\t{}\n".format(i, classSubject[i]))
        f.close()

        roomAndSubject = {}
        for x in range(len(subject)):
            roomAndSubject.update( { classroomID[x]: subject[x] } )

        sortedSubjectClassroom = {}
        roomOptions = []
        for x in range(len(subject)):
            if subject[x] in sortedSubjectClassroom:
                if classroomID[x] not in sortedSubjectClassroom[subject[x]] and is_nan(classroomID[x]) == False:
                    if tuple((classroomID[x], roomSize[classroomID[x]])) not in sortedSubjectClassroom[subject[x]]: 
                        toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
                        sortedSubjectClassroom[subject[x]].append(toAppend)
            else:
                toAppend = tuple((classroomID[x], roomSize[classroomID[x]])) 
                sortedSubjectClassroom.update({subject[x] : [toAppend]})

        for k in sortedSubjectClassroom:
            sortedSubjectClassroom[k].sort(key=lambda tup: tup[1], reverse=True)

        f = open("haverford_sortedSubjectClassroom.txt","w+")
        for i in sortedSubjectClassroom:
            f.write("{}\t{}\n".format(i, sortedSubjectClassroom[i]))
        f.close()


        # overview of all arrays created in this function
        '''
        **see txt files with [college]_[name of data structure].txt for external version of parsed data

        !!following are from haverfordConstraints file 

        timeID = [] - list of times from 1 - 60
        startTime = [] - list of start times 
        endTime = [] - list of end times 
        daysOfWeek = [] - list of the days the times are scheduled for
        timeTupes = [] - a list of tuples of all this data meshed into one 

        classroomID_fromtxt = [] - list of room names specifically from haverfordConstraints file
        classroomCap = [] - list of room size capacity 
        roomSize = {} - dictionary of roomSizeName:roomSizeCap

        !!following are parsed from other haverfordfile (haverfordConstraints_withZeros) in which i filled in zeros for when there isn't a corresponding teacherID for a particular classID

        classID = [] - list of classID 
        teacherID = [] - list of teacherID
        classID_teacherID = {} - dictionary of classID:teacherID correspondence 

        !!following are parsed from haverfordStudentPrefs.txt

        studentNumber = [] - list of student ID numbers
        student_pref = [] - list of student preferences 
        studentPreferences = {} - dictionary of studentNumber:student_pref ie a students ID number and their corresponding list of classID preferences

        !!following are parsed from haverford-classroom-data.csv
        courseID = [] - list of IDs for each course
        subject = [] - list of subjects
        classroomID = [] = list of the IDs for each classroom 
        classSubject = {} - dictionary of courseID:subject

        roomAndSubject = {} - dictionary of classroomID:subject
        sortedSubjectClassroom = {} - dictionary of subject_:[list of tuples that store (classroomID, classroomCap) that are availble for that key/subject] where the items in the second part of the tuple, meaning the classroomIDs, are sorted in order of LARGEST cap room to SMALLEST cap room
        '''


        return timeID, startTime, endTime, daysOfWeek, timeTupes, classroomID_fromtxt, classroomCap, roomSize, classID, teacherID, classID_teacherID, studentNumber, student_pref, studentPreferences, courseID, subject, classroomID, classSubject, roomAndSubject, sortedSubjectClassroom

# Convert times to 24-hour format (for comparison).

def convertTimes(startTime, endTime):
    for i in range(0, len(startTime)):
        st = startTime[i]
        et = endTime[i]
        startTime[i] = datetime.datetime.strptime(st, '%I:%M %p').time()
        endTime[i] = datetime.datetime.strptime(et, '%I:%M %p').time()
    # startTime and endTime now contain time objects that can be compared to one another.
    return startTime, endTime

# parameter: a list of 4-tuples (timeID, startTime, endTime, daysOfWeek). Account for overlapping times.
def getOverlappingTimes(timeTuples):
    # remove duplicate times
    # timeTuples = set(timeTuples)
    timeIDs = [t[0] for t in timeTuples]
    MWF = [t for t in timeTuples if t[3] in ['M', 'W', 'F', 'MW', 'WF', 'MF', 'MWF']]
    TTH = [t for t in timeTuples if t[3] in ['T', 'TH', 'TTH']]
    # overlapsWithTime: a dictionary {time: all times that overlap with this time}
    overlapsWithTime = {i: [] for i in timeIDs}

    # sort MWF and TR by start times
    MWF = sorted(MWF, key = lambda x: x[1])
    TTH = sorted(TR, key = lambda x: x[1])

    for i in range(1, len(MWF) - 1):
        for j in range(i + 1, len(MWF)):
        # if start time of this slot is earlier than the finish time of the original slot => overlapping
            if MWF[j][1] < MWF[i][2]:
                overlapsWithTime[MWF[i][0]].append(MWF[j][0])
                overlapsWithTime[MWF[j][0]].append(MWF[i][0])
            else:
                break
    
    for i in range(1, len(TTH) - 1):
        for j in range(i + 1, len(TTH)):
            if TTH[j][1] < TTH[i][2]:
                overlapsWithTime[TTH[i][0]].append(TTH[j][0])
                overlapsWithTime[TTH[j][0]].append(TTH[i][0])
            else:
                break
    return overlapsWithTime

# Next level for constructing the inputs.
def construct(students, preferences, classes, roomSize, times, dictClasses = None, relationMode = False):
# def construct(students, preferences, classes, classrooms, sizesOfClassrooms, times):

    # ASSUME that classes is a list of tuples: c in classes = (major, class #)

    # studentsInClass: a dictionary (key = class, value = list of students in that class)
    # studentsInClass = {c: [] for c in range(0, 15)}
    studentsInClass = {c: [] for c in classes}
    studentsInClass[0] = [0]
    # overlap: a 2D matrix (row = all classes, column = all classes, entry at (i, j) = # of students taking both classes i and j)
    overlap = [[0 for c in range(0, 15)] for c in range(0, 15)]
    # overlap = [[0 for c in classes] for c in classes]
    relation = None

    if relationMode:
        subjects = set(list(dictClasses.values()))
        relation = [[1 for s in subjects] for s in subjects]

        for s, p in zip(students, preferences):
            for c in p:
                for other_c in p[(p.index(c) + 1):]:
                    # construct relation between 2 majors
                    relation[dictClasses[c]][dictClasses[other_c]] += 1
                    relation[dictClasses[other_c]][dictClasses[other_c]] += 1
    
    for s, p in zip(students, preferences):
            # for each class c in the preference list of student s
            for c in p:
                # add s to student list of class c
                if studentsInClass[c] is None:
                    studentsInClass[c] = [s]
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

    # sort the classroom from small to big, paired with their size.
    # sortedClassroom=[(y, x) for x, y in sorted(zip(sizesOfClassrooms, classrooms))]
    
    sortedClassroom = [(k, roomSize[k]) for k in sorted(roomSize, key = roomSize.get, reverse = False)]
    
    # availableRoomsInTime: a dictionary (key = time, value = list of tuples (room, size), ranked from smallest to largest)
    availableRoomsInTime = {t: sortedClassroom for t in times}
    return studentsInClass, overlap, classes, availableRoomsInTime, relation

def assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, profOfCDict, times, overlap, classes, timeOfClass, roomOfClass, overlapTimeMode = False, overlapsWithTime = None, relationMode = False, dictClasses = None, relation = None):
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
        
        if (overlapTimeMode & relationMode):
            for assigned_c in classesInTime[t]:
                count += overlap[c][assigned_c] * (relation[dictClasses[c]][dictClasses[assigned_c]] / 100)
            
            # account for other classes in overlapping times
            if len(overlapsWithTime[t]) > 0:
                for overlap_t in overlapsWithTime[t]:
                    for assigned_c in classesInTime[overlap_t]:
                        count += overlap[c][assigned_c] * (relation[dictClasses[c]][dictClasses[assigned_c]] / 100)
        else:  
            for assigned_c in classesInTime[t]:
                count += overlap[c][assigned_c]

        if count < min_overlap:
            min_overlap = count
            chosen_time = t

    # add class c to the chosen time
    classesInTime[chosen_time].append(c)
    # add the professor teaching class c to the list of professors occupied in the chosen time
    professorsInTime[chosen_time].append(prof)
    temp = copy.deepcopy(availableRoomsInTime[chosen_time])
    # roomOfClass[c] = temp.pop()[0]
    roomOfClass[c] = availableRoomsInTime[chosen_time].pop()[0]
    availableRoomsInTime[chosen_time] = copy.deepcopy(temp)
    timeOfClass[c] = chosen_time

# This function is for optimality analysis.
def calculateStudentsInClass(timeOfClass, classes, students, preferencesDict):
    studentsTakingClass = {}
    for c in classes:
        studentsTakingClass[c] = []
    for s in students:
        busyTime = []
        wishList = preferencesDict[s]
        for i in range(0,4):
            if timeOfClass[wishList[i]] not in busyTime:
                busyTime.append(timeOfClass[wishList[i]])
                studentsTakingClass[wishList[i]].append(s)
            # else, just pass
    return studentsTakingClass
# need to change to a more complicated algorithm to maximize the overall optimality
# brute force: which class to prioritize to receive the largest # classes out of 4.



def main():
    # Below is how we will use HCparse() to get a list of mutually exclusive time slots.
    
    # timeIDs, startTime, endTime, daysOfWeek, professorOfClass, dictClasses = HCparse()
    # timeID, startTime, endTime, daysOfWeek, professorOfClass, dictClasses = HCparse()
    # startTime, endTime = convertTimes(startTime, endTime)

    # make a list of tuples (daysOfWeek, startTime, endTime)
    # timeTuples = list(zip(timeIDs, startTime, endTime, daysOfWeek))
    # overlapsWithTime = getOverlappingTimes(timeTuples)

    roomSize, students, preferences, classes, times, professorOfClass = parseTXT()
    studentsInClass, overlap, classes, availableRoomsInTime, relation = construct(students, preferences, classes, roomSize, times, dictClasses = None, relationMode = False)

    # Now, initialize two arrays to store the results.
    # classesInTime:  a dictionary (key = time, value = list of classes in that time)
    classesInTime = {t: [] for t in times}
    # professorsInTime: a dictionary (key = time, value = list of professors teaching a class in that time)
    professorsInTime = {t: [] for t in times}
    
    profOfCDict = {}
    for c in classes:
        profOfCDict[c] = professorOfClass[int(c)]

    # Below are some reorganization for the outputs.
    roomOfClass = {} # courseID: roomID
    timeOfClass = {} # courseID: timeID

    BMCparse()
    HCparse()
    
    preferencesDict = {}
    for s in students:
        preferencesDict[s] = preferences[int(s)]
    for c in classes:
        assignClassToTime(c, availableRoomsInTime, professorsInTime, classesInTime, studentsInClass, profOfCDict, times, overlap, classes, timeOfClass, roomOfClass, overlapTimeMode = False, overlapsWithTime = None, relationMode = False, dictClasses = None, relation = None)

    # preferencesDict = {}
    # for s in students:
    #     preferencesDict[s] = preferences[int(s)]

    # Now calculate optimality.

    studentsTakingClass = calculateStudentsInClass(timeOfClass, classes, students, preferencesDict)

    f = open("schedule.txt", "w+")
    f.write("Course" + '\t' + "Room" + '\t' + "Teacher" + '\t' + "Time" + '\t' + "Students" + '\n')
    for i in range(len(classes)):
        c = classes[i]
        f.write(str(c) + '\t' + str(roomOfClass[c]) + '\t' + professorOfClass[c] + '\t' + timeOfClass[c] + '\t' + ' '.join(studentsTakingClass[c]) + '\n')  
    # with open("schedule.txt") as f:
        # print(f.read())
    
    total = 0
    for key in studentsTakingClass:
        total += len(studentsTakingClass[key])
    opt = total / (len(students) * 4)
    # print(opt)

"""
    print('\n')
    print('\n')
    print("Below are what's returned by parseTXT: " + '\n')
    print("students,", students)
    print("classes,", classes)
    print("preferences", preferences)
    print("times",times)
    print("roomSize",roomSize)
    print("professorOfClass",professorOfClass)
    
    print('\n' + "OtherThings" + '\n')
    
    print("roomOfClass", roomOfClass)
    print("professorOfClass", professorOfClass) #{7: '7', 10: '3'}
    print("timeOfClass", timeOfClass)
    print("studentsTakingClass", studentsTakingClass)
    print(students, '\n', '\n', preferences, '\n', '\n', classes, '\n', '\n', times, '\n', '\n', professorOfClass)

"""
if __name__ == "__main__":
    main()
