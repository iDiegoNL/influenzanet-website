from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User as DjangoUser
from models import EpiworkUser

"""
 Customize Backend
 Real user identity is handled by EpiworkUser
"""

class EpiworkAuthBackend(ModelBackend):
    
    def authenticate(self, username=None, password=None):
        try:
            user = EpiworkUser.objects.get(login=username)
            if user.check_password(password):
                
                try:
                    u = user.get_django_user()
                    u._epiwork_user = user # temporary store it in user
                    return u
                except DjangoUser.DoesNotExist:
                    return None
              
        except EpiworkUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return EpiworkUser.objects.get(pk=user_id)
        except EpiworkUser.DoesNotExist:
            return None


# Connect to auth login signal
def login_handler(sender,**kwargs):
    user = kwargs['user']
    request = kwargs['request']
    epiwork_user = user._epiwork_user
    request.session['epiwork_user'] = epiwork_user # store real user in session