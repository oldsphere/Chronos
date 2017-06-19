from datetime import datetime
from time import sleep
import random
import re
from .DynamicLine import DynamicLine 
from .TimeTable import TimeBlockCollection, TimeBlock

class Timer():
    '''
    - Timer object -

    The basic functionality of the Timer is to record the
    time elapsed between start and stop calls.
    The system records the time of the start and compares it to the current
    time on every request by the method check. This way it is not necesary to
    run the object in a parallel threat to account precisely the time
    elapsed.

    Everytime the Timer is stopped a new TimeBlock will be added to the
    timeChain property. This TimeBlock contains information of the duration,
    beginning and stop time.
    Additionally the status of the block will be included. Currently the status
    are:
        'normal' - Uninterrupted timer from the begining to the end
        will be marked

    Additional status can be defined by the used modifing the status property
    before calling the stop method.
   
    '''
    
    def __init__(self,time_offset=0):
        self._blockInitTime = datetime.now()
        self._initTime = datetime.now()
        self.seconds = 0 + time_offset
        self.timeChain = TimeBlockCollection()
        self._running = False
        self.status = 'normal'

    def start(self):
        ''' Start recording the time '''
        self._blockInitTime = datetime.now()
        self._initTime = datetime.now()
        self._running = True
    
    def stop(self):
        ''' Stop recording the time '''
        _ = self.check()
        self._running = False
        TB = TimeBlock(init=self._blockInitTime,
                       end=datetime.now(),
                       status=self.status)
        self.timeChain.append(TB)

    def reset(self,time_offset=0):
        ''' Reset the elapsed time recorded '''
        self.timeChain = []
        self.seconds = 0 + time_offset
        self.status = 'normal'
    
    def check(self,**kargs):
        self._update()
        return self.format_time(self.seconds)
    
    def format_time(self,seconds):
        ''' Given the time on seconds, format the output to match HH:MM:SS format'''
        hours = int( seconds//3600 )
        mins = int( (seconds - hours*3600) // 60 )
        secs = int( seconds - mins*60 - hours*3600 )
        
        return '{:02}:{:02}:{:02}'.format(hours,mins,secs)
        
    def run(self):
        ''' Run the Timer in a visual mode '''
        print('\n')
        self.start()
        line = DynamicLine(refreshTime=0.5)
        priorTime = '00:00:00'
        try:
            while True:
                time = self.check()
                if not time == priorTime:
                    line.overwrite(time)
                    priorTime = time
                sleep(0.1)
        
        except KeyboardInterrupt:
            self.stop()

    def _update(self):
        if self._running:
            self.seconds += (datetime.now() - self._initTime).total_seconds()
            self._initTime = datetime.now()
