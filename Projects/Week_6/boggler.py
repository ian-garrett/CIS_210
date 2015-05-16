"""
  boggler.py: CIS 210 assignment 6, Winter 2014
  author: Ian Garrett igarrett@uoregon.edu

  Program file for running boggler program, which determines the number
  of words contained within a boggler board provided by the user.

  Usage: python3 boggler.py  "board" dict.txt
  where "board" is 16 characters of board, in left-to-right reading
  order and dict.txt can be any file containing a list of words in alphabetical order
    
"""

from boggle_board import BoggleBoard   
import argparse   # Command line processing
import game_dict  # Dictionary of legal game words

def main():
    """
    Main program: 
    Find all words of length 3 or greater on a boggle board. Converts list to
    a set, then back to list, which is then sorted. This eliminates duplicates
    and orders the contents of list results alphabetically
    
    Arguments:
        none (but expect two arguments on command line)
        
    Returns:
        nothing
        
    Effects:
        prints found words in alphabetical order, without duplicates,
        one word per line, then prints the total score
    """
    prefix = ""
    dict_file, board_text = getargs()
    game_dict.read(dict_file)
    board = BoggleBoard(board_text)
    results = [ ]
    for row in range(4):
        for col in range(4):
            find_words(board, row, col, prefix, results)
    final_score = 0
    results = sorted(list(set(results)))
    for word in results:
        final_score += score(word)
        print (word, score(word))
    print ("Total score:", final_score)

        
def getargs():
    """
    Get command line arguments.
    
    Args:
        none (but expects two arguments on program command line)
        
    Returns:
        pair (dictfile, text)
        where dictfile is a file containing dictionary words (the words boggler will look for)
        and   text is 16 characters of text that form a board
        
    Effects:
        also prints meaningful error messages when the command line does not have the right arguments
   """
    parser = argparse.ArgumentParser(description="Find boggle words")
    parser.add_argument('board', type=str, help="A 16 character string to represent 4 rows of 4 letters. Q represents QU.")
    parser.add_argument('dict', type=argparse.FileType('r'),
                        help="A text file containing dictionary words, one word per line.")
    args = parser.parse_args()  # will get arguments from command line and validate them
    text = args.board
    dictfile = args.dict
    if len(text) != 16 :
        print("Board text must be exactly 16 alphabetic characters")
        exit(1)
    return dictfile, text

        
def find_words(board, row, col, prefix, results):
    """
    Find all words starting with prefix that
    can be completed from row,col of board.
    
    Args:
        row:  row of position to continue from (need not be on board)
        col:  col of position to continue from (need not be on board)
        prefix: looking for words that start with this prefix
        results: list of words found so far
        
    Returns: nothing
        (side effect is filling results list)
        
    Effects:
        inserts found words (not necessarily unique) into results
    """
	# FIXME: one base case is that position row,col is not
	#    available (could be off the board, could be currently
	#    in use).  board.py can check that
	# FIXME:  For the remaining cases, where the tile at row,col 
	#    is available, we need to consider the new prefix that 
	#    includes the letter on this tile
	# FIXME:  Another base case is that no word can start with 
	#    the current prefix.  No use searching further on that path.
	# FIXME:  If the current position is a complete word, it is NOT 
	#    a base case, because it might also be part of a longer word. 
	#    We save the word we found into the global results list, and
	#    continue with the recursive case. 
	# FIXME: The recursive case is when the current prefix (including
	#    the tile at row,col) is a possible prefix of a word.  We 
	#    must mark it as currently in use, then search in all 8 directions
	#    around it, and finally mark it as no longer in use. See board.py
	#    for how to mark and unmark tiles, and how to get the text
	#    on the current tile
    if board.available(row,col) == True:
        current = board.get_char(row, col)
        new_prefix = prefix + current
        if (game_dict.search(new_prefix) == game_dict.WORD): # recursive case
            results.append(new_prefix)
        if (game_dict.search(new_prefix) == game_dict.PREFIX) or (game_dict.search(new_prefix) == game_dict.WORD):
            board.mark_taken(row, col)
            find_words(board, row+1, col, new_prefix, results)
            find_words(board, row-1, col, new_prefix, results)
            find_words(board, row, col+1, new_prefix, results)
            find_words(board, row, col-1, new_prefix, results)
            find_words(board, row+1, col-1, new_prefix, results)
            find_words(board, row+1, col+1, new_prefix, results)
            find_words(board, row-1, col+1, new_prefix, results)
            find_words(board, row-1, col-1, new_prefix, results)
            board.unmark_taken(row, col)    

    
def score(word):
    """
    Compute the Boggle score for a word, based on the scoring table
    at http://en.wikipedia.org/wiki/Boggle.

    Args:
        word: string, word taken from results list
        
    Returns:
        score: integer, determined by number of letters in word
     """
    score_count = 0
    if (len(word) == 3) or (len(word) == 4):
        score_count = 1
    if len(word) == 5:
        score_count = 2
    if len(word) == 6:
        score_count = 3
    if len(word) == 7:
        score_count = 5
    if len(word) >= 8:
        score_count = 11
    return score_count


if __name__ == "__main__":
    main()
    input("Press enter to end")

