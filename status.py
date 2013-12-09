#!/usr/bin/python3
###############################################################################
# status.py - python i3bar status line generator
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import importlib
import json
import os.path
import sys
import time
import widgets
import yaml

if len(sys.argv) > 1:
    configpath = sys.argv[1]
else:
    try:
        import xdg.BaseDirectory
        configpath = xdg.BaseDirectory.load_first_config('mmbar/config.yml')
    except:
        configpath = os.path.expanduser('~/.config/mmbar/config.yml')

config = yaml.safe_load(open(configpath))
interval = config['interval']
icon_path = os.path.dirname(os.path.abspath(__file__))
widgets = []

# load widgets from config
for item in config['widgets']:
    if isinstance(item, dict):
        # grab the first dict from the list of widgets
        components, args = item.popitem()
    else:
        # if the item is not a dict, then it is a widget with no args
        # for backwards compatibility, we split on spaces
        splat = item.split(' ')
        components = splat[0]
        if len(splat) > 1:
            args = splat[1:]
        else:
            args = []

    components = components.split('.')
    path = '.'.join(components[:-1])
    module = importlib.import_module(path)

    class_ = getattr(module, components[-1])

    if isinstance(args, dict):
        # keyword arguments
        instance = class_(**args)
    elif isinstance(args, list):
        # positional arguments
        instance = class_(*args)
    else:
        # single argument
        instance = class_(args)

    widgets.append(instance)


def theme_widget(wout):
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
            wout['icon'] = os.path.join(icon_path, 'icons', icon)
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


print(json.dumps({'version': 1}) + '[[]')
while True:
    output = []
    for widget in widgets:
        wout = widget.output()

        if wout is not None:
            if wout['name'] in config['theme']:
                wout = theme_widget(wout)
            output.append(wout)
    print(',' + json.dumps(output), flush=True)
    time.sleep(interval)
print(']')
