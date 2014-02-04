import datetime
import os.path


class Widget(object):
    def themed_output(self, config, iconpath):
        wout = self.output()

        if wout is not None and wout['name'] in config['theme']:
            widget_cfg = config['theme'][wout['name']]

            wout['icon'] = ""
            if 'icon' in widget_cfg:
                widget_icons = widget_cfg['icon'].split()
                if len(widget_icons) > 2 and '_status' in wout:
                    if wout['_status'] == 'error':
                        icon = widget_icons[2]
                    elif wout['_status'] == 'warn':
                        icon = widget_icons[1]
                    else:
                        icon = widget_icons[0]
                else:
                    icon = widget_icons[0]

                if icon[0:2] == 'U+':
                    icon = chr(int(icon[2:], 16))
                    wout['full_text'] = icon + '  ' + wout['full_text']
                else:
                    wout['icon'] = os.path.join(iconpath, 'icons', icon)
                    wout['full_text'] = ' ' + wout['full_text']

            if 'color' in widget_cfg:
                widget_colors = widget_cfg['color'].split()
                if len(widget_colors) > 2 and '_status' in wout:
                    if wout['_status'] == 'error':
                        wout['color'] = widget_colors[2]
                    elif wout['_status'] == 'warn':
                        wout['color'] = widget_colors[1]
                    else:
                        wout['color'] = widget_colors[0]
                else:
                    wout['color'] = widget_colors[0]

        return wout



class IntervalWidget(Widget):
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
