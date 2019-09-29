This is a proposed solution to the class scheduling problem of Bryn Mawr and Haverford Colleges, created by **Xinyi Wang**, **Elizabeth Chan**, and **Tessa Pham** with a **0.8** optimality.

Code construction:

``` 
- parseTXT(): 
    Parses the demo and randomly-generated data.

- construct(...): 
    Constructs data parsed by parseTXT().

- parseHC.py: 
    Contains all functions we wrote to parse and processes Haverford data.

- assignClassToTime(...): 
    Assigns a class to a schedule, using either demo data or Haverford data.

- calculateStudentsInClass(...): 
    A naive function for calculating the optimality of the schedule.

- main(): 
    Calls parseTXT(), construct(...), and assignClassToTime(...) to create a schedule from
    demo and randomly-generated data, then calls calculateStudentsInClass(...) to report the optimality.

- mainHC(): 
    Calls functions in parseHC.py and assignClassToTime(...) to create a schedule from
    demo and randomly-generated data, then calls calculateStudentsInClass(...) to report the optimality.
```
