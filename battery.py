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
                'full_text': ' ' + str(charge_percent) + '%',
                'color': '#87af87',
                'icon': '.config/dzen/icons/bat_full_01.xbm',
            }
        else:
            return {
                'full_text': ' ' + str(charge_percent) + '%',
                'color': '#a36666',
                'icon': '.config/dzen/icons/bat_low_01.xbm',
            }
