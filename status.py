#!/usr/bin/python3
################################################################################
# status.py - python i3bar status line generator
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import json
import sys
import time

from battery import *
from clock import *
from mpdstatus import *
from weather import *
from wifi import *

RUN_INTERVAL = 2
widgets = [
    WifiWidget('wlan0'),
    BatteryWidget('CMB1'),
    #MpdStatusWidget('gigantea.mutantmonkey.in'),
    WeatherWidget('KBCB'),
    ClockWidget(),
]


prnt(json.dumps({'version': 1}) + '[[]')
while True:
    output = []
    for widget in widgets:
        output.append(widget.output())
    print(',' + json.dumps(output), flush=True)
    time.sleep(RUN_INTERVAL)
prnt(']')
