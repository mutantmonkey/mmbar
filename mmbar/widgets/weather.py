# -*- coding: utf-8 -*-
import time
import urllib.error
import urllib.request
from mmbar import metar
from mmbar.widgets import base


class WeatherWidget(base.Widget):
    uri = "http://weather.noaa.gov/pub/data/observations/metar/stations/"\
          "{icao}.TXT"

    def __init__(self, icao_code, interval=300):
        super().__init__('weather', icao_code)
        self.icao_code = icao_code
        self.interval = interval

    def run(self):
        uri = self.uri.format(icao=self.icao_code)
        while True:
            try:
                r = urllib.request.urlopen(uri)
                w = metar.parse(r.read().decode('utf-8'))
                self.output['full_text'] = '{weather}, {temperature}°C'.format(
                    weather=w.conditions or w.cover or "fair",
                    temperature=w.temperature)
            except:
                pass

            time.sleep(self.interval)
