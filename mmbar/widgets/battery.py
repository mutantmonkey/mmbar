import time
from mmbar.widgets import base


class BatteryWidget(base.Widget):
    def __init__(self, device='BAT0', interval=6):
        super().__init__('battery', device)
        self.device = device
        self.interval = interval

    def run(self):
        capacity_path = '/sys/class/power_supply/{dev}/capacity'.format(
            dev=self.device)

        while True:
            charge_percent = int(open(capacity_path).read())
            if charge_percent > 100:
                charge_percent = 100

            self.output['full_text'] = str(charge_percent) + '%' 

            if charge_percent > 15:
                self.output['_status'] = 'normal'
            else:
                self.output['_status'] = 'warn'

            time.sleep(self.interval)
