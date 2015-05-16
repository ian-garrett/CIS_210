'''
alphacode.py: CIS 210 assignment 1.1, Winter 2014
author: Ian Garrett, igarrett@uoregon.edu

Covert 4-digit PIN to alphabetic code
'''
## Constants used by this program
CONSANANTS = "bcdfghjklmnpqrstvwyz"
VOWELS = "aeiou"

## Get pin code from command line
import sys
if (len(sys.argv) > 1) :
          pincode = int(sys.argv[1])
else :
          print ("Usage: python3 alphacode 9999")
          exit(1)

## These functions split the 4-digit code into 2 2-digit pairs
chunk_1 = pincode%100
new_pincode_1 = pincode//100
chunk_2 = new_pincode_1%100

## These functions assign a vowel and consanant to each of the 2 pairs
consonant1 = CONSANANTS[chunk_2//5]
vowel1 = VOWELS[chunk_2%5]

consonant2 = CONSANANTS [chunk_1//5]
vowel2 = VOWELS[chunk_1%5]

pair1 = (consonant1 + vowel1)
pair2 =(consonant2 + vowel2)

## This final print statement combines the 2 letter pairs and prints the result

print ("Encoding of", pincode, "is", pair1 + pair2)
