from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    MyModel,
    )
from web_app.user import login, register


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
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    if "email" and "password" in request.POST:
        if login(request.POST['email'], request.POST['password']):
        #return {"email": login(request.POST['email'], request.POST['password'])}
            return {'status': "Login!"}
    return {}

@view_config(route_name='registration', renderer='templates/registration.jinja2')
def registration_view(request):
    if "name" and "email" and "password" in request.POST:
        if register(request.POST['name'], request.POST['email'], request.POST['password']):
            return {'status': "Register!"}
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

