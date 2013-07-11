#-*- coding: utf-8 -*-
from song_part import EndOfLine
from chord import get_tone, shift_tone


def chord_text(base, chord):
    "Возвращаем название аккорда"
    try:
        tone = shift_tone(get_tone(base), chord.distance)
        if chord.add_tone:
            return tone + chord.modification + "/" + shift_tone(tone, chord.add_tone)
        else:
            return tone + chord.modification
    except AttributeError as error:
        print "Broken on {}\n{}".format(chord, base)


def couplet_text(couplet, main_chord):
    """:param couplet - объект Couplet, состоящий из объектов SongPart,
     который будет равен слогу(syllable) или аккорду(chord)
     :param main_chord - главный аккорд песни,
     необходим для определения названия аккорда
     :return lines - строки куплета,
     состоят из строк аккодов и строк слогов"""
    string_chords = []
    string_words = []
    lines = []
    for i, part in enumerate(couplet.song_parts):
        if isinstance(part, EndOfLine):
            chords = "".join(string_chords)
            if not chords.isspace() and chords:
                lines.append(chords)
            words = "".join(string_words)
            if not words.isspace() and words:
                lines.append(words)
            string_chords = []
            string_words = []
            continue

        syl = part.syllable
        chord = part.chord
        chord_str = ""
        if chord:
            next_part = couplet.song_parts[i+1]
            if next_part.chord:
                chord_str = chord_text(main_chord, chord) + " "
            else:
                chord_str = chord_text(main_chord, chord)
        if len(chord_str) > len(syl):
            if i+1 < len(couplet.song_parts):
                if syl == '':
                    sep = " "
                else:
                    next_part = couplet.song_parts[i+1]
                    if next_part.chord:
                        sep = "-" if not next_part.is_space else " "
                    else:
                        sep = ""
                        string = ""
                        for j, st in enumerate(chord_str):
                            if j != len(chord_str) - 1:
                                string += st
                        chord_str = string
            else:
                sep = ""
            syl += sep * (len(chord_str) - len(syl))
        else:
            chord_str += " " * (len(syl) - len(chord_str))
        string_chords.append(chord_str)
        string_words.append(syl)
    return "\r\n".join(lines)


def print_song(song, base_chord):
    return "\r\n".join([couplet_text(i, base_chord) for i in song.couplets])
