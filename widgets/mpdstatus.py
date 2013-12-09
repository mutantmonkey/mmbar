import mpd
import os.path


class MpdStatusWidget(object):
    def __init__(self, server='localhost', port=6600, password=None,
                 timeout=10):
        self.server = server
        self.port = port
        self.password = password
        self.timeout = timeout

        self._client = mpd.MPDClient()
        self._client.timeout = self.timeout
        self.connected = False

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

    def output(self):
        if not self.connected:
            try:
                self.connect()
            except Exception as e:
                return {
                    'name': "mpdstatus",
                    'instance': self.server,
                    'full_text': str(e),
                    '_status': 'error',
                }

        try:
            song = self._client.currentsong()
        except (mpd.MPDError, mpd.ConnectionError, IOError):
            # disconnect, will attempt again on next refresh
            self.disconnect()
            song = None

        if song:
            if 'artist' in song and 'title' in song:
                text = "{artist} - {title}".format(**song)
            elif 'name' in song:
                text = song['name']
            else:
                text = os.path.basename(song['file'])

            return {
                'name': "mpdstatus",
                'instance': self.server,
                'full_text': text[:100],
                '_status': 'normal',
            }
