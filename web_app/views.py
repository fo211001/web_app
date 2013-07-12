#coding: utf-8
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.request import Request
from pyramid.response import Response, FileResponse
from pyramid.security import remember, authenticated_userid, forget
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    User,
    WebSong,
    login,
    register
)

from song.chord import all_chord_tones
from song.parse import parse_text
from song.text import song_text
from song.chord import musicals
from song.fingering.filters import (AllNotesNeededFilter, CountOfFingersFilter,
                                    DistFilter, OnlyBarreFilter, TunesFilter, WithCordsFilter, WithoutBarreFilter)
from song.fingering import iterate_fingerings
from song.drawer import image_fingering




@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


def auth_required(func):
    def wrapper(request):
        owner = authenticated_userid(request)
        if owner is None:
            raise HTTPForbidden()
        return func(request)

    return wrapper


@view_config(route_name='about', renderer='templates/about.jinja2')
def about_view(request):
    return {'About': "us"}


@view_config(route_name='chords', renderer='templates/chords.jinja2')
def chords_view(request):
    return {}


def get_current_user(request):
    id_= authenticated_userid(request)
    # import pdb; pdb.set_trace()
    session = DBSession()

    return session.query(User).get(id_)


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    nxt = request.params.get('next') or request.route_url('home')
    did_fail = False
    if 'email' in request.POST:
        #LOGIN PROCESSING
        user = login(request.POST["email"], request.POST["password"])
        if user:
            headers = remember(request, user.id)
            return HTTPFound(location=nxt, headers=headers)
        else:
            did_fail = True
    return {
        'login': "",
        'next': nxt,
        'failed_attempt': did_fail,
    }


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


@view_config(route_name='favicon')
def favicon_view(request):
    headers = forget(request)
    return HTTPFound(location='/static/images/favicon.ico', headers=headers)


@view_config(route_name='registration', renderer='templates/registration.jinja2')
def registration_view(request):
    nxt = request.params.get('next') or request.route_url('home')
    did_fail = False
    if 'email' in request.POST:
        user = register(request.POST["name"], request.POST["email"], request.POST["password"])
        if user:
            headers = remember(request, user.id)
            return HTTPFound(location=nxt, headers=headers)
        else:
            did_fail = True
    return {
        'login': "",
        'next': nxt,
        'failed_attempt': did_fail,
    }


@view_config(route_name='add', renderer='templates/add.jinja2')
@auth_required
def add_view(request):
    if "text" in request.POST:
        song = parse_text(request.POST['text'])
        web_song = WebSong(song=song, title=request.POST['title'])
        user = get_current_user(request)
        user.songs.append(web_song)
        DBSession().commit()
        return HTTPFound(location='/edit/{}'.format(web_song.id))
    return {}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
@auth_required
def edit_view(request):
    try:
        song_id = request.matchdict['song_id']
        web_song = DBSession().query(WebSong).get(song_id)
        if "song_text" in request.POST:
            song = parse_text(request.POST["song_text"])
            song.base_chord = request.POST["base_chord"]
            web_song.song = song
            web_song.title = request.POST["title"]
            # import pdb; pdb.set_trace()
            if authenticated_userid(request) != web_song.user_id:
                raise HTTPForbidden()
            DBSession().commit()
        if "delete_song" in request.POST:
            song_delete(song_id)
            return HTTPFound(location='/')
        return {'song_text': song_text(web_song.song, web_song.song.base_chord), 'song_title': web_song.title, 'tones':all_chord_tones, 'base_chord': web_song.song.base_chord}
    except:
        return HTTPFound(location='/')

@view_config(route_name='home', renderer='templates/songs.jinja2')
@auth_required
def songs(request):
    user = get_current_user(request)
    return {'songs': user.songs, 'login': True}


def song_delete(song_id):
    web_song = DBSession().query(WebSong).get(song_id)
    DBSession().delete(web_song)
    DBSession().commit()

@view_config(route_name='fingering')
def generate_fingering(request):
    fingering = request.matchdict['name'].split(',')
    return FileResponse(image_fingering(fingering))

@view_config(route_name='chord', renderer='templates/chord.jinja2')
def filters_for_fingerings(request):
    puth = ""
    chord = request.matchdict['name']
    notes = musicals(chord)
    cords_set = []
    filters = []
    default_filt = AllNotesNeededFilter(notes)
    filters.append(default_filt)
    if 'go' in request.POST:
        if 'only_barre' in request.POST:
            barre_filt = OnlyBarreFilter(notes)
            filters.append(barre_filt)
        if 'without_barre' in request.POST:
            not_barre_filt = WithoutBarreFilter(notes)
            filters.append(not_barre_filt)
        if 'dist_text' in request.POST:
            dist = request.POST['dist_text']
            dist_filt = DistFilter(dist)
            filters.append(dist_filt)
        if 'first_cord' in request.POST:
            cords_set.append(0)
        if 'second_cord' in request.POST:
            cords_set.append(1)
        if 'third_cord' in request.POST:
            cords_set.append(2)
        if 'forth_cord' in request.POST:
            cords_set.append(3)
        if 'fifth_cord' in request.POST:
            cords_set.append(4)
        if 'sixth_cord' in request.POST:
            cords_set.append(5)
        if cords_set:
            cords_filt = WithCordsFilter(cords_set)
            filters.append(cords_filt)
        if 'max_count_fingers' in request.POST:
            count_fingers = request.POST['max_count_fingers']
            fingers_filt = CountOfFingersFilter(count_fingers)
            filters.append(fingers_filt)
        if 'min_tune' in request.POST and 'max_tune' in request.POST:
            min = request.POST['min_tune']
            max = request.POST['max_tune']
            tunes_filt = TunesFilter(min, max)
            filters.append(tunes_filt)
    return {
        "notes": notes,
        "fingerings": [",".join(map(unicode, x)) for x in iterate_fingerings(notes, filters)],
        "filters": filters,
         "puth": puth
    }

    conn_err_msg = """
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_web_app_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

