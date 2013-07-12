from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from .models import (
    DBSession,
    Base,
    )

#-----4444

def not_found(request):
    return HTTPNotFound('Not found, bro.')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    config = Configurator(
        settings=settings,
        authentication_policy=SessionAuthenticationPolicy())
    config.include("pyramid_beaker")
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("web_app:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('chord', '/chord/{name}')
    config.add_route('chords', '/chords')
    config.add_route('about', '/about')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('favicon', '/favicon')
    config.add_route('registration', '/registration')
    config.add_route('add', '/add')
    config.add_route('songs', '/songs')
    config.add_notfound_view(not_found, append_slash=True)
    config.scan()
    return config.make_wsgi_app()
