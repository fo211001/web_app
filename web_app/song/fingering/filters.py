#-*- coding: utf-8 -*-
from web_app.song.chord import shift_tone


class AppFilter(object):

    def filter(self, fingering):
        pass


class DistFilter(AppFilter):
    max_dist = None

    def __init__(self, dist):
        self.max_dist = dist

    def filter(self, fingering):
        is_good = True
        for i, c in enumerate(fingering):
            for j in xrange(i+1, len(fingering)):
                if not (c == 'x' or fingering[j] == 'x'):
                    if abs(int(c) - int(fingering[j])) > self.max_dist:
                        is_good = False
        return is_good


class OnlyBarreFilter(AppFilter):
    notes = []

    def __init__(self, notes):
        self.notes = notes

    def filter(self, fingering):
        is_barre = False
        probably_indexes_barre = []
        for i, c in enumerate(fingering):
            for j in xrange(i+1, len(fingering)):
                if c == fingering[j]:
                    probably_indexes_barre.append(c)
        for index_barre in probably_indexes_barre:
            if index_barre == min(*fingering):
                is_barre = True
        if is_barre:
            count = 0
            for i in fingering:
                if i != min(*fingering) and i != 'x':
                    count += 1
            if count != len(self.notes):
                is_barre = False
        return is_barre


class WithoutBarreFilter(AppFilter):
    notes = []

    def __init__(self, notes):
        self.notes = notes

    def filter(self, fingering):
        barre = OnlyBarreFilter(self.notes)
        if not barre.filter(fingering):
            count = CountOfFingersFilter()
            return count.filter(fingering)
        else:
            return False


class OnlyAllCordsFilter(AppFilter):

    def filter(self, fingering):
        for chord in fingering:
            if chord == 'x':
                return False
        return True


class WithoutCordsFilter(AppFilter):
    without_cords = []

    def __init__(self, cords):
        self.without_cords = cords

    def filter(self, fingering):
        is_good = True
        for i, chord in enumerate(fingering):
            if i in self.without_cords:
                if not chord == 'x':
                    is_good = False
        return is_good


class AllNotesNeededFilter(AppFilter):
    line_up = ["E", "H", "G", "D", "A", "E"]
    notes = None

    def __init__(self, notes):
        self.notes = notes

    def filter(self, fingering):
        played_notes = [shift_tone(self.line_up[i], int(tune)) for i, tune in enumerate(fingering) if tune != 'x']
        return set(played_notes) == set(self.notes)


class CountOfFingersFilter(AppFilter):

    def __init__(self, max_count_of_fingers=4):
        self.max_count_of_fingers = max_count_of_fingers

    def filter(self, fingering):
        count = 0
        for chord in fingering:
            if chord != 'x':
                count += 1
        if count <= self.max_count_of_fingers:
            return True
        else:
            return False

