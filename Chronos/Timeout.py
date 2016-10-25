from time import sleep
import re

from Chrono.Timer import Timer as Timer
from Chrono.DynamicLine import DynamicLine as DynamicLine

class Timeout(Timer):
    def __init__(self, strTime, onStart=None, onStop=None, onEnd=None, onTimeOut=None):
        Timer.__init__(self, onStart=onStart)
        self._timespan = self.parse_strtime(strTime)
        self._remainSeconds = self._timespan

        #Events
        self._onStop = onStop
        self._onTimeOut = onTimeOut
        self._onEnd = onEnd
        
    def reset(self,strTime):
        self._timespan = self.parse_strtime(strTime)
        self._remainSeconds = self._timespan
		
    def parse_strtime(self,strtime):
        try:
            days = re.findall('(\d+\.?\d*)\s*[Dd]',strtime) 
            hours =  re.findall('(\d+\.?\d*)\s*[Hh]',strtime)  
            mins =  re.findall('(\d+\.?\d*)\s*[Mm]',strtime)
            secs =  re.findall('(\d+\.?\d*)\s*[Ss]',strtime)          
            
            if days: days = float(days[0])
            else: days = 0
            if hours: hours = float(hours[0])
            else: hours = 0    
            if mins: mins = float(mins[0])
            else: mins = 0
            if secs: secs = float(secs[0])
            else: secs = 0
            
            return days*24*3600 + hours*3600 + mins*60 + secs            
            
        except IndexError:
            print('Invalid strtime sentence')
       
    def check(self):
        self._update()
        self._remainSeconds = self._timespan - self._elapsedTime
        if self._remainSeconds <= 0:
            return self.format_time(0)
        return self.format_time(self._remainSeconds)
        
        
    def run(self):
        print('\n')
        self.start()
        line = DynamicLine(refreshTime=0.5)
        priorTime = '00:00:00'
        try:
            while True:
                time = self.check()
                if time == "00:00:00": 
                    if self._onTimeOut: self._onTimeOut()
                    line.blink(time, nBlinks=1000)
                
                if not time == priorTime:
                    line.overwrite(time)
                    priorTime = time
                sleep(0.1)
                
        except KeyboardInterrupt:
            if time == "00:00:00" and self._onEnd: self._onEnd()
            if self._onStop: self._onStop()
            self.stop()