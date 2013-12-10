import subprocess
from widgets import base


class TaskwarriorWidget(base.IntervalWidget):
    def __init__(self, interval=60):
        self.name = "taskwarrior"
        super().__init__(interval)

    def get_output(self):
        try:
            overdue = int(subprocess.check_output([
                '/usr/bin/task', '+OVERDUE', 'count']).strip())
            duetoday = int(subprocess.check_output([
                '/usr/bin/task', '+DUETODAY', 'count']).strip())

            if overdue + duetoday > 0:
                return {
                    'name': "taskwarrior",
                    'full_text': str(overdue + duetoday),
                }
            else:
                return {'name': "taskwarrior"}
        except:
            pass
