def HCparse():

    professorOfClass = []
    courseID = []
    subject = []
    with open('haverford/haverfordEnrollmentDataS14.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            professorOfClass_ = row[11]
            professorOfClass.append(professorOfClass_)

            courseID_ = row[1]
            subject_ = row[2]

            courseID.append(courseID_)
            subject.append(subject_)
     
        professorOfClass.pop(0)
    
    classSubject = dict(zip(courseID, subject))
        
        # populating arrays from haverfordConstraints.txt file and haverfordConstraints_withZerios.txt file 

    timeID = []
    for i in range(1,61):
        timeID.append(str(i))
    # print timeID

    # OLD PARSING CONSTRAINTS 
    # HCconstraints = open("haverford/haverfordConstraints.txt", "r")
    # constraints = HCconstraints.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

    # constraints = list(filter(None, constraints))
    
    # justTimes = []
    # for i in range(4, 363):
    #     justTimes.append(constraints[i])
    # # print justTimes

    # startTime = []
    # endTime = []
    # daysOfWeek = []

    # count = 0
    # for i in range (len(justTimes)):
    #     if count % 6 == 0:
    #         startTime.append(justTimes[i]+""+justTimes[i+1])
    #     count = count + 1
    # count = 0

    # for i in range (2, len(justTimes)):
    #     if count % 6 == 0:
    #         endTime.append(justTimes[i]+""+justTimes[i+1])
    #     count = count + 1

    # # print endTime
    
    # count = 0
    # for i in range (4, len(justTimes)):
    #     if count % 6 == 0:
    #         daysOfWeek.append(justTimes[i])
    #     count = count + 1

    # timeTuples = list(zip(timeID, startTime, endTime, daysOfWeek))
    # print timeTuples

    # PARSING NEW CONSTRAINTS FILE 
    HCconstraints = open("haverford/newConstraints.txt", "r")
    constraints = HCconstraints.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

    constraints = list(filter(None, constraints))
    
    justTimes = []
    for i in range(4, 351):
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

    # print startTime

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
    
    # print daysOfWeek

    timeTuples = list(zip(timeID, startTime, endTime, daysOfWeek))

    f = open("haverford_times.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in range(len(timeTuples)):
        f.write("{}\t{}\t{}\n".format(startTime[i], endTime[i], daysOfWeek[i]))

    for i in timeTuples: 
        f.write("{}\n".format(i))
    f.close()

    justRooms = []
    for i in range(365, 465):
        justRooms.append(constraints[i])
    print justRooms

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

    # print classroomCap

    roomSize = dict(zip(classroomID_fromtxt, classroomCap))

    f = open("haverford_roomSize.txt","w+")
    # f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
    for i in roomSize:
        f.write("{}\t{}\n".format(i, roomSize[i]))
    f.close()

    # HCconstraints.close()


    # PARSING OF OLD CONSTRAINTS FILE
    # HCconstraintsEnd = open("haverford/haverfordConstraints_withZeros.txt", "r")
    # Endconstraints = HCconstraintsEnd.read().replace("\t", " ").replace("\r", " ").replace("\n", " ").split(" ")

    # justClassesAndTeachers = []
    # for i in range(564, len(Endconstraints)):
    #     justClassesAndTeachers.append(Endconstraints[i])
    # # print justClassesAndTeachers

    # classID = []
    # teacherID = []
    # classID_teacherID = {}
    # count = 0 
    # for i in range (len(justClassesAndTeachers)):
    #     if count % 2 == 0:
    #         classID.append(justClassesAndTeachers[i])
    #     count = count + 1; 

    # # print classID

    # count = 0
    # for i in range (1, len(justClassesAndTeachers)):
    #     if count % 2 == 0:
    #         teacherID.append(justClassesAndTeachers[i])
    #     count = count + 1; 

    # # print teacherID

    # # for i in range(len(classID)):
    # #     classID_teacherID.update({classID[i], teacherID[i]})
    
    # classID_teacherID = dict(zip(classID, teacherID))

    # # print classID_teacherID

    # f = open("haverford_classID_teacherID.txt","w+")
    # for i in classID_teacherID:
    #     f.write("{}\t{}\n".format(i, classID_teacherID[i]))
    # f.close()

    # HCconstraintsEnd.close()



    

    # HCstudentprefs = open("haverford/newPrefs.txt", "r")

    # #OLD PARSING FOR PREFERENCES 
    # # HCstudentprefs = open("haverford/haverfordStudentPrefs.txt", "r")
    # studentprefs = HCstudentprefs.read().replace("\t", " ").replace("\r", " ").split('\n')

    # studentprefs.pop(0)

    # studentNumber = []
    # for i in range(len(studentprefs)-1):
    #     temp = studentprefs[i].split(' ', 1)
    #     studentNumber.append(temp[0])

    # preferences = []
    # student_pref = []
    # for i in range(len(studentNumber)):
    #     temp = studentprefs[i].split(' ', 1)
    #     individualPrefs = temp[1].split(" ")
    #     individualPrefs.pop(-1)
    #     student_pref.append(individualPrefs)
    # # print student_pref[0]

    # # studentPreferences = dict(zip(studentNumber, student_pref))
    # preferences.append(individualPrefs)

    # preferencesDict = dict(zip(studentNumber, preferences))

    # f = open("haverford_studentPreferences.txt","w+")
    # for i in studentNumber:
    #     f.write("{}\t{}\n".format(i, preferencesDict[i]))
    # f.close()




    # OLD PARSING 

    # courseID = []
    # subject = []
    # classroomID = []
    
    # new excel file made by Xinyi
    # with open('haverford/haverford-classroom-data.csv') as csvfile:
    #     readHC = csv.reader(csvfile, delimiter = ',')

    #     for row in readHC:
    #         courseID_ = row[0]
    #         subject_ = row[1]
    #         classroomID_ = row[2]

    #         courseID.append(courseID_)
    #         subject.append(subject_)
    #         classroomID.append(classroomID_)

    #     courseID.pop(0)
    #     subject.pop(0)
    #     classroomID.pop(0)

    # print classroomID 
    
    # classSubject = {}
    # for x in range(len(courseID)):
    #     classSubject.update( {courseID[x] : subject[x]} )

    # f = open("haverford_classSubject.txt","w+")
    # for i in classSubject:
    #     f.write("{}\t{}\n".format(i, classSubject[i]))
    # f.close()

    # roomAndSubject = {}
    # for x in range(len(subject)):
    #     roomAndSubject.update( { classroomID[x]: subject[x] } )

    # sortedSubjectClassroom = {}
    # roomOptions = []
    # for x in range(len(subject)):
    #     if subject[x] in sortedSubjectClassroom:
    #         if classroomID[x] not in sortedSubjectClassroom[subject[x]] and is_nan(classroomID[x]) == False:
    #             if tuple((classroomID[x], roomSize[classroomID[x]])) not in sortedSubjectClassroom[subject[x]]:
    #                 # print(classroomID[x], roomSize[classroomID[x]])
    #                 toAppend = tuple((classroomID[x], roomSize[classroomID[x]]))
    #                 sortedSubjectClassroom[subject[x]].append(toAppend)
    #     else:
    #         toAppend = tuple((classroomID[x], roomSize[classroomID[x]])) 
    #         sortedSubjectClassroom.update({subject[x] : [toAppend]})

    # for k in sortedSubjectClassroom:
    #     sortedSubjectClassroom[k].sort(key=lambda tup: tup[1], reverse=True)

    # f = open("haverford_sortedSubjectClassroom.txt","w+")
    # for i in sortedSubjectClassroom:
    #     f.write("{}\t{}\n".format(i, sortedSubjectClassroom[i]))
    # f.close()


    # overview of all arrays created in this function
    """
    **see txt files with [college]_[name of data structure].txt for external version of parsed data

    !!following are from haverfordConstraints file 

    timeID = [] - list of times from 1 - 60
    startTime = [] - list of start times 
    endTime = [] - list of end times 
    daysOfWeek = [] - list of the days the times are scheduled for
    timeTuples = [] - a list of tuples of all this data meshed into one 

    classroomID_fromtxt = [] - list of room names specifically from haverfordConstraints file
    classroomCap = [] - list of room size capacity 
    roomSize = {} - dictionary of roomSizeName:classroomCap

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
    """

    # return professorOfClass, courseID, subject, classroomID, classSubject, timeID, startTime, endTime, daysOfWeek, classroomID_fromtxt, classroomCap, roomSize, classID, teacherID, classID_teacherID, students, preferences, preferencesDict,sortedSubjectClassroom

    return timeID, startTime, endTime, daysOfWeek, timeTupes, classroomID_fromtxt, classroomCap, roomSize, classID, teacherID, classID_teacherID, studentNumber, student_pref, studentPreferences, courseID, subject, classroomID, classSubject, roomAndSubject, sortedSubjectClassroom
