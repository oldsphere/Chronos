from time import sleep
import re

from .Timer import Timer
from .TimeTable import TimeBlockCollection, TimeBlock
from .DynamicLine import DynamicLine

class Timeout(Timer):
    '''
       -  Timeout object -

       Object based on Timer object.
       The main difference is that this object count down the time from an
       specific span.

       Aditionally to the states afore mentioned there is the 'overtime' state,
       which is activated when the the inital span is overdue.
    '''

    def __init__(self, strTime):
        Timer.__init__(self)
        self._timespan = self.parse_strtime(strTime)
        self.seconds = 0
        self._strTime = strTime

    def extend(self,strTime):
        extend_time = self.parse_strtime(strTime)
        self._timespan += extend_time

    def reset(self,strTime=None):
        ''' Reset the timeout timer
        strTime will set a new timespan for the Timeout.
        If not strTime is provided the last valid timespan will be used'''

        if not strTime:
            strTime = self._strTime
        self._timespan = self.parse_strtime(strTime)
        self.seconds = 0

    def parse_strtime(self,strtime):
        ''' Extract the number of seconds in the strtime provided.
        The strtime must have the following valid tags:
            D - Days
            H - Hours
            M - Minutes
            S - Seconds

        The format is any tag preceded by the number. This number can be a
        float number (separated by "." character)

        Example:

            >parse_strtime('1h30m5s')
            95.0
        '''

        try:

            days = re.findall('(\d+\.?\d*)\s*[Dd]',strtime)
            hours =  re.findall('(\d+\.?\d*)\s*[Hh]',strtime)
            mins =  re.findall('(\d+\.?\d*)\s*[Mm]',strtime)
            secs =  re.findall('(\d+\.?\d*)\s*[Ss]',strtime)

            if days:
                days = float(days[0])
            else:
                days = 0

            if hours:
                hours = float(hours[0])
            else:
                hours = 0

            if mins:
                mins = float(mins[0])
            else:
                mins = 0
            if secs:
                secs = float(secs[0])
            else:
                secs = 0

            return days*24*3600 + hours*3600 + mins*60 + secs

        except IndexError:
            print('Invalid strtime sentence')

    def check(self, limit_zero=True):
        ''' Check the remain time '''
        self._update()
        self.remain = self._timespan - self.seconds
        if self.remain <= 0:
            if limit_zero:
                return self.format_time(0)
            else:
                return '-' + self.format_time(abs(self.remain))

        return self.format_time(self.remain)

    def run(self):
        print('\n')
        self.start()
        line = DynamicLine(refreshTime=0.5)
        priorTime = '00:00:00'
        try:
            while True:
                time = self.check()
                if time == "00:00:00":
                    line.blink(time, nBlinks=1000)

                if not time == priorTime:
                    line.overwrite(time)
                    priorTime = time
                sleep(0.1)

        except KeyboardInterrupt:
            self.stop()
