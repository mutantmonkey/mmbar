import abc
import datetime
import os.path
import threading


class Widget(threading.Thread):
    def __init__(self, name=None, instance=None):
        self.output = {}
        self.output['name'] = name
        self.output['instance'] = instance
        self.output['full_text'] = None

        super().__init__(name="{}-{}".format(name, instance))

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError()

    def themed_output(self, config, iconpath):
        wout = self.output.copy()

        if wout is not None and wout['name'] in config['theme']:
            widget_cfg = config['theme'][wout['name']]

            if wout['full_text'] is None:
                return None

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
