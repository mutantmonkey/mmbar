import mpd


class MpdStatusWidget(object):
    def __init__(self, server, timeout=10):
        self.server = server
        self.client = mpd.MPDClient()
        self.client.timeout = timeout
        self.client.connect(server, 6600)

    def output(self):
        song = self.client.currentsong()
        if song:
            return {
                'name': "mpdstatus",
                'instance': self.server,
                'full_text': ' {artist} - {title}'.format(**song),
                'color': '#8cd0d3',
                'icon': 'mmbar/icons/note.xbm',
            }
        else:
            pass
