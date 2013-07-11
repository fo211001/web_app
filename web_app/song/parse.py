#-*- coding: utf-8 -*-

from song_part import SongPart, EndOfLine
from song_chord import Chord
from song import Song
from couplet import Couplet
from chord import get_tone, is_chord, normal_view, parse_chord, semitone_distance, all_chords

vowels = [u'а', u'е', u'ё', u'и', u'о', u'у', u'ы', u'э', u'ю', u'я',
          u'А', u'Е', u'Ё', u'И', u'О', u'У', u'Ы', u'Э', u'Ю', u'Я']


def parse_text(text):
    """
    Парсим из текста песни с аккордами в пересенную класса Song
    :param text:
    :return:
    """
    text = text.replace(u'\ufeff', '')
    list_of_couplets_text = parse_to_couplet_text(text)
    list_of_couplets = []
    list_of_couplets_tokens = []

    for i in list_of_couplets_text:
        list_of_strings = []
        for line in i.splitlines():
            tokens = list(tokenize(line))
            list_of_strings.append(tokens)
        list_of_couplets_tokens.append(list_of_strings)

    base_chord = get_base_chord(list_of_couplets_tokens)

    for couplet in list_of_couplets_tokens:
        chorded_list = []
        for tokens in couplet:
            optimized = list(make_chords(base_chord, tokens))
            optimized = optimize_tokens(optimized)
            chorded_list.append(optimized)
        list_of_couplets.append(Couplet(list(create_couplet(chorded_list))))

    song = Song(base_chord, list_of_couplets)

    return song


def get_base_chord(list_of_couplets_tokens):
    for couplet in list_of_couplets_tokens:
        for tokens in couplet:
            for token, pos in tokens:
                chord = token.split("/")
                if len(chord) > 1 and chord[1] != "9":
                    if chord[0].lower() in chord:
                        return get_tone(chord[0])
                else:
                    if token.lower() in all_chords:
                        return get_tone(token)

    return None


def parse_to_syl(word):
    listSyllables = []
    temp_str = ""
    for i in word:
        if i in vowels:
            temp_str += i
            listSyllables.append(temp_str)
            temp_str = ""
        else:
            temp_str += i
            if i == word[-1] or i == '-':
                if not len(listSyllables) == 0:
                    last_syl = listSyllables.pop()
                else:
                    last_syl = ""
                listSyllables.append(last_syl + temp_str)
                temp_str = ""

    return listSyllables


def parse_to_couplet_text(song):
    list_couplets = []
    couplet = ""
    i = 0
    while i < len(song):
        if song[i] == "\n" or song[i] == "\r\n" or song[i] == "\n\r":
            couplet += song[i]
            if i+1 < len(song):
                if song[i+1] == "\n" or song[i+1] == "\r\n":
                    if not couplet == "":
                        list_couplets.append(couplet)
                        couplet = ""
        else:
            couplet += song[i]
        i += 1
    if not couplet == "":
        list_couplets.append(couplet)
    return list_couplets


def parse_to_list_of_string(base_chord, string):
    """
    принимаем куплет в виде строки, возвращаем список списков, в которых хранятся или аккорды или слоги
    :param base_chord:
    :param string:
    """
    list_of_strings = []
    for i in string.splitlines():
        tokens = tokenize(i)
        list_of_strings.append(list(make_chords(base_chord, tokens)))
    return list_of_strings


def tokenize(string):
    index = 0
    word = []
    for i in string:
        if i.isspace():
            if word:
                yield ("".join(word), index - len(word))
            word = []
        else:
            word.append(i)
        index += 1

    yield ("".join(word), index - len(word))


def make_chords(base, tokens):
    for word, pos in tokens:
        if is_chord(word.lower()):
            chord, modif, add_note = parse_chord(word)
            chord = normal_view(chord)
            distance = semitone_distance(base, chord)
            if add_note:
                add_distance = semitone_distance(chord, add_note)
            else:
                add_distance = 0
            yield (Chord(distance, modif, add_distance), pos)
        else:
            yield (word, pos)


def optimize_tokens(tokens):
    """
    Ожидаем что tokens - это пары (Chord, position) или (Str, position)
    :param tokens:
    """
    if chords_only(tokens):
        return [(chord, pos) for chord, pos in tokens if isinstance(chord, Chord)]
    else:
        optimized_tokens = []

        for word, pos in tokens:
            if isinstance(word, Chord):
                optimized_tokens.append((word, pos))
            elif not word.isspace() and word:
                if optimized_tokens:
                    optimized_tokens.append((" ", pos-1))
                for syl in parse_to_syl(word):
                    optimized_tokens.append((syl, pos))
                    pos += len(syl)

        return optimized_tokens


def create_couplet(list_of_string):
    i = 0
    while i < len(list_of_string):
        string = list_of_string[i]
        if chords_only(string) and i+1 < len(list_of_string):
            if not chords_only(list_of_string[i+1]):
                for part in join_chords(string, list_of_string[i+1]):
                    yield part
                i += 1
            else:
                for part in join_chords(string, [("", 0)]):
                    yield part

        else:
            for part in parts_of_string(string):
                yield part
        i += 1


def parts_of_string(string):
    for part, pos in string:
        if isinstance(part, Chord):
            yield SongPart(chord=part)
        else:
            yield SongPart(part)

    yield EndOfLine()


def chords_only(string):
    """
    Проверяем, в строке только аккорды?
    :param string:
    :return: False - если в строке есть что-нибудь кроме аккордов,
    иначе True
    """
    for chord, pos in string:
        if not isinstance(chord, Chord) and not chord.isspace() and chord:
            return False
    return len(string)


def join_chords(chords, words):
    i, j = 0, 0
    while i < len(chords) and j < len(words):
        chord, word = chords[i], words[j]
        cpos, wpos, wlen = chord[1], word[1], len(word[0])
        if cpos >= wpos and cpos < (wpos + wlen):
            j += 1
            i += 1
            yield SongPart(word[0], chord[0])

        elif cpos < wpos:
            i += 1
            yield SongPart("", chord[0])
        elif cpos >= wpos+wlen:
            j += 1
            yield SongPart(word[0])

    while i < len(chords):
        yield SongPart("", chords[i][0])
        i += 1

    while j < len(words):
        yield SongPart((words[j])[0])
        j += 1

    yield EndOfLine()


