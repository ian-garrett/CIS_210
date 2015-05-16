"""
   meetme.py: CIS 210 assignment 9, Winter 2014
   author: Ian Garrett igarrett@uoregon.edu

   Usage: python3 meetme.py 2012.12.1 8:30 17:00  keiko.ag.txt Emanuela.txt 

   Find potential times to meet by finding the available times in common
   among a set of agendas. Each agenda file is a list of appointments.

   Arguments (given through commandwindow):
       date: int
       begin time: int
       end time: int
       agenda*(zero or more agenda input files): .txt files
       containing times for corresponding appointments
       
   Returns (to commandwindow):
       an agenda containing appointments that work for commandline appointment
       and agendas of each person involved. If no common times are found, a message
       is returned through the commandwindow notifying the "No free times in common"
"""

from agenda import Appt, Agenda
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a time we can all meet.")
    parser.add_argument('date', help="Date to check for available times, format like 2012.05.31")
    parser.add_argument('earliest', help="Earliest potential time to start, format like 8:30")
    parser.add_argument('latest', help="Latest potential time to end, format like 18:00")
    parser.add_argument('participant', help="A text file containing an agenda, e.g., 'charles.ag'", 
                         nargs="*", type=argparse.FileType('r'))

    available = Agenda()
    args = parser.parse_args()
    blockspec = args.date + " " + args.earliest + " " + args.latest + "|Available"
    freeblock = Appt.from_string(blockspec)
    available.append(freeblock)

    for f in args.participant: 
        participant = Agenda.from_file(f)
        participant = participant.complement(freeblock)
        available = available.intersect(participant)

    if len(available) == 0:
        print("No free times in common")

    else:
        print(available)
    

    
