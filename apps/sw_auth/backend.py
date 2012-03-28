from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User as DjangoUser
from models import EpiworkUser

"""
 Customize Backend
 Real user identity is handled by EpiworkUser
"""

class CustomModelBackend(ModelBackend):
    
    def authenticate(self, username=None, password=None):
        try:
            user = EpiworkUser.objects.get(login=username)
            if user.check_password(password):
                
                try:
                    u = user.get_django_user()
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

