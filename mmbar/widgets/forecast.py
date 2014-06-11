# -*- coding: utf-8 -*-
import json
import requests
import time
from mmbar.widgets import base


class ForecastWidget(base.Widget):
    uri = "https://api.forecast.io/forecast/{api_key}/{lat},{lon}?units=si&"\
          "exclude=minutely,hourly,daily"

    def __init__(self, api_key, lat, lon, interval=300):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.interval = interval
        super().__init__("forecast",
                         "{lat} {lon}".format(lat=self.lat, lon=self.lon))

    def run(self):
        uri = self.uri.format(api_key=self.api_key, lat=self.lat, lon=self.lon)

        while True:
            try:
                r = requests.get(uri, verify=True)
                w = json.loads(r.text)
                self.output['full_text'] = '{weather}, {temperature}°C'.format(
                    weather=w['currently']['summary'],
                    temperature=round(w['currently']['temperature']))
            except:
                pass

            time.sleep(self.interval)
