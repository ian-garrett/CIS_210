''''
 passwdcheck.py: CIS 210 assignment 1.2, Winter 2014
 authors: Ian Garrett, igarrett@uoregon.edu
 
 Check that password is 8-32 contains required elements:
  Upper case letters
  Lower case letters
  Digits
 '''
## Get password from command line
import sys
if (len(sys.argv) > 1) :
          passwd = (sys.argv[1])
else :
          print("Usage: python3 passwdcheck.py 9999")
          exit(1) ## Quit the program right here, indicating a problem

## Variables for keeping track of criteria for password
digit = False
upper = False
lower = False
length = False

## This for loop goes through and saves password criteria met
for character in passwd :
          if (character.islower()):
                    lower = True
          if (character.isupper()) :
                    upper = True
          if (character.isdigit()) :
                    digit = True

## These if statements use the end value of the criteria variables to decide what response(s) to give to the user

if ((len(passwd)) < 6) :
          print ("Password must be at least 6 charactors long")      
if not lower :
          print ("Password must include lower case letters")
if not upper :
          print ("Password must include upper case letters")
if not digit :
          print ("Password must include digits")
if lower and upper and digit and (len(passwd)>=6)  :
          print ("Good password")



                    
          
