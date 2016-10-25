from time import sleep
import sys
import random
import re

class DynamicLine():
    def __init__(self,refreshTime=0.2):
        self._message = ''
        self._refreshTime = refreshTime
        
    def write(self,msg):
        self._message = msg
        print(msg,end='')
        sys.stdout.flush()
        
    def overwrite(self,msg):
        self.clean()
        self.write(msg)
    
    def clean(self):
        whiteMessage = ''
        if self._message:
            whiteMessage = ' ' * len(self._message)
        print('\r'+whiteMessage,end='\r')
        sys.stdout.flush()
        self._message = ''
        
        
    def blink(self,msg,nBlinks=10):
        for t in range(nBlinks):
            if  t % 2:
                self.write(msg)
            else:
                self.clean()
            sleep(self._refreshTime)

    def appear(self,msg):
        self._message = msg
        for c in msg:
            print(c,end='')
            sys.stdout.flush()
            if c:
                sleep(self._refreshTime)
                
    def appear_random(self,msg):
        self._message = msg
        
        def makeString(msg,validPositions):
            newMsg = ''
            for pos,letter in enumerate(msg):
                if pos in validPositions:
                    newMsg += letter
                else:
                    newMsg += ' '
            return newMsg
        
        positionPool = list( range(len(msg)))
        validPositions = []
        
        for i in range(len(msg)):
            letterPos = random.choice(positionPool)
            validPositions.append( letterPos )
            positionPool.remove(letterPos)
            self.overwrite( makeString(msg, validPositions) )
            sleep(self._refreshTime)
                
    def erase_charater(self,n=1):
        print('\b'*n + ' '*n,end='')
        sys.stdout.flush()
        
    def disappear(self,msg,reverse=False):
        print(msg)   
        sys.stdout.flush()
        for c in msg:
            self.erase_charater(1)
            sleep(self._refreshTime)
        
        self._message = ''    