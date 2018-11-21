Major code construct:
    
    - parseTXT(): 
        Parsing the demo/randomly generated data

    - construct(...): 
        construct data parsed by parseTXT()
    
    - parseHC.py: 
        Containing all functions we wrote to parse and process Haverford data
    
    - assignClassToTime(...): 
        assign a class to a schedule, using either demo data or HC data
    
    - calculateStudentsInClass(...): 
        a naive function calculating the optimality of the schedule
    
    - main(): 
        Calls parseTXT(), construct(...), and assignClassToTime(...) to create 
        a schedule from demo/randomly generated data, and calls calculateStudentsInClass(...) 
        to reports the optimality
    
    - mainHC(): 
        Calls functions in parseHC.py and assignClassToTime(...) to create 
        a schedule from demo/randomly generated data, and calls calculateStudentsInClass(...) 
        to reports the optimality
