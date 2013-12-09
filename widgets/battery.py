import os


class BatteryWidget(object):
    def __init__(self, device='BAT0'):
        self.device = device

    def output(self):
        if os.path.exists('/sys/class/power_supply/{dev}/energy_now'.
                          format(dev=self.device)):
            charge_now = int(open('/sys/class/power_supply/{dev}/energy_now'.
                                  format(dev=self.device)).read())
            charge_full = int(open('/sys/class/power_supply/{dev}/energy_full'.
                                   format(dev=self.device)).read())
        else:
            charge_now = int(open('/sys/class/power_supply/{dev}/charge_now'.
                                  format(dev=self.device)).read())
            charge_full = int(open('/sys/class/power_supply/{dev}/charge_full'.
                                   format(dev=self.device)).read())
        charge_percent = int(charge_now / charge_full * 100)

        if charge_percent > 15:
            return {
                'name': "battery",
                'instance': self.device,
                'full_text': str(charge_percent) + '%',
                '_status': 'normal',
            }
        else:
            return {
                'name': "battery",
                'instance': self.device,
                'full_text': str(charge_percent) + '%',
                '_status': 'warn',
            }
