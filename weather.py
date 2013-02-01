# -*- coding: utf-8 -*-
import datetime
import urllib.request
import metar


class WeatherWidget(object):
    def __init__(self, icao_code, interval=900):
        self.icao_code = icao_code
        self.interval = interval
        self.last_run = None

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            uri = 'http://weather.noaa.gov/pub/data/observations/metar/stations/'\
                    '{0}.TXT'.format(self.icao_code)
            r = urllib.request.urlopen(uri)
            w = metar.parse(r.read().decode('utf-8'))

            self.last_run = datetime.datetime.now()
            self.full_text = ' {weather}, {temperature}°C'.format(
                    weather=w.conditions or w.cover,
                    temperature=w.temperature)

        return {
            'full_text': self.full_text,
            'icon': '.config/dzen/icons/temp.xbm',
        }
