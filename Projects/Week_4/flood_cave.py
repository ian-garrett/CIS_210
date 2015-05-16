"""
flood_cave.py: CIS 210 assignment 4, Winter 2014
author: Ian Garrett igarrett@uoregon.edu
Credits: Used starter code from Michal Young as listed on Blackboard. 

Determines the number of distinct chambers in a grid representation of 
a cavern by flood-filling each discovered air pocket. 

Usage: python3 cavern.py cave.txt

Requires grid.py, graphics.py  (for displaying cavern as grid of cells)
"""

import sys
import grid

sys.setrecursionlimit(10000) # Max cavern size 100 x 100 = 10,000 cells

# Symbols to represent what is in a particular cell of the cavern.
AIR = " "
STONE = "#"
WATER = "~"

def read_cave( path ):
    """Read a cave description from file at path.
    
    Args: 
        path:  file name path for cave description, e.g., 
               "/Users/bart/caves/cave1.txt" or "c:\caves\cave1.txt"
               or "cave1.txt" if the cave is in the current directory.
    Returns:  
        the cavern as a matrix (list of lists) of strings. 
    """
    file = open(path)
    cave_open = False
    for line in file:
        fields = line.split()
        command = fields[0]
        if command == "cave" :
            validate(len(fields) == 3, "Syntax 'cave rows cols'", line)
            nrows = int(fields[1])
            ncols = int(fields[2])
            validate(nrows > 0, "Rows should be a positive integer", line)
            validate(ncols > 0, "Columns should be a positive integer", line)
            cave = new_cave(nrows, ncols)
            cave_open = True
        elif command == "hwall" :
            validate(cave_open, "First line should be 'cave rows cols'", line)
            validate(len(fields) == 4, "Syntax 'hwall startrow startcol length'", line)
            validate(cave_open, "cave command must precede hwall command", line)
            start_row = int(fields[1])
            start_col = int(fields[2])
            length = int(fields[3])
            validate(start_row >= 0, "Start row must be integer, zero or greater", line)
            validate(start_col >= 0, "Start column must be integer, zero or greater", line)
            validate(length >= 1, "Length of wall must be integer, at least 1", line)
            validate(start_col + length <= ncols, "Wall cannot extend beyond right edge", line)
            hwall(cave, start_row, start_col, length)
        elif command == "vwall" :
            validate(cave_open, "First line should be 'cave rows cols'", line)
            validate(len(fields) == 4, "Syntax 'vwall startrow startcol length'", line)
            validate(cave_open, "cave command must precede vwall command", line)
            start_row = int(fields[1])
            start_col = int(fields[2])
            length = int(fields[3])
            validate(start_row >= 0, "Start row must be integer, zero or greater", line)
            validate(start_col >= 0, "Start column must be integer, zero or greater", line)
            validate(length >= 1, "Length of wall must be integer, at least 1", line)
            validate(start_row + length <= nrows, "Wall cannot extend through floor", line)
            vwall(cave, start_row, start_col, length)
        else:
            print("**Command not understood: ", line)
    return cave


def validate(condition, msg, line):
    """If condition (boolean value) is not true, give the error message and the
    line that violates the condition, and exit the program.
    (Otherwise no effect)
    
    Args: 
        condition:  A boolean value (typically written as an expression, e.g., "x > 12")
        msg:  Message to user if the condition is not true
        line:  An input line to display to the user to show where the error occurred
    Returns:
        Nothing if the condition is true.  If the condition is false, this 
        function also doesn't return because it stops the program. 
    """
    if condition:
        return
    print("*** Invalid command line:", msg)
    print("*** in line: ", line)
    exit(1)


def new_cave(nrows, ncols):
    """Create and return a new cave with
    nrows rows and ncols columns, initially filled
    entirely with air.
    
    Args: 
        nrows:  How many rows of cells in this cavern?  
                At most 50 recommended for reasonable performance. 
        ncols:  How many columns of cells in this cavern? 
                At most 50 recommended for reasonable performance. 
                
    Returns:  A matrix of cells in the form of a list of 
        nrows lists of ncols cells.  Each cell is represented as a 
        one-character string. 
    """
    cave = [ ]
    for row in range(nrows):
        newRow = [ ]
        cave.append(newRow)
        for col in range(ncols):
            newRow.append(AIR)
    return cave

def hwall(cave,row,col,length):
    """Build a horizontal wall of stone starting from (row,col) and
    extending length cells to the right.
    
    Example: hwall(cave,3,3,2) sets cells (3,3) and (3,4) of cave to STONE
    
    Args: 
        cave:  A matrix (list of lists) representing the cavern
        row:   Row in which the new wall will be built
        col:   Beginning column of the new wall
        length:   The new wall starts at (row, col) and extends length
               cells to (row, col + length - 1)
    """
    for i in range(length):
        cave[row][col+i] = STONE

def vwall(cave,row,col,length):
    """Build a vertical wall of stone starting from (row,col) and
    extending length cells down.
    
    Args: 
        cave:  A matrix (list of lists) representing the cavern
        row:   Beginning row of the new wall
        col:   Column in which the new wall will be built
        length:   The new wall starts at (row, col) and extends length
               cells to (row + length - 1, col)
    Returns: nothing
    """
    for i in range(length):
        cave[row+i][col] = STONE
    
def display(cave):
    """Create a graphical representation of cave using the grid.
    This graphical representation can be further manipulated
    (e.g., filling cave cells with water of various colors)
    using the fill_cell method of module grid.
    
    Args: 
        cave: A matrix (list of lists) representing the cavern
    Returns: 
        Nothing, but has the side effect of creating a graphical 
        grid representation of the cavern in a 500x500 pixel window. 
    """
    nrows = len(cave)
    ncols = len(cave[0])
    grid.make(nrows, ncols, 500, 500)
    for row in range(nrows):
        for col in range(ncols):
            if cave[row][col] == STONE :
                grid.fill_cell(row, col, grid.black)

def fill(cave, row, col, color):
    """Fill a chamber of the cave with water, starting
    at row, col. Water can spread in all four cardinal
    directions, but cannot penetrate stone.  No effect
    if row or col are not inside the cave.
    
    Attempting to pour water where there is already WATER or STONE
    has no effect.  Attempting to pour water outside the cavern has
    no effect.  Attempting to pour water in a cell containing AIR 
    not only places colored water in that cell, but also spreads it
    in all directions by causing it to be poured in the cell to the 
    left and right and above and below. 
    
    Args: 
        cave: A matrix (list of lists) representing the cavern. Each 
            cell in the cave may hold AIR, STONE, or WATER.
        row: Starting row of the grid cell where we pour water
        col: Starting column of the grid cell where we pour water
        color: color of the water we try to pour in.
    Returns:
        Boolean value, False value until full cave is filled with recursion function
        at which point True is assigned (used to count chambers)
    """
    if row > (len(cave)-1) or col > (len(cave[0])-1) or row < 0 or col < 0:
        return False
        
    if cave[row][col] == AIR: 
        cave[row][col] = WATER ## labels square as WATER
        grid.fill_cell(row, col, color)
        fill(cave,row,col+1,color) # 4 fill functions, one of each direction 1 square
        fill(cave,row+1,col,color)
        fill(cave,row,col-1,color)
        fill(cave,row-1,col,color)
        return True
    
def main():
    """Reads a cave from a specified configuration file, 
    displays it, and fills each chamber with a different color
    of water.
    
    Args (from command line):
        Cave description file, example, "cave.txt"
        
    Usage: python3 cavern.py cave.txt
    """
    desc = sys.argv[1]
    cave = read_cave(desc)
    display(cave)
    chamber_count = 0
    for row in range( len(cave)) :
        for col in range( len(cave[0])):
            color = grid.get_cur_color()
            if fill(cave, row, col, color) is True: # each time a chamber is filled
                 chamber_count += 1
            grid.get_next_color()
    print(chamber_count,"chambers in cavern")
    input("Press enter to close display")

main()
