from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import get_hexdigest, check_password, User
from django.db import transaction
import utils

from apps.sw_auth.utils import create_token

class EpiworkUserManager(models.Manager):
    
    @transaction.commit_manually()
    def create_user(self, login, email, password):
        user = EpiworkUser()
        user.login = login
        user.email = email
        user.set_password(password)
        
        # Create a random username and a fake email
        dj_username = utils.random_string(30)
        dj_email = "%s@localhost" % (dj_username,)
        
        user.set_user(dj_username)
       
        try:
            django_user = User.objects.create_user(dj_username, dj_email)
            django_user.is_active = False
            django_user.save()
            user.save()
            transaction.commit()
        except:
            transaction.rollback()
            raise 
        return user

class EpiworkUser(models.Model):
    user = models.CharField(_('username'),max_length=255) # encrypted user name in auth_user
    email = models.CharField(_('e-mail address'),max_length=255) # encrypted email
    login = models.CharField(_('username'),max_length=255) # 
    password = models.CharField(_('password'),max_length=128) # sha1 hash
    token_password = models.CharField(max_length=40)
    token_activate = models.CharField(max_length=40)
    is_active = models.BooleanField(default=False)
    
    objects = EpiworkUserManager()
    
    # Get the user login
    def get_user(self):
        return self.user

    def set_user(self, username):
        self.user = username

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
    
    def create_token_activate(self):
        token = create_token()
        self.token_activate = token