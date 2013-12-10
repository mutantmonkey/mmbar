# -*- coding: utf-8 -*-
import urllib.error
import urllib.request
import metar
from widgets import base


class WeatherWidget(base.IntervalWidget):
    uri = "http://weather.noaa.gov/pub/data/observations/metar/stations/"\
          "{icao}.TXT"

    def __init__(self, icao_code, interval=300):
        self.icao_code = icao_code
        super().__init__(interval)

    def get_output(self):
        uri = self.uri.format(icao=self.icao_code)
        try:
            r = urllib.request.urlopen(uri)
            w = metar.parse(r.read().decode('utf-8'))
            text = '{weather}, {temperature}°C'.format(
                weather=w.conditions or w.cover or "fair",
                temperature=w.temperature)

            return {
                'name': "weather",
                'instance': self.icao_code,
                'full_text': text,
            }
        except:
            pass
