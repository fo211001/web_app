from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.renderers import render
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    MyModel,
    )
from song.chord import parse_chord, musicals
from song.drawer import image_fingering
from song.fingering import iterate_fingerings


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'web_app'}


@view_config(route_name='about',renderer='templates/about.jinja2')
def about_view(request):
    return {"hello":"world"}
#
# @view_config(route_name='login')
# def login_view(request):




@view_config(route_name='chords')
def chords_view(request):
    result = render('templates/chords.pt', {}, request=request)
    response = Response(result)
    return response


@view_config(route_name='newsong')
def newsong_view(request):
    return Response("New")


@view_config(route_name='chord',renderer='templates/chord.pt')
def chord_view(request):
    matchdict = request.matchdict
    chord = matchdict.get('name', None)
    notes = musicals(chord)
    dictionary = {
        'a': 'Aaa',
        'foo': 'Foo!'
    }

    return {'Chord': str(chord), 'dict': dictionary}
        # Response("Chord:" + str("\n") +
        #             "\r|\n".join((",".join((unicode(z) for z in x)) for x in iterate_fingerings(notes))))




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

