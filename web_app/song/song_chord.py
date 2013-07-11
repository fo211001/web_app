#-*- coding: utf-8 -*-


class Chord(object):
    def __init__(self, dist, modif="", add_note=None):
        self._distance = dist
        self._modification = modif
        self._add_note = add_note

    def __repr__(self):
        return u"{}.{}".format(self.distance, self.modification)
        
    @property
    def distance(self):
        return self._distance
    
    @property
    def modification(self):
        return self._modification

    @property
    def add_tone(self):
        return self._add_note


