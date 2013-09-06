class BatteryWidget(object):
    def __init__(self, device='BAT0'):
        self.device = device

    def output(self):
        charge_now = int(open('/sys/class/power_supply/{dev}/charge_now'.\
                format(dev=self.device)).read())
        charge_full = int(open('/sys/class/power_supply/{dev}/charge_full'.\
                format(dev=self.device)).read())
        charge_percent = int(charge_now / charge_full * 100)

        if charge_percent > 15:
            return {
                'name': "battery",
                'full_text': ' ' + str(charge_percent) + '%',
                'color': '#7f9f7f',
                'icon': 'bat_full_01.xbm',
            }
        else:
            return {
                'name': "battery",
                'instance': self.device,
                'full_text': ' ' + str(charge_percent) + '%',
                'color': '#e37170',
                'icon': 'bat_low_01.xbm',
            }
