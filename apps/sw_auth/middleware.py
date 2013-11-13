from django.contrib.auth import get_user
from .logger import auth_notify

"""
Authentication Midlleware
"""

class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        u = get_user(request)
        try:
            e = request.session['epiwork_user']
            e.personalize(u)
            auth_notify('middleware', u.username)
        except KeyError:
            pass
            
        request.user = u
        return None
