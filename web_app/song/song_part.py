#-*- coding: utf-8 -*-

from song_chord import Chord


class SongPart(object):
    
    def __init__(self,  syllable="", chord=None):
        if not isinstance(chord, Chord) and chord is not None:
            raise TypeError("chord reequired, `{}` given".format(chord))
        self._chord = chord
        self._syllable = syllable

    def __repr__(self):
        if not self.chord:
            return self.syllable
        return u"{}:{}".format(self.syllable, self.chord)
        
    @property
    def chord(self):
        return self._chord
    
    @property
    def syllable(self):
        if isinstance(self._syllable, unicode):
            return self._syllable
        return unicode(self._syllable, 'utf-8')

    @property
    def is_space(self):
        return not len(self.syllable)


class Space (SongPart):
    def __init__(self):
        super(Space, self).__init__(" ")

    @property
    def is_space(self):
        return True


class EndOfLine (SongPart):
    def __init__(self):
        super(EndOfLine, self).__init__("\n")

    @property
    def is_space(self):
        return True