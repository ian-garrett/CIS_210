"""
  game_dict.py: CIS 210 assignment 6, Winter 2014
  author: Ian Garrett igarrett@uoregon.edu

  Differs from a spelling dictionary in that looking up a string
  has three possible outcomes:  The string matches a word exactly,
  or it does not match exactly but is a prefix of a word, or there is
  no word starting with that string.
    
"""

dictionary = [ ]  

# Codes for result of search
WORD = 1
PREFIX = 2
NO_MATCH = 0

def read(file, min_length=3 ):
    """
    Read the dictionary from a sorted list of words.

    Args:
        file: dictionary file (already open)
        min_length: integer, minimum length of words to
            include in dictionary. Useful for games in
            which short words don't count.  For example,
            in Boggle the limit is usually 3, but in
            some variations of Boggle only words of 4 or
            more letters count.
            
    Returns:  nothing    
    """
    global dictionary
    dictionary = [ ] 
    for line in file:
        new_line = line.strip()
        if len(new_line) >= min_length and (new_line.isalpha()):
            dictionary.append(new_line)
    #FIXME: read the dictionary file into dict.  Skip words that
    #   are too short or contain non-alphabetic characters
    dictionary = sorted(dictionary)  # Being sorted is most important for binary search
            
def search(string):
    """
    Search for a prefix string in the dictionary.

    Args:
        string:  A string to look for in the dictionary

    Returns:
        code WORD if string exactly matches a word in the dictionary,
        PREFIX if string does not match a word exactly but is a prefix
        of a word in the dictionary, or NO_MATCH if string is not a prefix
        of any word in the dictionary
    """
    global dictionary
    for entry in dictionary:
        if string == entry:
            return WORD
        if entry.startswith(string):
            return PREFIX
    return NO_MATCH
    # FIXME: I suggest using a linear search first, checking for exact matches
    # with == and then for partial matches with the "startswith" function, e.g.,
    # dict[i].startswith(str). 
    # Once you get the whole program working, you can make it much, much faster
    # using a binary search (which we will discuss in class). 
    
    
######################################################
#  Test driver
#    for testing game_dict.py by itself,
#    separate from boggler.py
#   Note we will need shortdict.txt and dict.txt for
#    testing.  Using the module does not require those files,
#    but this suite of test cases requires exactly those files
#    with exactly those names. 
#   
#
#   To test your game_dict module, invoke it on the
#   command line:
#      python3  game_dict.py    (in MacOS), or
#      python  game_dict.py     (in Windows)
#
#######################################################


if __name__ == "__main__":
    # This code executes only if we execute game_dict.py by itself,
    # not if we import it into boggler.py
    from test_harness import testEQ
    read(open("shortdict.txt"))
    # shortdict contains "alpha", "beta","delta", "gamma", "omega"
    testEQ("First word in dictionary (alpha)", search("alpha"), WORD)
    testEQ("Last word in dictionary (omega)", search("omega"), WORD)
    testEQ("Within dictionary (beta)", search("beta"), WORD)
    testEQ("Within dictionary (delta)", search("delta"), WORD)
    testEQ("Within dictionary (gamma)", search("gamma"), WORD)
    testEQ("Prefix of first word (al)", search("al"), PREFIX)
    testEQ("Prefix of last word (om)", search("om"), PREFIX)
    testEQ("Prefix of interior word (bet)", search("bet"),PREFIX)
    testEQ("Prefix of interior word (gam)", search("gam"),PREFIX)
    testEQ("Prefix of interior word (del)", search("del"),PREFIX)
    testEQ("Before any word (aardvark)", search("aardvark"), NO_MATCH)
    testEQ("After all words (zephyr)", search("zephyr"), NO_MATCH)
    testEQ("Interior non-word (axe)", search("axe"), NO_MATCH)
    testEQ("Interior non-word (carrot)", search("carrot"), NO_MATCH)
    testEQ("Interior non-word (hagiography)",
        search("hagiography"), NO_MATCH)
    # Try again with only words of length at least 5
    # Now beta should be absent
    read(open("shortdict.txt"), min_length=5)
    print("New dictionary: ", dictionary)
    testEQ("First word in dictionary (alpha)", search("alpha"), WORD)
    testEQ("Last word in dictionary (omega)", search("omega"), WORD)
    testEQ("Short word omitted (beta)", search("beta"), NO_MATCH)
    read(open("dict.txt"))  # Long dictioanry
    testEQ("Can I find farm in long dictonary?", search("farm"), WORD)
    testEQ("Can I find bead in long dictionary?", search("bead"), WORD)
    
    
