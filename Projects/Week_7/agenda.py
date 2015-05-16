"""
   agenda.py: CIS 210 assignment 7, Winter 2014
   author: Ian Garrett igarrett@uoregon.edu

   An Agenda is a list-like container of Appt (appointment).
   Each Appt occurs on a single day, with a start time, an end time, and
   a textual description.   They can be converted to and
   from strings, using the from_string class method and the __str__
   method.  An Agenda is essentially a list of appointments,
   with some special methods.  An Agenda can be read from a file using the
   from_file class method.  Intersecting Agendas produces
   a new Agenda whose Appts are periods that are in the overlap
   of Appts in the first and second Agenda.
   
"""

import datetime

class Appt:

    """
    A single appointment, starting on a particular
    date and time, and ending at a later time the same day.
    """
    
    def __init__(self, day, begin, end, desc):
        """Create an appointment on date
        from begin time to end time.
        
        Arguments:
            day:   A datetime.date object.  The appointment occurs this day.
            begin: A datetime.time object.  When the appointment starts. 
            end:  A datetime.time object, 
                after begin.                When the appointments ends.
            desc: A string describing the appointment
            
        Raises: 
        	ValueError if appointment ends before it begins
        	
        Example:
            Appt( datetime.date(2012,12,1),
                datetime.time(16,30),
                datetime.time(17,45))
            (December 1 from 4:30pm to 5:45pm)
        """
        self.begin = datetime.datetime.combine(day, begin)
        self.end = datetime.datetime.combine(day, end)
        if self.begin > self.end:
            raise ValueError
        self.desc = desc
        return
    
    @classmethod
    def from_string(cls, txt):
        """Factory parses a string to create an Appt.
           Args:
               txt: String specifying appointment date, time, and description
                    Format is "2014.2.14 15:10 15:35 | Umbrella lessons"
        """
        fields = txt.split("|")
        if len(fields) != 2:
            raise ValueError("Appt literal requires exactly one '|' before description")
        timespec = fields[0].strip()
        desc = fields[1].strip()
        fields = timespec.split()
        if len(fields) != 3:
            raise ValueError("Appt literal must start with date, time, time, separated by blanks")
        appt_date_text = fields[0]
        appt_begin_text = fields[1]
        appt_end_text = fields[2]
        fields = appt_date_text.split(".")
        try:
            year = int(fields[0].strip())
            month = int(fields[1].strip())
            day = int(fields[2].strip())
        except:
            raise ValueError("Date in Appt literal should be 9999.99.99 (Year.Month.Day)")

        date = datetime.date(year,month,day)
        begin = datetime.datetime.strptime(appt_begin_text, "%H:%M").time()
        end =   datetime.datetime.strptime(appt_end_text, "%H:%M").time()

        result = Appt(date, begin, end, desc)
        return result
        
    def __lt__(self, other):
        """Does this appointment finish before other begins?

        Arguments:
        	other: another Appt
        Returns: 
        	True iff this Appt is done by the time other begins.
        """
        if self.end <= other.begin:
            return True
        return False
        
    def __gt__(self, other):
        """Does other appointment finish before this begins?      
        Arguments:
        	other: another Appt
        Returns: 
        	True iff other is done by the time this Appt begins
        """
        if self.begin >= other.end:
            return True
        return False
        
    def overlaps(self, other):
        """Is there a non-zero overlap between this appointment
           and the other appointment.

           Arguments:
               self: an appointment
               other: another appointment
           Returns:
               Boolean Value: True if there is an overlap, False if no overlap
        """
        if (self < other) or (other < self):
            return False
        return True
            
    def intersect(self, other, desc=""):
        """Return an appointment representing the period in
        common between this appointment and another.
        Requires self.overlaps(other).
        An Agenda is a list-like container of Appt (appointment).
	Arguments:
	    other:  Another Appt
	    desc:  (optional) description text for this appointment.

	Returns:
	    An appointment representing the time period in common
	    between self and other.   Description of returned Appt 
	    is copied from this (self), unless a non-null string is 
	    provided as desc. 
        """
        if desc=="":
            desc = self.desc
        assert(self.overlaps(other))
        begin_time = max(self.begin.time(), other.begin.time())
        end_time = min(self.end.time(), other.end.time())
        return Appt(self.begin.date(), begin_time, end_time, desc)

    

    def __str__(self):
        """String representation of appointment.
        Example:
            2012.10.31 13:00 13:50 | CIS 210 lecture
            
        This format is designed to be easily divided
        into parts:  Split on '|', then split on whitespace,
        then split date on '.' and times on ':'.
        """
        daystr = self.begin.date().strftime("%Y.%m.%d ")
        begstr = self.begin.strftime("%H:%M ")
        endstr = self.end.strftime("%H:%M ")
        return daystr + begstr + endstr + "| " + self.desc

class Agenda:
    """An Agenda is essentially a list of appointments,
    with some agenda-specific methods.
    """

    appts = []
    
    def __init__(self):
        """An empty agenda."""
        self.appts = [ ]
        
    @classmethod
    def from_file(cls, f):
        """Factory: Read an agenda from a file.
        
        Arguments: 
            f:  A file object (as returned by io.open) or
               an object that emulates a file (like stringio).
        Returns: 
            An Agenda object
        """
        agenda = cls()
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                pass
            else: 
                try: 
                    agenda.append(Appt.from_string(line))
                except ValueError as err: 
                    print("Failed on line: ", line)
                    print(err)
        return agenda

    def append(self,appt):
        """Add an Appt to the agenda."""
        self.appts.append(appt)

    def intersect(self,other,desc=""): 
        """Return a new agenda containing appointments
        that are overlaps between appointments in this agenda
        and appointments in the other agenda.

        Titles of appointments in the resulting agenda are
        taken from this agenda, unless they are overridden with
        the "desc" argument.

        Arguments:
           other: Another Agenda, to be intersected with this one
           desc:  If provided, this string becomes the title of
                all the appointments in the result.
        """
        use_default_desc = (desc == "")
        result = Agenda()
        for appt_self in self.appts:
            for appt_other in other.appts:
                if appt_self.overlaps(appt_other):
                    if use_default_desc:
                        result.append(appt_self.intersect(appt_other,appt_self.desc))
                    else:
                        result.append(appt_self.intersect(appt_other))
                        
        return result

    def __len__(self):
        """Number of appointments, callable as built-in len() function"""
        return len(self.appts)

    def __iter__(self):
        """An iterator through the appointments in this agenda."""
        return self.appts.__iter__()

    def __str__(self):
        """String representation of a whole agenda"""
        rep = ""
        for appt in self.appts:
            rep += str(appt) + "\n"
        return rep[:-1]

    def __eq__(self,other):
        """Equality, ignoring descriptions --- just equal blocks of time"""
        if len(self.appts) != len(other.appts):
            return False
        for i in range(len(self.appts)):
            mine = self.appts[i]
            theirs = other.appts[i]
            return (mine.begin == theirs.begin and
                    mine.end == theirs.end)


#########################
#  Self-test invoked when module is run
#  as main program. 
#########################
    
from test_harness import *
import io
def selftest_appt():
    """Simple smoke test for Appt class."""
    sample = Appt(datetime.date(2012, 10, 31),
                  datetime.time(14, 30), datetime.time(15, 45),
                  "Sample appointment")
    testEQ("Create and format",str(sample),
           "2012.10.31 14:30 15:45 | Sample appointment") 
    
    earlier = Appt(datetime.date(2012, 10, 31),
                    datetime.time(13, 30), datetime.time(14,30), 
                    "Before my appt")
    later = Appt(datetime.date(2012, 10, 31),
                  datetime.time(16,00), datetime.time(21,00), "Long dinner")
    testEQ("Strictly before is '<'", earlier < later, True)
    testEQ("Strictly after is '>'", later > earlier, True)
    testEQ("Not earlier than itself", earlier < earlier, False)
    testEQ("Not later than itself", earlier > later, False)
    
    testEQ("Earlier doesn't overlap later", earlier.overlaps(later), False) 
    testEQ("Later doesn't overlap earlier", later.overlaps(earlier), False)
    
    conflict = Appt(datetime.date(2012, 10, 31), 
                    datetime.time(13, 45), datetime.time(16,00),
        "Conflicting appt")

    testEQ("Should overlap", sample.overlaps(conflict), True)
    testEQ("Opposite overlap", conflict.overlaps(sample), True)
    overlap = sample.intersect(conflict)
    testEQ("Expected intersection", str(overlap), 
           "2012.10.31 14:30 15:45 | Sample appointment")
    overlap = conflict.intersect(sample)
    testEQ("Expected intersection", str(overlap), 
           "2012.10.31 14:30 15:45 | Conflicting appt")
    overlap = conflict.intersect(sample,"New desc")
    testEQ("Expected intersection", str(overlap), 
           "2012.10.31 14:30 15:45 | New desc")

    text = "2012.10.31 14:30 15:45 | from text"
    from_text = Appt.from_string(text)
    testEQ("String <-> Appt",text, str(from_text))
    def die():
       Appt.from_string("2012.10.31 15:45 14:30 | time traveler")
    testRaise("Time order error", ValueError, die)       
       

def selftest_agenda():
    """Simple smoke test for Agenda class."""

    keiko_agtxt="""# Free times for Keiko on December 1
           2012.12.1 07:00 08:00  | Possible breakfast meeting
           2012.12.1 10:00 12:00  | Late morning meeting
           2012.12.1 14:00 18:00  | Afternoon meeting
         """

    kevin_agtxt="""2012.11.30 09:00 14:00 | I have an afternoon commitment on the 30th
          2012.12.1  09:00 15:00 | I prefer morning meetings
          # Kevin always prefers morning, but can be available till 3, except for 
          # 30th of November.
          """

    emanuela_agtxt = """
    2012.12.1 12:00 14:00 | Early afternoon
    2012.12.1 16:00 18:00 | Late afternoon into evening
    2012.12.2 8:00 17:00 | All the next day
    """
    
    keiko_ag = Agenda.from_file(io.StringIO(keiko_agtxt))
    kevin_ag = Agenda.from_file(io.StringIO(kevin_agtxt))
    emanuela_ag = Agenda.from_file(io.StringIO(emanuela_agtxt))    

    keiko_kevin = keiko_ag.intersect(kevin_ag)
    kk = ("2012.12.01 10:00 12:00 | Late morning meeting\n" +
         "2012.12.01 14:00 15:00 | Afternoon meeting")
    kkactual = str(keiko_kevin)
    testEQ("Keiko and Kevin", kkactual.strip(), kk.strip())

    kevin_emanuela = kevin_ag.intersect(emanuela_ag)
    ke = "2012.12.01 12:00 14:00 | I prefer morning meetings"
    keactual = str(kevin_emanuela)
    testEQ("Kevin and Emanuela", keactual, ke)

    everyone = keiko_kevin.intersect(emanuela_ag)
    testEQ("No overlap of all three", len(everyone), 0)


if __name__ == "__main__":
    selftest_appt()
    selftest_agenda()    
    
    
    
