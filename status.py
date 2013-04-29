#!/usr/bin/python3
################################################################################
# status.py - python i3bar status line generator
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import importlib
import json
import sys
import time
import widgets
import yaml

try:
    import xdg.BaseDirectory
    configpath = xdg.BaseDirectory.load_first_config('mmbar/config.yml')
except:
    import os.path
    configpath = os.path.expanduser('~/.config/mmbar/config.yml')

config = yaml.safe_load(open(configpath))
interval = config['interval']
widgets = []

# load widgets from config
for args in config['widgets']:
    args = args.split(' ')

    components = args[0].split('.')
    path = '.'.join(components[:-1])
    module = importlib.import_module(path)

    class_ = getattr(module, components[-1])
    instance = class_(*args[1:])
    widgets.append(instance)


print(json.dumps({'version': 1}) + '[[]')
while True:
    output = []
    for widget in widgets:
        output.append(widget.output())
    print(',' + json.dumps(output), flush=True)
    time.sleep(interval)
print(']')
