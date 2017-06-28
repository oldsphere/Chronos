from time import sleep
import random
from datetime import datetime , timedelta
import re

from Chrono.Timer import Timer as Timer
from Chrono.DynamicLine import DynamicLine as DynamicLine
from Chrono.Timeout import Timeout as Timeout

class TimeNotebook():
    def __init__(self, filePath):
        self._path = filePath
        self._timers = {}
        self._dates = {}
        self._activeTag = None
        self._delimiter = '\t'
        self.Timer = Timer()
        
        try:
            self.readFile(filePath)
        except:
            pass
        
    def readFile(self,filePath,span=''):
        '''
            Other options:
                [-] since
                [-] date
                ...
        '''
        try:
            with open(filePath,'r') as f:
                content = f.read().split('\n')
        except FileNotFoundError:
            return
        
        if re.match('\d+[dD]',span):
            match = re.match('(?P<time>\d+)[dD]',span)
            days = float( match.groupdict()['time'] )
            limDate = datetime.now() - timedelta(days=days)
            print( datetime.strftime(limDate,"%d/%m/%Y"))

        if re.match('\d+[wW]',span):
            match = re.match('(?P<time>\d+)[wW]',span)
            weeks = float( match.groupdict()['time'] )
            limDate = datetime.now() - timedelta(days=weeks)
            print( datetime.strftime(limDate,"%d/%m/%Y"))
            
        for line in content:
            try:
                date,task,time = self._parseLine(line)
                if span:
                    if date < limDate:
                        continue
                self._timers[task] = time         
                self._dates[task] = date
            except ValueError:
                continue

    def _getDate(self):
        return datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
            
    def updateFile(self):
        # Store the time spend
        if self._activeTag: 
            tag = self._activeTag        
        self._timers[tag] += self.Timer._elapsedTime

        with open(self._path,'a+') as f:
            date = self._getDate()
            
            etime = self.Timer.format_time(self.Timer._elapsedTime)       
            msg = self._delimiter.join([date,'{0: <20}'.format(tag),etime])
                                                                 
            f.write(msg)
            f.write('\n')
                       
    def run(self, tag, cont=None):
        print('\n')
        self.Timer = Timer(cont)
        self.Timer.start()
        line = DynamicLine(refreshTime=0.5)
        
        self._activeTag = tag
        if not tag in self._timers.keys():
            self._timers[tag] = 0        
        
        priorTime = self.Timer.check()
        try:
            while True:
                time = self.Timer.check()
                totalTime = self.Timer.format_time(self._timers[tag] + self.Timer._elapsedTime)
                
                lineMsg = '\t'.join([tag,
                                    time,
                                    'Total Time: {0}'.format(totalTime)])
                
                
                if not time == priorTime:
                    line.overwrite(lineMsg)
                    priorTime = time
                sleep(0.1)                  
        
        except KeyboardInterrupt:
            self.updateFile()
            print('\nTime data stored')
            self.Timer.reset()
     
    def resume(self):
        if not self._activeTag:
            raise AttributeError('No previous task located')
        date,task,time = self._parseLine(self._getLine(-1))
        self.run(self._activeTag,time)
                    
    def _getLine(self,n=1):
        with open(self._path,'r') as f:
            content = f.read().split('\n')
        if content[-1] == '':
            del(content[-1])
        if n < 0:
            n = len(content) + n
        return content[n]
            
    def _parseLine(self,line):
        timestamp, task, time = line.split(self._delimiter)
        
        date = datetime.strptime(timestamp,'%d/%m/%Y %H:%M')        
        
        time = time.replace(':','h',1)
        time = time.replace(':','m',1)
        time +='s'
        
        TO = Timeout('1s')
        time_seconds = TO.parse_strtime(time)
        
        return (date,task,time_seconds)
               
    def _remove_last(self,n=1):
        # Read the entire file
        with open(self._path,'r') as f:
            content = f.read().split('\n')
            
        # Rewrite without the last lines.
        with open(self._path,'w') as f:
            f.write('\n'.join(content[:-1-n]))
            
    def __repr__(self):
        Timer = self.Timer        
        return '\n'.join(['{0} -> {1}'.format(k,Timer.format_time(v)) 
                         for k,v in self._timers.items()])








    