from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from .models import (
    DBSession,
    Base,
    )

#-----44

def notfound(request):
    return HTTPNotFound('Not found, bro.')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("web_app:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('chord', '/chord/{name}')
    config.add_route('chords', '/chords')
    config.add_route('about', '/about')
    config.add_route('newsong', '/newsong')
    config.add_route('login', '/login/{email}')
    config.add_notfound_view(notfound, append_slash=True)
    config.scan()
    return config.make_wsgi_app()
