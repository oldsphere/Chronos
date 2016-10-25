from datetime import datetime
from time import sleep
import random
import re

from Chrono.DynamicLine import DynamicLine as DynamicLine

class Timer():
    
    def __init__(self,  preTime=None, onStop=None, onStart=None):
        self._initTime = datetime.now()
        self._elapsedTime = 0
        if preTime:
            self._elapsedTime = preTime
        self._running = False
        
        # Events
        self._onStop = onStop
        self._onStart = onStart

    def stop(self):
        self._running = False
    
    def start(self):
        self._initTime = datetime.now()
        if self._onStart: self._onStart()
        self._running = True
    
    def reset(self):
        self._elapsedTime = 0
    
    def _update(self):
        if self._running:
            self._elapsedTime += (datetime.now() - self._initTime).total_seconds()
            self._initTime = datetime.now()
    
    def check(self):
        self._update()
        return self.format_time(self._elapsedTime)
        
    def format_time(self,seconds):
        hours = int( seconds//3600 )
        mins = int( (seconds - hours*3600) // 60 )
        secs = int( seconds - mins*60 - hours*3600 )
        
        return '{:02}:{:02}:{:02}'.format(hours,mins,secs)
        
    def run(self):
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
            if self._onStop: self._onStop()
            self.stop()
