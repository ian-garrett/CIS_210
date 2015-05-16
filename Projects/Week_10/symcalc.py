"""
symcalc.py: CIS 210 assignment 10, Winter 2014
author: Ian Garrett igarrett@uoregon.edu

Reads input in postfix format from standard input
Normally builds expression tree; # means evaluate the top item
   
"""

import argparse  # Command line parsing
import re        ## Regular expression pattern matching, for user input
import sys      # For reading from sys.stdin (keyboard or redirected file)

class Expr(object):
    """Arithmetic expression node.  This serves as the "supertype" of 
       all the expression node types (binary operators, variables, 
       constants.
       
       The methods in this class are stubs.  They should be overridden in any 
       'concrete' subclass, i.e., in any subclass for which we want to make 
       actual objects.  If they are not overridden, an exception will be raised.
    """

    def __init__(self):
        raise NotImplementedError("Expr is just a base class, and should not be instantiated")

    def eval(self):
        """
        Each subclass of Expr should provide an 'eval' method that evaluates the expression
        as far as possible and returns the resulting expression.  If the expression is already
        evaluated as far as possible (e.g., because it is or contains a variable), then eval
        can just return self. 
        
        Args: 
            none (just self)
        Returns:
            an evaluated version of expression.  
            For example, eval( PlusExpr(ConstExpr(3),ConstExpr(4))
            should return ConstExpr(7)
        """
        raise NotImplementedError("eval method missing in Expr subclass")

    def __str__(self):
        """
        The __str__ method of each expression type should produce an infix representation
        of the expression. 
        """
        raise NotImplementedError("__str__ method not overridden in Expr subclass")

class ConstExpr(Expr):
    """
    A ConstExpr (constant expression) is a leaf of the tree.  It has no children, and
    prints simply as itself. 
    """
    def __init__(self, val):
        self.val = val

    def eval(self):
        """The evaluated version of a constant is itself"""
        return self

    def __str__(self):
        """Constant expressions are represented by their values"""
        return str(self.val) # this pulls the string contained within the object to be worked with

class VarExpr(Expr):
    """
    A variable acts almost like a constant, but is treated differently in evaluation.
    """
    def __init__(self, name):
        self.val = None
        self.name = name

    def set(self, value):
        """
        Give the variable a numeric value.  Henceforth the 'eval' method will return
        that value instead of the variable name.
        Args:
           value:  a ConstExpr
        Returns:
           nothing  (just changes the object state)
        """
        if not (isinstance(value, ConstExpr)):
            raise TypeError("Cannot set " + self.name + " to non-constant value " + str(value))
        self.val = value

    def eval(self):
        """
        A variable evaluates to its value if available, otherwise to itself
        """
        if self.val:         ## None is also considered False in Python
            return self.val
        else:
            return self

    def __str__(self):
        """Variables are represented by their names"""
        return self.name

class BinOpExpr(Expr):
    """
    A 'binary' operator is an operation like addition or subtraction 
    that has two operands, like BinOpExpr( ConstExpr(5), VarExpr('x') )
    to represent 5+x.  Binary operator expressions may evaluate to simpler
    expressions.  For example, 
       BinOpExpr( ConstExpr(5), ConstExpr(3)).eval() 
    returns
       ConstExpr(8)
       
    Each subclass of BinOpExpr should override the apply_op method.
    """

    def __init__(self, opsym, left, right):
        self.opsym = opsym
        self.left = left
        self.right = right

    def eval(self):
        """
        Evaluate a binary expression as far as possible.  This will sometimes
        be a 'partial' evaluation, e.g., (3+7)+x evaluates to 10+x, while 
        (3+7)+5 evaluates to 15.
        Args: none
        Returns:  An Expr node that is the (partial or full) evaluation fo this node
        """
        self.left = self.left.eval()
        self.right = self.right.eval()
        if isinstance(self.left, ConstExpr) and isinstance(self.right, ConstExpr):
            result = self.apply_op()
            # print(self, "=>", result)
            return result
        else:
        	return self

    def __str__(self):
        """String representation is fully parenthesized infix, e.g., ((3+7)+4)"""
        return "(" + str(self.left) + str(self.opsym) + str(self.right) + ")"

class AddOpExpr(BinOpExpr):
    """
    Tree representation of the '+' operation. 
    Fills in the apply_op operation, otherwise inherits from BinOpExpr.
    """
    def apply_op(self):
        """Addition of constants."""
        return ConstExpr(self.left.val + self.right.val)

class MulOpExpr(BinOpExpr):
    """
    Tree representation of the '*' operation.
    Fills in the apply_op operation, otherwise inherits from BinOpExpr.
    """
    def apply_op(self):
        """Multiplication of constants"""
        return ConstExpr(self.left.val * self.right.val)
        
class DivOpExpr(BinOpExpr):
    """
    Tree representation of the '/' operation.
    Fills in the apply_op operation, otherwise inherits from BinOpExpr.
    """
    def apply_op(self):
        """Division of constants"""
        return ConstExpr(self.left.val / self.right.val)

class SubOpExpr(BinOpExpr):
	"""
	Tree representation of the '-' operation.
	Fills in the apply_op operation, otherwise inherits from BinOpExpr.
	"""
	def apply_op(self):
		"""Subtraction of constants"""
		return ConstExpr(self.left.val - self.right.val)

#################################################################################
# What follows is the interpreter that reads from the standard input
# (usually the keyboard) and interprets it, including pushing and 
# popping items on the stack.  You do not need to make changes below 
# here,  but you might be interested in seeing how simple a postfix interpreter
# is.  Pattern matching is done with 'regular expressions', a powerful
# facility which, although easy to write, are unfortunately
# difficult to read. 
#################################################################################

def interpret(inp):
    """Read and interpret each line of input.
    Args:
       inp:  The input file (which might be the keyboard)
    Returns:
       nothing
    Effects:
       Interactive loop - displays calculator stack after
       each line of input.  Exits when the "quit" token is
       encountered, or at end of file.
    """
    FLOATPAT = re.compile(r"""\-?\d+\.\d*$""")  ### Float number, e.g., 42.9
    INTPAT = re.compile(r"""\-?\d+$""")         ### Integer with optional sign
    VARPAT = re.compile(r"""[a-zA-Z]+[a-zA-Z0-9_]*$""") ### Variable names 

    stack = [ ] ## Calculator stack
    environment = dict()  ## variables names -> unique VarExpr objects
    for line in inp:
        try:
            for token in line.strip().split():

                if token == "#" : 
                    ### Evaluates an expression to a number if possible
                    stack.append(stack.pop().eval())

                elif token == "cl" : 
                    ### Clears the stack
                    stack = [ ] 

                elif token == "^" : 
                    ### Takes off the one item from the stack
                    stack.pop()

                elif token == "quit":
                    print("Thank you for your patience.  Sorry for any bugs.")
                    exit(0)
                    
                elif token == "+":
                	### Adds together the two elements if possible
                    right = stack.pop()
                    left = stack.pop()
                    stack.append( AddOpExpr(token, left, right) )

                elif token == "*":
                	### Multiplies together the two elements if possible
                    right = stack.pop()
                    left = stack.pop()
                    stack.append( MulOpExpr(token, left, right) )

                elif token == "-":
                	### Subtracks  the two elements if possible
                    right = stack.pop()
                    left = stack.pop()
                    stack.append( SubOpExpr(token, left, right) )
                
                elif token == "/":
                	### Divides the two elements if possible
                    right = stack.pop()
                    left = stack.pop()
                    stack.append( DivOpExpr(token, left, right) )

                elif re.match(INTPAT,token):
                    ### Looks like an integer (digits only)
                    stack.append(ConstExpr(int(token)))
                    
                elif re.match(FLOATPAT,token): 
                    ### Looks like a floating point number
                    stack.append(ConstExpr(float(token)))

                elif re.match(VARPAT,token):
                    ### Looks like a variable name.  One name should
                    ### always refer to a unique node with that name
                    if token in environment:
                        node = environment[token]
                    else:
                        node = VarExpr(token)
                        environment[token] = node
                    stack.append(node)

                elif token == "=":
                    # Assign value to variable
                    var = stack.pop()
                    val = stack.pop()
                    if isinstance(var, VarExpr) and isinstance(val, ConstExpr):
                        var.set(val)
                    else:
                        print("Can't set ", var, "to", val)
                        print("Only assignment of constants to variables is supported.")
                        
                else: 
                    ### if something else is put in  
                    print("Unknown token '" + token + "', skipping it")
                    print("To quit, type 'quit'")

            show_state(stack, environment)
        
        except IndexError as e: 
            print("Expression syntax: Too many operations for available operands")
        except TypeError as e: 
            print("Type error:", e)
        except Exception as e: 
            print("Unexpected exception: ", type(e))
            raise ## Re-raises the same exception so that we can see a stack trace 

def show_state( stack, environment):
    """Print the execution stack and environment.
    Args:
        stack:  A list of Expr nodes, to be printed 
        environment: a dict of (name, VarExpr) pairs
    Returns: 
        nothing
    Effect: 
        stack and environment are printed, one line each
    """
    print("Stack: ", end="")
    for expr in stack: 
        print(str(expr), end="; ")
    print()
    print("Variables: ", end="")
    for var_name in environment:
        var = environment[var_name]
        val = var.eval()
        if isinstance(val, ConstExpr):
            print(str(var)+"->"+str(val), end="; ")
        else: 
            print(str(var), end="; ")
    print()


def main(): 
   parser = argparse.ArgumentParser(description="""
   Read and print arithmetic expressions, with optional 
   evaluation.""",
   epilog="""
   Input (file or keyboard) is in postfix (reverse Polish notation), with each
   operation or operand separated by whitespace.  Integers and floating point
   numbers are interpreted as numbers.  Recognized operators are:
   #    (evaluate top item on stack)
   cl   (clear the stack)
   ^    (remove top item from stack)
   quit (quit)
   +    (addition)
   -    (subtraction)
   *    (multiplication)
   /    (division)
   =    (assignment, e.g., 17 x =  will assign 17 to x)
   Anything else is interpreted as a variable name.
   Example:   5 3 + x * is interpreted as (5+3)*x,
   and 5 3 + x * # evaluates to 8*x
   """,
   formatter_class=argparse.RawDescriptionHelpFormatter
   )

   parser.add_argument('input', metavar="filename",
                    nargs = '?', ### It's optional
                    type=argparse.FileType('r'), 
                    default=sys.stdin, 
                    help="input source (file name or - for command line)")

   args = parser.parse_args()

   interpret(args.input)

if __name__ == "__main__":
    main()
    
