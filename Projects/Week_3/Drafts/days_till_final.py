
"""
calpr.py: CIS 210 assignment 3, Winter 2014
author: Ian Garrett and Zoe Olson, igarrett@uoregon.edu
Credits: Used starter code from Michal Young as listed on Blackboard.

Returns number of days between two dates given by user inputted months and a days, and a single year.
Does not use Python's build in calendar functions.
"""

import sys  # for exite with a message
import argparse  # Fancier command line parsing
active_months = []


def main():
    
    """
    Main program gets year number from command line, 
    invokes computation, reports result on output. 
    args: none (reads from command line)
    returns: none (write to standard output)
    effects: message or result printed on standard output
    """
    ## The standard way to get arguments from the command line, 
    ##    make sure they are the right type, and print help messages
    parser = argparse.ArgumentParser(description="Compute days from yyyy-mm-dd to next mm-dd.")
    parser.add_argument('year', type=int, help="Start year, between 1800 and 2500")
    parser.add_argument('start_month', type=int, help="Starting month, integer 1..12")
    parser.add_argument('start_day', type=int, help="Starting day, integer 1..31")
    parser.add_argument('end_month', type=int, help="Ending month, integer 1..12")
    parser.add_argument('end_day', type=int, help="Ending day, integer 1..12")
    args = parser.parse_args()  # will get arguments from command line and validate them
    
    year = args.year
    start_month = args.start_month
    start_day = args.start_day
    end_month = args.end_month
    end_day = args.end_day
    
    if not is_valid(year, start_month, start_day):
        sys.exit("Must start on a valid date between 1800 and 2500")
    else:
        print(count_days_main(year, start_month, start_day, end_month, end_day))


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
	if detect_leapyear(year) is True:
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
            return True	#if year is divisible by 4 and 400 it is a leap year
        if year%100!= 0:
            return True	#if year is divisible by 4 and not 100 it is a leap year
    else:
        return False	#all other cases year is not a leap year

# used to count up days between dates when second dates goes into a new year
def count_days_newyear(year, start_month, start_day, end_month, end_day):
    start_day_count = 0 #first day counter
    end_day_count = 0   #day counter for second year
    full_year_count = 0 #total number of days in first year
    final_count = 0 #total days between dates
    active_months = []
    
    if detect_leapyear(year) is True:
        active_months = L_MONTHS  #use leap year list
    else:
        active_months = MONTHS    #otherwise use non leap year list
    
    for i in range (start_month):
        start_day_count += active_months[i]
    start_day_count += start_day
    
    for i in range (13):
        full_year_count += active_months[i]
    start_day_count =(full_year_count) - (start_day_count) # redefines start_day_count to be the days from start_day to end of the year
            
    if detect_leapyear(year+1) is True:
        full_year_count = 0 # if leap year is detected, full_year_count is reset and recalculated in the next for loop
        active_months = L_MONTHS #use leap year list
    
    for i in range(13):
        full_year_count += active_months[i]
    
    for i in range (end_month):
        end_day_count += active_months[i]
    end_day_count += end_day
    
    final_count=(start_day_count) + (end_day_count) # defines final_count as the product
    return final_count

#Counts number of days from first date to second date
def count_days_main(year,start_month, start_day, end_month, end_day):
    start_day_count = 0	#first day counter
    end_day_count = 0	#day counter for second year
    full_year_count = 0	#total number of days in first year
    final_count = 0	#total days between dates
    active_months = []	#tracks the correct list (standard year or leap year)
    
    if detect_leapyear(year) is True:
        active_months = L_MONTHS  #use leap year list
    else:
        active_months = MONTHS    #otherwise use non leap year list
    
    if detect_newyear(start_month, start_day, end_month, end_day) is True: # if a new year is detected between the two dates, call count_days_newyears
        count_days_newyear(year, start_month, end_day, end_month, end_day) # function to calculate days between dates of different years
    else: #Counts days for two dates in the same year if a new year is not detected
        for i in range (start_month):
            start_day_count += active_months[i] #add up days for each month
        start_day_count += start_day  #adds days from partial month
        for i in range (end_month):
            end_day_count += active_months[i] #adds up days to second month
        end_day_count += end_day #adds days from partial second month
        final_count=(end_day_count)-(start_day_count) #finds difference between two day counts
        return final_count

if __name__ == "__main__":
    main()
