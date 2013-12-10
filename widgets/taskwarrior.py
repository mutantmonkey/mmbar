# -*- coding: utf-8 -*-
import datetime
import subprocess


class TaskwarriorWidget(object):
    def __init__(self, interval=60):
        self.interval = interval
        self.last_run = None
        self.full_text = ""

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            try:
                overdue = int(subprocess.check_output([
                    '/usr/bin/task', '+OVERDUE', 'count']).strip())
                duetoday = int(subprocess.check_output([
                    '/usr/bin/task', '+DUETODAY', 'count']).strip())

                if overdue + duetoday > 0:
                    self.full_text = str(overdue + duetoday)
                else:
                    self.full_text = ""
            except:
                pass

        if len(self.full_text) > 0:
            return {
                'name': "taskwarrior",
                'full_text': self.full_text,
            }
