#coding: utf-8
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.request import Request
from pyramid.response import Response
from pyramid.security import remember, authenticated_userid, forget
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    MyModel,
    )
from web_app.user import login, register

from song.parse import parse_text
from user import User, WebSong
from song.text import song_text


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


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
@auth_required
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'web_app'}


@view_config(route_name='about', renderer='templates/about.jinja2')
def about_view(request):
    return {'About': "us"}


@view_config(route_name='chords', renderer='templates/chords.jinja2')
def chords_view(request):
    return {}


def get_current_user(request):
    id = authenticated_userid(request)
    session = DBSession()
    return session.query(User).get(id)


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    nxt = request.params.get('next') or request.route_url('home')
    email = ''
    did_fail = False
    if 'email' in request.POST:
        #LOGIN PROCESSING
        if login(request.POST["email"], request.POST["password"]):
            headers = remember(request, id)
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
    if "name" and "email" and "password" in request.POST:
        if register(request.POST['name'], request.POST['email'], request.POST['password']):
            return {'status': "зарегистрированы!".decode('utf-8')}
    return {}


@view_config(route_name='add', renderer='templates/add.jinja2')
def add_view(request):
    if "text" in request.POST:
        song = parse_text(request.POST['text'])
        web_song = WebSong(song=song, title=request.POST['title'])
        user = get_current_user(request)
        user.songs.append(web_song)
        DBSession().commit()
        return {'song': song_text(song, song.base_chord)}
    return {}

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

