import mpd
import os.path


class MpdStatusWidget(object):
    def __init__(self, server, timeout=10):
        self.server = server
        self.timeout = timeout

        self._client = mpd.MPDClient()
        self._client.timeout = self.timeout
        self.connect()

    def connect(self):
        self._client.connect(self.server, 6600)

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

    def output(self):
        try:
            song = self._client.currentsong()
        except (mpd.MPDError, mpd.ConnectionError, IOError):
            # attempt to reconnect and fetch song title again
            try:
                self.disconnect()
                self.connect()
                song = self._client.currentsong()
            except (mpd.MPDError, mpd.ConnectionError, IOError, OSError):
                return

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
                'full_text': ' ' + text,
                'color': '#8cd0d3',
                'icon': 'note.xbm',
            }
        else:
            return
