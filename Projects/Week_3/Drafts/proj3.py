"""
calpr.py: CIS 210 assignment 3, Winter 2014
author: Ian Garrett and Zoe Olson, igarrett@uoregon.edu
Credits:

Returns # of days between two different dates (month, day) in the same year
(without using any of Python's built in functions to simplify the process[wording alright?])
"""

import sys

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


# Inputs used for initial testing (hashtagged to take them out of the program without deleating them)
#year = int(input("Year: "))
#month1 = int(input("m1: "))
#day1 = int(input("d1: "))
#month2 = int(input("m2: "))
#day2 = int(input("d2: "))

month_1 = int(sys.argv[1])
day_1 = int(sys.argv[2])
month_2 = int(sys.argv[3])
day_2 = int(sys.argv[4])
year = int(sys.argv[5])

              

# Detects if two given dates carry into a new year
def detect_newyear(month1, day1, month2, day2):
          if month1 > month2:
                    return True
          if (month1 == month2) and (day1 > day2):
                    return True
          else:
                    False

# test
if detect_newyear(1,2,1,1) is True:
          print ("newyear check")

# Detects leap year
def detect_leapyear(year):
          while year %4==0:
                    if [year%100 ==0 and year%400 == 0] or [year%100 != 0]:
                              return True
# test
if detect_leapyear(2016) is True:
          print ("leapyear check")

#
def newyear_count(month_1, day_1, month_2, day_2):
          for i in range (month_1): # tallies days from January 1st to given date
                    day_count_1 += active_months[i]
          day_count_1 += day_1 # adds remaining days to day_count_1
          for i in range (13):
                    full_year_count += active_months[i]
          day_count_1 = (full_year_count) - (day_count_1) # redefines day_count_1 to add all days from given date to the end of that year
          if detect_leapyear(year+1) is True:
                    full_year_count = 0 # if leap year is detected, full_year_count is reset and recalculated in the next for loop
                    active_months = L_MONTHS
                    for i in range(13):
                              full_year_count += active_months[i]
                    for i in range (month_2):
                              day_count_2 += active_months[i]
                    day_count_2 += day_2 # adds remaining days to day_count_2
                    final_count=day_count_1 + day_count_2
                    return final_count
          
# Counts number of days from first date to second date
def count_days_main(month_1, day_1, month_2, day_2, year):
          day_count_1 = 0
          day_count_2 = 0
          full_year_count = 0
          final_count = 0
          active_months = [] # tracks the correct list (standard year or leap year)
          if detect_leapyear(year) is True:
                    active_months = L_MONTHS
          if detect_leapyear(year) is False:
                    active_months = MONTHS
          if detect_newyear(month_1, day_1, month_2, day_2) == True: # uses different system of calculating days if the year changes [(full year-month_1)+(month)]
                    newyear_count(month_1, day_1, month_2, day_2)
          else:     
                    for i in range (month_1):
                              day_count_1 += MONTHS[i]
                    day_count_1 += day_1
                    print (day_count_1)
                    for i in range (month_2):
                              day_count_2 += MONTHS[i]
                    day_count_2 += day_2
                    final_count=(day_count_2)-(day_count_1)
                    return final_count

print (count_days_main(4,1,3,4,2011)) # testing function outside of command window for greater convenience


# Subtractive Loop to find different in date values
# length_between_days = ((count_days(month2, day2)) - count_days(month1, day1))

# print ("# of days between dates: " + str(length_between_days))



                    
