#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: Xinyi Wang, Elizabeth Chan, Tessa Pham
"""

import time
import ClassSchedulingEx234
import ClassSchedulingEx1

if __name__ == "__main__":
    print("Basic mode on Demo/Randomly generated input without extension:")
    start=time.time()
    ClassSchedulingEx234.main()
    print("The time is", time.time()-start, "seconds. ")
    print("\n")
    
    print("Basic mode using HC data.")
    start=time.time()
    ClassSchedulingEx234.mainHC(overlapTimeMode =False, relationMode = False, subjectClassroomMode=False)
    print("The time is", time.time()-start, "seconds.")
    print("\n")
    
    print("HC data with overlapTime and relation extension on.")
    start=time.time()
    ClassSchedulingEx234.mainHC(overlapTimeMode =True, relationMode = True, subjectClassroomMode=False)
    print("The time is", time.time()-start, "seconds.")
    print("\n")
    
    print("HC data with subjectClassroom extension on.")
    start=time.time()
    ClassSchedulingEx234.mainHC(overlapTimeMode =False, relationMode = False, subjectClassroomMode=True)
    print("The time is", time.time()-start, "seconds.")
    print("\n")
    
    
    print("HC data with ClassLevel extension on.")
    start=time.time()
    ClassSchedulingEx1.mainHC(classLevelMode=True, overlapTimeMode =False, relationMode = False, subjectClassroomMode=True)
    print("The time is", time.time()-start, "seconds.")