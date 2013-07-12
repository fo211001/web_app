from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.security import authenticated_userid, remember, forget
from pyramid.view import view_config, forbidden_view_config
from user import login


def auth_required(func):
    def wrapper(request):
        owner = authenticated_userid(request)
        if owner is None:
            raise HTTPForbidden()
        return func(request)
    return wrapper


@view_config(route_name='favicon')
def favicon_view(request):
    headers = forget(request)
    return HTTPFound(location='/static/images/favicon.ico', headers=headers)


@view_config(route_name='home', renderer='admin-index.pmt')
@auth_required
def my_view(request):  # pylint: disable=W0613
    return {}


@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


@view_config(route_name='login', renderer='login.pmt')
def login_view(request):
    nxt = request.params.get('next') or request.route_url('home')
    email = ''
    did_fail = False
    if 'submit' in request.POST:
        #LOGIN PROCESSING
        if login(request.POST["email"], request.POST["password"]):
            headers = remember(request, email)
            return HTTPFound(location=nxt, headers=headers)

    return {
        'login': "",
        'next': nxt,
        'failed_attempt': did_fail,
    }
