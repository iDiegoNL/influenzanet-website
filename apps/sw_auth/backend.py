from django.contrib.auth.backends import ModelBackend

from .models import EpiworkUser, FakedUser
from django.contrib.auth.models import User as DjangoUser
from .logger import auth_notify

"""
 Customize Backend
 Real user identity is handled by EpiworkUser
"""

class EpiworkAuthBackend(ModelBackend):
    
    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):
        try:
            auth_notify('authenticate', "check for %s" % username)
            user = EpiworkUser.objects.get(login=username)
            if user.check_password(password):
                try:
                    u = user.get_django_user()
                    print u
                    auth_notify('auth_success',"success login '%s" % username )
                    u._epiwork_user = user # temporary store it in user
                    return u
                except DjangoUser.DoesNotExist:
                    return None
            else:
                auth_notify('auth_failure',"bad password for '%s'" % username)
              
        except EpiworkUser.DoesNotExist:
            auth_notify('auth_unknown',"user '%s' not found " % username)
            return None

    def get_user(self, user_id):
        """
         user_id is here the user if stored by django and refer to User of Django Model
        """
        try:
            return FakedUser.objects.get(pk=user_id)
        except FakedUser.DoesNotExist:
            return None
