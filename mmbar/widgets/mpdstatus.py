import mpd
import os.path
import time
from mmbar.widgets import base


class MpdStatusWidget(base.Widget):
    def __init__(self, server='localhost', port=6600, password=None,
                 timeout=10, interval=2):
        self.server = server
        self.port = port
        self.password = password
        self.timeout = timeout
        self.interval = interval

        self._client = mpd.MPDClient()
        self._client.timeout = self.timeout
        self.connected = False

        super().__init__('mpdstatus', '{0}:{1}'.format(server, port))

    def connect(self):
        self._client.connect(self.server, self.port)
        if self.password:
            self._client.password(self.password)
        self.connected = True

    def disconnect(self):
        # we can safely ignore errors if this fails
        try:
            self._client.close()
        except (mpd.MPDError, IOError):
            pass

        try:
            self._client.disconnect()
        except:
            self._client = mpd.MPDClient()
            self._client.timeout = self.timeout

        self.connected = False

    def update_currentsong(self):
        song = self._client.currentsong()
        if song:
            if type(song['artist']) == list:
                song['artist'] = ', '.join(song['artist'])

            if 'artist' in song and 'title' in song:
                text = "{artist} - {title}".format(**song)
            elif 'title' in song:
                text = song['title']
            elif 'name' in song:
                text = song['name']
            else:
                text = os.path.basename(song['file'])

            self.output.update({
                'full_text': text[:100],
                '_status': 'normal',
            })
        else:
            self.output['full_text'] = None

    def run(self):
        while True:
            if not self.connected:
                try:
                    self.connect()
                except Exception as e:
                    self.output.update({
                        'full_text': str(e),
                        '_status': 'error',
                    })
                    time.sleep(self.interval)
                    break

            try:
                self.update_currentsong()
                self._client.idle('player')
            except (mpd.MPDError, mpd.ConnectionError, IOError):
                # disconnect, will attempt again on next refresh
                self.disconnect()
                time.sleep(self.interval)
