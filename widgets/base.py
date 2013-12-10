import datetime


class IntervalWidget(object):
    def __init__(self, interval, retry_interval=30):
        self.interval = interval
        self.retry_interval = retry_interval
        self.last_run = None
        self.cached_output = None

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            out = self.get_output()
            if out is not None:
                self.cached_output = out
                self.last_run = datetime.datetime.now()
            else:
                self.last_run = datetime.datetime.now() + datetime.timedelta(
                    seconds=self.retry_interval)

        if self.cached_output is not None:
            # we need to return a copy, otherwise the icon logic will keep
            # adding icons
            return self.cached_output.copy()
