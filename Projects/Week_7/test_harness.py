"""
Test harness:
   Utility functions for writing test cases in Python programs.

   Python has a standard module, unittest, that provides a more
   powerful but but more complex testing framework. This module
   is designed to be very simple.

   Currently test_harness provides just one function, testEQ,
   for comparing an actual value to an expected value. More
   functions may be provided later.

   Author: M Young, michal@cs.uoregon.edu
   October 2012 for CIS 210 at U. Oregon
"""

def testEQ( desc, actual, expect ) : 
    """General framework for running a single test case
    with an expected result.  Prints a log message depending
    on whether the actual result was the same as the expected result.
    Args: 
        desc: Description of the test case
        actual:  Actual result (should be same as expected)
        expect:  Expected result
    """
    try: 
       if actual == expect : 
           print("   Passed -- ",desc, " result: ", actual)
       else: 
           print("***FAILED*** ", desc, " Expected: |", expect, 
               "| but got |", actual, "|")
    except Exception as E:
         print("***FAILED WITH EXCEPTION***", desc, E)

def testRaise(desc, kind, func):
    """Make sure an expected exception is raised.
    
    Args:
        desc: Description of the test case
        func: A function to call
    """
    try:
        func()
        print("***FAILED TO RAISE EXCEPTION***", desc)
    except kind as E:
        print("   Raised expected exception --", desc)
        print("    " + str(E))
    except Exception as E:
        print("***WRONG EXCEPTION**", str(E), desc)
    