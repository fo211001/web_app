from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    MyModel,
    )



@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
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
    return


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    email = request.matchdict['email']
    return {'email': email}




# @view_config(route_name='chord',renderer='templates/chord.pt')
# def chord_view(request):
#     matchdict = request.matchdict
#     chord = matchdict.get('name', None)
#     notes = musicals(chord)
#     dictionary = {
#         'a': 'Aaa',
#         'foo': 'Foo!'
#     }
#
#     return {'Chord': str(chord), 'dict': dictionary}
#         # Response("Chord:" + str("\n") +
#         #             "\r|\n".join((",".join((unicode(z) for z in x)) for x in iterate_fingerings(notes))))




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

