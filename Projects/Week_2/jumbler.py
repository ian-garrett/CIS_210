"""
jumbler.py: CIS 210 assignment 2.1, Winter 2014
author: Ian Garrett, igarrett@uoregon.edu
Credits: Used starting code provided  in the assignment page on the class websight

Takes user input from command-line and runs it through a text document to
find all words that are composed of the charactors entered by the user.
"""
import sys

word = sys.argv[1]
dictionary = sys.argv[2]

possible_matches = []
# opens dictionary
def open_dict(path):
    """Return a file object corresponding to the path"""
    dictionary= open(path)
    return dictionary

# Main Program
dictionary = open_dict(dictionary)
word_count = 0
match_count = 0

# Runs through each line in dictionary
for line in dictionary:
          word_count += 1
          dict_word = line.strip() # Strips each line of blank spaces, allowing it to match given letter combination
          if sorted(dict_word) == sorted(word): # When the loop finds a match, it prints that match
                    print (dict_word)
                    match_count += 1
print (match_count, "matches from", word_count, "words")



        
