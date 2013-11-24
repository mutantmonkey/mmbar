import datetime


class ClockWidget(object):
    def output(self):
        return {
            'name': "clock",
            'full_text': datetime.datetime.now().strftime("%a %b %d %H:%M"),
            'short_text': datetime.datetime.now().strftime("%H:%M"),
            'icon': 'clock.xbm',
        }
