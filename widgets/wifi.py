import array
import fcntl
import socket
import struct


class WifiWidget(object):
    INTERFACE_MAXLEN = 16

    # these values come from linux/wireless.h (V22)
    ESSID_MAXLEN = 32
    SIOCGIWESSID = 0x8B1B

    def __init__(self, interface='wlan0'):
        self.interface = interface

    def essid(self):
        # danger: Python that is written like C :)
        # http://stackoverflow.com/a/14142016

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # allocate a buffer for the essid
        essid = array.array('b', b'\0' * self.ESSID_MAXLEN)
        eptr, elen = essid.buffer_info()

        # allocate and fill buffer for ioctl call
        request = array.array(
            'b',
            self.interface.ljust(self.INTERFACE_MAXLEN, '\0').encode('utf-8') +
            struct.pack('PHH', eptr, elen, 0))

        # make ioctl call; essid will be placed into essid buffer
        fcntl.ioctl(s.fileno(), self.SIOCGIWESSID, request)
        essid = essid.tobytes().rstrip(b'\0')

        if essid:
            return essid.decode('utf-8')
        return None

    def output(self):
        try:
            essid = self.essid()
        except:
            essid = None

        if essid:
            return {
                'name': "wifi",
                'instance': self.interface,
                'full_text': essid,
            }
