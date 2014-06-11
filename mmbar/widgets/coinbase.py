import json
import requests
import time
from mmbar.widgets import base


class Coinbase(base.Widget):
    uri = "https://coinbase.com/api/v1/currencies/exchange_rates"

    def __init__(self, currency, interval=60):
        super().__init__('coinbase', currency)
        self.currency = currency
        self.interval = interval

    def run(self):
        while True:
            try:
                r = requests.get(self.uri)
                w = json.loads(r.text)

                self.output['full_text'] = '${amount:.2f}'.format(
                    amount=float(w[self.currency]))
            except:
                pass

            time.sleep(self.interval)
