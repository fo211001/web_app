#-*- coding: utf-8 -*-

from itertools import product


all_chord_types = {
    "": (0, 4, 7),
    "7sus2": (0, 2, 7),
    "m": (0, 3, 7),
    "7": (0, 4, 8, 11),
    "m7": (0, 3, 7, 10),
    "maj7": (0, 4, 7, 11),
    "m+7": (0, 3, 7, 11),
    "m7b5": (0, 3, 6, 10),
    "dim7": (0, 3, 6, 9),
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),
    "7sus4": (0, 5, 7, 10),
    "sus": (0, 5, 7),
    "5": (0, 5),
    "dim": (0, 3, 6),
    "6": (0, 4, 7, 16),
    "m6": (0, 3, 7, 16),
    "6/9": (0, 4, 7, 11, 16),
    "m6/9": (0, 3, 7, 16, 30),
    "9": (0, 4, 7, 10),
    "11": (0, 4, 7, 10, 14, 17),
    "13": (0, 4, 7, 10, 14, 19),
    "add9": (0, 4, 7, 21),
    "madd9": (0, 4, 7, 21)
}


all_chord_tones = ["A", "B", "H", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

all_chords = set([u"{}{}".format(x, y).lower() for x, y in product(all_chord_tones, all_chord_types.keys())])

tones_indexed = {x: i for i, x in enumerate(all_chord_tones)}

sin_tones = {"Ab": 11, "Bb": 0, "Hb": 1, "Cb": 2, "Db": 4, "Eb": 6, "Fb": 7, "Gb": 9,
             "A#": 1, "B#": 2, "H#": 3, "E#": 8}

sin_chord_tones = sin_tones.keys()

all_sin = set(["{}{}".format(x, y).lower() for x, y in product(sin_chord_tones, all_chord_types.keys())])


def is_chord(chord_string):
    chord_and_add_note = chord_string.split("/")
    if len(chord_and_add_note) > 1:
        if len(chord_and_add_note) > 2:
            return False
        add_tone = chord_and_add_note[1]
        if (
            add_tone not in map(lambda x: x.lower(), all_chord_tones) and
            add_tone not in map(lambda x: x.lower(), sin_tones.keys()) and
            add_tone != "9"
        ):
            return False
    return chord_and_add_note[0] in all_chords or chord_and_add_note[0] in all_sin


def normal_view(chord_string):
    if chord_string.lower() in all_chords:
        return chord_string
    else:
        converted_tone = all_chord_tones[sin_tones[get_tone(chord_string)]]
        return converted_tone + get_modif(chord_string)

def get_all_chord_tones():
    return all_chord_tones

def get_tone(chord):
    return parse_chord(chord)[0]


def get_modif(chord):
    return parse_chord(chord)[1]

def get_add_note(chord):
    return parse_chord(chord)[2]


def parse_chord(chord):
    """
    :param chord: Принимаем строку, которая является аккордом
    :return: Тьюпл, 1-й элемент - тон аккорда, 2-й - модификация, 3-й - дополнительная нота
    """
    tone, mod, add = None, None, None
    parts = chord.split("/")
    if len(parts) > 1:
        if parts[1] != "9":
            add = parts[1]
            chord = parts[0]

    if len(chord) > 1 and chord[1] in "#b":
        tone = chord[:2]
        mod = chord[2:]
    else:
        tone = chord[:1]
        mod = chord[1:]

    return tone, mod, add


def semitone_distance(first_chord, second_chord):
    "Возвращаем число полутонов от первого до 2-го аккорда"
    dist = (tones_indexed[get_tone(normal_view(second_chord))] - tones_indexed[get_tone(normal_view(first_chord))]) % 12
    if dist < 0:
        dist += 12
    return dist


def shift_tone(base_tone, distance):
    t = (tones_indexed[base_tone] + distance) % 12
    return all_chord_tones[t]


def musicals(chord):
    """Принимаем аккорд с модификацией, тоном и дополнительной нотой,
    и возвращаем ноты аккорда.
    :param chord:
    """
    tone, mod, note = parse_chord(chord)
    if note:
        dist = semitone_distance(tone, note)
        all_chord_types[mod] = list(all_chord_types[mod])
        all_chord_types[mod].append(dist)                         # добавляем ноту к модификации
        tuple(all_chord_types[mod])
    return [shift_tone(tone, x) for x in all_chord_types[mod]]