import os
import pandas as pd
import xlrd


DSP2 = open("demo_schedule.txt", "r")
studentInfo = DSP2.read().split(" ")
print(studentInfo)


f= open("our_schedule.txt", "w+")
f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
f.write()