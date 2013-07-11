
class Couplet(object):
    _song_parts = []
    def __init__(self, *args):
        self._song_parts = list(*args)

    @property
    def song_parts(self):
        "SongPart"
        return self._song_parts

