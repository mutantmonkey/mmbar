import datetime


class ClockWidget(object):
    def output(self):
        return {
            'full_text': datetime.datetime.now().strftime(" %a %b %d %H:%M "),
            'icon': '.config/dzen/icons/clock.xbm',
        }
