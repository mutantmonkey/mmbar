# -*- coding: utf-8 -*-
import datetime
import requests
import json


class ForecastWidget(object):
    full_text = ""
    uri = "https://api.forecast.io/forecast/{api_key}/{lat},{lon}?units=si&"\
          "exclude=minutely,hourly,daily"

    def __init__(self, api_key, lat, lon, interval=300):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.interval = interval
        self.last_run = None

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            uri = self.uri.format(
                api_key=self.api_key,
                lat=self.lat,
                lon=self.lon)
            try:
                r = requests.get(uri, verify=True)
                w = json.loads(r.text)

                self.last_run = datetime.datetime.now()
                self.full_text = ' {weather}, {temperature}°C'.format(
                    weather=w['currently']['summary'],
                    temperature=round(w['currently']['temperature']))
            except:
                pass

        if len(self.full_text) > 0:
            return {
                'name': "forecast",
                'full_text': self.full_text,
                'color': '#c3bf9f',
                'icon': 'temp.xbm',
            }
