import re
import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import subprocess as sub


# Function to set the title of the window
def set_title(string):
    sys.stdout.write("\x1b]2;{0}\x07".format(string))

# Default alarm path
ALARM_PATH = os.path.join(os.path.dirname(__file__), 'alarm.mp3')


# Alarm class
class Alarm:
    ''' Run a alarm on the system. '''
    def __init__(self, tonePath=None):
        self._disableAlarm = False
        self._tonePath = tonePath
        self._runningAlarm = False
        self._alarm = None

    def disable(self):
        self._disableAlarm = True
        self.stop()

    def enable(self):
        self._disableAlarm = False

    def start(self):
        if not self._runningAlarm and not self._disableAlarm:
            FNULL = open(sub.os.devnull, 'w')
            self._alarm = sub.Popen(['cvlc', self._tonePath],
                                    stdout=FNULL, stderr=FNULL)
            self._runningAlarm = True

    def stop(self):
        if self._runningAlarm:
            self._alarm.kill()
            self._runningAlarm = False


def printHelp():
    print('''
help, ?           Expose the command shell options
resume, r         Resume the timer
add, a            Add aditional time to the task
quit, q           Stop recording current task
omit, o           Not record the present task
silent, s         Disable the alarm''')


class MyCompleter(object):  # Custom completer
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def date_parser(str_span):
    '''
    This function parse a string and returns a tupple with init and end time of
    the period to analyze.
    '''
    pattern = '([+-]?\d+)*\s*([wWmMdDyY])\s*([-+]?\d+)*'
    match = re.findall(pattern, str_span)

    if len(match) > 1 or not match:
        raise ValueError('Invalid data string!')
        return None

    # Parse the match
    scale = match[0][1]
    offset = match[0][2]
    now = datetime.now()

    if offset:
        offset = int(offset)
    else:
        offset = 0

    if offset > 0:
        if scale.upper() == 'D':
            cDay = datetime.strftime(now, '%j')
            offset -= int(cDay)
        if scale.upper() == 'W':
            cWeek = datetime.strftime(now, '%W')
            offset -= int(cWeek)
        if scale.upper() == 'M':
            cMonth = datetime.strftime(now, '%m')
            offset -= int(cMonth)

    if scale.upper() == 'D':
        init = now - relativedelta(days=-offset)
        end = init

    if scale.upper() == 'M':
        init = now - relativedelta(months=-offset)
        init = init.replace(day=1)
        end = init
        end = end + relativedelta(months=1) - relativedelta(days=1)

    if scale.upper() == 'W':
        init = now - relativedelta(weeks=-offset)
        init = init - relativedelta(days=init.weekday())
        end = init
        end = init + relativedelta(days=6)

    init = init.replace(hour=0, minute=0, second=0)
    end = end.replace(hour=23, minute=59, second=59)

    return (init, end)
