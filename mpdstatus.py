import mpd
import os.path


class MpdStatusWidget(object):
    def __init__(self, server, timeout=10):
        self.server = server
        self.client = mpd.MPDClient()
        self.client.timeout = timeout
        self.client.connect(server, 6600)

    def output(self):
        try:
            song = self.client.currentsong()
        except:
            pass

        if song:
            if 'artist' in song and 'title' in song:
                text = "{artist} - {title}".format(**song)
            else:
                text = os.path.basename(song['file'])

            return {
                'name': "mpdstatus",
                'instance': self.server,
                'full_text': ' ' + text,
                'color': '#8cd0d3',
                'icon': 'mmbar/icons/note.xbm',
            }
        else:
            pass
