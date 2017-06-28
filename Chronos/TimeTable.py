import re
import matplotlib.pyplot as plt

class TimeBlock():
    def __init__(self, t_init,t_end, label):
        self.t_init = t_init
        self.t_end = t_end
        self._proj , self._task = self.parse_label(label)
        self._initTime = self.parse_Time(t_init)
        self._endTime = self.parse_Time(t_end)
        
        self.span = self._endTime - self._initTime        
        
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
        ax.set_xticks([0,6,12,18,24])
        ax.set_ylim(0,5)
        ax.set_xlabel('Time [h]')
        ax.grid(True)
        
        for tBlock in self.TimeBlocks:
            if not tBlock._proj in self._projs.keys():
                self._projs[tBlock._proj] = self.cmap.pop()
            color = self._projs[tBlock._proj]
            ax.add_patch( tBlock.draw(level=2, color=color) ) 
            tBlock.write_label(level=2)
        
        plt.show()

# Example
tb1 = TimeBlock('00:00','01:00','Working - Improve profile')
tb2 = TimeBlock('10:00','15:00','Atacama')
tb3 = TimeBlock('08-08-2016 17:00','08-08-2016 20:00','Sleeping - Pero como un cabrón!')
tt = TimeTable()
tt.add_TimeBlock(tb1)
tt.add_TimeBlock(tb2)
tt.add_TimeBlock(tb3)
tt.plot()