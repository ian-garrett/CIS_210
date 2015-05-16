"""
days_till.py: CIS 210 assignment 3, Winter 2014
author: Ian Garrett and Zoe Olson, igarrett@uoregon.edu
Credits: Used starter code from Michal Young as listed on Blackboard. 

Returns number of days between two dates given by user inputted months and a days, and a single year.
Does not use Python's build in calendar functions.
"""

import sys
import argparse
 

def main():
    """
    Main program gets year number from command line, 
    invokes computation, reports result on output.
    
    Args: none (reads from command line)

    Returns: none (write to standard output)
    
    Effects: message or result printed on standard output
    """ 
    year = int(sys.argv[1])
    start_month = int(sys.argv[2])
    start_day = int(sys.argv[3])
    end_month = int(sys.argv[4])
    end_day = int(sys.argv[5])
    parser = argparse.ArgumentParser(description="Compute days from yyyy-mm-dd to next mm-dd.")
    parser.add_argument('year', type=int, help="Year must be between 1800 and 2500")
    parser.add_argument('start_month', type=int, help="Starting month must be an integer between 1 and 12")
    parser.add_argument('start_day', type=int, help="Starting day must be an integer between 1 and 31")
    parser.add_argument('end_month', type=int, help="Ending month must be an integer between 1 and 12")
    parser.add_argument('end_day', type=int, help="Ending day must be an integer between 1 and 31")
    args = parser.parse_args()  # will get arguments from command line and validate them
    if not is_valid(year, start_month, start_day): # if components of start date given are not valid
        sys.exit("Must start on a valid date between 1800 and 2500")
    if not is_valid(2000, end_month, end_day): #if components of end date given are not valid
        sys.exit("Ending month and day must be a part of a valid date")
    else:
        print (days_total(year,start_month,start_day,end_month,end_day))

# Lists
MONTHS = [ 0, # No month zero
    31, # 1. January
    28, # 2. February
    31, # 3. March
    30, # 4. April
    31, # 5. May
    30, # 6. June
    31, # 7. July
    31, # 8. August
    30, # 9. September
    31, #10. October
    30, #11. November
    31, #12. December
    ]

L_MONTHS = [ 0, # No month zero
    31, # 1. January
    29, # 2. February
    31, # 3. March
    30, # 4. April
    31, # 5. May
    30, # 6. June
    31, # 7. July
    31, # 8. August
    30, # 9. September
    31, #10. October
    30, #11. November
    31, #12. December
    ]

# Functions
def detect_leapyear(year):
    """
    Checks if year given is a leap year.

    Args:
    *year: integer between 1800 and 2500

    Returns: Boolean value-> True=year is a leapyear, False=year is not a leapyear
    EX-> detect_leapyear(2016) returns True
    EX-> detect_leapyear(2015) returns False
    """
    
    if year%4 == 0: # checks if year is divisible by 4
        if year%400 == 0: 
            return True # if year is divisible by 4 and 400 it is a leap year
        if year%100 != 0: 
            return True # if year is divisible by 4 and not 100 it is a leap year
    else:
        return False    #all other case years are not leap years


def is_valid(year, month, day):
    """
    Checks if date given by user is valid.

    Args:
    *year: integer
    *month: integer (1=January, 6=June)
    *day: integer

    Returns: Boolean value-> True=date is valid, False=date is not valid
    EX-> is_valid(1498, 12, 15)returns False
    EX-> is_valid(2013, 11, 20)returns True
    

    Effects: assigned one of two lists (MONTHS and L_MONTHS) to variable active_months
    """
    
    if detect_leapyear(year):
        active_months = L_MONTHS
    else:
        active_months = MONTHS
    if (1 <= month <= 12) and (1 <= day <= active_months[month]) and (1800 <= year <= 2500):
                return True
    else:
        return False
      

def days_total(year,start_month, start_day, end_month, end_day):
    """
    Calculates the number of days between year/start_month/start_day and end_month/end_day using days_between function.
    This function implements the days_between function differently depending on if the two dates span over a new year.

    Args:
    *years: integer between 1800 and 2500
    *start_month: integer between 1 and 12 (1=January, 6=June)
    *start_day: integer between 1 and (28,29,30,or 31)
    *end_month: integer between 1 and 12 (1=January, 6=June)
    *end_day: integer between 1 and (28,29,30,or 31)

    Returns: integer number of days between two dates
    EX-> days_between(2013 1 1 1 6) returns 5
    """
    total = 0
    if ((start_month == end_month) and (start_day > end_day)) or (start_month > end_month): #if the dates span over a year divider 
        total += days_between(year,start_month,start_day,12,31) # days between start date and end of year
        total += days_between((year+1),1,0,end_month,end_day) # days between begininning of the year and end date (start_day is 0 so all days are counted)
    else:
        total += days_between(year,start_month,start_day,end_month,end_day) # run days_between from start date to end date of the same year
    return total
        

def days_between(year,start_month,start_day,end_month,end_day):
    """
    Calculates the number of days between year/start_month/start_day and end_month/end_day.
    

    Args:
    *years: integer between 1800 and 2500
    *start_month: integer between 1 and 12 (1=January, 6=June)
    *start_day: integer between 1 and (28,29,30, or 31)
    *end_month: integer between 1 and 12 (1=January, 6=June)
    *end_day: integer between 1 and (28,29,30, or 31)

    Returns: integer number of days between two dates
    EX-> days_between(2013 1 1 1 6) returns 5

    Effects: assignes one of two lists (MONTHS and L_MONTHS) to variable active_months
    """
    total = 0
    if detect_leapyear(year)is True: #tests for leap year
        active_months = L_MONTHS # switches months to leapyear months
    else: 
        active_months = MONTHS
    for month in range(start_month, end_month):
        total += active_months[month] # adds up days of full months between start_day and end_day
    total -= start_day # removes days prior to start_day in start_month from total
    total += end_day # adds days from end_month to total
    return total

if __name__ == "__main__":
    main()
