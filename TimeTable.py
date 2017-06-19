import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

class TimeBlockCollection(list):
    def __init__(self,ID=None,label=None,category=None):
        self.ID = ID
        self.label = label
        self.category = category

    def assign_task(self,task,category=None):
        self.label = task
        self.category = category

    def assing_category(self,category):
        self.category = category

    def add_TimeBlock(self, Block):
        self.append(Block)
 
    def new_TimeBlock(self,init,end,status):
        self.append(TimeBlock(init,end,status))

    def overwrite_all_status(self,new_status):
        for i in self:
            i.status = new_status

    def interruption_time(self):
        return self.absolute_time() - self.total_time()

    def total_time(self):
        ''' Total time spent in the task '''
        return sum([t.seconds for t in self])

    def absolute_time(self):
        ''' Absolute time, including interruptions '''
        return (self[-1].end - self[0].init).seconds

    def inSpan(self,init,end):
        ''' Evaluate if the time is in the provided time span '''
        return any([init < t.end < end for t in self]) | \
               any([init < t.init < end for t in self])
                
    def total_span_time(self,init,end):
        time = 0
        for t in self:
            if not ((init < t.init < end) | (init < t.end < end)):
                continue

            t_init = t.init
            t_end = t.end
            if t.init < init:
                t_init = init
            if t.end > end:
                t_end = end

            time += (t_end-t_init).seconds
        return time

class TimeBlock():
    def __init__(self, init,end,status,label=None ):
        self.init =init
        self.end = end
        self.status = status
        self.seconds = (self.end - self.init).seconds
        
    def parse_Time(self,timeStr):
        # Extract time in h from the time stamp 'dd/mm/yyyy HH:MM'
        timeRes = re.findall('(\d\d):(\d\d)',timeStr)
        assert len(timeRes) == 1, print('Multiple match has been found in time stamp')        
        hour = timeRes[0][0]
        mins = timeRes[0][1]
        
        return float(hour) + float(mins)/60
        
    def parse_label(self,label):
        content = label.split('-')
        proj = content[0].strip()
        task = ''
        if len(content) > 1:
            task = content[1].strip()
        return proj,task
        
    def draw(self, level=0,color=None):
        return plt.Rectangle(xy=(self._initTime , level),
                             width=self.span,
                             height=1,color=color)
                             
    def write_label(self,level=0):
        mid_x = (self._initTime +self._endTime)*0.5
        rotation=0
        if self.span < 3:
            rotation = 90
        return plt.text(x=mid_x, y=level+0.5,
                        s=self._proj,
                        rotation=rotation,
                        horizontalalignment='center',
                        verticalalignment='center')
    
class TimeTable():
    def __init__(self,text=True):
        self.TimeBlocks = []
        self._projs = {}
        self.cmap = ['#48ff4a',         #Green
                     '#56fbff',         # Blue
                     '#f4ff56',         # Yellow
                     '#5685ff',         # Deep blue
                     '#c256ff',         # Purple
                     '#FF0000']         # Red

    def add_TimeBlock(self, TimeBlock):
        self.TimeBlocks.append(TimeBlock)
        
    def plot(self):
        fig,ax = plt.subplots()
        ax.set_xlim(0,24)
        ax.set_xticks(list(range(0,24)))
        ax.set_xlabel('Time [h]')
        ax.ylabel.set_major_formatter( plticker.NullFormatter )
        ax.grid(True)
 
        for tBlock in self.TimeBlocks:
            if not tBlock._proj in self._projs.keys():
                self._projs[tBlock._proj] = self.cmap.pop()
            color = self._projs[tBlock._proj]
            ax.add_patch( tBlock.draw(level=2, color=color) ) 
            tBlock.write_label(level=2)
        
        plt.show()
