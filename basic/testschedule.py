# Import `os` 
import os
# Import pandas
import pandas as pd

import xlrd


DSP2 = open("demo_schedule.txt", "r") # opens file with name of "test.txt"
studentInfo = DSP2.read().split(" ")
print studentInfo


f= open("our_schedule.txt","w+")
f.write("Course\tRoom\tTeacher\tTime\tStudents\n")
f.write()


# Load spreadsheet
# xl = pd.ExcelFile(file)

# Print the sheet names
# print(xl.sheet_names)

# Load a sheet into a DataFrame by name: df1
# df1 = xl.parse('Sheet1')