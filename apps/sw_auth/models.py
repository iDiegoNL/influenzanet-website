from django.db import models
from django.contrib.auth.models import get_hexdigest, check_password, User

import utils
from apps.sw_auth.utils import create_token

class EpiworkUser(models.Model):
    user = models.CharField(max_length=255) # encrypted user name in auth_user
    email = models.CharField(max_length=255) # encrypted email
    login = models.CharField(max_length=255) # 
    password = models.CharField(max_length=128) # sha1 hash
    token_password = models.CharField(40)
    token_activate = models.CharField(40)
    is_active = models.BooleanField()
    
    # Get the user login
    def get_user(self):
        return self.user

    def set_password(self, raw_password):
        if raw_password is None:
            self.set_unusable_password()
        else:
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.password = '%s$%s$%s' % (algo, salt, hsh)

    def check_password(self, raw_password):
        check_password(raw_password, self.password)
        
    def get_django_user(self):
        username = self.get_user()
        return User.objects.get(username=username)

    def create_token_password(self):
        token = create_token()
        self.token_password = token
        self.save()
        return token