import datetime
import time
from mmbar.widgets import base


class ClockWidget(base.Widget):
    def __init__(self, interval=1):
        super().__init__('clock')
        self.interval = interval

    def run(self):
        while True:
            self.output.update({
                'full_text': datetime.datetime.now().strftime(
                    "%a %b %d %H:%M"),
                'short_text': datetime.datetime.now().strftime("%H:%M"),
            })
            time.sleep(self.interval)
