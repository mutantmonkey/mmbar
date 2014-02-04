import datetime
from widgets import base


class ClockWidget(base.Widget):
    def output(self):
        return {
            'name': "clock",
            'full_text': datetime.datetime.now().strftime("%a %b %d %H:%M"),
            'short_text': datetime.datetime.now().strftime("%H:%M"),
        }
