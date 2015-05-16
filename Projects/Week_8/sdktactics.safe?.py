"""
Tactics and checks for Sudoku.

sdktactics.py: CIS 211 assignment 8, Winter 2014
Authors: Ian Garrett igarrett@uoregon.edu
Consulted with: Anna, assisted me with structuring my naked_single function

A tactic is a rule that can be used to determine and/or constrain the
possible choices for a Sudoku tile.

A check determines whether a given Sudoku board
(whether complete or incomplete) is legal.  A board is
legal if it contains only digits and open spaces, and
if all of the digits are unique in each row, column,
and 3x3 block.
"""
import sdkboard

# The following variables are private but global to the module
global groups
global progress

def prepare(board):
    """ 
    Prepare for checking and solving a sudoku board.
    Args:
       board:  An sdkboard.Board object
    Returns:
       nothing
    Effects:
       prepared for check(board) and solve(board)
    """
    global groups  # rows, columns, and blocks

    groups = [ ]

    # Rows
    for row in range(9):
        groups.append(board.tiles[row])

    # Columns
    for col in range(9):
        col_tile = [ ]
        for row in range(9):
            col_tile.append(board.tiles[row][col])
        groups.append(col_tile)
        
    # Blocks
    for start_row in [0, 3, 6]:
        for start_col in [0, 3, 6]:
            sq_tiles = [ ] 
            for row in range(3):
                for col in range(3): 
                    t = board.tiles[start_row + row][start_col+col]
                    sq_tiles.append(t)
            groups.append(sq_tiles)
            
    # Communicates progress throughout program
    for row in board.tiles:
        for tile in row:
            tile.register(progress_listener)

        


 
def progress_listener(tile, event):
    """
    An event listener, used to determine whether we have made
    some progress in solving a Sudoku puzzle.  This listener
    will be attached to Sudoku Tile objects, and informed when
    "determined" and "constrained" events occur.
    Args:
       tile:  The tile on which an event occurred
       event: What happened.  The events we listen for are "determined"
         and "constrained"
    Returns:  nothing
    Effects: module-global variable progress may be set to True
    """
    global progress 
    if event == "determined" or event == "constrained":
       progress = True

def good_board(): 
        """Check that every group (row, column, and block)
        contains unique elements (no duplicate digits).
        Args:
           none  (implicit through prepare_board)
        Returns:
           Boolean True iff all groups contain unique elements
        Effects:
           Will announce "duplicate" event on tiles that are
           not unique in a group.
        Requires:
           prepare(board) must be called before good_board
        """
        duplicate_found = False
        for group in groups:
            seen = []
            for tile in group:
                if tile.symbol not in seen:
                    if tile.symbol.isdigit():
                        seen.append(tile.symbol)
                else:
                    tile.announce('duplicate')
                    duplicate_found = True
        if duplicate_found is False:
            return True
        else:
            return False
        
def solve():
    """
    Keep applying naked_single and hidden_single tactics to every
    group (row, column, and block) as long as there is progress.
    Args: 
        none
    Requires:
        prepare(board) must be called once before solve()
        use only if good_board() returns True
    Effects: 
        May modify tiles in the board passed to prepare(board), 
        setting symbols in open tiles, and reducing the possible
        sets in some tiles. 
    """
    global progress
    progress = True
    while(progress):
        progress = False
        for group in groups:
            naked_single(group)
            hidden_single(group)

def naked_single(group):
        """Constrain each tile to not contain any of the digits 
        that have already been used in the group.
        Args: 
            group: a list of 9 tiles in a row, column, or block
        Returns:
            nothing
        Effects:
            For each tile in the group, eliminates "possible" elements
            that match a digit used by another tile in the group.  If 
            this reduces it to one possibility, the selection will be 
            made (Tile.remove_choices does this), and progress may be 
            signaled.
        """
        seen = set()
        # Adds all symbols found in group to set seen
        for tile in group:
            if tile.symbol != sdkboard.OPEN:
                seen.add(tile.symbol)

        # Removes all symbols in set seen from each blank tiles tile.possible
        for tile in group:
            if tile.symbol == sdkboard.OPEN:
                tile.remove_choices(seen)
        return
        
        
def hidden_single(group):
        """Each digit has to go somewhere.  For each digit, 
        see if there is only one place that digit should 
        go.  If there is, put it there. 
        Args: 
           group:  a list of 9 tiles in a row, column, or block
        Returns: 
           nothing
        Effects: 
           For each tile, if it is the only tile that can accept a 
           particular digit (according to its "possible" set), 
        """
        need_placed = ["1","2","3","4","5","6","7","8","9"]

        # Removes symbols found in group from list need_placed
        for tile in group:
            if tile.symbol != sdkboard.OPEN:
                need_placed.remove(tile.symbol)

        # Checks each number from need_placed to see if only one
        # of the nine tiles in group has number in tile.possible
        for number in need_placed:
            last_tile = 0
            possibility_count = 0
            for tile in group:
                if number in tile.possible:
                    last_tile = tile
                    possibility_count += 1
                   
            if possibility_count == 1:
                last_tile.determine(number)
                last_tile.announce("determine")
        return


        
