from .TimeTable import TimeBlockCollection, TimeBlock

from datetime import datetime


class TimeNotebook():
    def __init__(self, filePath):
        self.path = filePath
        self._timers = []
        self.delimiter = ';'

        # Ensure that the file exists
        open(self.path, 'a+').close()

    def readFile(self):
        ''' Read the file '''

        f = open(self.path, 'r')
        content = f.readlines()

        for line in content:
            # Extract the information form the line
            info = line.split(self.delimiter)

            ID = info[0]
            category = info[1]
            label = info[2]
            init = self.get_date(info[3])
            end = self.get_date(info[4])
            status = info[5]

            # Creates a new TimeBlock
            block = TimeBlock(init=init,
                              end=end,
                              status=status)

            # Create new task
            task = TimeBlockCollection(ID=ID,
                                       label=label,
                                       category=category)
            task.add_TimeBlock(block)

            # Compare with the previous task
            try:
                if task.ID == self._timers[-1].ID:
                    self._timers[-1].add_TimeBlock(block)
                    continue
                else:
                    self._timers.append(task)
            except:
                self._timers.append(task)

    def count_lines(self):
        ''' Count the number of lines on the notebook '''
        with open(self.path, 'r') as f:
            return len(f.readlines())

    def format_date(self, timestamp):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def updateFile(self, task):
        ''' Write a specific task on the notebook '''
        self._timers.append(task)
        taskID = str(self.count_lines()+1)
        f = open(self.path, 'a+')
        for tBlock in task:
            f.write(self.delimiter.join([taskID,
                                        task.category,
                                        task.label,
                                        self.format_date(tBlock.init),
                                        self.format_date(tBlock.end),
                                        tBlock.status]) + '\n')
        f.close()

    def format_time(self, seconds):
        ''' Given the time on seconds,
        format the output to match HH:MM:SS format'''
        hours = int(seconds//3600)
        mins = int((seconds - hours*3600) // 60)
        secs = int(seconds - mins*60 - hours*3600)

        return '{:02}h {:02}m'.format(hours, mins)

    def get_date(self, timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    def get_categories(self):
        category_list = [task.category for task in self._timers]
        return list(set(category_list))

    def get_tasks(self, init, end):
        '''
            Get the task contained in a given time spam
        '''

        # Caculates total time:
        span_time = (end-init)
        if end > datetime.now():
            span_time = (datetime.now()-init)
        span_seconds = span_time.seconds + span_time.days*3600*24

        resume = {}
        time_recorded = 0
        for task in self._timers:
            # Check if the timer is in the span of interest
            if not task.inSpan(init=init, end=end):
                continue

            # Parse the tasks
            if not task.category:
                task.category = 'Untagged'

            if task.category not in resume.keys():
                resume[task.category] = dict(time=0, tasks={})

            resume[task.category]['time'] += task.total_span_time(init, end)
            if task.label not in resume[task.category]['tasks'].keys():
                resume[task.category]['tasks'][task.label] = 0
            resume[task.category]['tasks'][task.label] += task.total_span_time(init, end)
            time_recorded += task.total_span_time(init, end)

        return resume

    def get_resume(self, init, end):
        '''
            Returns a text resume of the time spam provided
        '''
        # Get the tasks contained in the time spam
        resume = self.get_tasks(init, end)

        # Generate the resume text
        resume_text = ''
        time_recorded = 0
        for cat, task in resume.items():
            resume_text += '\n{0} - {1}:\r\n'.format(cat,
                self.format_time(task['time']))
            for lab, time in task['tasks'].items():
                resume_text += '\t+{0} - {1}\n'.format(lab,
                    self.format_time(time))

        #resume_text += '\nTotal time recorded: {0}\n'.format(
        #        self.format_time(time_recorded))
        #resume_text += 'Not recorded time: {0}\n'.format(
        #        self.format_time(span_seconds - time_recorded))
        #resume_text += 'Recorded time: {0:0.02f}%'.format(
        #        time_recorded/span_seconds*100)

        return resume_text

    def rename_category(self, old_name, new_name, verbose=False):
        pass

    def list_tasks(self, init=None, end=None):
        pass

    def rename_task(self, ID, new_name):
        pass
