
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
    else:
        print (count_days_main(year, start_month, start_day, end_month, end_day))


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

#Do the dates given fall between the years 1800 and 2500, and are they valid dates?
def is_valid(year, start_month, start_day):
    if detect_leapyear(year):
        active_months = L_MONTHS
    else:
        active_months = MONTHS
    if start_day <= active_months[start_month] and 1800 <= year <= 2500:
        return True 
    else:
        return False    

#Checks if the two dates span through a new year?
def detect_newyear(start_month, start_day, end_month, end_day):
    if start_month > end_month:  
        return True
    if (start_month == end_month) and (start_day > end_day):
        return True
    return False

#Detects leap year
def detect_leapyear(year): 
    if year%4 == 0: #checks if year is divisible by 4
        if year%400 == 0: 
            return True #if year is divisible by 4 and 400 it is a leap year
        if year%100 != 0: 
            return True #if year is divisible by 4 and not 100 it is a leap year
        #all other cases year is not a leap year
    else:
        return False

#Counts number of days from first date to second date
def count_days_main(year,start_month, start_day, end_month, end_day):
    day_count_1 = 0   #first day counter
    day_count_2 = 0   #day counter for second year
    full_year_count = 0   #total number of days in first year
    final_count = 0   #total days between dates
    active_months = []    #tracks the correct list (standard year or leap year)
    if detect_leapyear(year) is True:
        active_months = L_MONTHS  #use leap year list
    else:
        active_months = MONTHS    #otherwise use non leap year list
    if detect_newyear(start_month, start_day, end_month, end_day) is True: 
      #uses different system of calculating days if the year changes [full year-start_month+month]
        for i in range (start_month):
            day_count_1 += active_months[i]
        day_count_1 += start_day
        for i in range (13):
            full_year_count += active_months[i] #adds up days in the year
        day_count_1 = full_year_count - day_count_1  #days to count in first year
        if detect_leapyear(year+1) is True:  #is second year a leap year?
            active_months = L_MONTHS
        else:
            active_months = MONTHS
        for i in range (end_month):
            day_count_2 += active_months[i] #days to count in second year
        day_count_2 += end_day
        final_count = day_count_1 + day_count_2 #add days in both years
        return final_count
    else:
        #counts days for two dates in the same year
        for i in range (start_month):
            day_count_1 += active_months[i] #add up days for each month
        day_count_1 += start_day  #adds days from partial month
        for i in range (end_month):
            day_count_2 += active_months[i] #adds up days to second month
        day_count_2 += end_day #adds days from partial second month
        final_count=(day_count_2)-(day_count_1) #finds difference between two day counts
        return final_count

if __name__ == "__main__":
    main()
