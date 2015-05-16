"""
Boggle board, a 4x4 matrix of tiles
where each tile represents a character
(except "qu" is a single tile).  In addition
to the character(s), each tile can be in
available or not.

Michal Young, 26 Oct 2012 for CIS 210 at U. Oregon
    Revised Feb 2013, introducing class

"""
import grid

class BoggleBoard(object): 

    # global content   # Character(s) on tiles
    # global in_use   # Whether each tile is currently marked as in use

   def __init__(self,  tiles):
       """
       Create a boggle board from a string of 16 characters.
       Args:
        self:  the board (to be initialized)
        tiles: A string of exactly 16 characters, each
               representing one tile.  Most characters
               represent a tile containing that character,
               but 'q' represents the pair 'qu' on a tile.
        Returns:  Nothing.  The board is encapsulated in this module.
        """
       assert(len(tiles) == 16)
       self.content = [ ]
       self.in_use = [ ]
       grid.make(4,4,500,500)
       for row in range(4):
           self.content.append([ ])
           self.in_use.append([ ])
           for col in range(4):
               char = tiles[4*row + col]
               if char == "q" :
                   char = "qu"
               self.content[row].append(char)
               self.in_use[row].append( False )
               grid.fill_cell(row,col,grid.white)
               grid.label_cell(row,col,char)

   def get_char(self, row, col):
       """
       Returns the character at (row,col)
       Args:
           self: this board
           row: row of board, 0..3
           col: col of board, 0..3
       Returns:
           the string labeling the tile at board[row,col]
       """
       assert row >= 0 and row < len(self.content)
       assert col >= 0 and col < len(self.content[0])
       assert not self.in_use[row][col] 
       return self.content[row][col]

   def available(self, row, col):
       """Check whether we can take a tile at row, col.
       Args:
          self: this board
          row: row of board (may be outside board)
          col: col of board (may be outside board)
       Returns:
           boolean True iff (row,col) is a tile position on
           the board and that tile is not currently marked as
           in use.
       """
       if row < 0 or row >= len(self.content):
           return False
       if col < 0 or col >= len(self.content[0]):
           return False
       return not self.in_use[row][col]

   def mark_taken(self, row, col):
       """
       Marks the tile at row,col as currently in use
       Args:
          self: this board
          row: row of board, 0..3
          col: col of board, 0..3
       Returns:
          nothing
       """
       assert row >= 0 and row < len(self.content)
       assert col >= 0 and col < len(self.content[0])
       assert not self.in_use[row][col] 
       self.in_use[row][col] = True
       grid.fill_cell(row,col,grid.green)
       grid.label_cell(row,col,self.content[row][col])

   def unmark_taken(self, row, col):
       """
       Marks the tile at row,col as no longer in use. 
       Tile at row,col must be in use when this function is called.
       Args:
          self: this board
          row: row of board, 0..3
          col: col of board, 0..3
       Returns:
          nothing
       """
       assert row >= 0 and row < len(self.content)
       assert col >= 0 and col < len(self.content[0])
       assert self.in_use[row][col] 
       self.in_use[row][col] = False
       grid.fill_cell(row,col,grid.white)
       grid.label_cell(row,col,self.content[row][col])


   def dump(self):
       """For debugging: Print representation of board
          Args: 
            self:  this board       
          Returns: nothing
       """
       print(self.content)

   def __str__(self):
       """For debugging: Return string representation of board.
          The __str__ method is called implicitly when the board is 
          printed or when it is coerced into a string. 
          
          Args: 
            self:  this board
       """
       rep = ""
       for row in self.content :
           rep += "".join( row ) + "\n"
       return rep
    

    



    
