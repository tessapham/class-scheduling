final project for CS340 by Elizabeth Chan, Tessa Pham, Xinyi Wang



Structure for ClassScheduling file:
    
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

