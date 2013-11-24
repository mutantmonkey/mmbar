# -*- coding: utf-8 -*-
import datetime
import urllib.error
import urllib.request
import metar


class WeatherWidget(object):
    full_text = ""
    uri = "http://weather.noaa.gov/pub/data/observations/metar/stations/"\
          "{icao}.TXT"

    def __init__(self, icao_code, interval=300):
        self.icao_code = icao_code
        self.interval = interval
        self.last_run = None

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            uri = self.uri.format(icao=self.icao_code)
            try:
                r = urllib.request.urlopen(uri)
                w = metar.parse(r.read().decode('utf-8'))

                self.last_run = datetime.datetime.now()
                self.full_text = '{weather}, {temperature}°C'.format(
                    weather=w.conditions or w.cover or "fair",
                    temperature=w.temperature)
            except:
                pass

        if len(self.full_text) > 0:
            return {
                'name': "weather",
                'full_text': self.full_text,
                'color': '#c3bf9f',
                'icon': 'temp.xbm',
            }
