"""
calpr.py: CIS 210 assignment 2.2, Winter 2014
author: Ian Garrett, igarrett@uoregon.edu
Credits: Used starting code provided  in the assignment page on the class websight

Print the calendar for a month
(without using the Python 'calendar' module).

Limitations: Treats February as always having 28 days. 
"""
import datetime
import sys

month = int(sys.argv[1])
year = int(sys.argv[2])

MONTHLEN = [ 0, # No month zero
	31, # 1. January
	28, # 2. February (ignoring leap years)
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
a_date = datetime.date(year, month, 1)
starts_weekday = a_date.weekday()
starts_weekday = (1 + starts_weekday) % 7

month_day = 1
last_day = MONTHLEN[month]

print(" Su Mo Tu We Th Fr Sa")
# Prints first week
for i in range(7):
                if i < starts_weekday :
                        print("   ", end="")
                else:
                        # Logic for printing one day, moving to next
                        print(format(month_day, "3d"), end="")
                        month_day += 1
print ()

# Prints all full weeks
while month_day <= (((last_day)-7)+1):
          for i in range(7):
                    print(format(month_day, "3d"), end="")
                    month_day += 1
          print ()
# Prints remaining days 
while month_day <= last_day:
        print(format(month_day, "3d"), end="")
        month_day += 1
print ()

          



