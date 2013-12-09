import datetime
import requests
import json


class Coinbase(object):
    full_text = ""
    uri = "https://coinbase.com/api/v1/currencies/exchange_rates"

    def __init__(self, currency, interval=60):
        self.currency = currency
        self.interval = interval
        self.last_run = None

    def output(self):
        if not self.last_run or datetime.datetime.now() >= \
                self.last_run + datetime.timedelta(seconds=self.interval):
            try:
                r = requests.get(self.uri)
                w = json.loads(r.text)

                self.last_run = datetime.datetime.now()
                self.full_text = '${amount:.2f}'.format(
                    amount=float(w[self.currency]))
            except:
                pass

        if len(self.full_text) > 0:
            return {
                'name': "coinbase",
                'full_text': self.full_text,
            }
