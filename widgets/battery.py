import os


class BatteryWidget(object):
    def __init__(self, device='BAT0', color_full='#7f9f7f',
                 color_low='#e37170'):
        self.device = device
        self.color_full = color_full
        self.color_low = color_low

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
                'full_text': str(charge_percent) + '%',
                'color': self.color_full,
                'icon': 'bat_full_01.xbm',
            }
        else:
            return {
                'name': "battery",
                'instance': self.device,
                'full_text': str(charge_percent) + '%',
                'color': self.color_low,
                'icon': 'bat_low_01.xbm',
            }
