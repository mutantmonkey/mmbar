import requests
import json
from widgets import base


class Coinbase(base.IntervalWidget):
    uri = "https://coinbase.com/api/v1/currencies/exchange_rates"

    def __init__(self, currency, interval=60):
        self.currency = currency
        super().__init__(interval)

    def get_output(self):
        try:
            r = requests.get(self.uri)
            w = json.loads(r.text)

            text = '${amount:.2f}'.format(amount=float(w[self.currency]))
            return {
                'name': "coinbase",
                'full_text': text,
            }
        except:
            pass
