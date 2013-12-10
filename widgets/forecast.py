# -*- coding: utf-8 -*-
import requests
import json
from widgets import base


class ForecastWidget(base.IntervalWidget):
    uri = "https://api.forecast.io/forecast/{api_key}/{lat},{lon}?units=si&"\
          "exclude=minutely,hourly,daily"

    def __init__(self, api_key, lat, lon, interval=300):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        super().__init__(interval)

    def get_output(self):
        uri = self.uri.format(
            api_key=self.api_key,
            lat=self.lat,
            lon=self.lon)
        try:
            r = requests.get(uri, verify=True)
            w = json.loads(r.text)
            text = '{weather}, {temperature}°C'.format(
                weather=w['currently']['summary'],
                temperature=round(w['currently']['temperature']))

            return {
                'name': "forecast",
                'instance': "{lat} {lon}".format(lat=self.lat, lon=self.lon),
                'full_text': text,
            }
        except:
            pass
