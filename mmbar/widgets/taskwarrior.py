import subprocess
import time
from mmbar.widgets import base


class TaskwarriorWidget(base.Widget):
    def __init__(self, interval=60):
        super().__init__('taskwarrior')
        self.interval = interval

    def run(self):
        while True:
            try:
                overdue = int(subprocess.check_output([
                    '/usr/bin/task', '+OVERDUE', 'count']).strip())
                duetoday = int(subprocess.check_output([
                    '/usr/bin/task', '+DUETODAY', 'count']).strip())

                if overdue + duetoday > 0:
                    self.output['full_text'] = str(overdue + duetoday),
                else:
                    self.output['full_text'] = None
            except:
                pass

            time.sleep(self.interval)
