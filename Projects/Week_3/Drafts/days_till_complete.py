
"""
calpr.py: CIS 210 assignment 3, Winter 2014
author: Ian Garrett and Zoe Olson, igarrett@uoregon.edu
Credits: Used starter code from Michal Young as listed on Blackboard. 

Returns number of days between two dates given by user inputted months and a days, and a single year.
Does not use Python's build in calendar functions.
"""

import sys  # for exite with a message
import argparse  # Fancier command line parsing
 

def main():
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
    parser.add_argument('end_day', type=int, help="Ending day must be an integer between 1 and 12")
    args = parser.parse_args()  # will get arguments from command line and validate them
    if not is_valid(year, start_month, start_day):
        sys.exit("Must start on a valid date between 1800 and 2500")
    if not is_valid(2000, end_month, end_day):
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



#Detects leap year
def detect_leapyear(year):
    """Checks if year given is a leap year

    Year given is checked for a leap year by checking divisibility of the 4 digit year
    by 4, 100, and 400.

    Args:
    *years

    Returns Boolean Value"""
    
    if year%4 == 0: #checks if year is divisible by 4
        if year%400 == 0: 
            return True #if year is divisible by 4 and 400 it is a leap year
        if year%100 != 0: 
            return True #if year is divisible by 4 and not 100 it is a leap year
    return False    #all other cases year is not a leap year


#Do the dates given fall between the years 1800 and 2500, and are they valid dates?

def is_valid(year, start_month, start_day):
    """Checks if date given by user is valid

    Before checking date, one of two lists, normal and leap year,is assigned to
    the variable active_months. This ensures that dates given for checking are
    treated appropriately (feb. 29 accepted as start date in leap year)

    The month and day are checked for both start/end_month and start/end_day:

    Args:
    *years
    *start_month
    *start_day

    Returns Boolean Value"""
    
    if detect_leapyear(year):
        active_months = L_MONTHS
    else:
        active_months = MONTHS
    if 1 <= start_month <= 12:
        pass
        if 1 <= start_day <= active_months[start_month]:
            pass
            if 1800 <= year <= 2500:
                return True
    else:
        return False
      

#Checks if the two dates span through a new year
def days_total(year,start_month, start_day, end_month, end_day):
    """Calculates the number of days between year/start_month/start_day and end_month/end_day using days_between function.
    This function implements the days_between function differently depending on if the two dates span over a new year.

    If both of the conditions for the first if statement are true(indicating that the two given dates span over
    a year), then the date is calculated by totaling the number of days between the start_month/start_day and the
    end of that year and adding that to the number of days between the start of the following year and end_month/end_day.
    If the conditions are not met, then the function simply counts the number of days between year/start_month/start_day
    and end_month/end_day.

    Args:
    *years
    *start_month
    *start_day
    *end_month
    *end_day

    Returns integer"""
    total = 0
    if start_month > end_month or ((start_month == end_month) and (start_day > end_day)): #if the dates span over a year divider 
        total += days_between(year,start_month,start_day,12,31) #days between start date and end of year
        total += days_between((year+1),1,1,end_month,end_day) #days between begininning of the year and end date
    else:
        total += days_between(year,start_month,start_day,end_month,end_day)
    return total
        

#Adds up 
def days_between(year,start_month,start_day,end_month,end_day):
    """Calculates the number of days between year/start_month/start_day and end_month/end_day.

    Function first checks for if year given is a leap year, and responds by assigning list L_MONTHS to active_months if it is. If
    year is not a leap year, then list MONTHS is assigned to active_months. After this assignment, the days in the full months
    are added up, followed by the remainding days in end_month.
    

    Args:
    *years
    *start_month
    *start_day
    *end_month
    *end_day

    Returns integer"""
    total = 0
    if detect_leapyear(year): #tests for leap year
        active_months = L_MONTHS # switches months to leapyear months
        days_total(year,start_month,start_day,end_month,end_day)# uses days_total function to add up days between dates
    else: 
        active_months = MONTHS
        total += (active_months[start_month] - start_day) + end_day # adds up days remaining in the last month
    for month in range (start_month+1,end_month):
        total += active_months[month] # adds up days of full months between two days
    return total

if __name__ == "__main__":
    main()
