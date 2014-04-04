#!/usr/bin/python3
###############################################################################
# status.py - python i3bar status line generator
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import importlib
import json
import os.path
import subprocess
import sys
import time
import widgets
import yaml


def load_config(configpath):
    config = yaml.safe_load(open(configpath))

    if 'interval' in config:
        config['interval'] = int(config['interval'])
    else:
        config['interval'] = 2

    if 'netctl_check_interval' in config:
        config['netctl_check_interval'] = int(config['netctl_check_interval'])
    else:
        config['netctl_check_interval'] = 30

    return config


def active_profile(config):
    if 'widgets_netctl' in config:
        out = subprocess.check_output(['netctl', 'list']).decode('utf-8')
        for line in out.splitlines():
            if line[0:2] == '* ':
                return line[2:]
    return None


def get_widgets(config, profile):
    if 'widgets_netctl' in config:
        if profile in config['widgets_netctl']:
            return load_widgets(config['widgets_netctl'][profile])
    return load_widgets(config['widgets'])


def load_widgets(cwidgets):
    widgets = []
    for item in cwidgets:
        if isinstance(item, dict):
            # grab the first dict from the list of widgets
            components, args = item.copy().popitem()
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

        instance.start()
        widgets.append(instance)

    return widgets


if __name__ == '__main__':
    if len(sys.argv) > 1:
        configpath = sys.argv[1]
    else:
        try:
            import xdg.BaseDirectory
            configpath = xdg.BaseDirectory.load_first_config(
                'mmbar/config.yml')
        except:
            configpath = os.path.expanduser('~/.config/mmbar/config.yml')

    iconpath = os.path.dirname(os.path.abspath(__file__))
    config = load_config(configpath)
    profile = active_profile(config)
    widgets = get_widgets(config, profile)
    i = 0

    print(json.dumps({'version': 1}) + '[[]')
    while True:
        if i >= config['netctl_check_interval']:
            i = 0
            if active_profile(config) != profile:
                profile = active_profile(config)
                widgets = get_widgets(config, profile)

        output = []
        for widget in widgets:
            wout = widget.themed_output(config, iconpath)
            if wout is not None:
                output.append(wout)
        print(',' + json.dumps(output), flush=True)

        i += config['interval']
        time.sleep(config['interval'])
    print(']')
