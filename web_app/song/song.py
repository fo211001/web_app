#-*- coding: utf-8 -*-

class Song(object):

    def __init__(self, base_chord, couplets=None):
        self._couplets = couplets or []
        self._base_chord = base_chord
     
    @property
    def couplets (self):
        "Возвращает список из объектов Couplet"
        return self._couplets 

    @property
    def base_chord (self):
        "Возвращает объект Chord"
        return self._base_chord

    @base_chord.setter
    def base_chord (self, value):
        self._base_chord = value
